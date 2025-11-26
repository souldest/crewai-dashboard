import pandas as pd
from akquise_plan import generate_acquisition_plan

def generate_proposals(branch, leads_per_branch, action_icons=None, top_n=None):
    """
    Generiert den Proposal-Report basierend auf dem Akquiseplan.
    
    - branch: Branche für die Proposal-Daten
    - leads_per_branch: Dictionary aus sales_leads.py {branch: DataFrame}
    - action_icons: Mapping für Aktionen -> Icons
    - top_n: Anzahl der Leads im Akquiseplan, die berücksichtigt werden
    """
    if action_icons is None:
        action_icons = {"Sofort kontaktieren":"🔴", "Anschreiben":"🟠", "Demo vereinbaren":"🟢"}

    # Akquiseplan für die Branche erstellen
    df_plan = generate_acquisition_plan(branch, leads_per_branch, action_icons, top_n=top_n)
    
    if df_plan.empty:
        # Leere Struktur zurückgeben, falls keine qualifizierten Leads
        return pd.DataFrame(columns=[
            "Proposal_Type", "Avg_Score", "Count", "Interpretation", "Handlungsempfehlung"
        ])
    
    relevant_actions = ["Sofort kontaktieren", "Anschreiben", "Demo vereinbaren"]
    df_rel = df_plan[df_plan["Empfohlene_Aktion"].isin(relevant_actions)].copy()
    
    # Aggregation
    agg = df_rel.groupby("Empfohlene_Aktion").agg(
        Avg_Score=("score", "mean"),
        Count=("score", "count")
    ).reset_index().rename(columns={"Empfohlene_Aktion": "Proposal_Type"})
    agg["Avg_Score"] = agg["Avg_Score"].round(2)
    
    # Interpretation
    def interpret(score):
        if score >= 75:
            return "Sehr hohe Abschlusswahrscheinlichkeit"
        elif score >= 55:
            return "Mittlere Abschlusswahrscheinlichkeit"
        else:
            return "Niedrige Abschlusswahrscheinlichkeit"

    # Handlungsempfehlung
    def recommendation(score):
        if score >= 75:
            return "Priorität: Sofort bearbeiten"
        elif score >= 55:
            return "Priorität: Nachfassen"
        else:
            return "Priorität: Demo anbieten und beobachten"
    
    agg["Interpretation"] = agg["Avg_Score"].apply(interpret)
    agg["Handlungsempfehlung"] = agg["Avg_Score"].apply(recommendation)
    
    # Sicherstellen, dass alle 3 Aktionen enthalten sind
    for act in relevant_actions:
        if act not in agg["Proposal_Type"].values:
            agg = pd.concat([agg, pd.DataFrame([{
                "Proposal_Type": act,
                "Avg_Score": 0.0,
                "Count": 0,
                "Interpretation": "Keine qualifizierten Leads",
                "Handlungsempfehlung": "Keine Aktion"
            }])], ignore_index=True)
    
    # Reihenfolge fixieren
    agg["Order"] = agg["Proposal_Type"].map({a:i for i,a in enumerate(relevant_actions)})
    agg = agg.sort_values("Order").drop(columns=["Order"]).reset_index(drop=True)
    
    return agg

