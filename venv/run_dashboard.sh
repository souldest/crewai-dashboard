#!/bin/bash
# -----------------------------
# CrewAI Dashboard Deployment Script
# -----------------------------

echo "🚀 Starte CrewAI Sales Dashboard..."

# 1️⃣ Virtuelle Umgebung aktivieren
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️ Virtuelle Umgebung nicht gefunden. Erstelle venv..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 2️⃣ Prüfe ob PostgreSQL läuft (hier Port 5432 anpassen)
PG_RUNNING=$(pg_isready -p 5432)
if [[ $PG_RUNNING != *"accepting connections"* ]]; then
    echo "⚠️ PostgreSQL nicht erreichbar. Bitte starten Sie den DB-Server."
    exit 1
fi

# 3️⃣ Backend prüfen (muss database.py und models.py enthalten)
if [ ! -f "backend/database.py" ] || [ ! -f "backend/models.py" ]; then
    echo "⚠️ Backend nicht gefunden. Bitte sicherstellen, dass database.py und models.py existieren."
    exit 1
fi

# 4️⃣ Streamlit starten
echo "🌐 Starte Streamlit Dashboard auf http://localhost:8501"
streamlit run frontend/streamlit_demo.py
