import sqlite3
from pathlib import Path

# Proje klasörünün ana dizinini bul
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Veritabanı ve SQL dosyalarının yolları
DATABASE_PATH = PROJECT_DIR / "database" / "restoran.db"
SCHEMA_PATH = PROJECT_DIR / "database" / "schema.sql"


def create_database():
    # SQLite veritabanına bağlan
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        # SQL dosyasındaki komutları oku
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            schema = file.read()

        # Tabloları oluştur
        connection.executescript(schema)
        connection.commit()

        print("Veritabanı ve tablolar başarıyla oluşturuldu!")

    finally:
        # Veritabanı bağlantısını kapat
        connection.close()


if __name__ == "__main__":
    create_database()