# frontend/streamlit_demo.py
import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# -----------------------------
# Backend-Pfad hinzufügen
# -----------------------------
import sys
import os

# Backend-Pfad hinzufügen
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Jetzt können die Module direkt importiert werden
from database import SessionLocal, Base, engine
from models import CustomerRequest

# -----------------------------
# DB Session erstellen
# -----------------------------
session = SessionLocal()

st.set_page_config(page_title="CrewAI Sales Dashboard – Branchenvergleich", layout="wide")

# -----------------------------
# Branchen / Szenarien
# -----------------------------
branches = ["Modellhäuser", "IT", "Finance", "Banken", "Automobil",
            "Versicherungen", "Marketing", "Werbekampagnen", "Dienstleister",
            "Freelancer", "Jobsuchende", "E-Commerce", "Bildung", "Gesundheit",
            "Tourismus", "Logistik", "Media", "Consulting", "Software", "Hardware"]

selected_branch = st.sidebar.selectbox("Wählen Sie eine Branche / Szenario", branches)
selected_agent = st.sidebar.radio("Agenten / Ansicht", ["Sales Leads", "Akquiseplan", "Proposal", "KPIs & Vorteile", "Kontaktformular"])

# -----------------------------
# 300 Unternehmen simulieren (15 pro Branche)
# -----------------------------
def generate_companies(branches, n_per_branch=15):
    companies = []
    for branch in branches:
        for i in range(n_per_branch):
            companies.append(f"{branch} Company {i+1}")
    return companies

all_companies = generate_companies(branches, n_per_branch=15)

# -----------------------------
# Leads pro Branche generieren (10 Leads pro Branche)
# -----------------------------
def generate_branch_leads(branch, n_leads=10):
    companies = [c for c in all_companies if branch in c]
    data = []
    for company in companies[:n_leads]:
        lead = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "lead_id": f"{company[:3]}-{random.randint(1,999):03d}",
            "company": company,
            "city": random.choice(["Berlin","Hamburg","München","Köln","Frankfurt"]),
            "industry": branch,
            "score": round(random.uniform(30,100),2),
            "status": random.choice(["qualifiziert","inqualifiziert"]),
            "product_interest": random.choice(["Produkt A","Produkt B","Produkt C"]),
            "recommended_action": random.choice(["Kontakt aufnehmen","Angebot senden","Demo vereinbaren"]),
            "Priorität": random.choice(["hoch","mittel","niedrig"])
        }
        data.append(lead)
    return pd.DataFrame(data)

# -----------------------------
# Alle Branches Leads simulieren
# -----------------------------
leads_per_branch = {branch: generate_branch_leads(branch, 10) for branch in branches}

# Ausgewählte Branche verwenden
df_leads = leads_per_branch[selected_branch]

# -----------------------------
# Akquiseplan generieren
# -----------------------------
def generate_acquisition_plan(df):
    df_plan = df.copy()
    df_plan["Akquise_Status"] = df_plan["score"].apply(lambda x: "hoch" if x>70 else ("mittel" if x>40 else "niedrig"))
    return df_plan

df_plan = generate_acquisition_plan(df_leads)

# -----------------------------
# Proposal Generator
# -----------------------------
def generate_proposals(df):
    df_prop = df.groupby("recommended_action").agg(
        Success_Rate=("score","mean")
    ).reset_index()
    df_prop["Proposal_Type"] = df_prop["recommended_action"]
    df_prop["Success_Rate"] = df_prop["Success_Rate"].round(2)
    return df_prop

df_prop = generate_proposals(df_plan)

# -----------------------------
# KPIs berechnen
# -----------------------------
total_leads = len(df_leads)
qualified_leads = df_leads[df_leads["status"]=="qualifiziert"].shape[0]
avg_score = df_leads["score"].mean()
max_rate = df_prop["Success_Rate"].max() if not df_prop.empty else 0

# -----------------------------
# Dashboard Ausgabe
# -----------------------------
st.title("CrewAI Sales Dashboard – Branchenvergleich")

# -----------------------------
# Sales Leads
# -----------------------------
if selected_agent == "Sales Leads":
    st.header(f"🎯 Sales Leads – {selected_branch}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gesamtanzahl Leads", total_leads)
    col2.metric("Qualifizierte Leads", qualified_leads)
    col3.metric("Durchschnittlicher Lead Score", f"{avg_score:.2f}")
    
    st.dataframe(df_leads, use_container_width=True)

    fig_score = px.histogram(
        df_leads,
        x="score",
        nbins=10,
        hover_data=["company","city","industry"],
        color="status",
        color_discrete_map={"qualifiziert":"green","inqualifiziert":"red"},
        title="Lead Score Verteilung"
    )
    st.plotly_chart(fig_score, use_container_width=True)
    st.markdown("**Interpretation:** Höhere Scores = besser qualifizierte Leads.")
    st.markdown("**Handlungsempfehlung:** Priorisieren Sie Leads mit Score > 50.")

# -----------------------------
# Akquiseplan
# -----------------------------
elif selected_agent == "Akquiseplan":
    st.header(f"📈 Akquiseplan – {selected_branch}")
    st.dataframe(df_plan, use_container_width=True)
    
    counts = df_plan["recommended_action"].value_counts().reset_index()
    counts.columns = ["Aktion","Anzahl"]
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
    st.markdown("**Interpretation:** Priorisieren Sie Aktionen mit hoher Häufigkeit.")
    st.markdown("**Handlungsempfehlung:** Beginnen Sie mit Aktionen, die Leads mit hoher Score betreffen.")

# -----------------------------
# Proposal
# -----------------------------
elif selected_agent == "Proposal":
    st.header(f"💼 Proposal Generator – {selected_branch}")
    st.dataframe(df_prop, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Anzahl Proposals", len(df_prop))
    col2.metric("Max. Erfolgsrate", f"{max_rate:.2f}")
    col3.metric("Durchschnittliche Erfolgsrate", f"{df_prop['Success_Rate'].mean():.2f}")
    
    fig_prop = px.bar(
        df_prop,
        x="Proposal_Type",
        y="Success_Rate",
        text_auto=True,
        title="Erfolgsrate der Proposal-Typen",
        color="Success_Rate",
        color_continuous_scale=px.colors.sequential.Cividis
    )
    st.plotly_chart(fig_prop, use_container_width=True)
    st.markdown("**Interpretation:** Zeigt, welche Proposal-Typen am besten konvertieren.")
    st.markdown("**Handlungsempfehlung:** Priorisieren Sie Proposal-Typen mit hoher Erfolgsrate.")

# -----------------------------
# KPIs & Vorteile
# -----------------------------
elif selected_agent == "KPIs & Vorteile":
    st.header(f"📊 KPIs & Vorteile – {selected_branch}")
    st.metric("Gesamtanzahl Leads", total_leads)
    st.metric("Qualifizierte Leads", qualified_leads)
    st.metric("Durchschnittlicher Lead Score", f"{avg_score:.2f}")
    st.metric("Max. Proposal Erfolgsrate", f"{max_rate:.2f}")
    
    st.markdown("""
    **Vorteile der CrewAI Simulation:**  
    - Alle Branchen können getestet werden  
    - Agenten arbeiten automatisch zusammen (Sales Leads → Akquise → Proposal)  
    - Graphen, Tabellen, Interpretation & Handlungsempfehlung für jede Branche  
    - Kundenanfragen werden direkt in PostgreSQL gespeichert  
    """)

# -----------------------------
# Kontaktformular
# -----------------------------
elif selected_agent == "Kontaktformular":
    st.header("📬 Kontaktformular / Kundenanfrage")
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("E-Mail")
        firma = st.text_input("Firma / Organisation")
        branch = st.selectbox("Branche / Szenario", branches, index=branches.index(selected_branch))
        nachricht = st.text_area("Nachricht / Anfrage")
        submit = st.form_submit_button("Anfrage senden")
        
        if submit:
            request = CustomerRequest(
                timestamp=datetime.now(),
                name=name,
                email=email,
                firma=firma,
                branch=branch,
                nachricht=nachricht
            )
            session.add(request)
            session.commit()
            st.success("✅ Ihre Anfrage wurde erfolgreich gesendet. Wir melden uns zeitnah bei Ihnen.")
    
    st.subheader("📋 Alle Kundenanfragen")
    df_requests = pd.read_sql(session.query(CustomerRequest).statement, session.bind)
    st.dataframe(df_requests, use_container_width=True)
