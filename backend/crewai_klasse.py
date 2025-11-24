from pathlib import Path
import pandas as pd
import numpy as np
from random import choice, randint, sample

class CrewAI:
    def __init__(self, data_dir="backend/data"):
        self.DATA_DIR = Path(data_dir)
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.sales_leads_file = self.DATA_DIR / "sales_leads.csv"
        self.acquisition_file = self.DATA_DIR / "acquisition_plan.csv"
        self.proposal_file = self.DATA_DIR / "proposals.csv"

    # ----------------------------
    # Agent 1: Sales Leads
    # ----------------------------
    def sales_leads(self, num_companies=50, num_qualified=10):
        companies = [f"Firma_{i:03d}" for i in range(1, num_companies+1)]
        industries = ["Bau", "Immobilien", "Handwerk", "Dienstleistung"]
        cities = ["Berlin", "Hamburg", "München", "Köln", "Frankfurt"]

        qualified_indices = sample(range(num_companies), num_qualified)
        lead_status = ["Nicht qualifiziert"] * num_companies
        for idx in qualified_indices:
            lead_status[idx] = "Qualifiziert"

        scores = [randint(10, 50) for _ in range(num_companies)]
        for idx in qualified_indices:
            scores[idx] = randint(70, 100)

        product_interest = ["Modulhaus" if lead_status[i]=="Qualifiziert" else "keine" for i in range(num_companies)]
        dates = pd.date_range(start="2025-10-01", periods=num_companies).to_list()
        lead_ids = [f"{dates[i].date()}_L{i+1}" for i in range(num_companies)]
        df = pd.DataFrame({
            "date": dates,
            "lead_id": lead_ids,
            "company": companies,
            "city": [choice(cities) for _ in companies],
            "industry": [choice(industries) for _ in companies],
            "score": scores,
            "status": lead_status,
            "product_interest": product_interest,
            "recommended_action": ["Contact & Follow-up" if s=="Qualifiziert" else "keine Aktion" for s in lead_status]
        })
        df.to_csv(self.sales_leads_file, index=False)
        print(f"Sales Leads gespeichert: {self.sales_leads_file}")
        return df

    # ----------------------------
    # Agent 2: Kundengewinnung
    # ----------------------------
    def kunden_gewinnung(self, df_leads):
        plan_rows = []
        for _, row in df_leads.iterrows():
            if row["status"]=="Qualifiziert":
                for day in range(1, randint(2,5)+1):
                    plan_rows.append({
                        "date": row["date"],
                        "lead_id": row["lead_id"],
                        "score": row["score"],
                        "recommended_action": row["recommended_action"],
                        "day": day,
                        "action": row["recommended_action"]
                    })
        df_plan = pd.DataFrame(plan_rows)
        df_plan.to_csv(self.acquisition_file, index=False)
        print(f"Acquisition Plan gespeichert: {self.acquisition_file}")
        return df_plan

    # ----------------------------
    # Agent 3: Proposal
    # ----------------------------
    def proposal(self, df_plan):
        proposal_rows = []
        # Beispiel-Proposals
        proposal_rows.append({"Proposal_Type":"Forecast: Umsatz","Count":1,"Success_Rate":0.7,"Recommendation":"Trend steigend"})
        proposal_rows.append({"Proposal_Type":"Vorrat prüfen: Modulhaus","Count":1,"Success_Rate":0.8,"Recommendation":"Lager auffüllen"})

        for _, row in df_plan.iterrows():
            proposal_rows.append({
                "Proposal_Type": f"Lead: {row['lead_id']}",
                "Count": 1,
                "Success_Rate": row["score"]/100,
                "Recommendation": row["recommended_action"]
            })
        df_proposal = pd.DataFrame(proposal_rows)
        df_proposal.to_csv(self.proposal_file, index=False)
        print(f"Proposals gespeichert: {self.proposal_file}")
        return df_proposal

    # ----------------------------
    # Crew ausführen
    # ----------------------------
    def run_crew(self):
        df_leads = self.sales_leads()
        df_plan = self.kunden_gewinnung(df_leads)
        df_proposal = self.proposal(df_plan)
        return df_leads, df_plan, df_proposal

# ----------------------------
# CrewAI starten
# ----------------------------
if __name__=="__main__":
    crew = CrewAI()
    crew.run_crew()
