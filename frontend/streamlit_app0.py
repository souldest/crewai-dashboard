import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ----------------------------
# Pfad zum Backend-Datenordner
# ----------------------------
import os
BASE_DIR = Path(os.path.abspath(os.path.join(__file__, "../../backend/data")))
st.write("Pfad:", BASE_DIR)
st.write("Existiert:", BASE_DIR.exists())

LEADS_FILE = BASE_DIR / "sales_leads.csv"
ACQUISITION_FILE = BASE_DIR / "acquisition_plan.csv"
PROPOSAL_FILE = BASE_DIR / "proposals.csv"

st.set_page_config(page_title="Agent Platform Dashboard (CrewAI)", layout="wide")
st.title("Agent Platform Dashboard (CrewAI)")

# ----------------------------
# Prüfen, ob Daten existieren
# ----------------------------
if not BASE_DIR.exists():
    st.error(f"Datenordner '{BASE_DIR}' existiert nicht.")
else:
    # ----------------------------
    # Sales Leads
    # ----------------------------
    if LEADS_FILE.exists():
        df_leads = pd.read_csv(LEADS_FILE)
        st.header("Sales Leads")
        st.dataframe(df_leads)

        # Leads nach Status zählen
        total_leads = len(df_leads)
        qualified = len(df_leads[df_leads['status'] == "Qualifiziert"])
        not_qualified = total_leads - qualified

        st.metric("Gesamt-Leads", total_leads)
        st.metric("Qualifizierte Leads", qualified)
        st.metric("Nicht qualifizierte Leads", not_qualified)

        # Plot: Score vs Lead
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_leads['lead_id'],
            y=df_leads['score'],
            marker_color=df_leads['score'].apply(lambda x: 'green' if x>=70 else 'red')
        ))
        fig.update_layout(title="Lead Scores", xaxis_title="Lead ID", yaxis_title="Score")
        st.plotly_chart(fig, width="stretch")

    else:
        st.warning("sales_leads.csv nicht gefunden.")

    # ----------------------------
    # Acquisition Plan
    # ----------------------------
    if ACQUISITION_FILE.exists():
        df_plan = pd.read_csv(ACQUISITION_FILE)
        st.header("Acquisition Plan")
        st.dataframe(df_plan)

        # Plot: Aktionen pro Tag
        df_actions = df_plan.groupby('date')['action'].count().reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=df_actions['date'], y=df_actions['action'], name="Aktionen"))
        fig2.update_layout(title="Aktionen pro Tag", xaxis_title="Datum", yaxis_title="Anzahl Aktionen")
        st.plotly_chart(fig2, width="stretch")

    else:
        st.warning("acquisition_plan.csv nicht gefunden.")

    # ----------------------------
    # Proposals
    # ----------------------------
    if PROPOSAL_FILE.exists():
        df_proposals = pd.read_csv(PROPOSAL_FILE)
        st.header("Proposals & Empfehlungen")
        st.dataframe(df_proposals)

        # Top Proposal anzeigen
        top_proposal = df_proposals.sort_values("Success_Rate", ascending=False).iloc[0]
        st.subheader("Bestes Proposal")
        st.write(f"{top_proposal['Proposal_Type']} | Empfehlung: {top_proposal['Recommendation']} | Erfolgsrate: {top_proposal['Success_Rate']:.2f}")

    else:
        st.warning("proposals.csv nicht gefunden.")
