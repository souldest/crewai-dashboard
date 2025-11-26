import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime
import io

from marketing_demo import HEADER, CREWAI, AGENTEN, VORTEILE, KONTAKT
from frontend.sales_leads import generate_branch_leads
from frontend.akquise_plan import generate_acquisition_plan
from frontend.proposal import generate_proposals

# -----------------------------
# Seiteinstellungen
# -----------------------------
st.set_page_config(page_title="CrewAI Sales Dashboard", layout="wide")

# -----------------------------
# Marketing-Bereich oben
# -----------------------------
st.markdown(f"<h1 style='text-align:center; font-size:48px; font-weight:800;'>{HEADER}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center; font-size:32px; font-weight:700;'>{CREWAI}</h2>", unsafe_allow_html=True)
for kategorie, text in AGENTEN.items():
    with st.expander(kategorie, expanded=False):
        st.markdown(text, unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:20px; font-weight:600; color:#0073e6;'>{VORTEILE}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:18px; font-weight:500;'>{KONTAKT}</p>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top:20px; margin-bottom:20px;'>", unsafe_allow_html=True)

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
menu_options = [
    "Branche auswählen",
    "Sales Leads",
    "Akquiseplan",
    "Proposal",
    "KPIs & Vorteile",
    "Kontaktformular",
    "Branchenübersicht"
]
selected_menu = st.sidebar.radio("Bereich wählen", menu_options)

branches = ["Modellhäuser","IT","Finance","Banken","Automobil","Versicherungen",
            "Marketing","Werbekampagnen","Dienstleister","Freelancer","Jobsuchende",
            "E-Commerce","Bildung","Gesundheit","Tourismus","Logistik","Media",
            "Consulting","Software","Hardware"]

if selected_menu == "Branche auswählen":
    selected_branch = st.sidebar.selectbox("Branche / Szenario auswählen", branches)
else:
    selected_branch = branches[0]

# -----------------------------
# Session-State & Daten
# -----------------------------
if "leads_per_branch" not in st.session_state:
    all_companies = [f"{b} Company {i+1}" for b in branches for i in range(45)]
    branch_profiles = {b:{"score_mean":random.randint(50,70),"score_sd":random.randint(8,16)} for b in branches}
    st.session_state.leads_per_branch = {b: generate_branch_leads(all_companies, branch_profiles, b) for b in branches}

action_icons = {"Sofort kontaktieren":"🔴","Anschreiben":"🟠","Demo vereinbaren":"🟢"}
priority_colors = {"hoch":"red", "mittel":"orange", "niedrig":"green"}

df_leads = st.session_state.leads_per_branch[selected_branch].copy()
df_plan = generate_acquisition_plan(selected_branch, all_companies, branch_profiles, action_icons)
df_prop = generate_proposals(selected_branch, all_companies, branch_profiles, action_icons)

# -----------------------------
# Inhalte basierend auf Sidebar Auswahl
# -----------------------------
if selected_menu == "Sales Leads":
    st.header("Sales Leads")
    df_display = df_leads.sort_values(by='score', ascending=False)
    st.dataframe(df_display)

    df_display['Farbe'] = df_display['Priorität'].map(priority_colors)
    fig = px.bar(df_display, x='company', y='score', color='Priorität', color_discrete_map=priority_colors,
                 hover_data=['score','status','product_interest'], title="Leads nach Score und Priorität")
    st.plotly_chart(fig, use_container_width=True)

elif selected_menu == "Akquiseplan":
    st.header("Akquiseplan")
    st.dataframe(df_plan)

    fig = px.bar(df_plan, x='company', y='score', color='Empfohlene_Aktion', color_discrete_map=action_icons,
                 hover_data=['score','Priorität','Aktion_Icon'], title="Akquiseplan nach Score & Aktion")
    st.plotly_chart(fig, use_container_width=True)

elif selected_menu == "Proposal":
    st.header("Proposal Übersicht")
    st.table(df_prop)

    fig = px.bar(df_prop, x='Proposal_Type', y='Avg_Score', color='Avg_Score', color_continuous_scale='Blues',
                 text='Handlungsempfehlung', title="Proposal Auswertung: Durchschnittsscore und Handlungsempfehlung")
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

elif selected_menu == "KPIs & Vorteile":
    st.header("KPIs & Vorteile")
    st.metric("Total Leads", len(df_leads))
    st.metric("Qualifizierte Leads", df_leads[df_leads['status'].isin(['qualifiziert','neu'])].shape[0])
    st.metric("Durchschnittsscore", round(df_leads['score'].mean(),2))
    st.subheader("Top 5 Leads")
    st.dataframe(df_leads.sort_values(by='score', ascending=False).head(5))

elif selected_menu == "Kontaktformular":
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
            anfrage = {"name":name, "email":email, "nachricht":nachricht, "datum":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            st.session_state.kundenanfragen.append(anfrage)
            pd.DataFrame(st.session_state.kundenanfragen).to_csv(csv_file, index=False)
            st.success("✅ Anfrage gespeichert.")

    if st.session_state.kundenanfragen:
        st.subheader("Alle Kundenanfragen")
        st.dataframe(pd.DataFrame(st.session_state.kundenanfragen))

elif selected_menu == "Branchenübersicht":
    st.header("Branchenübersicht")
    summary = []
    for b in branches:
        df_b = st.session_state.leads_per_branch[b]
        summary.append({"Branche":b, "Anzahl Leads":len(df_b), "Durchschnittsscore":round(df_b['score'].mean(),2)})
    st.dataframe(pd.DataFrame(summary))
