import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime
import io

# Marketing Texte & Agenten
from technologien import TECHNOLOGIEN
from marketing_demo import HEADER, CREWAI, AGENTEN, VORTEILE, KONTAKT
from sales_leads import generate_all_leads, generate_branch_leads
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
st.markdown("<hr style='margin-top:20px; margin-bottom:20px;'>", unsafe_allow_html=True)

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
sections = [
    "Branchenübersicht",        # 1. Branchen
    "Sales Leads",              # 3. CrewAI Sales Leads
    "Akquiseplan",              # 4. CrewAI Akquiseplan
    "Proposal",                 # 5. CrewAI Proposal
    "KPIs & Vorteile",          # 6. KPIs & Vorteile
    "Kontaktformular"           # 7. Kontaktformular
]
selected_section = st.sidebar.radio("Bereich wählen", sections)

# -----------------------------
# Sidebar: Branche auswählen
# -----------------------------
branches = [
    "Modellhäuser", "IT", "Finance", "Banken", "Automobil",
    "Versicherungen", "Marketing", "Werbekampagnen", "Dienstleister",
    "Freelancer", "Jobsuchende", "E-Commerce", "Bildung", "Gesundheit",
    "Tourismus", "Logistik", "Media", "Consulting", "Software", "Hardware"
]
selected_branch = st.sidebar.selectbox("Branche auswählen", branches)

# -----------------------------
# Sidebar: Agenten nach Funktion
# -----------------------------
st.sidebar.markdown("### Agenten nach Funktion")
function_keys = list(AGENTEN.keys())
selected_function = st.sidebar.selectbox("Funktion wählen", function_keys)

st.sidebar.markdown("**Agenten in dieser Funktion:**")
for line in AGENTEN[selected_function].strip().split("\n"):
    st.sidebar.markdown(f"- {line}")

# -----------------------------
# Session-State initialisieren
# -----------------------------
if "leads_per_branch" not in st.session_state:
    st.session_state.leads_per_branch, st.session_state.branch_profiles = generate_all_leads(branches)

# Action Icons & Farben
action_icons = {"Sofort kontaktieren":"🔴", "Anschreiben":"🟠", "Demo vereinbaren":"🟢"}
priority_colors = {"hoch":"red","mittel":"orange","niedrig":"green"}

# -----------------------------
# Tabs & Inhalt
# -----------------------------
# -----------------------------
# Sales Leads Tab
# -----------------------------
if selected_section == "Sales Leads":
    st.header(f"Sales Leads - {selected_branch}")
    df_leads = st.session_state.leads_per_branch[selected_branch].copy()

    # Filter Priorität
    st.subheader("Filter Leads")
    selected_priorities = st.multiselect("Priorität auswählen", options=["hoch","mittel","niedrig"], default=["hoch","mittel","niedrig"])
    df_filtered = df_leads[df_leads["Priorität"].isin(selected_priorities)]

    st.dataframe(df_filtered, use_container_width=True)

    # Histogram Score
    fig = px.histogram(df_filtered, x="score", nbins=20,
                       title=f"Score-Verteilung - {selected_branch}",
                       color="Priorität", color_discrete_map=priority_colors,
                       hover_data=["company","status"])
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Akquiseplan Tab
# -----------------------------
elif selected_section == "Akquiseplan":
    st.header(f"Akquiseplan - {selected_branch}")
    df_plan = generate_acquisition_plan(selected_branch, st.session_state.leads_per_branch, action_icons)

    # Filter nach Aktion
    st.subheader("Filter nach empfohlener Aktion")
    selected_actions = st.multiselect("Aktion auswählen", options=list(action_icons.keys()), default=list(action_icons.keys()))
    df_filtered_plan = df_plan[df_plan["Empfohlene_Aktion"].isin(selected_actions)]

    st.dataframe(df_filtered_plan[["company","score","Priorität","Empfohlene_Aktion","Aktion_Icon"]], use_container_width=True)

    # Balkendiagramm Score
    fig_bar = px.bar(df_filtered_plan, x="company", y="score",
                     color="Priorität", color_discrete_map=priority_colors,
                     text="score", title=f"Akquiseplan: Score & Priorität - {selected_branch}",
                     hover_data=["Empfohlene_Aktion"])
    fig_bar.update_layout(xaxis_title="Unternehmen", yaxis_title="Score", xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    # Kreisdiagramm Aktionen
    df_counts = df_filtered_plan.groupby("Empfohlene_Aktion")["company"].count().reset_index(name="Anzahl")
    fig_pie = px.pie(df_counts, names="Empfohlene_Aktion", values="Anzahl",
                     title=f"Verteilung der empfohlenen Aktionen - {selected_branch}", color="Empfohlene_Aktion")
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# Proposal Tab
# -----------------------------
elif selected_section == "Proposal":
    st.header(f"Proposal - {selected_branch}")
    df_prop = generate_proposals(selected_branch, st.session_state.leads_per_branch, action_icons)

    # Filter Aktion
    st.subheader("Filter nach Aktion")
    selected_actions = st.multiselect("Aktion auswählen", options=list(action_icons.keys()), default=list(action_icons.keys()))
    df_filtered = df_prop[df_prop["Proposal_Type"].isin(selected_actions)]

    # Filter Mindestscore
    min_score = st.slider("Minimale durchschnittliche Score", 0, 100, 0)
    df_filtered = df_filtered[df_filtered["Avg_Score"] >= min_score]

    st.dataframe(df_filtered, use_container_width=True)

    # Balkendiagramm Avg_Score
    fig_bar = px.bar(df_filtered, x="Proposal_Type", y="Avg_Score",
                     text="Avg_Score", color="Proposal_Type",
                     title=f"Durchschnittlicher Score pro Aktion - {selected_branch}",
                     hover_data=["Interpretation","Handlungsempfehlung"])
    fig_bar.update_layout(yaxis_range=[0,100])
    st.plotly_chart(fig_bar, use_container_width=True)

    # Interpretation
    st.subheader("Interpretation & Handlungsempfehlung")
    for _, row in df_filtered.iterrows():
        st.markdown(f"**{row['Proposal_Type']}**: {row['Interpretation']} – _{row['Handlungsempfehlung']}_")

    # Kreisdiagramm Aktion
    df_counts = df_filtered.groupby("Proposal_Type")["Count"].sum().reset_index()
    fig_pie = px.pie(df_counts, names="Proposal_Type", values="Count",
                     title=f"Anteil der Leads pro Aktion - {selected_branch}", color="Proposal_Type")
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# KPIs & Vorteile
# -----------------------------
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

# -----------------------------
# Kontaktformular
# -----------------------------
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
            pd.DataFrame(st.session_state.kundenanfragen).to_csv(csv_file, index=False)
            st.success("✅ Anfrage gesendet und gespeichert.")

    st.subheader("Alle Kundenanfragen")
    st.dataframe(pd.DataFrame(st.session_state.kundenanfragen), use_container_width=True)

# -----------------------------
# Branchenübersicht
# -----------------------------
elif selected_section == "Branchenübersicht":
    st.header("Branchenübersicht")
    summary = []
    for branch in branches:
        df = st.session_state.leads_per_branch[branch]
        total = len(df)
        qualified = df[df["status"]=="qualifiziert"].shape[0]
        avg_score = round(df["score"].mean(),2)
        summary.append({"Branche":branch,"Leads":total,"Qualifizierte":qualified,"Avg_Score":avg_score})
    df_summary = pd.DataFrame(summary)

    st.subheader("Tabellarische Übersicht")
    st.dataframe(df_summary, use_container_width=True)

    fig_bar = px.bar(df_summary, x="Branche", y="Leads",
                     text="Leads", color="Qualifizierte", color_continuous_scale="Blues",
                     title="Leads pro Branche (Qualifizierte farblich hervorgehoben)")
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    df_summary["Nicht_qualifiziert"] = df_summary["Leads"] - df_summary["Qualifizierte"]
    df_melted = df_summary.melt(id_vars=["Branche"], value_vars=["Qualifizierte","Nicht_qualifiziert"],
                                var_name="Status", value_name="Anzahl")
    fig_pie = px.pie(df_melted, names="Status", values="Anzahl",
                     title="Anteil qualifizierter vs. nicht qualifizierter Leads (gesamt)", color="Status")
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# Agentenübersicht
# -----------------------------
elif selected_section == "Agentenübersicht":
    st.header("Agenten nach Funktion")
    st.markdown(f"### {selected_function}")
    st.markdown(AGENTEN[selected_function])
    
