import pandas as pd
import numpy as np
from pathlib import Path
import random
from datetime import datetime, timedelta

# ----------------------------
# Pfade
# ----------------------------
BASE_DIR = Path("data")
BASE_DIR.mkdir(parents=True, exist_ok=True)

LEADS_FILE = BASE_DIR / "sales_leads.csv"
ACQUISITION_FILE = BASE_DIR / "acquisition_plan.csv"
PROPOSAL_FILE = BASE_DIR / "proposals.csv"

# ----------------------------
# Simulation von 50 Unternehmen
# ----------------------------
np.random.seed(42)
random.seed(42)

company_names = [f"Firma_{i:02d}" for i in range(1, 51)]
cities = ["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Düsseldorf"]
dates = [datetime.today() + timedelta(days=i) for i in range(1, 31)]

leads = []
for i, company in enumerate(company_names, 1):
    score = np.random.randint(30, 70)
    status = "Nicht qualifiziert"
    # ca. 10 Leads qualifizieren
    if i <= 10:
        score = np.random.randint(70, 100)
        status = "Qualifiziert"
    lead_id = f"{datetime.today().strftime('%Y-%m-%d')}_L{i}"
    city = random.choice(cities)
    recommended_action = "Contact & Follow-up" if status == "Qualifiziert" else "Info-Mail"
    leads.append({
        "date": datetime.today().strftime("%Y-%m-%d"),
        "lead_id": lead_id,
        "company": company,
        "city": city,
        "score": score,
        "status": status,
        "recommended_action": recommended_action
    })

df_leads = pd.DataFrame(leads)
df_leads.to_csv(LEADS_FILE, index=False)
print(f"sales_leads.csv erstellt: {LEADS_FILE}")

# ----------------------------
# Acquisition Plan generieren
# ----------------------------
actions = []
for _, row in df_leads.iterrows():
    num_actions = np.random.randint(1, 5)
    for day_offset in range(num_actions):
        action_date = (datetime.today() + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        actions.append({
            "date": action_date,
            "lead_id": row["lead_id"],
            "score": row["score"],
            "recommended_action": row["recommended_action"],
            "day": day_offset + 1,
            "action": row["recommended_action"]
        })

df_plan = pd.DataFrame(actions)
df_plan.to_csv(ACQUISITION_FILE, index=False)
print(f"acquisition_plan.csv erstellt: {ACQUISITION_FILE}")

# ----------------------------
# Proposals basierend auf Leads & Aktionen
# ----------------------------
proposals = []

# Forecast/Trend Beispiel
proposals.append({
    "Proposal_Type": "Modulhaus Forecast: umsatz",
    "Count": 1,
    "Success_Rate": 0.75,
    "Recommendation": "Trend für Umsatz: steigend"
})

# Vorrat prüfen Beispiel
proposals.append({
    "Proposal_Type": "Vorrat prüfen: vorrat",
    "Count": 1,
    "Success_Rate": 0.8,
    "Recommendation": "Vorrat unter Soll, Lager auffüllen / Produktion anpassen"
})

# Lead-basierte Proposals
for _, row in df_leads.iterrows():
    proposals.append({
        "Proposal_Type": f"Lead: {row['lead_id']}",
        "Count": 1,
        "Success_Rate": row["score"]/100,
        "Recommendation": row["recommended_action"]
    })

df_proposals = pd.DataFrame(proposals)
df_proposals.to_csv(PROPOSAL_FILE, index=False)
print(f"proposals.csv erstellt: {PROPOSAL_FILE}")
