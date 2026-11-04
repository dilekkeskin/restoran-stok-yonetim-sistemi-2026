"""
Bu dosya veritabanındaki ürünleri listelemek için kullanılır.
"""

from database.db_connection import get_connection


def list_products(status="active"):
    """Aktif, pasif veya tüm ürünleri listeler."""

    connection = get_connection()

    try:
        # Seçilen duruma göre SQL sorgusunu belirle
        if status == "active":
            query = "SELECT id, name, category, unit, critical_stock, is_active FROM products WHERE is_active = 1"
            print("Aktif Ürünler:")

        elif status == "inactive":
            query = "SELECT id, name, category, unit, critical_stock, is_active FROM products WHERE is_active = 0"
            print("Pasif Ürünler:")

        elif status == "all":
            query = "SELECT id, name, category, unit, critical_stock, is_active FROM products"
            print("Tüm Ürünler:")

        else:
            raise ValueError("Geçersiz listeleme durumu!")

        # Sorguyu çalıştır ve sonuçları al
        cursor = connection.execute(query)
        products = cursor.fetchall()

        # Ürünleri ekrana yazdır
        if products:
            for product in products:
                print(product)
        else:
            print("Listelenecek ürün bulunamadı.")

    finally:
        # İşlem bitince bağlantıyı kapat
        connection.close()


# Dosya doğrudan çalıştırıldığında aktif ürünleri listele
if __name__ == "__main__":
    list_products("all")