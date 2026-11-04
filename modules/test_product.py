"""
Bu dosya ürünün yeniden aktif hâle getirilmesini test eder.
"""

from modules.product_operations import activate_product

# ID numarası 1 olan ürünü yeniden aktif hâle getir
result = activate_product(product_id=1)

if result:
    print("Ürün başarıyla aktif hâle getirildi!")
else:
    print("Aktif hâle getirilecek ürün bulunamadı!")