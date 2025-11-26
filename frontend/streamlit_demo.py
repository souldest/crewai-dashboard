import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Marketing Texte & Agenten
from technologien import TECHNOLOGIEN
from marketing_demo import HEADER, CREWAI, AGENTEN, VORTEILE, KONTAKT
from sales_leads import generate_all_leads
from akquise_plan import generate_acquisition_plan
from proposal import generate_proposals

# -----------------------------
# Streamlit Seiteneinstellungen
# -----------------------------
st.set_page_config(page_title="CrewAI Sales Dashboard", layout="wide")

# -----------------------------
# Hintergrundfarbe schwarz
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {background-color: #000000;}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# HEADER Abschnitt
# -----------------------------
st.markdown(
    f"""
    <div style='padding:20px; background-color:#0073e6; color:white; border-radius:15px; margin-bottom:20px; max-width:900px; margin:auto;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
        <h1 style='font-size:28px; text-align:center; line-height:1.4;'>{HEADER}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# CREWAI Abschnitt
# -----------------------------
st.markdown(
    f"""
    <div style='padding:20px; background-color:#4da6ff; color:white; border-radius:15px; margin-bottom:20px; max-width:900px; margin:auto;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
        <h2 style='font-size:24px; margin-bottom:12px; text-align:center;'>CrewAI – Wachstumsbooster</h2>
        <p style='font-size:18px; line-height:1.6;'>{CREWAI}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Agenten nach Funktion direkt unter CREWAI
# -----------------------------
st.markdown("<h2 style='text-align:center; color:white; margin-top:20px;'>Agenten nach Funktion</h2>", unsafe_allow_html=True)
for func_name, func_text in AGENTEN.items():
    func_text_html = func_text.replace("\n", "<br>")
    st.markdown(
        f"""
        <div style='padding:15px; background-color:#4da6ff; color:white; border-radius:15px; margin-bottom:20px; max-width:900px; margin:auto;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
            <h3 style='font-size:22px; text-align:center; margin-bottom:12px;'>{func_name}</h3>
            <p style='font-size:18px; line-height:1.6;'>{func_text_html}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Technologien Abschnitt
# -----------------------------
st.markdown(
    f"""
    <div style='padding:15px; background-color:#4da6ff; color:white; border-radius:15px; margin-bottom:20px; max-width:900px; margin:auto;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
        <h3 style='font-size:22px; margin-bottom:12px; text-align:center;'>Technologien & Infrastruktur</h3>
        <p style='font-size:18px; line-height:1.6;'>{TECHNOLOGIEN}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar Navigation & Branchen
# -----------------------------
st.sidebar.title("Navigation & Auswahl")

branches = [
    "Modellhäuser", "IT", "Finance", "Banken", "Automobil",
    "Versicherungen", "Marketing", "Werbekampagnen", "Dienstleister",
    "Freelancer", "Jobsuchende", "E-Commerce", "Bildung", "Gesundheit",
    "Tourismus", "Logistik", "Media", "Consulting", "Software", "Hardware"
]
selected_branch = st.sidebar.selectbox("Branche auswählen", branches)

sections = [
    "Branchenübersicht",
    "Sales Leads",
    "Akquiseplan",
    "Proposal",
    "KPIs & Vorteile",
    "Kontaktformular"
]
selected_section = st.sidebar.radio("Bereich wählen", sections)

# -----------------------------
# Session State initialisieren
# -----------------------------
if "leads_per_branch" not in st.session_state:
    st.session_state.leads_per_branch, st.session_state.branch_profiles = generate_all_leads(branches)

action_icons = {"Sofort kontaktieren":"🔴", "Anschreiben":"🟠", "Demo vereinbaren":"🟢"}
priority_colors = {"hoch":"red","mittel":"orange","niedrig":"green"}

# -----------------------------
# Sales Leads Tab
# -----------------------------
if selected_section == "Sales Leads":
    st.header(f"Sales Leads - {selected_branch}")
    df_leads = st.session_state.leads_per_branch[selected_branch].copy()

    st.subheader("Filter Leads")
    selected_priorities = st.multiselect("Priorität auswählen", ["hoch","mittel","niedrig"], default=["hoch","mittel","niedrig"])
    df_filtered = df_leads[df_leads["Priorität"].isin(selected_priorities)]
    st.dataframe(df_filtered, use_container_width=True)

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

    st.subheader("Filter nach empfohlener Aktion")
    selected_actions = st.multiselect("Aktion auswählen", options=list(action_icons.keys()), default=list(action_icons.keys()))
    df_filtered_plan = df_plan[df_plan["Empfohlene_Aktion"].isin(selected_actions)]
    st.dataframe(df_filtered_plan[["company","score","Priorität","Empfohlene_Aktion","Aktion_Icon"]], use_container_width=True)

    fig_bar = px.bar(df_filtered_plan, x="company", y="score",
                     color="Priorität", color_discrete_map=priority_colors,
                     text="score", title=f"Akquiseplan: Score & Priorität - {selected_branch}",
                     hover_data=["Empfohlene_Aktion"])
    fig_bar.update_layout(xaxis_title="Unternehmen", yaxis_title="Score", xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

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

    st.subheader("Filter nach Aktion")
    selected_actions = st.multiselect("Aktion auswählen", options=list(action_icons.keys()), default=list(action_icons.keys()))
    df_filtered = df_prop[df_prop["Proposal_Type"].isin(selected_actions)]

    min_score = st.slider("Minimale durchschnittliche Score", 0, 100, 0)
    df_filtered = df_filtered[df_filtered["Avg_Score"] >= min_score]

    st.dataframe(df_filtered, use_container_width=True)

    fig_bar = px.bar(df_filtered, x="Proposal_Type", y="Avg_Score",
                     text="Avg_Score", color="Proposal_Type",
                     title=f"Durchschnittlicher Score pro Aktion - {selected_branch}",
                     hover_data=["Interpretation","Handlungsempfehlung"])
    fig_bar.update_layout(yaxis_range=[0,100])
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Interpretation & Handlungsempfehlung")
    for _, row in df_filtered.iterrows():
        st.markdown(f"**{row['Proposal_Type']}**: {row['Interpretation']} – _{row['Handlungsempfehlung']}_")

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
