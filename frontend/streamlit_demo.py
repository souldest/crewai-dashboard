import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime
import numpy as np
import io

from marketing_demo import HEADER, CREWAI, AGENTEN, VORTEILE, KONTAKT

# -----------------------------
# Streamlit-Seiteneinstellungen
# -----------------------------
st.set_page_config(page_title="CrewAI Sales Dashboard", layout="wide")

# -----------------------------
# UI: Header & Marketing-Text
# -----------------------------
header_html = """
<h1 style='text-align:center; font-size:48px; font-weight:800;'>Revolutionieren Sie Ihr Unternehmen mit KI-Agenten</h1>
<p style='text-align:center; font-size:22px; line-height:1.5;'>Die Zukunft der Automatisierung beginnt heute.<br>Unsere Agenten arbeiten 24/7, um Leads zu qualifizieren, Prozesse zu automatisieren und Umsatz zu skalieren.</p>
<p style='text-align:center; font-size:24px; font-weight:700; color:#0073e6;'>▶ Jetzt Demo anfragen und das Potenzial von CrewAI live erleben</p>
<hr style='margin-top:20px; margin-bottom:20px;'>
"""
st.markdown(header_html, unsafe_allow_html=True)

# -----------------------------
# CrewAI Abschnitt
# -----------------------------
st.subheader("CrewAI – Intelligente Agenten-Teams")

# KI-Agenten nach Funktion
st.subheader("KI-Agenten nach Funktion")
for kategorie, text in AGENTEN.items():
    with st.expander(kategorie, expanded=False):
        st.markdown(text)

# -----------------------------
# Vorteile
# -----------------------------
st.subheader("Ihre Vorteile")
st.markdown(VORTEILE)

# -----------------------------
# Kontakt & Demo
# -----------------------------
st.subheader("Kontakt & Demo")
st.markdown(KONTAKT)

# -----------------------------
# Sidebar: Branchen & Agenten-Auswahl
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
    ["Sales Leads", "Akquiseplan", "Proposal", "KPIs & Vorteile", "Kontaktformular", "Branchenübersicht"] )

# -----------------------------
# Action Icons
# -----------------------------
action_icons = {
    "Sofort kontaktieren": "🔴",
    "Anschreiben": "🟠",
    "Demo vereinbaren": "🟢"
}

# -----------------------------
# Branchendaten generieren
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
# Session-State für Leads initialisieren
# -----------------------------
if "leads_per_branch" not in st.session_state:
    def generate_branch_leads(branch, n_companies_per_branch=45, n_qualifiziert=None):
        if n_qualifiziert is None:
            n_qualifiziert = random.randint(10, 30)
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

    st.session_state.leads_per_branch = {
        branch: generate_branch_leads(branch) for branch in branches
    }

# Current branch leads
df_leads = st.session_state.leads_per_branch[selected_branch].copy()

# -----------------------------
# Akquiseplan generieren
# -----------------------------
def generate_acquisition_plan(df, top_n=30):
    df_qualified = df[df["status"].isin(["qualifiziert", "neu"])].copy().sort_values(by="score", ascending=False)
    df_qualified = df_qualified.head(top_n).reset_index(drop=True)

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

df_plan = generate_acquisition_plan(df_leads)

# -----------------------------
# Proposal Generator
# -----------------------------
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

    # Interpretation und Handlungsempfehlung
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

    # Alle drei Aktionen sicherstellen
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
max_rate = df_prop["Avg_Score"].max() if not df_prop.empty else 0

# -----------------------------
# Dashboard-Titel
# -----------------------------
st.title("CrewAI Sales Dashboard")

# -----------------------------
# Tabs / Views
# -----------------------------
if selected_agent == "Kontaktformular":
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
            st.download_button(
                label="Kundenanfragen + Leads als Excel herunterladen",
                data=buffer.getvalue(),
                file_name="kundenanfragen_leads.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.subheader("Automatische Lead-Aktionen (inkl. neuer Kundenanfragen)")
    st.dataframe(df_plan[["company", "score", "Priorität", "Empfohlene_Aktion", "Aktion_Icon"]], use_container_width=True)
    st.markdown("**Legende:** 🔴 Sofort kontaktieren 🟠 Anschreiben 🟢 Demo vereinbaren")

else:
    # Fallback: implement other views
    if selected_agent == "Sales Leads":
        st.header("Sales Leads")
        st.write(f"Branch: {selected_branch}")
        st.dataframe(df_leads, use_container_width=True)

    elif selected_agent == "Akquiseplan":
        st.header("Akquiseplan")
        st.dataframe(df_plan, use_container_width=True)

    elif selected_agent == "Proposal":
        st.header("Proposal Übersicht")
        st.table(df_prop)

    elif selected_agent == "KPIs & Vorteile":
        st.header("KPIs")
        cols = st.columns(4)
        cols[0].metric("Total Leads", total_leads)
        cols[1].metric("Qualifizierte Leads", qualified_leads)
        cols[2].metric("Durchschnittsscore", f"{avg_score:.2f}")
        cols[3].metric("Max Proposal Score", f"{max_rate:.2f}")

    elif selected_agent == "Branchenübersicht":
        st.header("Branchenübersicht")
        branch_summary = []
        for b in branches:
            df_b = st.session_state.leads_per_branch[b]
            branch_summary.append({
                "Branche": b,
                "Anzahl Leads": len(df_b),
                "Durchschnittsscore": round(df_b['score'].mean(),2)
            })
        st.dataframe(pd.DataFrame(branch_summary), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("© CrewAI | Demo Dashboard")
