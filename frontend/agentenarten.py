import streamlit as st

# Schwarzen Hintergrund für das Dashboard setzen
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def get_agent_types_markdown():
    return """
**Arten von KI-Agenten – sofort einsatzbereit und zukunftssicher**

Unsere KI-Agenten decken eine breite Palette an Funktionen ab – von schnellen Automationen über datengetriebene Analysen bis hin zu komplexen Multi-Agenten-Systemen. Sie helfen Unternehmen, Prozesse zu beschleunigen, Fehler zu reduzieren und Entscheidungen auf Basis präziser Daten zu treffen – **rund um die Uhr, skalierbar und sicher**.

**Zusammenfassung der Agentenarten:**

| Agententyp                     | Einsatzbereich                                   | Vorteile                                                   | Status / Einsatzfähigkeit          |
|--------------------------------|-------------------------------------------------|-----------------------------------------------------------|----------------------------------|
| Reaktive Agenten               | Support, Chat, einfache Automationen           | Schnelle Reaktionen, keine Historie nötig                | 🟢 Sofort einsetzbar               |
| Modellbasierte Agenten         | Analyse, Research, Dokumentenverarbeitung     | Kontextbasierte Entscheidungen, präzise Ergebnisse      | 🟢 Sofort einsetzbar               |
| Zielorientierte Agenten        | Preisoptimierung, Disposition, Automatisierungen | Selbstständige Planung, Zielverfolgung                  | 🟢 Sofort einsetzbar               |
| Utility-Agenten                | Finance, Logistik                              | Optimale Entscheidungen nach Kosten/Nutzen/Risiko       | 🟡 In Entwicklung / skalierbar    |
| Multi-Agenten-Systeme (Crews) | Sales, Support, Marketing, Reporting           | Zusammenarbeit mehrerer Agenten, Prozessautomatisierung | 🟡 Pilotphase                     |
| Planungs-Agenten               | Produktionsplanung, Projektmanagement          | Automatisierte Ablaufplanung, Ressourceneffizienz       | 🟡 In Entwicklung                  |
| Prognose-Agenten               | Umsatz, Nachfrage, Supply-Chain               | Früherkennung von Trends, präzisere Forecasts           | 🟢 Sofort einsetzbar               |
| Überwachungs-Agenten           | IT, Security, Compliance                        | Permanente Systemüberwachung, Echtzeit-Alerts           | 🟢 Sofort einsetzbar               |
| Interaktions-Agenten           | Kundenservice, HR, Chatbots                     | Natürliche Kommunikation, schnelle Bearbeitung von Anfragen | 🟢 Sofort einsetzbar           |
| Empfehlungs-Agenten            | Marketing, E-Commerce                           | Personalisierte Empfehlungen, Umsatzsteigerung          | 🟢 Sofort einsetzbar               |

**Besonders wertvolle Agenten für Unternehmen – sofort einsetzbar:**  
- **Reaktive Agenten** – schnelle Unterstützung für Kundenservice und interne Automationen  
- **Modellbasierte Agenten** – Analysen, Research, Dokumentenmanagement  
- **Zielorientierte Agenten** – automatisierte Planung und Optimierung  
- **Empfehlungs-Agenten** – direkte Umsatzsteigerung durch personalisierte Empfehlungen  
- **Prognose-Agenten** – frühzeitige Erkennung von Trends  
- **Überwachungs-Agenten** – permanente Kontrolle von IT, Security und Compliance  

**Agenten im Aufbau – bald verfügbar:**  
- **Utility-Agenten** – Optimierung von Finance- und Logistikentscheidungen  
- **Multi-Agenten-Systeme (Crews)** – komplexe Prozessautomatisierung  
- **Planungs-Agenten** – automatisierte Produktions- und Projektplanung  

**Technologien dahinter:**  
- **KI & Machine Learning:** NLP, Deep Learning, Predictive Analytics  
- **Automatisierung & RPA:** Prozessautomatisierung, Scheduling Engines  
- **Datenanalyse & BI:** Python, R, SQL, BI-Tools  
- **Cloud & Infrastruktur:** AWS, Azure, Docker, APIs  
- **Multi-Agenten-Koordination:** Orchestrierung, Messaging-Queues, Event-Driven Architecture  

Mit CrewAI erhalten Unternehmen **sofort einsatzbereite, messbare Ergebnisse, Entlastung für Teams und nachhaltige KI-Lösungen**, die direkt Umsatz, Effizienz und Kundenzufriedenheit steigern – heute und morgen.
"""

# Anzeige in Streamlit mit hellblauer Karte und weißer Schrift
st.markdown(
    f"""
    <div style='background-color:#1a73e8; color:#ffffff; padding:20px; border-radius:12px;'>
    {get_agent_types_markdown()}
    </div>
    """,
    unsafe_allow_html=True
)
