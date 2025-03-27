from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///conference.db"  # Veritabanı URL'si (SQLite örneği)

# Veritabanı bağlantısını kuruyoruz
engine = create_engine(DATABASE_URL)

# Veritabanı bağlantı oturumu (session) oluşturuyoruz
Session = sessionmaker(bind=engine)
