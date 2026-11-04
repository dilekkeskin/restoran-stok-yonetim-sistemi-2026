"""
Restoran Stok ve Operasyon Yönetim Sistemi
Ana uygulama penceresi.
"""

import sys
from ui.product_window import ProductWindow

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QPushButton, QWidget, QVBoxLayout
)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Ana pencere özellikleri
        self.setWindowTitle("Restoran Stok ve Operasyon Yönetim Sistemi")
        self.setGeometry(300, 150, 1000, 650)

        # Ana içerik alanını oluştur
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Dikey yerleşim düzeni oluştur
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Karşılama yazısı
        welcome_label = QLabel(
            "Restoran Stok ve Operasyon Yönetim Sistemine Hoş Geldiniz!"
        )
        welcome_label.setAlignment(Qt.AlignCenter)

        # Ürün yönetimi butonu
        product_button = QPushButton("Ürün Yönetimi")
        # Butona tıklandığında ürün yönetimi penceresini aç
        product_button.clicked.connect(self.open_product_window)
        product_button.setMinimumHeight(45)

        # Bileşenleri pencereye yerleştir
        layout.addWidget(welcome_label)
        layout.addWidget(product_button)

    def open_product_window(self):
        """Ürün yönetimi penceresini açar."""

        self.product_window = ProductWindow()
        self.product_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())