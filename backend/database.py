# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Prüfen, ob Streamlit verfügbar ist (Secrets nutzen)
try:
    import streamlit as st
    USING_STREAMLIT = True
except ImportError:
    USING_STREAMLIT = False

# -----------------------------
# DB Konfiguration
# -----------------------------
if USING_STREAMLIT:
    # Streamlit Cloud: Secrets auslesen
    DB_USER = st.secrets["PGUSER"]
    DB_PASSWORD = st.secrets["PGPASSWORD"]
    DB_HOST = st.secrets["PGHOST"]
    DB_PORT = st.secrets["PGPORT"]
    DB_NAME = st.secrets["PGDATABASE"]
else:
    # Lokale Entwicklung: Standardwerte oder Umgebungsvariablen
    DB_USER = os.environ.get("DB_USER", "crewai_user")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "Tochter2026?")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5433")
    DB_NAME = os.environ.get("DB_NAME", "crewai_db")

# SQLAlchemy URL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine & Session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Info-Ausgabe zum Testen
if USING_STREAMLIT:
    st.write(f"ℹ️ DB-Verbindung: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
else:
    print(f"ℹ️ DB-Verbindung: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
