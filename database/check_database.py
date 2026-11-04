"""
Bu dosya veritabanı bağlantısını ve tablo ilişkilerini kontrol eder.
"""

from database.db_connection import get_connection


def check_database():
    connection = get_connection()

    try:
        # Yabancı anahtar kontrolünün açık olup olmadığını öğren
        foreign_keys = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()

        print("Yabancı anahtar kontrolü:", foreign_keys[0])

        # Stok hareketleri tablosunun ilişkilerini kontrol et
        stock_relations = connection.execute(
            "PRAGMA foreign_key_list(stock_movements)"
        ).fetchall()

        print("\nStok hareketleri tablosu ilişkileri:")
        for relation in stock_relations:
            print(relation)

        # Fire kayıtları tablosunun ilişkilerini kontrol et
        waste_relations = connection.execute(
            "PRAGMA foreign_key_list(waste_records)"
        ).fetchall()

        print("\nFire kayıtları tablosu ilişkileri:")
        for relation in waste_relations:
            print(relation)

        # Olmayan bir ürüne stok hareketi eklemeyi dene
        print("\nHatalı ürün ID'si kontrolü:")

        try:
            connection.execute(
                """
                INSERT INTO stock_movements
                (product_id, movement_type, quantity)
                VALUES (?, ?, ?)
                """,
                (9999, "IN", 5)
            )

            connection.commit()
            print("HATA: Geçersiz ürün kaydı kabul edildi!")

        except Exception:
            connection.rollback()
            print("Başarılı: Geçersiz ürün kaydı engellendi!")

    finally:
        connection.close()


if __name__ == "__main__":
    check_database()