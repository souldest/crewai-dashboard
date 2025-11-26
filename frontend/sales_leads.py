import pandas as pd
import random
from datetime import datetime

def generate_all_leads(branches, n_companies_per_branch=45):
    """
    Simuliert Leads für alle Branchen.
    - branches: Liste von Branchen
    - n_companies_per_branch: Anzahl Unternehmen pro Branche
    """
    all_companies = []
    branch_profiles = {}

    # Zufällige Score-Profile für jede Branche erstellen
    for branch in branches:
        branch_profiles[branch] = {
            "score_mean": random.randint(50, 70),
            "score_sd": random.randint(8, 16)
        }
        # Unternehmensliste
        all_companies += [f"{branch} Company {i+1}" for i in range(n_companies_per_branch)]

    # Leads pro Branche generieren
    leads_per_branch = {}
    for branch in branches:
        n_qualifiziert = random.randint(10, 30)  # zufällig zwischen 10 und 30
        leads_per_branch[branch] = generate_branch_leads(
            all_companies, branch_profiles, branch, n_per_branch=n_companies_per_branch,
            n_qualifiziert=n_qualifiziert
        )

    return leads_per_branch, branch_profiles

def generate_branch_leads(all_companies, branch_profiles, branch, n_per_branch=45, n_qualifiziert=20):
    """
    Generiert Leads für eine einzelne Branche
    - n_qualifiziert: Anzahl der qualifizierten Leads (Top Scores)
    """
    profile = branch_profiles[branch]
    companies = [c for c in all_companies if c.startswith(branch)][:n_per_branch]

    # Score zufällig generieren
    all_scores = [max(0, min(100, random.gauss(profile['score_mean'], profile['score_sd']))) for _ in companies]
    sorted_idx = sorted(range(len(all_scores)), key=lambda i: all_scores[i], reverse=True)

    data = []
    for rank_pos, idx in enumerate(sorted_idx):
        score = all_scores[idx]
        status = 'qualifiziert' if rank_pos < n_qualifiziert else 'inqualifiziert'
        lead = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'lead_id': f'{branch[:3].upper()}-{random.randint(1,9999):04d}',
            'company': companies[idx],
            'city': random.choice(['Berlin','Hamburg','München','Köln','Frankfurt']),
            'industry': branch,
            'score': round(score,2),
            'status': status,
            'product_interest': random.choice(['Produkt A','Produkt B','Produkt C']),
            'Priorität': 'hoch' if score>70 else ('mittel' if score>40 else 'niedrig')
        }
        data.append(lead)

    df = pd.DataFrame(data).sort_values(by='score', ascending=False).reset_index(drop=True)
    return df

