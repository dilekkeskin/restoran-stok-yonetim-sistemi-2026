"""
Restoran Stok ve Operasyon Yönetim Sistemi
Ürün yönetimi ekranı.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QComboBox, QDoubleSpinBox,
    QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QFormLayout
)

from PyQt5.QtWidgets import QMessageBox
from modules.product_operations import (
    add_product,
    update_product,
    deactivate_product,
    activate_product
)
from database.db_connection import get_connection


class ProductWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Pencere özellikleri
        self.setWindowTitle("Ürün Yönetimi")
        self.setGeometry(350, 180, 950, 600)

        # Ana içerik alanı
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Başlık
        title = QLabel("ÜRÜN YÖNETİMİ")
        main_layout.addWidget(title)

        # Ürün bilgileri alanı
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ürün adını giriniz")

        # Ürün kategorisinin hazır seçeneklerden seçilmesini sağla
        self.category_input = QComboBox()

        self.category_input.addItems([
            "Et Ürünleri",
            "Tavuk Ürünleri",
            "Patates Ürünleri",
            "Peynir ve Süt Ürünleri",
            "Diğer"
        ])

        self.unit_input = QComboBox()
        self.unit_input.addItems(["kg", "adet"])

        self.critical_stock_input = QDoubleSpinBox()
        self.critical_stock_input.setRange(0, 100000)
        self.critical_stock_input.setDecimals(2)

        form_layout.addRow("Ürün Adı:", self.name_input)
        form_layout.addRow("Kategori:", self.category_input)
        form_layout.addRow("Birim:", self.unit_input)
        form_layout.addRow("Kritik Stok Seviyesi:", self.critical_stock_input)

        main_layout.addLayout(form_layout)

        # İşlem butonları
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Ürün Ekle")
        # Ürün ekleme butonuna tıklama işlemini bağla
        self.add_button.clicked.connect(self.add_product_to_database)

        self.update_button = QPushButton("Güncelle")
        # Güncelle butonuna tıklama işlemini bağla
        self.update_button.clicked.connect(self.update_selected_product)

        # Pasifleştir butonunu oluştur
        self.deactivate_button = QPushButton("Pasifleştir")
        # Pasifleştir butonuna tıklama işlemini bağla
        self.deactivate_button.clicked.connect(self.deactivate_selected_product)

        # Pasif ürünü yeniden aktifleştirme butonu
        self.activate_button = QPushButton("Yeniden Aktifleştir")
        self.activate_button.clicked.connect(self.activate_selected_product)

        main_layout.addWidget(self.activate_button)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.deactivate_button)

        main_layout.addLayout(button_layout)

        # Ürün arama alanı
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ürün adına göre ara...")
        main_layout.addWidget(self.search_input)

        # Ürün durumuna göre listeleme filtresi
        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "Aktif Ürünler",
            "Pasif Ürünler",
            "Tüm Ürünler"
        ])
        main_layout.addWidget(self.status_filter)
        # Seçim değiştiğinde ürün tablosunu yeniden yükle
        self.status_filter.currentIndexChanged.connect(self.load_products)

        # Arama alanına yazıldıkça ürün tablosunu filtrele
        self.search_input.textChanged.connect(self.load_products)


        # Ürün listesi tablosu
        self.product_table = QTableWidget()

        self.product_table.setColumnCount(5)
        self.product_table.setHorizontalHeaderLabels([
            "ID", "Ürün Adı", "Kategori", "Birim", "Kritik Stok"
        ])

        # Tabloda bir ürün seçildiğinde bilgilerini forma aktar
        self.product_table.itemSelectionChanged.connect(
            self.fill_form_with_selected_product
        )

        main_layout.addWidget(self.product_table)
        self.load_products()

        # Ürün yönetimi ekranının genel görünümünü düzenle
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F4F6F9;
            }

            QLabel {
                color: #263238;
                font-size: 13px;
            }

            QLineEdit, QComboBox, QDoubleSpinBox {
                background-color: white;
                border: 1px solid #CBD5E1;
                border-radius: 5px;
                padding: 7px;
                min-height: 22px;
            }

            QPushButton {
                background-color: #315B78;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 9px 15px;
                min-height: 25px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #24465F;
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #EDF2F7;
                border: 1px solid #CBD5E1;
                border-radius: 5px;
                gridline-color: #E2E8F0;
            }

            QHeaderView::section {
                background-color: #315B78;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

    def add_product_to_database(self):
        """Formdaki ürün bilgilerini veritabanına kaydeder."""

        # Formdaki bilgileri al
        name = self.name_input.text().strip()
        category = self.category_input.currentText()
        unit = self.unit_input.currentText()
        critical_stock = self.critical_stock_input.value()

        # Ürün adının boş bırakılmasını engelle
        if not name:
            QMessageBox.warning(self, "Uyarı", "Ürün adı boş bırakılamaz!")
            return

        try:
            # Ürünü veritabanına kaydet
            add_product(name, category, unit, critical_stock)

            QMessageBox.information(
                self, "Başarılı", "Ürün başarıyla eklendi!"
            )

            # Form alanlarını temizle
            self.name_input.clear()
            self.critical_stock_input.setValue(0)

            # Ürün tablosunu yenile
            self.load_products()

        except Exception as error:
            QMessageBox.critical(
                self, "Hata", f"Ürün eklenirken hata oluştu:\n{error}"
            )

    def deactivate_selected_product(self):
        """Seçilen ürünü silmeden pasif duruma getirir."""

        # Tabloda seçili satırı öğren
        selected_row = self.product_table.currentRow()

        # Kullanıcı herhangi bir ürün seçmemişse işlemi durdur
        if selected_row < 0:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Lütfen pasifleştirmek istediğiniz ürünü seçin!"
            )
            return

        # Seçilen ürünün ID değerini tablodan al
        product_id = int(self.product_table.item(selected_row, 0).text())

        # Pasifleştirme işlemi için kullanıcıdan onay al
        answer = QMessageBox.question(
            self,
            "Pasifleştirme Onayı",
            "Seçilen ürünü pasifleştirmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        # Kullanıcı Hayır derse işlemi durdur
        if answer != QMessageBox.Yes:
            return

        # Pasifleştirme işlemini veritabanında gerçekleştir
        try:
            success = deactivate_product(product_id)

            if success:
                QMessageBox.information(
                    self,
                    "Başarılı",
                    "Ürün başarıyla pasifleştirildi!"
                )
                self.load_products()
            else:
                QMessageBox.warning(
                    self,
                    "Uyarı",
                    "Ürün pasifleştirilemedi!"
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Hata",
                f"İşlem sırasında hata oluştu:\n{error}"
            )

    def activate_selected_product(self):
        """Seçilen pasif ürünü yeniden aktif hale getirir."""

        # Tabloda seçili satırı kontrol et
        selected_row = self.product_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Lütfen aktifleştirmek istediğiniz ürünü seçin!"
            )
            return

        # Seçilen ürünün ID değerini al
        product_id = int(self.product_table.item(selected_row, 0).text())

        try:
            success = activate_product(product_id)

            if success:
                QMessageBox.information(
                    self,
                    "Başarılı",
                    "Ürün yeniden aktifleştirildi!"
                )
                self.load_products()
            else:
                QMessageBox.warning(
                    self,
                    "Uyarı",
                    "Ürün aktifleştirilemedi!"
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Hata",
                f"İşlem sırasında hata oluştu:\n{error}"
            )

    def update_selected_product(self):
        """Seçilen ürünün bilgilerini veritabanında günceller."""

        selected_row = self.product_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self, "Uyarı", "Lütfen güncellemek istediğiniz ürünü seçin!"
            )
            return

        product_id = int(self.product_table.item(selected_row, 0).text())

        # Formdaki güncel bilgileri al
        name = self.name_input.text().strip()
        category = self.category_input.currentText()
        unit = self.unit_input.currentText()
        critical_stock = self.critical_stock_input.value()

        if not name:
            QMessageBox.warning(self, "Uyarı", "Ürün adı boş bırakılamaz!")
            return

        try:
            success = update_product(
                product_id, name, category, unit, critical_stock
            )

            if success:
                QMessageBox.information(
                    self, "Başarılı", "Ürün başarıyla güncellendi!"
                )
                self.load_products()
            else:
                QMessageBox.warning(
                    self, "Uyarı", "Ürün güncellenemedi!"
                )

        except Exception as error:
            QMessageBox.critical(
                self, "Hata", f"Güncelleme sırasında hata oluştu:\n{error}"
            )

    def fill_form_with_selected_product(self):
        """Seçilen ürünün bilgilerini giriş alanlarına aktarır."""

        selected_row = self.product_table.currentRow()

        if selected_row < 0:
            return

        # Tablodaki ürün bilgilerini al
        name = self.product_table.item(selected_row, 1).text()
        category = self.product_table.item(selected_row, 2).text()
        unit = self.product_table.item(selected_row, 3).text()
        critical_stock = float(
            self.product_table.item(selected_row, 4).text()
        )

        # Bilgileri form alanlarına aktar
        self.name_input.setText(name)
        self.category_input.setCurrentText(category)
        self.unit_input.setCurrentText(unit)
        self.critical_stock_input.setValue(critical_stock)



    def load_products(self):
        """Ürünleri durum ve ürün adına göre filtreleyerek listeler."""

        selected_status = self.status_filter.currentText()
        search_text = self.search_input.text().strip()

        # SQL sorgusuna eklenecek koşulları ve parametreleri hazırla
        conditions = []
        parameters = []

        if selected_status == "Aktif Ürünler":
            conditions.append("is_active = 1")
        elif selected_status == "Pasif Ürünler":
            conditions.append("is_active = 0")

        # Ürün adına göre arama koşulu ekle
        if search_text:
            conditions.append("name LIKE ?")
            parameters.append(f"%{search_text}%")

        # Koşulları SQL sorgusuna ekle
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        connection = get_connection()

        try:
            cursor = connection.execute(
                f"""
                SELECT id, name, category, unit, critical_stock
                FROM products
                {where_clause}
                ORDER BY name
                """,
                parameters
            )

            products = cursor.fetchall()

            self.product_table.setRowCount(len(products))

            for row_index, product in enumerate(products):
                for column_index, value in enumerate(product):
                    self.product_table.setItem(
                        row_index,
                        column_index,
                        QTableWidgetItem(str(value))
                    )

        finally:
            connection.close()


# Bu dosya doğrudan çalıştırıldığında ürün penceresini aç
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = ProductWindow()
    window.show()

    sys.exit(app.exec_())