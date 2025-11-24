import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import random
from sqlalchemy.orm import Session

# Backend-Pfad hinzufügen, damit database und models gefunden werden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from database import engine
from models import SalesLead, SalesLeadAction, CustomerRequest

# ----------------------------
# Simulierte Daten generieren
# ----------------------------
branches = [
    "KI", "IT", "Finance", "Banken", "Automobil", "Automotive",
    "Versicherungen", "Pharma", "Biostatistik", "Transport",
    "Logistik", "Solar", "Modelhäuser", "Bau", "Lebensmittel"]

companies_per_branch = 20  # 300 Unternehmen über alle Branchen verteilen

leads_list = []
lead_id_counter = 1
for branch in branches:
    for i in range(companies_per_branch):
        company_name = f"{branch}_Firma_{i+1}"
        for lead_num in range(10):  # 10 Leads pro Unternehmen
            status = random.choice(["qualifiziert", "nicht qualifiziert"])
            score = random.randint(50, 100) if status == "qualifiziert" else random.randint(20, 49)
            recommended_action = random.choice(["Kontaktaufnahme", "Angebot senden", "Follow-up Telefonat"])
            leads_list.append({
                'lead_id': lead_id_counter,
                'company': company_name,
                'branch': branch,
                'city': f"Stadt_{random.randint(1,50)}",
                'score': score,
                'status': status,
                'recommended_action': recommended_action
            })
            lead_id_counter += 1

leads_df = pd.DataFrame(leads_list)

# ----------------------------
# Streamlit App
# ----------------------------
st.title("Sales Leads & Akquise Dashboard")
selected_branch = st.sidebar.selectbox("Branche auswählen", ["Alle"] + branches)

if selected_branch != "Alle":
    df_filtered = leads_df[leads_df['branch'] == selected_branch]
else:
    df_filtered = leads_df.copy()

# ----------------------------
# KPIs
# ----------------------------
total_leads = len(df_filtered)
qualified_leads = len(df_filtered[df_filtered['status'] == 'qualifiziert'])
not_qualified_leads = total_leads - qualified_leads

col1, col2, col3 = st.columns(3)
col1.metric("Gesamt-Leads", total_leads)
col2.metric("Qualifizierte Leads", qualified_leads)
col3.metric("Nicht qualifizierte Leads", not_qualified_leads)

# ----------------------------
# Tabellen anzeigen
# ----------------------------
st.subheader("Leads Übersicht")
st.dataframe(df_filtered)

# ----------------------------
# Graphen
# ----------------------------
st.subheader("Score-Verteilung")
fig_score = px.histogram(df_filtered, x='score', nbins=10, title='Score-Verteilung der Leads')
st.plotly_chart(fig_score, use_container_width=True)

st.subheader("Status-Verteilung")
df_filtered['color'] = df_filtered['status'].apply(lambda x: 'green' if x=='qualifiziert' else 'red')
fig_status = px.histogram(df_filtered, x='status', color='color', color_discrete_map={'green':'green','red':'red'}, title='Qualifizierte vs. nicht qualifizierte Leads')
st.plotly_chart(fig_status, use_container_width=True)

# ----------------------------
# Interaktive Aktionen & Proposal
# ----------------------------
st.header("Akquise & Proposal")
with Session(engine) as session:
    for idx, lead in df_filtered.iterrows():
        with st.expander(f"{lead['company']} - Lead {lead['lead_id']}"):
            planned_action = st.text_input(f"Aktion planen für {lead['company']}", lead['recommended_action'], key=f'action_{lead['lead_id']}')
            responsible = st.text_input(f"Verantwortlicher Sales-Mitarbeiter", '', key=f'resp_{lead['lead_id']}')
            proposal_type = st.text_input(f"Proposal Typ", '', key=f'proposal_{lead['lead_id']}')
            success_rate = st.number_input(f"Erwartete Erfolgsrate", min_value=0.0, max_value=1.0, step=0.01, key=f'success_{lead['lead_id']}')
            recommendation = st.text_area(f"Empfehlung", '', key=f'rec_{lead['lead_id']}')

            if st.button(f"Speichern {lead['company']}", key=f'save_{lead['lead_id']}'):
                action = SalesLeadAction(
                    lead_id=lead['lead_id'],
                    planned_action=planned_action,
                    responsible=responsible,
                    proposal_type=proposal_type,
                    success_rate=success_rate,
                    recommendation=recommendation
                )
                session.add(action)
                session.commit()
                st.success(f"Daten für {lead['company']} gespeichert!")

# ----------------------------
# Interpretation / Handlungsempfehlungen
# ----------------------------
st.header("Interpretation / Handlungsempfehlungen")
top_leads = df_filtered[df_filtered['status']=='qualifiziert'].sort_values('score', ascending=False).head(10)
st.write("**Top Leads:**")
st.dataframe(top_leads[['lead_id','company','score','recommended_action']])

# ----------------------------
# Kundenanfragen Formular
# ----------------------------
st.header("Kundenanfrage / Kontaktformular")
with st.form("customer_request_form"):
    name = st.text_input("Name")
    email = st.text_input("E-Mail")
    company = st.text_input("Firma")
    branch = st.selectbox("Branche", branches)
    request_text = st.text_area("Anfrage / Nachricht")
    submitted = st.form_submit_button("Absenden")

    if submitted:
        if name and email and request_text:
            with Session(engine) as session:
                customer_request = CustomerRequest(
                    name=name,
                    email=email,
                    company=company,
                    branch=branch,
                    request_text=request_text
                )
                session.add(customer_request)
                session.commit()
            st.success("Ihre Anfrage wurde erfolgreich gespeichert!")
        else:
            st.error("Bitte alle Pflichtfelder ausfüllen.")
