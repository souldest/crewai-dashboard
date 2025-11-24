# frontend/streamlit_demo.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random
import sys, os

# ---------------------------------------------
# Backend-Pfad hinzufügen
# ---------------------------------------------
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.append(backend_path)

try:
    from crewai_klasse import CrewAI
except:
    CrewAI = None

# ---------------------------------------------
# Config & Farben
# ---------------------------------------------
st.set_page_config(page_title="CrewAI – Branchenneutrale Demo", layout="wide")
PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#FF5722"

st.markdown(f"""
<style>
.stButton>button {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border-radius: 8px;
    height: 50px;
    font-size: 16px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------
# Szenario-abhängige Leads generieren
# ---------------------------------------------
def generate_scenario_leads(scenario="Allgemein", num_companies=50, num_qualified=10):
    companies = [f"Unternehmen {i}" for i in range(1, num_companies+1)]
    all_industries = {
        "Modellhäuser": ["Bau", "Immobilien", "Architektur", "Investoren", "Ingenieurwesen"],
        "IT": ["Software", "Hardware", "Cloud", "Consulting", "Cybersecurity"],
        "Finance": ["Banking", "Investments", "Fintech", "Insurance", "Accounting"],
        "Banken": ["Retail Banking", "Corporate Banking", "Investment Banking"],
        "Automobil": ["OEM", "Zulieferer", "Händler", "E-Mobility", "Logistik"],
        "Versicherungen": ["Life", "Health", "Property", "Automotive", "Reinsurance"],
        "Marketing": ["Digital", "Social Media", "Content", "SEO", "Branding"],
        "Werbekampagnen": ["Online Ads", "TV", "Radio", "Print", "Events"],
        "Dienstleister": ["IT-Service", "Logistik", "Facility Management", "Beratung", "Recruiting"],
        "Freelancer": ["Designer", "Developer", "Consultant", "Writer", "Marketer"],
        "Jobsuchende": ["Engineering", "Sales", "Marketing", "Finance", "IT"]
    }
    industries = all_industries.get(scenario, ["Allgemein"])
    products = [f"{scenario} Produkt {i}" for i in range(1,4)]
    statuses = ["Neu", "In Bearbeitung", "Follow-Up", "Abgeschlossen"]
    recommended_actions = ["Kontaktaufnahme","Follow-up","Meeting","Angebot senden"]

    leads_list = []

    # Nicht-qualifizierte Leads (0-3 pro Firma)
    for company in companies:
        num_leads = random.randint(0,3)
        for _ in range(num_leads):
            lead = {
                "company": company,
                "industry": random.choice(industries),
                "score": np.round(np.random.uniform(50,79),1),
                "status": random.choice(statuses),
                "product_interest": random.choice(products),
                "recommended_action": random.choice(recommended_actions)
            }
            leads_list.append(lead)

    # 10 hochqualifizierte Leads
    qualified_companies = random.sample(companies, num_qualified)
    for company in qualified_companies:
        lead = {
            "company": company,
            "industry": random.choice(industries),
            "score": np.round(np.random.uniform(80,100),1),
            "status": "Neu",
            "product_interest": random.choice(products),
            "recommended_action": "Kontaktaufnahme"
        }
        leads_list.append(lead)

    df = pd.DataFrame(leads_list)
    return df

# ---------------------------------------------
# Akquiseplan & Proposal Funktionen
# ---------------------------------------------
def generate_plan(df):
    df_plan = df.copy()
    df_plan["Priorität"] = ["Hoch" if s>80 else "Mittel" if s>65 else "Niedrig" for s in df_plan["score"]]
    return df_plan

def generate_proposals(df_plan):
    types = ["Standard","Premium","Enterprise"]
    df = df_plan.copy()
    df["Proposal_Type"] = [random.choice(types) for _ in range(len(df))]
    df["Success_Rate"] = np.round(np.random.uniform(40,95,len(df)),1)
    return df

# ---------------------------------------------
# Szenario Auswahl in Sidebar
# ---------------------------------------------
st.sidebar.subheader("Szenario wählen")
scenario_options = ["Modellhäuser", "IT", "Finance", "Banken", "Automobil", "Versicherungen",
                    "Marketing", "Werbekampagnen", "Dienstleister", "Freelancer", "Jobsuchende"]
selected_scenario = st.sidebar.selectbox("Szenario", scenario_options)

# ---------------------------------------------
# Daten generieren
# ---------------------------------------------
df = generate_scenario_leads(selected_scenario)
df_plan = generate_plan(df)
df_prop = generate_proposals(df_plan)

# ---------------------------------------------
# Sidebar Filter
# ---------------------------------------------
st.sidebar.subheader("Filter für Leads")
industry_filter = st.sidebar.multiselect("Branche", options=df["industry"].unique(), default=df["industry"].unique())
product_filter = st.sidebar.multiselect("Produktinteresse", options=df["product_interest"].unique(), default=df["product_interest"].unique())
status_filter = st.sidebar.multiselect("Lead-Status", options=df["status"].unique(), default=df["status"].unique())
score_min, score_max = st.sidebar.slider("Score Bereich", min_value=0, max_value=100, value=(0,100))

df_filtered = df[
    (df["industry"].isin(industry_filter)) &
    (df["product_interest"].isin(product_filter)) &
    (df["status"].isin(status_filter)) &
    (df["score"].between(score_min, score_max))
]

# ---------------------------------------------
# Hauptnavigation
# ---------------------------------------------
pages = ["Leads","Akquiseplan","Proposals","KPIs","Vorteile"]
page = st.sidebar.radio("Navigation", pages)

# ---------------------------------------------
# Leads Seite
# ---------------------------------------------
if page=="Leads":
    st.header(f"🔍 Leads – Szenario: {selected_scenario}")
    st.success(f"{len(df_filtered)} Leads nach Filter")
    st.dataframe(df_filtered)
    if not df_filtered.empty:
        fig = px.histogram(df_filtered, x="score", nbins=10,
                           title="Lead Score Verteilung",
                           color_discrete_sequence=["#4CAF50"],
                           labels={"score":"Lead Score"})
        st.plotly_chart(fig, width='stretch')
    st.markdown("**Interpretation:**")
    st.info("""
    - Score >80 → Top-Priorität (qualifizierte Leads)  
    - Score 65-80 → Mittlere Priorität  
    - Score <65 → Niedrige Priorität  
    Zeigt, welche Leads am wahrscheinlichsten konvertieren.
    """)
    st.markdown("**Handlungsempfehlung:**")
    st.success("""
    - Fokus auf Top-Leads für direkte Kontaktaufnahme  
    - Mittlere Leads beobachten & Follow-Ups planen  
    - Niedrige Leads nur selektiv bearbeiten
    """)

# ---------------------------------------------
# Akquiseplan Seite
# ---------------------------------------------
elif page=="Akquiseplan":
    st.header("📈 Akquiseplan")
    st.dataframe(df_plan)
    if "recommended_action" in df_plan.columns:
        counts = df_plan["recommended_action"].value_counts()
        fig = px.bar(counts, title="Häufigkeit der Akquise-Aktionen",
                     color=counts.index,
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     labels={"value":"Anzahl","index":"Aktion"})
        st.plotly_chart(fig, width='stretch')
    st.markdown("**Interpretation & Handlungsempfehlung:**")
    st.info("""
    - Zeigt die vorgeschlagenen Aktionen und Prioritäten  
    - Fokus auf Aktionen mit hoher Priorität  
    - Regelmäßige Follow-Ups für mittlere Priorität
    """)

# ---------------------------------------------
# Proposals Seite
# ---------------------------------------------
elif page=="Proposals":
    st.header("📄 Proposal Generator")
    st.dataframe(df_prop)
    if "Proposal_Type" in df_prop.columns and "Success_Rate" in df_prop.columns:
        fig = px.bar(df_prop, x="Proposal_Type", y="Success_Rate",
                     title="Erfolgsrate der Proposal-Typen",
                     color_discrete_sequence=["#2196F3"])
        st.plotly_chart(fig, width='stretch')
    st.markdown("**Interpretation & Handlungsempfehlung:**")
    st.info("""
    - Priorisieren Sie Proposal-Typen mit hoher Erfolgsrate  
    - Analysieren und optimieren Sie Proposal-Typen mit niedriger Erfolgsrate  
    - Erfolgreiche Proposal-Typen standardmäßig einsetzen
    """)

# ---------------------------------------------
# KPI Seite
# ---------------------------------------------
elif page=="KPIs":
    st.header("📊 KPI Dashboard")
    c1,c2,c3=st.columns(3)
    c1.metric("Unternehmen gesamt",50)
    c2.metric("Qualifizierte Leads",len(df[df["score"]>80]))
    c3.metric("Durchschn. Erfolgsrate",f"{df_prop['Success_Rate'].mean():.2f}%" if "Success_Rate" in df_prop.columns else "n/a")
    
    if "score" in df.columns:
        fig1 = px.histogram(df_filtered, x="score", nbins=10, color_discrete_sequence=["#4CAF50"])
        st.plotly_chart(fig1,width='stretch')
    if "recommended_action" in df_plan.columns:
        fig2 = px.bar(df_plan["recommended_action"].value_counts(),
                      title="Akquise Aktionen Häufigkeit",
                      color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig2,width='stretch')
    if "Proposal_Type" in df_prop.columns and "Success_Rate" in df_prop.columns:
        fig3 = px.bar(df_prop, x="Proposal_Type", y="Success_Rate",
                      color_discrete_sequence=["#2196F3"])
        st.plotly_chart(fig3,width='stretch')
    st.markdown("**Interpretation & Handlungsempfehlung:**")
    st.info("""
    - Fokus auf Top-Leads und Priorisierung der Aktionen  
    - Erfolgreiche Proposal-Typen standardmäßig einsetzen  
    - Schwache Proposal-Typen analysieren & optimieren
    """)

# ---------------------------------------------
# Vorteile Seite
# ---------------------------------------------
elif page=="Vorteile":
    st.header("💼 Warum CrewAI")
    st.markdown(f"""
    <div style="display:flex;gap:20px">
    <div style='flex:1;padding:20px;background:#E8F5E9;border-radius:10px;text-align:center'>
        <h4>💡 Weniger Aufwand</h4>
        <p>Automatisierte Analyse & Planung</p>
    </div>
    <div style='flex:1;padding:20px;background:#FFF3E0;border-radius:10px;text-align:center'>
        <h4>📈 Mehr Umsatz</h4>
        <p>Bessere Conversion durch KI</p>
    </div>
    <div style='flex:1;padding:20px;background:#E1F5FE;border-radius:10px;text-align:center'>
        <h4>⚡ Schnellere Entscheidungen</h4>
        <p>Teams sehen sofort Prioritäten</p>
    </div>
    </div>
    """,unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;margin-top:30px'>
        <a href='mailto:kontakt@firma.de' style='background-color:{SECONDARY_COLOR};padding:15px 30px;color:white;border-radius:8px;text-decoration:none;font-weight:bold;'>Jetzt Kontakt aufnehmen</a>
    </div>
    """,unsafe_allow_html=True)
