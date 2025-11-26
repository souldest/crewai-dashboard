# marketing_text.py

HEADER = """
<div style='font-size:20px; line-height:1.4;'>
<b>Revolutionieren Sie Ihr Unternehmen mit KI-Agenten</b><br><br>
Die Zukunft der Automatisierung beginnt heute.<br>
Unser intelligentes System liefert leistungsstarke KI-Agenten, die Ihre Geschäftsprozesse effizienter gestalten,
Routineaufgaben automatisieren und Ihr Team bei strategisch wichtigen Entscheidungen unterstützen.<br><br>

Mit unseren Agenten können Sie:
<ul>
<li>Vertriebs- und Marketingprozesse optimieren und Leads schneller qualifizieren</li>
<li>Kundenanfragen automatisch analysieren und personalisierte Antworten liefern</li>
<li>Datenbasierte Entscheidungen treffen, die Wachstum und Umsatz steigern</li>
<li>Ressourcen freisetzen, damit Ihr Team sich auf kreative und wertschöpfende Aufgaben konzentrieren kann</li>
</ul>

Erleben Sie, wie intelligente Automatisierung Ihren Arbeitsalltag verändert und Wettbewerbsvorteile schafft.<br><br>

▶ Jetzt Demo anfragen und das volle Potenzial Ihrer KI-Agenten entdecken
</div>
"""

CREWAI = """
<div style='font-size:20px; line-height:1.4;'>
<b>CrewAI – Wachstumsbooster durch vernetzte KI-Agenten</b><br><br>

Statt isolierter Einzellösungen erhalten Sie mit CrewAI ein orchestriertes Team aus
spezialisierten KI-Agenten, das gemeinsam arbeitet, kommuniziert und Entscheidungen
autonom abstimmt.<br><br>

<b>Typische Crews:</b>
<ul>
<li><b>Sales-Crew:</b> Lead-Agent → Akquise-Agent → Proposal-Agent → CRM-Update</li>
<li><b>Management-Crew:</b> Analyse-Agent → Forecast-Agent → Controlling-Agent</li>
<li><b>Operations-Crew:</b> Data-Agent → Automations-Agent → Monitoring-Agent</li>
</ul>

<b>Was macht CrewAI einzigartig?</b>
<ul>
<li>Gemeinsamer Datenkontext in Echtzeit</li>
<li>Autonome Abstimmungen zwischen allen Agenten</li>
<li>Vollautomatisierte End-to-End-Prozesse</li>
</ul>

<b>Ihre Vorteile:</b>
<ul>
<li>Massiv schnellere Entscheidungen</li>
<li>Höhere Datenkonsistenz & Transparenz</li>
<li>Weniger manuelle Arbeit, mehr Fokus</li>
<li>Skalierbares Wachstum in Vertrieb, Operations & IT</li>
</ul>
</div>
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
