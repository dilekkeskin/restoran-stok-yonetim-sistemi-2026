"""
Bu dosya ürünlerle ilgili veritabanı işlemlerini yönetir.
Ürün ekleme, listeleme, güncelleme ve silme fonksiyonları burada bulunur.
"""

# Veritabanı paketinden bağlantı fonksiyonunu içe aktar
from database.db_connection import get_connection

def add_product(name, category, unit, critical_stock):
    """Yeni bir ürünü veritabanına kaydeder."""

    # Veritabanı bağlantısını aç
    connection = get_connection()

    try:
        # Ürün bilgilerini products tablosuna ekle
        # Soru işaretleri (?) verileri güvenli şekilde aktarır
        connection.execute(
            """
            INSERT INTO products (name, category, unit, critical_stock)
            VALUES (?, ?, ?, ?)
            """,
            (name, category, unit, critical_stock)
        )

        # Yapılan değişikliği kalıcı olarak kaydet
        connection.commit()

        return True

    except Exception:
        # Hata oluşursa yapılan değişiklikleri geri al
        connection.rollback()

        # Hatayı gizlemeden çağıran koda bildir
        raise

    finally:
        # İşlem başarılı veya başarısız olsa da bağlantıyı kapat
        connection.close()


def update_product(product_id, name, category, unit, critical_stock):
    """Belirtilen ürünün bilgilerini günceller."""

    # Veritabanı bağlantısını aç
    connection = get_connection()

    try:
        # ID numarasına göre ürün bilgilerini güncelle
        cursor = connection.execute(
            """
            UPDATE products
            SET name = ?, category = ?, unit = ?, critical_stock = ?
            WHERE id = ?
            """,
            (name, category, unit, critical_stock, product_id)
        )

        # Değişiklikleri kalıcı olarak kaydet
        connection.commit()

        # Ürün bulunamadıysa False, güncellendiyse True döndür
        return cursor.rowcount > 0

    except Exception:
        # Hata oluşursa işlemi geri al
        connection.rollback()
        raise

    finally:
        # Veritabanı bağlantısını kapat
        connection.close()


def deactivate_product(product_id):
    """Ürünü silmeden kullanım dışı bırakır."""

    # Veritabanı bağlantısını aç
    connection = get_connection()

    try:
        # Ürünün aktiflik durumunu pasif olarak değiştir
        cursor = connection.execute(
            """
            UPDATE products
            SET is_active = 0
            WHERE id = ?
            """,
            (product_id,)
        )

        # Değişikliği kalıcı olarak kaydet
        connection.commit()

        # Ürün bulunduysa True, bulunamadıysa False döndür
        return cursor.rowcount > 0

    except Exception:
        # Hata oluşursa değişiklikleri geri al
        connection.rollback()
        raise

    finally:
        # Veritabanı bağlantısını kapat
        connection.close()

def activate_product(product_id):
    """Pasif durumdaki ürünü yeniden aktif hâle getirir."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE products
            SET is_active = 1
            WHERE id = ?
            """,
            (product_id,)
        )

        connection.commit()
        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()