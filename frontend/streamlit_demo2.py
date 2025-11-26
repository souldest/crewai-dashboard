import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime
import numpy as np

st.set_page_config(page_title="CrewAI Sales Dashboard – Branchenvergleich", layout="wide")

# -----------------------------
# Branchen
# -----------------------------
branches = [
    "Modellhäuser", "IT", "Finance", "Banken", "Automobil",
    "Versicherungen", "Marketing", "Werbekampagnen", "Dienstleister",
    "Freelancer", "Jobsuchende", "E-Commerce", "Bildung", "Gesundheit",
    "Tourismus", "Logistik", "Media", "Consulting", "Software", "Hardware"
]

selected_branch = st.sidebar.selectbox("Wählen Sie eine Branche / Szenario", branches)
selected_agent = st.sidebar.radio(
    "Agenten / Ansicht",
    ["Sales Leads", "Akquiseplan", "Proposal", "KPIs & Vorteile", "Kontaktformular", "Branchenübersicht"]
)

# -----------------------------
# Action Icons
# -----------------------------
action_icons = {
    "Sofort kontaktieren": "🔴",
    "Anschreiben": "🟠",
    "Demo vereinbaren": "🟢"
}

# -----------------------------
# Branchendaten generieren (900 Unternehmen = 45 pro Branche)
# -----------------------------
def generate_companies(branches, n_per_branch=45):
    companies = []
    for branch in branches:
        for i in range(n_per_branch):
            companies.append(f"{branch} Company {i+1}")
    return companies

all_companies = generate_companies(branches, n_per_branch=45)

# Branchenprofile für Score-Generierung
branch_profiles = {
    branch: {"score_mean": random.randint(50, 70), "score_sd": random.randint(8, 16)}
    for branch in branches
}

# -----------------------------
# Session-State für Leads initialisieren
# -----------------------------
if "leads_per_branch" not in st.session_state:
    def generate_branch_leads(branch, n_companies_per_branch=45, n_qualifiziert=None):
        if n_qualifiziert is None:
            n_qualifiziert = random.randint(10, 30)  # 10–30 qualifizierte Leads pro Branche

        profile = branch_profiles[branch]
        companies = [c for c in all_companies if c.startswith(branch)]
        companies = companies[:n_companies_per_branch]

        all_scores = [max(0, min(100, random.gauss(profile["score_mean"], profile["score_sd"]))) for _ in companies]
        sorted_idx = sorted(range(len(all_scores)), key=lambda i: all_scores[i], reverse=True)

        data = []
        for rank_pos, idx in enumerate(sorted_idx):
            score = all_scores[idx]
            status = "qualifiziert" if rank_pos < n_qualifiziert else "inqualifiziert"
            lead = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "lead_id": f"{branch[:3].upper()}-{random.randint(1,9999):04d}",
                "company": companies[idx],
                "city": random.choice(["Berlin", "Hamburg", "München", "Köln", "Frankfurt"]),
                "industry": branch,
                "score": round(score, 2),
                "status": status,
                "product_interest": random.choice(["Produkt A", "Produkt B", "Produkt C"]),
                "Priorität": "hoch" if score > 70 else ("mittel" if score > 40 else "niedrig")
            }
            data.append(lead)
        df = pd.DataFrame(data).sort_values(by="score", ascending=False).reset_index(drop=True)
        return df

    st.session_state.leads_per_branch = {branch: generate_branch_leads(branch) for branch in branches}

df_leads = st.session_state.leads_per_branch[selected_branch].copy()

# -----------------------------
# Akquiseplan – Top Qualifizierte Leads und Aktionszuordnung
# -----------------------------
def generate_acquisition_plan(df, top_n=None):
    df_qualified = df[df["status"].isin(["qualifiziert", "neu"])].copy().sort_values(by="score", ascending=False)
    if top_n is not None:
        df_qualified = df_qualified.head(top_n).reset_index(drop=True)
    else:
        df_qualified = df_qualified.reset_index(drop=True)

    # Aktion zuweisen: Top 5 → Sofort, nächste 4 → Anschreiben, Rest → Demo
    actions = []
    for i in range(len(df_qualified)):
        if i < 5:
            actions.append("Sofort kontaktieren")
        elif i < 9:
            actions.append("Anschreiben")
        else:
            actions.append("Demo vereinbaren")

    df_qualified["Empfohlene_Aktion"] = actions
    df_qualified["Aktion_Icon"] = df_qualified["Empfohlene_Aktion"].map(action_icons)
    return df_qualified

df_plan = generate_acquisition_plan(df_leads, top_n=30)

# -----------------------------
# Proposal – Handlungsempfehlung
# -----------------------------
def generate_proposals(df):
    if df is None or df.empty:
        return pd.DataFrame(columns=["Proposal_Type", "Success_Rate", "Count", "Empfehlung"])

    relevant_actions = ["Sofort kontaktieren", "Anschreiben", "Demo vereinbaren"]
    df_rel = df[df["Empfohlene_Aktion"].isin(relevant_actions)].copy()

    agg = df_rel.groupby("Empfohlene_Aktion").agg(
        Success_Rate=("score", "mean"),
        Count=("score", "count")
    ).reset_index().rename(columns={"Empfohlene_Aktion": "Proposal_Type"})
    agg["Success_Rate"] = agg["Success_Rate"].round(2)

    def recommendation(score):
        if score >= 75:
            return "Priorisieren (hohe Abschlusswahrscheinlichkeit)"
        elif score >= 55:
            return "Verfolgen (mittlere Wahrscheinlichkeit)"
        else:
            return "Niedrige Priorität (Demo sinnvoll)"

    agg["Empfehlung"] = agg["Success_Rate"].apply(recommendation)

    for act in relevant_actions:
        if act not in agg["Proposal_Type"].values:
            agg = pd.concat([agg, pd.DataFrame([{
                "Proposal_Type": act,
                "Success_Rate": 0.0,
                "Count": 0,
                "Empfehlung": "Keine qualifizierten Leads"
            }])], ignore_index=True)

    agg["Order"] = agg["Proposal_Type"].map({a: i for i, a in enumerate(relevant_actions)})
    agg = agg.sort_values("Order").drop(columns=["Order"]).reset_index(drop=True)
    return agg

df_prop = generate_proposals(df_plan)

# -----------------------------
# KPIs
# -----------------------------
total_leads = len(df_leads)
qualified_leads = df_leads[df_leads["status"].isin(["qualifiziert", "neu"])].shape[0]
avg_score = df_leads["score"].mean() if not df_leads.empty else 0
max_rate = df_prop["Success_Rate"].max() if not df_prop.empty else 0

# -----------------------------
# Dashboard-Titel
# -----------------------------
st.title("CrewAI Sales Dashboard")

# -----------------------------
# Sales Leads Tab
# -----------------------------
if selected_agent == "Sales Leads":
    st.header(f"Sales Leads – {selected_branch}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gesamtanzahl Leads", total_leads)
    col2.metric("Qualifizierte Leads", qualified_leads)
    col3.metric("Durchschnittlicher Lead Score", f"{avg_score:.2f}")

    st.subheader("Top qualifizierte Leads (Auszug)")
    st.dataframe(df_plan[["company", "score", "Priorität", "city", "product_interest", "Empfohlene_Aktion", "Aktion_Icon"]],
                 use_container_width=True)

    fig_score = px.histogram(
        df_leads,
        x="score",
        nbins=10,
        hover_data=["company", "city", "industry"],
        color="status",
        color_discrete_map={"qualifiziert": "green", "inqualifiziert": "red", "neu": "blue"},
        title="Lead Score Verteilung"
    )
    st.plotly_chart(fig_score, use_container_width=True)

# -----------------------------
# Akquiseplan Tab
# -----------------------------
elif selected_agent == "Akquiseplan":
    st.header(f"Akquiseplan – {selected_branch}")
    st.subheader("Strategieplan für Top 30 qualifizierte Leads")
    st.dataframe(df_plan[["company", "score", "Priorität", "Empfohlene_Aktion", "Aktion_Icon"]], use_container_width=True)

    counts = df_plan["Empfohlene_Aktion"].value_counts().reset_index()
    counts.columns = ["Aktion", "Anzahl"]
    fig_actions = px.bar(
        counts,
        x="Aktion",
        y="Anzahl",
        text_auto=True,
        title="Häufigkeit der Akquise-Aktionen",
        color="Anzahl",
        color_continuous_scale=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig_actions, use_container_width=True)

    # -----------------------------
    # Heatmap der Top 30 qualifizierten Leads
    # -----------------------------
    if not df_plan.empty:
        df_heat = df_plan.copy()
        df_heat["Rang"] = df_heat.index + 1
        df_heat.sort_values(["Empfohlene_Aktion", "score"], ascending=[True, False], inplace=True)
        heat_data = df_heat.pivot(index="Empfohlene_Aktion", columns="Rang", values="score")
        fig_heat = px.imshow(
            heat_data,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Viridis",
            labels=dict(x="Lead Rang", y="Aktion", color="Score"),
            title="Heatmap: Lead Score pro Aktion"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

# -----------------------------
# Proposal Tab
# -----------------------------
elif selected_agent == "Proposal":
    st.header(f"Proposal Generator – {selected_branch}")
    st.dataframe(df_prop, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Anzahl Proposal-Typen", len(df_prop))
    col2.metric("Max. Erfolgsrate (avg Score)", f"{max_rate:.2f}")
    col3.metric("Durchschnittliche Erfolgsrate (avg Score)", f"{df_prop['Success_Rate'].mean():.2f}" if not df_prop.empty else "0.00")

    fig_prop = px.bar(
        df_prop,
        x="Proposal_Type", y="Success_Rate",
        text_auto=True,
        title="Durchschnittlicher Lead-Score je Aktion (Success_Rate)",
        color="Success_Rate",
        color_continuous_scale=px.colors.sequential.Cividis
    )
    st.plotly_chart(fig_prop, use_container_width=True)

    st.markdown("""
    <div style="background-color:#FFF3CD; padding:10px; border-left:5px solid #FFC107; border-radius:5px;">
    <b>ℹ️ Hinweis zur Success_Rate:</b><br>
    Die Spalte <b>„Success_Rate“</b> zeigt den <b>durchschnittlichen Lead-Score pro Aktion</b> (Mittelwert der Scores) und <b>nicht den prozentualen Anteil</b> aller Leads.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# KPIs & Vorteile Tab
# -----------------------------
elif selected_agent == "KPIs & Vorteile":
    st.header(f"KPIs & Vorteile – {selected_branch}")
    st.metric("Gesamtanzahl Leads", total_leads)
    st.metric("Qualifizierte Leads", qualified_leads)
    st.metric("Durchschnittlicher Lead Score", f"{avg_score:.2f}")
    st.metric("Max. Proposal Erfolgsrate (avg Score)", f"{max_rate:.2f}")

# -----------------------------
# Kontaktformular Tab
# -----------------------------
elif selected_agent == "Kontaktformular":
    st.header("Kontaktformular / Kundenanfrage")
    if "kundenanfragen" not in st.session_state:
        st.session_state.kundenanfragen = []

    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("E-Mail")
        nachricht = st.text_area("Nachricht / Anfrage")
        submit = st.form_submit_button("Anfrage senden")

        if submit:
            anfrage = {
                "name": name,
                "email": email,
                "nachricht": nachricht,
                "datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.kundenanfragen.append(anfrage)
            st.success("✅ Ihre Anfrage wurde erfolgreich gesendet.")

            new_lead = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "lead_id": f"CUST-{random.randint(1000,9999)}",
                "company": name if name else f"Interessent {len(st.session_state.kundenanfragen)}",
                "city": "N/A",
                "industry": selected_branch,
                "score": 100.0,
                "status": "neu",
                "product_interest": "Anfrageprodukt",
                "Priorität": "hoch"
            }
            df_branch = st.session_state.leads_per_branch[selected_branch].copy()
            df_branch = pd.concat([df_branch, pd.DataFrame([new_lead])], ignore_index=True)
            st.session_state.leads_per_branch[selected_branch] = df_branch

            df_leads = st.session_state.leads_per_branch[selected_branch].copy()
            df_plan = generate_acquisition_plan(df_leads, top_n=30)
            df_prop = generate_proposals(df_plan)

    st.subheader("Alle Kundenanfragen")
    df_requests = pd.DataFrame(st.session_state.kundenanfragen)
    st.dataframe(df_requests, use_container_width=True)

    st.subheader("Automatische Lead-Aktionen (inkl. neuer Kundenanfragen)")
    st.dataframe(df_plan[["company", "score", "Priorität", "Empfohlene_Aktion", "Aktion_Icon"]], use_container_width=True)
    st.markdown("""
    **Legende:**  
    🔴 Sofort kontaktieren  
    🟠 Anschreiben  
    🟢 Demo vereinbaren
    """)

# -----------------------------
# Branchenübersicht Tab
# -----------------------------
elif selected_agent == "Branchenübersicht":
    st.header(" Branchenüberblick – Alle 900 Unternehmen")
    df_all_leads = pd.concat(st.session_state.leads_per_branch.values(), ignore_index=True)

    df_kpis = df_all_leads.groupby("industry").agg(
        total_leads=("lead_id", "count"),
        qualified_leads=("status", lambda x: x.isin(["qualifiziert", "neu"]).sum()),
        avg_score=("score", "mean"),
        max_score=("score", "max")
    ).reset_index()
    df_kpis["avg_score"] = df_kpis["avg_score"].round(2)
    df_kpis["Empfehlung"] = df_kpis["avg_score"].apply(
        lambda x: "Priorisieren" if x > 60 else ("Optional" if x > 45 else "Nicht priorisieren")
    )

    st.subheader("KPIs pro Branche")
    st.dataframe(df_kpis, use_container_width=True)

    fig_kpi = px.bar(df_kpis.sort_values("avg_score", ascending=False), x="industry", y="avg_score",
                     title="Durchschnittlicher Lead Score pro Branche", text_auto=True)
    st.plotly_chart(fig_kpi, use_container_width=True)
