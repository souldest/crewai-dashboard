# marketing_text.py

HEADER = """
<div style="text-align:center; padding: 30px; background-color:#f5f7fa; border-radius:10px; margin-bottom:20px;">
    <h1 style="font-size:48px; font-weight:800; margin-bottom:20px;">
        Revolutionieren Sie Ihr Unternehmen mit KI-Agenten
    </h1>
    <p style="font-size:22px; line-height:1.5; margin-bottom:25px;">
        Die Zukunft der Automatisierung beginnt heute.<br>
        Unsere intelligenten, individuell trainierten KI-Agenten übernehmen Analyse, Planung,
        Entscheidungsfindung und operative Aufgaben – vollautomatisch und in Echtzeit.
        So werden Prozesse schneller, kosteneffizienter und skalierbar.
    </p>
    <p style="font-size:24px; font-weight:700; color:#0073e6; margin-top:20px;">
        ▶ Jetzt Demo anfragen und das Potenzial echter KI erleben.
    </p>
</div>
"""

# --- CREWAI Abschnitt ---
CREWAI = """
CrewAI – Wachstumsbooster durch vernetzte KI-Agenten

Statt isolierter Einzellösungen erhalten Sie mit CrewAI ein orchestriertes Team aus
spezialisierten KI-Agenten, das gemeinsam arbeitet, kommuniziert und Entscheidungen
autonom abstimmt.

Typische Crews:
- Sales-Crew: Lead-Agent → Akquise-Agent → Proposal-Agent → CRM-Update
- Management-Crew: Analyse-Agent → Forecast-Agent → Controlling-Agent
- Operations-Crew: Data-Agent → Automations-Agent → Monitoring-Agent

Was macht CrewAI einzigartig?
- Gemeinsamer Datenkontext in Echtzeit  
- Autonome Abstimmungen zwischen allen Agenten  
- Vollautomatisierte End-to-End-Prozesse  

Ihre Vorteile:
- Massiv schnellere Entscheidungen  
- Höhere Datenkonsistenz & Transparenz  
- Weniger manuelle Arbeit, mehr Fokus  
- Skalierbares Wachstum in Vertrieb, Operations & IT  
"""

# --- AGENTEN nach Funktion ---
AGENTEN = {
    "Analyse & Management": """
Analyse & Management
- Datenanalyse-Agent: Erkennt Muster, Chancen & Risiken
- Forecast-Agent: Umsatz-, Kosten- & Supply-Chain-Prognosen
- Controlling-Agent: KPI-Monitoring, Abweichungsalarme & Dashboards
- Data-Management-Agent: Datenqualität, Cleansing, Katalogisierung
- Preprocessing-Agent: Automatisiertes ETL & Feature Engineering
""",

    "Vertrieb & Marketing": """
Vertrieb & Marketing
- Sales Leads-Agent: Qualifiziert, bewertet & priorisiert Leads
- Vertriebs-Agent: Erstkontakt, Follow-ups, Terminierungen
- Pricing-Agent: Dynamische & KI-basierte Preisempfehlungen
- Marketing-Agent: Kampagnenoptimierung & Zielgruppenanalysen
- Social-Media-Agent: Posts, Trends & Community für Wachstum
""",

    "Produktion & Technik": """
Produktion & Technik
- Predictive-Maintenance-Agent: Verhindert Ausfälle durch Früherkennung
- Qualitätsmanagement-Agent: Fehleranalyse & Prozessoptimierung
- Supply-Chain-Agent: Steuerung von Materialfluss & Logistik
- Manufacturing-Agent: Automatisierte Produktionsüberwachung
""",

    "IT & Automatisierung": """
IT & Automatisierung
- IT-Monitoring-Agent: Überwacht Systeme, Services, Security
- DevOps-Agent: CI/CD, Tests, Dokumentation
- Automation-Agent: Wiederkehrende Office- & Systemprozesse automatisieren
- Ticket-Support-Agent: L1-L3 Automatisierung in IT-Support & Helpdesk
""",

    "ESG & Compliance": """
ESG & Compliance
- ESG-Agent: KPIs, Benchmarks & EU-Taxonomie
- Reporting-Agent: Vollautomatisiertes Nachhaltigkeitsreporting
- Compliance-Agent: Dokumentation, Audit-Check & Risikobewertung
""",

    "Forschung & Gesundheit": """
Forschung & Gesundheit
- Biostatistics-Agent: Statistische Studien & Modellierung
- MedTech-Agent: Mustererkennung & Patientenpfade
- Regulatory-Agent: ISO-, FDA- & EMA-konforme Dokumentation
""",

    "Office Automation": """
Office Automation
- Assistant-Agent: Ihr virtueller digitaler Mitarbeiter
- Invoice-Agent: Extrahiert, validiert & verarbeitet Rechnungen
- Document-Agent: Analysiert & fasst Verträge, PDFs & Berichte zusammen
- Support-Agent: 24/7 Kunden- und Mitarbeiterservice automatisiert
""",

    "Branchen-spezifische Agenten": """
Branchen-spezifische Agenten
Finance & Banken:
- Risiko-Agent, Fraud-Agent, Kreditbewertung-Agent, Portfolio-Analysen

Logistik & Transport:
- Routenoptimierungs-Agent, Dispatch-Agent, Flottenmonitoring

Lebensmittel & Ernährung:
- Qualitäts-Agent, Lieferketten-Agent, Produktdaten-Analytik

Bau & Immobilien:
- Projektplanungs-Agent, Kostenforecast-Agent, Immobilienanalyse

Freelancer & Jobsuchende:
- Bewerbungs-Agent, Profil-Optimierer, Projekt-Matching-Agent
"""
}

# --- VORTEILE ---
VORTEILE = """
Ihre Vorteile auf einen Blick
- Automatisierung repetitiver Prozesse – ohne manuelle Eingriffe
- Datenbasierte Entscheidungen in Sekunden statt Stunden
- KI-Agenten, die 24/7 arbeiten und niemals langsamer werden
- Skalierbare Lösungen für jede Branche & jedes Unternehmensmodell
- Mehr Effizienz, weniger Kosten, höherer Umsatz
- Intelligente Zusammenarbeit durch CrewAI-Teams
- Modelle & Agenten individuell anpassbar auf Ihre Daten
"""

# --- KONTAKT ---
KONTAKT = """
Kontakt & Demo

AI Solutions – KI-Agenten • Automatisierung • Data Science  
Vereinbaren Sie Ihre persönliche Demo über unser Kontaktformular.

Erleben Sie live, wie KI-Agenten Ihre Prozesse transformieren.
"""
