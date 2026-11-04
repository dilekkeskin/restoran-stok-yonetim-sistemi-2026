import sqlite3
from pathlib import Path

# Projenin ana klasörünü bul
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Veritabanının dosya yolunu belirle
DATABASE_PATH = PROJECT_DIR / "database" / "restoran.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    # Yabancı anahtar (Foreign Key) kontrollerini etkinleştir
    connection.execute("PRAGMA foreign_keys = ON")

    return connection