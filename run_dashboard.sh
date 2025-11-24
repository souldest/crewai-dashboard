#!/bin/bash
# -----------------------------
# CrewAI Dashboard Deployment Script (robust)
# -----------------------------

echo "🚀 Starte CrewAI Sales Dashboard..."

# 1️⃣ Virtuelle Umgebung aktivieren oder erstellen
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️ Virtuelle Umgebung nicht gefunden. Erstelle venv..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 2️⃣ DB_HOST und DB_PORT aus backend/database.py oder Defaults
if [ -f "backend/database.py" ]; then
    DB_HOST=$(python3 -c "from backend.database import DB_HOST; print(DB_HOST)")
    DB_PORT=$(python3 -c "from backend.database import DB_PORT; print(DB_PORT)")
else
    echo "⚠️ backend/database.py nicht gefunden, verwende Standardwerte"
    DB_HOST="localhost"
    DB_PORT=5432
fi

# 3️⃣ Lokale PostgreSQL-Prüfung nur, wenn DB_HOST=localhost
if [[ "$DB_HOST" == "localhost" ]]; then
    PG_RUNNING=$(pg_isready -h $DB_HOST -p $DB_PORT)
    if [[ $PG_RUNNING != *"accepting connections"* ]]; then
        echo "⚠️ PostgreSQL nicht erreichbar auf $DB_HOST:$DB_PORT. Bitte starten Sie den DB-Server."
        exit 1
    else
        echo "✅ Lokale PostgreSQL erreichbar auf $DB_HOST:$DB_PORT"
    fi
else
    echo "🌐 Azure PostgreSQL wird verwendet, lokale Prüfung übersprungen"
fi

# 4️⃣ Backend prüfen
if [ ! -f "backend/database.py" ] || [ ! -f "backend/models.py" ]; then
    echo "⚠️ Backend nicht gefunden. Bitte sicherstellen, dass database.py und models.py existieren."
    exit 1
fi

# 5️⃣ Streamlit starten
echo "🌐 Starte Streamlit Dashboard auf http://localhost:8501"
streamlit run frontend/streamlit_demo.py
