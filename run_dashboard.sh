#!/bin/bash
echo " Starte CrewAI Sales Dashboard..."

# 1️⃣ Virtuelle Umgebung aktivieren
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️Virtuelle Umgebung nicht gefunden. Erstelle venv..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 2️⃣ Cache leeren
echo " Streamlit Cache leeren..."
streamlit cache clear

# 3️⃣ Streamlit starten
echo " Starte Streamlit Dashboard auf http://localhost:8501"
streamlit run frontend/streamlit_demo3.py --server.port 8501
