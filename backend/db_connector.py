# db_connector.py
from sqlalchemy import create_engine, text

# PostgreSQL-Verbindungsstring
DB_USER = "crewai_user"
DB_PASSWORD = "Tochter2026?"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "crewai_db"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine erstellen
engine = create_engine(DATABASE_URL, echo=True)

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT now()"))
            current_time = result.fetchone()[0]
            print(f"✅ Verbindung erfolgreich! Serverzeit: {current_time}")
    except Exception as e:
        print(f"❌ Verbindung fehlgeschlagen: {e}")

def fetch_agents():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM agents"))
            for row in result.fetchall():
                print(row)
    except Exception as e:
        print(f"❌ Abfrage fehlgeschlagen: {e}")

if __name__ == "__main__":
    test_connection()
    print("Alle Agenten in der Datenbank:")
    fetch_agents()
