import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime
import io

# Marketing Texte & Agenten
from marketing_demo import HEADER, CREWAI, AGENTEN, VORTEILE, KONTAKT
from sales_leads import generate_all_leads
from akquise_plan import generate_acquisition_plan
from proposal import generate_proposals

# -----------------------------
# Streamlit Seiteneinstellungen
# -----------------------------
st.set_page_config(page_title="CrewAI Sales Dashboard", layout="wide")

# -----------------------------
# Marketing Header
# -----------------------------
st.markdown(f"<h1 style='text-align:center; color:#0073e6'>{HEADER}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center;'>{CREWAI}</h3>", unsafe_allow_html=True)
st.markdown(f"<hr style='margin-top:20px; margin-bottom:20px;'>", unsafe_allow_html=True)

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
sections = [
    "Branchen auswählen",
    "Sales Leads",
    "Akquiseplan",
    "Proposal",
    "KPIs & Vorteile",
    "Kontaktformular",
    "Branchenübersicht"
]
selected_section = st.sidebar.radio("Bereich wählen", sections)

# Branchenliste
branches = [
    "Modellhäuser", "IT", "Finance", "Banken", "Automobil",
    "Versicherungen", "Marketing", "Werbekampagnen", "Dienstleister",
    "Freelancer", "Jobsuchende", "E-Commerce", "Bildung", "Gesundheit",
    "Tourismus", "Logistik", "Media", "Consulting", "Software", "Hardware"
]

# Session-State initialisieren
if "leads_per_branch" not in st.session_state:
    st.session_state.leads_per_branch, st.session_state.branch_profiles = generate_all_leads(branches)

# Auswahl Branche
selected_branch = st.sidebar.selectbox("Branche auswählen", branches)

# Action Icons
action_icons = {"Sofort kontaktieren":"🔴", "Anschreiben":"🟠", "Demo vereinbaren":"🟢"}

# Farben für Priorität
priority_colors = {"hoch":"red","mittel":"orange","niedrig":"green"}

# -----------------------------
# Logik pro Abschnitt
# -----------------------------
if selected_section == "Sales Leads":
    st.header(f"Sales Leads - {selected_branch}")
    df_leads = st.session_state.leads_per_branch[selected_branch].copy()
    st.dataframe(df_leads, use_container_width=True)

    # Histogramm Score-Verteilung
    fig = px.histogram(df_leads, x="score", nbins=20,
                       title=f"Score-Verteilung - {selected_branch}",
                       color="Priorität", color_discrete_map=priority_colors)
    st.plotly_chart(fig, use_container_width=True)

elif selected_section == "Akquiseplan":
    st.header(f"Akquiseplan - {selected_branch}")
    df_plan = generate_acquisition_plan(selected_branch, st.session_state.leads_per_branch, action_icons)
    st.dataframe(df_plan[["company","score","Priorität","Empfohlene_Aktion","Aktion_Icon"]], use_container_width=True)

    # Balken Chart nach Priorität
    fig = px.bar(df_plan,
                 x="company",
                 y="score",
                 color="Priorität",
                 color_discrete_map=priority_colors,
                 text="score",
                 title=f"Akquiseplan: Score & Priorität - {selected_branch}",
                 hover_data=["Empfohlene_Aktion","Priorität"])
    fig.update_layout(xaxis_title="Unternehmen", yaxis_title="Score", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Legende Priorität:** 🔴 hoch 🟠 mittel 🟢 niedrig")

elif selected_section == "Proposal":
    st.header(f"Proposal - {selected_branch}")
    df_prop = generate_proposals(selected_branch, st.session_state.leads_per_branch, action_icons)
    st.dataframe(df_prop, use_container_width=True)

    # Balken Chart: Avg Score pro Aktion
    fig_bar = px.bar(df_prop,
                     x="Proposal_Type",
                     y="Avg_Score",
                     text="Avg_Score",
                     color="Proposal_Type",
                     title=f"Durchschnittlicher Score pro Aktion - {selected_branch}")
    fig_bar.update_layout(yaxis_range=[0,100])
    st.plotly_chart(fig_bar, use_container_width=True)

    # Kreisdiagramm: Anteil Leads pro Aktion
    df_counts = df_prop[["Proposal_Type","Count"]].copy()
    fig_pie = px.pie(df_counts,
                     names="Proposal_Type",
                     values="Count",
                     title=f"Anteil der Leads pro Aktion - {selected_branch}",
                     color="Proposal_Type")
    st.plotly_chart(fig_pie, use_container_width=True)

elif selected_section == "KPIs & Vorteile":
    st.header("KPIs & Vorteile")
    df_leads = st.session_state.leads_per_branch[selected_branch].copy()
    total_leads = len(df_leads)
    qualified_leads = df_leads[df_leads["status"]=="qualifiziert"].shape[0]
    avg_score = round(df_leads["score"].mean(),2) if not df_leads.empty else 0
    st.metric("Gesamtleads", total_leads)
    st.metric("Qualifizierte Leads", qualified_leads)
    st.metric("Durchschnittlicher Score", avg_score)
    
    st.subheader("Vorteile von CrewAI")
    st.markdown(VORTEILE)

elif selected_section == "Kontaktformular":
    st.header("Kontaktformular / Kundenanfragen")
    if "kundenanfragen" not in st.session_state:
        st.session_state.kundenanfragen = []

    csv_file = "kundenanfragen.csv"
    try:
        df_csv = pd.read_csv(csv_file)
        st.session_state.kundenanfragen = df_csv.to_dict(orient="records")
    except FileNotFoundError:
        df_csv = pd.DataFrame()

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
            df_to_save = pd.DataFrame(st.session_state.kundenanfragen)
            df_to_save.to_csv(csv_file, index=False)
            st.success("✅ Anfrage gesendet und gespeichert.")

    st.subheader("Alle Kundenanfragen")
    df_requests = pd.DataFrame(st.session_state.kundenanfragen)
    st.dataframe(df_requests, use_container_width=True)

elif selected_section == "Branchenübersicht":
    st.header("Branchenübersicht")
    summary = []
    for branch in branches:
        df = st.session_state.leads_per_branch[branch]
        total = len(df)
        qualified = df[df["status"]=="qualifiziert"].shape[0]
        avg_score = round(df["score"].mean(),2)
        summary.append({"Branche":branch, "Leads":total, "Qualifizierte":qualified, "Avg_Score":avg_score})
    df_summary = pd.DataFrame(summary)
    st.dataframe(df_summary, use_container_width=True)
