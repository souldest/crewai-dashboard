import pandas as pd
from sales_leads import generate_all_leads

def generate_acquisition_plan(branch, leads_per_branch, action_icons=None, top_n=None):
    """
    Generiert den Akquiseplan für eine Branche.
    
    - branch: Branche, für die der Plan erstellt werden soll
    - leads_per_branch: Dictionary aus sales_leads.py {branch: DataFrame}
    - action_icons: Mapping für Aktionen -> Icons
    - top_n: Anzahl der qualifizierten Leads, die im Plan berücksichtigt werden
    """
    if action_icons is None:
        action_icons = {"Sofort kontaktieren":"🔴", "Anschreiben":"🟠", "Demo vereinbaren":"🟢"}

    df = leads_per_branch[branch].copy()
    
    # Nur qualifizierte Leads
    df_qual = df[df['status'] == 'qualifiziert'].sort_values(by='score', ascending=False)
    
    if top_n is not None:
        df_qual = df_qual.head(top_n)
    
    # Aktion zuweisen
    actions = []
    for i in range(len(df_qual)):
        if i < 5:
            actions.append("Sofort kontaktieren")
        elif i < 10:
            actions.append("Anschreiben")
        else:
            actions.append("Demo vereinbaren")
    df_qual['Empfohlene_Aktion'] = actions
    df_qual['Aktion_Icon'] = df_qual['Empfohlene_Aktion'].map(action_icons)
    
    # Priorität: bereits in sales_leads definiert
    df_plan = df_qual.reset_index(drop=True)
    
    return df_plan

