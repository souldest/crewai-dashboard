from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = "crewai_user"
DB_PASSWORD = "Tochter2026?"   # ändere das auf dein echtes Passwort
DB_HOST = "localhost"
DB_PORT = "5433"  # PostgreSQL 18 läuft bei dir auf Port 5433
DB_NAME = "crewai_db"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
