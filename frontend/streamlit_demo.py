# streamlit_demo.py
import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime
import numpy as np

# Importiere die Texte (HEADER, CREWAI, AGENTEN, VORTEILE, KONTAKT)
# (Deine Datei heißt in deinem Setup vermutlich marketing_demo.py)
from marketing_demo import HEADER, CREWAI, AGENTEN, VORTEILE, KONTAKT

# Seite konfigurieren (muss ganz oben erfolgen)
st.set_page_config(page_title="CrewAI Sales Dashboard", layout="wide")

# -----------------------------
# UI: Header & Marketing-Text
# -----------------------------
st.markdown(HEADER, unsafe_allow_html=True)
st.markdown("<hr style='margin-top:20px; margin-bottom:20px;'>", unsafe_allow_html=True)

st.subheader("CrewAI – Intelligente Agenten-Teams")
st.markdown(CREWAI)

st.subheader("KI-Agenten nach Funktion")
for kategorie, text in AGENTEN.items():
    with st.expander(kategorie, expanded=False):
        st.markdown(text)

st.subheader("Ihre Vorteile")
st.markdown(VORTEILE)

st.subheader("Kontakt & Demo")
st.markdown(KONTAKT)

# -----------------------------
# Konfiguration: Branchen & Auswahl
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
# Daten-Generator: Unternehmen & Branch-Profiles
# -----------------------------
def generate_companies(branches, n_per_branch=45):
    companies = []
    for branch in branches:
        for i in range(n_per_branch):
            companies.append(f"{branch} Company {i+1}")
    return companies

all_companies = generate_companies(branches, n_per_branch=45)
branch_profiles = {
    branch: {"score_mean": random.randint(50, 70), "score_sd": random.randint(8, 16)}
    for branch in branches
}

# -----------------------------
# Session-State: Leads initialisieren
# -----------------------------
if "leads_per_branch" not in st.session_state:
    def generate_branch_leads(branch, n_companies_per_branch=45, n_qualifiziert=None):
        if n_qualifiziert is None:
            n_qualifiziert = random.randint(8, 28)

        profile = branch_profiles[branch]
        companies = [c for c in all_companies if c.startswith(branch)]
        companies = companies[:n_companies_per_branch]

        # Scores erzeugen und einschränken auf [0,100]
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
                # nur einmalig setzen
                "product_interest": random.choice(["Produkt A", "Produkt B", "Produkt C"]),
                "Priorität": "hoch" if score > 70 else ("mittel" if score > 40 else "niedrig")
            }
            data.append(lead)

        df = pd.DataFrame(data).sort_values(by="score", ascending=False).reset_index(drop=True)
        return df

    st.session_state.leads_per_branch = {branch: generate_branch_leads(branch) for branch in branches}

# -----------------------------
# Helper-Funktionen: Akquiseplan & Proposals
# -----------------------------
def generate_acquisition_plan(df, top_n=30):
    # Wähle qualifizierte oder neue Leads (neu ist möglich wenn man hinzufügen will)
    df_qualified = df[df["status"].isin(["qualifiziert", "neu"])].copy().sort_values(by="score", ascending=False)
    df_qualified = df_qualified.head(top_n).reset_index(drop=True)

    # Empfohlene Aktion je Rang
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

def generate_proposals(df_plan):
    if df_plan.empty:
        return pd.DataFrame(columns=["Proposal_Type", "Avg_Score", "Count", "Interpretation", "Handlungsempfehlung"])

    relevant_actions = ["Sofort kontaktieren", "Anschreiben", "Demo vereinbaren"]
    df_rel = df_plan[df_plan["Empfohlene_Aktion"].isin(relevant_actions)].copy()

    agg = df_rel.groupby("Empfohlene_Aktion").agg(
        Avg_Score=("score", "mean"),
        Count=("score", "count")
    ).reset_index().rename(columns={"Empfohlene_Aktion": "Proposal_Type"})

    agg["Avg_Score"] = agg["Avg_Score"].round(2)

    def interpret(score):
        if score >= 75:
            return "Sehr hohe Abschlusswahrscheinlichkeit"
        elif score >= 55:
            return "Mittlere Abschlusswahrscheinlichkeit"
        else:
            return "Niedrige Abschlusswahrscheinlichkeit"

    def recommendation(score):
        if score >= 75:
            return "Priorität: Sofort bearbeiten"
        elif score >= 55:
            return "Priorität: Nachfassen"
        else:
            return "Priorität: Demo anbieten und beobachten"

    agg["Interpretation"] = agg["Avg_Score"].apply(interpret)
    agg["Handlungsempfehlung"] = agg["Avg_Score"].apply(recommendation)

    # Sicherstellen, dass alle Aktionen vorhanden sind
    for act in relevant_actions:
        if act not in agg["Proposal_Type"].values:
            agg = pd.concat([agg, pd.DataFrame([{
                "Proposal_Type": act,
                "Avg_Score": 0.0,
                "Count": 0,
                "Interpretation": "Keine qualifizierten Leads",
                "Handlungsempfehlung": "Keine Aktion"
            }])], ignore_index=True)

    # Reihenfolge fixieren
    order_map = {a: i for i, a in enumerate(relevant_actions)}
    agg["Order"] = agg["Proposal_Type"].map(order_map)
    agg = agg.sort_values("Order").drop(columns=["Order"]).reset_index(drop=True)

    return agg

# -----------------------------
# Aktuelle Daten für die ausgewählte Branche
# -----------------------------
df_leads = st.session_state.leads_per_branch[selected_branch].copy()
df_plan = generate_acquisition_plan(df_leads)
df_prop = generate_proposals(df_plan)

# -----------------------------
# KPI-Berechnungen
# -----------------------------
total_leads = len(df_leads)
qualified_leads = df_leads[df_leads["status"].isin(["qualifiziert", "neu"])].shape[0]
avg_score = df_leads["score"].mean() if not df_leads.empty else 0
max_rate = df_prop["Avg_Score"].max() if not df_prop.empty else 0

# -----------------------------
# Dashboard Titel
# -----------------------------
st.title("CrewAI Sales Dashboard")

# -----------------------------
# Sales Leads View
# -----------------------------
if selected_agent == "Sales Leads":
    st.header(f"Sales Leads – {selected_branch}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gesamtanzahl Leads", total_leads)
    col2.metric("Qualifizierte Leads", qualified_leads)
    col3.metric("Durchschnittlicher Lead Score", f"{avg_score:.2f}")

    st.subheader("Top qualifizierte Leads (Akquiseplan)")
    display_cols = ["company", "score", "Priorität", "city", "product_interest", "Empfohlene_Aktion", "Aktion_Icon"]
    st.dataframe(df_plan[display_cols], use_container_width=True)

    # Histogram Score-Verteilung (Status als Farbe)
    fig_score = px.histogram(
        df_leads,
        x="score",
        nbins=10,
        hover_data=["company", "city", "industry"],
        color="status",
        title="Lead Score Verteilung"
    )
    st.plotly_chart(fig_score, use_container_width=True)

# -----------------------------
# Akquiseplan View
# -----------------------------
elif selected_agent == "Akquiseplan":
    st.header(f"Akquiseplan – {selected_branch}")
    st.subheader("Strategieplan für Top qualifizierte Leads")
    st.dataframe(df_plan[["company", "score", "Priorität", "Empfohlene_Aktion", "Aktion_Icon"]], use_container_width=True)

    counts = df_plan["Empfohlene_Aktion"].value_counts().reset_index()
    counts.columns = ["Aktion", "Anzahl"]
    fig_actions = px.bar(
        counts,
        x="Aktion",
        y="Anzahl",
        text_auto=True,
        title="Häufigkeit der Akquise-Aktionen"
    )
    st.plotly_chart(fig_actions, use_container_width=True)

# -----------------------------
# Proposal View
# -----------------------------
elif selected_agent == "Proposal":
    st.header(f"Proposal Generator – {selected_branch}")
    st.dataframe(df_prop, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Anzahl Proposal-Typen", len(df_prop))
    col2.metric("Max. Avg Score", f"{max_rate:.2f}")
    col3.metric("Durchschnittlicher Avg Score", f"{df_prop['Avg_Score'].mean():.2f}" if not df_prop.empty else "0.00")

    fig_prop = px.bar(
        df_prop,
        x="Proposal_Type",
        y="Avg_Score",
        text_auto=True,
        title="Durchschnittlicher Lead-Score je Aktion"
    )
    st.plotly_chart(fig_prop, use_container_width=True)

    # Heatmap: Score-Verteilung je Aktion (wenn Daten vorhanden)
    if not df_plan.empty:
        # Pivot: Unternehmen x Aktion mit Score
        df_heat = df_plan.pivot_table(index="company", columns="Empfohlene_Aktion", values="score", fill_value=0)
        # px.imshow erwartet matrix; transponieren, damit Aktionen in y-Achse sind
        fig_heat = px.imshow(
            df_heat.T,
            labels=dict(x="Unternehmen", y="Aktion", color="Score"),
            x=df_heat.index,
            y=df_heat.columns,
            title="Heatmap: Lead-Scores pro Aktion"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""
    **Interpretation & Handlungsempfehlung:**
    - 🔴 Sofort kontaktieren: höchste Scores → sofort bearbeiten.
    - 🟠 Anschreiben: mittlere Scores → gezielt bearbeiten, Follow-up.
    - 🟢 Demo vereinbaren: niedrigere Scores → Demo anbieten und beobachten.
    """)

# -----------------------------
# KPIs View
# -----------------------------
elif selected_agent == "KPIs & Vorteile":
    st.header(f"KPIs & Vorteile – {selected_branch}")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Gesamtanzahl Leads", total_leads)
    k2.metric("Qualifizierte Leads", qualified_leads)
    k3.metric("Durchschnittlicher Lead Score", f"{avg_score:.2f}")
    k4.metric("Max. Proposal Avg Score", f"{max_rate:.2f}")

    st.markdown(VORTEILE)

import io  # für In-Memory Excel

# -----------------------------
# Kontaktformular View mit Excel-Download
# -----------------------------
elif selected_agent == "Kontaktformular":
    st.header("Kontaktformular / Kundenanfrage")

    if "kundenanfragen" not in st.session_state:
        st.session_state.kundenanfragen = []

    csv_file = "kundenanfragen.csv"

    # CSV laden, falls vorhanden
    try:
        df_csv = pd.read_csv(csv_file)
        st.session_state.kundenanfragen = df_csv.to_dict(orient="records")
    except FileNotFoundError:
        df_csv = pd.DataFrame()

    # Formular
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

            # CSV speichern
            df_to_save = pd.DataFrame(st.session_state.kundenanfragen)
            df_to_save.to_csv(csv_file, index=False)

            st.success("✅ Ihre Anfrage wurde erfolgreich gesendet und gespeichert.")

            # Neuer Lead hinzufügen
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

            # UI aktualisieren
            df_leads = st.session_state.leads_per_branch[selected_branch].copy()
            df_plan = generate_acquisition_plan(df_leads)
            df_prop = generate_proposals(df_plan)

    # Alle Anfragen anzeigen
    st.subheader("Alle Kundenanfragen")
    df_requests = pd.DataFrame(st.session_state.kundenanfragen)
    st.dataframe(df_requests, use_container_width=True)

    # Excel-Download
    if not df_requests.empty:
        with io.BytesIO() as buffer:
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                df_requests.to_excel(writer, index=False, sheet_name="Kundenanfragen")
                df_plan.to_excel(writer, index=False, sheet_name="Leads_Akquiseplan")
                writer.save()
                st.download_button(
                    label="Kundenanfragen + Leads als Excel herunterladen",
                    data=buffer.getvalue(),
                    file_name="kundenanfragen_leads.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    st.subheader("Automatische Lead-Aktionen (inkl. neuer Kundenanfragen)")
    st.dataframe(df_plan[["company", "score", "Priorität", "Empfohlene_Aktion", "Aktion_Icon"]], use_container_width=True)
    st.markdown("**Legende:** 🔴 Sofort kontaktieren 🟠 Anschreiben 🟢 Demo vereinbaren")

# -----------------------------
# Branchenübersicht View
# -----------------------------
elif selected_agent == "Branchenübersicht":
    st.header("Branchenüberblick – Alle Unternehmen")
    df_all_leads = pd.concat(st.session_state.leads_per_branch.values(), ignore_index=True)

    df_kpis = df_all_leads.groupby("industry").agg(
        total_leads=("lead_id", "count"),
        qualified_leads=("status", lambda x: x.isin(["qualifiziert", "neu"]).sum()),
        avg_score=("score", "mean"),
        max_score=("score", "max")
    ).reset_index()

    df_kpis["avg_score"] = df_kpis["avg_score"].round(2)

    # Empfehlung nach avg_score
    df_kpis = df_kpis.sort_values("avg_score", ascending=False).reset_index(drop=True)
    df_kpis["Empfehlung"] = ""
    for i in range(len(df_kpis)):
        if i < 5:
            df_kpis.at[i, "Empfehlung"] = "Priorisieren"
        elif i < 10:
            df_kpis.at[i, "Empfehlung"] = "Optional"
        else:
            df_kpis.at[i, "Empfehlung"] = "Nicht priorisieren"

    st.subheader("KPIs pro Branche")
    st.dataframe(df_kpis, use_container_width=True)

    fig_kpi = px.bar(df_kpis.sort_values("avg_score", ascending=False), x="industry", y="avg_score",
                     title="Durchschnittlicher Lead Score pro Branche", text_auto=True)
    st.plotly_chart(fig_kpi, use_container_width=True)
