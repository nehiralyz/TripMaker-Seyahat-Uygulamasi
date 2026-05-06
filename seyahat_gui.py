"""
============================================================
  SEYAHAT PLANLAMA UYGULAMASI — Tam Sürüm & İptal Özellikli
============================================================
"""
import sys
from datetime import date, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFrame,
    QHeaderView, QLineEdit, QDateEdit, QDoubleSpinBox, QSpinBox, 
    QMessageBox, QGraphicsDropShadowEffect, QStackedWidget, QCheckBox,
    QGridLayout, QScrollArea, QComboBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QFont

from seyahat_sistemi import SeyahatUygulamasi

# ══════════════════════════════════════════════════════════
#  RENK PALETİ
# ══════════════════════════════════════════════════════════
C = {
    "bg":        "#F3F4F6",
    "sidebar":   "#0F4C5C",
    "card":      "#FFFFFF",
    "border":    "#D1D9E6",
    "accent":    "#E36414",
    "success":   "#2A9D8F",
    "danger":    "#EF4444",  # İptal butonu için eklendi
    "text_dark": "#1F2937",
    "text_sub":  "#6B7280",
    "card_alt":  "#F8FAFC"
}

def style_input():
    return f"""
        QLineEdit, QDateEdit, QDoubleSpinBox, QSpinBox, QComboBox {{
            background-color: #FFFFFF; color: {C['text_dark']};
            border: 1px solid {C['border']}; border-radius: 8px;
            padding: 12px; font-size: 14px;
        }}
        QLineEdit:focus, QDateEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus {{
            border: 2px solid {C['success']};
        }}
        QDateEdit::drop-down, QComboBox::drop-down {{ border: none; width: 25px; }}
        QDateEdit:disabled {{ background-color: #E5E7EB; color: #9CA3AF; }}
    """

def style_btn(renk):
    return f"""
        QPushButton {{
            background-color: {renk}; color: white; border-radius: 8px; 
            padding: 14px; font-weight: bold; font-size: 14px;
        }}
        QPushButton:hover {{ background-color: {renk}CC; }}
    """

def shadow(widget):
    fx = QGraphicsDropShadowEffect(widget)
    fx.setBlurRadius(15)
    fx.setColor(QColor(0, 0, 0, 20))
    fx.setOffset(0, 5)
    widget.setGraphicsEffect(fx)

# ══════════════════════════════════════════════════════════
#  ANA PENCERE
# ══════════════════════════════════════════════════════════
class SeyahatGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✈️ TripMaker - Seyahat Planlama ve Biletleme")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(f"background-color: {C['bg']}; color: {C['text_dark']};")

        self.sistem = SeyahatUygulamasi()
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana_lay = QHBoxLayout(merkez)
        ana_lay.setContentsMargins(0, 0, 0, 0)
        ana_lay.setSpacing(0)

        # ─── SOL MENÜ ───
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet(f"background-color: {C['sidebar']}; border-right: 1px solid {C['border']};")
        sb_lay = QVBoxLayout(sidebar)
        sb_lay.setContentsMargins(15, 40, 15, 30)

        logo = QLabel("🌍 TripMaker")
        logo.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin-bottom: 40px; border: none;")
        logo.setAlignment(Qt.AlignCenter)
        sb_lay.addWidget(logo)

        self.nav_butonlari = []
        menuler = [("➕ Yeni Rota Çiz", 0), ("🌟 Önerilen Rotalar", 1), ("✈️ Tüm Seyahatlerim", 2)]
        
        for metin, index in menuler:
            btn = QPushButton(metin)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda ch, i=index: self._sayfa_degistir(i))
            sb_lay.addWidget(btn)
            self.nav_butonlari.append(btn)

        sb_lay.addStretch()
        ana_lay.addWidget(sidebar)

        # ─── SAĞ İÇERİK ───
        self.stack = QStackedWidget()
        ana_lay.addWidget(self.stack)

        self.sayfa_yeni = self._sayfa_yeni_plan()
        self.sayfa_onerilenler = self._sayfa_onerilen_rotalar()
        self.sayfa_liste = self._sayfa_seyahatlerim()

        self.stack.addWidget(self.sayfa_yeni)         
        self.stack.addWidget(self.sayfa_onerilenler)  
        self.stack.addWidget(self.sayfa_liste)        

        self._sayfa_degistir(0)

    def _sayfa_degistir(self, index):
        self.stack.setCurrentIndex(index)
        self._tabloyu_guncelle()
        
        for i, btn in enumerate(self.nav_butonlari):
            if i == index:
                btn.setStyleSheet(f"background-color: rgba(42, 157, 143, 0.25); color: {C['success']}; text-align: left; padding: 18px; font-size: 16px; border: none; font-weight: bold; border-left: 5px solid {C['success']};")
            else:
                btn.setStyleSheet(f"background-color: transparent; color: #9CA3AF; text-align: left; padding: 18px; font-size: 16px; border: none; border-left: 5px solid transparent;")

    # ══════════════════════════════════════════════════════════
    #  SAYFA 1: YENİ ROTA (Kapsamlı Sürüm)
    # ══════════════════════════════════════════════════════════
    def _sayfa_yeni_plan(self):
        sayfa = QWidget()
        ana_v_lay = QVBoxLayout(sayfa)
        ana_v_lay.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        icerik = QWidget()
        icerik.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(icerik)
        lay.setContentsMargins(50, 30, 50, 30)
        lay.setSpacing(20)

        baslik = QLabel("✈️ Yeni Seyahat Planla")
        baslik.setStyleSheet(f"color: {C['sidebar']}; font-size: 28px; font-weight: bold;")
        lay.addWidget(baslik)

        # Yolcu Bilgileri Kartı
        kart_yolcu = QFrame()
        kart_yolcu.setStyleSheet(f"background-color: {C['card_alt']}; border-radius: 12px; border: 1px solid {C['border']};")
        shadow(kart_yolcu)
        yolcu_lay = QVBoxLayout(kart_yolcu)
        yolcu_lay.setContentsMargins(30, 25, 30, 25)
        
        lbl_y_baslik = QLabel("👤 Yolcu Bilgileri")
        lbl_y_baslik.setStyleSheet(f"color: {C['sidebar']}; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        yolcu_lay.addWidget(lbl_y_baslik)

        grid_yolcu = QGridLayout()
        grid_yolcu.setSpacing(15)
        
        self.inp_y_ad_yeni = QLineEdit()
        self.inp_y_ad_yeni.setStyleSheet(style_input())
        self.inp_y_mail_yeni = QLineEdit()
        self.inp_y_mail_yeni.setStyleSheet(style_input())
        self.inp_y_tel_yeni = QLineEdit()
        self.inp_y_tel_yeni.setPlaceholderText("05...")
        self.inp_y_tel_yeni.setStyleSheet(style_input())

        grid_yolcu.addWidget(QLabel("Ad Soyad:"), 0, 0)
        grid_yolcu.addWidget(self.inp_y_ad_yeni, 1, 0)
        grid_yolcu.addWidget(QLabel("E-Posta Adresi:"), 0, 1)
        grid_yolcu.addWidget(self.inp_y_mail_yeni, 1, 1)
        grid_yolcu.addWidget(QLabel("Telefon Numarası:"), 0, 2)
        grid_yolcu.addWidget(self.inp_y_tel_yeni, 1, 2)
        
        yolcu_lay.addLayout(grid_yolcu)
        lay.addWidget(kart_yolcu)

        # Seyahat Detayları Kartı
        kart_detay = QFrame()
        kart_detay.setStyleSheet(f"background-color: {C['card']}; border-radius: 12px; border: 1px solid {C['border']};")
        shadow(kart_detay)
        detay_lay = QVBoxLayout(kart_detay)
        detay_lay.setContentsMargins(30, 25, 30, 25)
        detay_lay.setSpacing(15)

        lbl_d_baslik = QLabel("🗺️ Seyahat & Ulaşım Detayları")
        lbl_d_baslik.setStyleSheet(f"color: {C['sidebar']}; font-size: 18px; font-weight: bold;")
        detay_lay.addWidget(lbl_d_baslik)

        grid_temel = QGridLayout()
        grid_temel.setSpacing(15)
        
        self.cb_ulke = QComboBox()
        self.cb_ulke.addItems(["Türkiye", "İtalya", "Fransa", "BAE", "Almanya", "İngiltere", "Kıbrıs", "Amerika", "Diğer"])
        self.cb_ulke.setStyleSheet(style_input())
        self.cb_ulke.setCursor(Qt.PointingHandCursor)
        self.cb_ulke.currentTextChanged.connect(self._ulke_degisti)

        self.cb_sehir = QComboBox()
        self.cb_sehir.setEditable(True)
        self.cb_sehir.setStyleSheet(style_input())
        self.cb_sehir.currentTextChanged.connect(self._rota_otomatik_doldur)

        self._ulke_degisti(self.cb_ulke.currentText()) 
        self.cb_sehir.setCurrentText("") 

        self.inp_tarih = QDateEdit()
        self.inp_tarih.setCalendarPopup(True)
        self.inp_tarih.setDate(QDate.currentDate().addDays(7))
        self.inp_tarih.setStyleSheet(style_input())

        self.chk_donus = QCheckBox("Dönüş Bileti Ekle")
        self.chk_donus.setStyleSheet(f"color: {C['text_dark']}; font-weight: bold;")
        self.inp_donus_tarihi = QDateEdit()
        self.inp_donus_tarihi.setCalendarPopup(True)
        self.inp_donus_tarihi.setDate(QDate.currentDate().addDays(14))
        self.inp_donus_tarihi.setStyleSheet(style_input())
        self.inp_donus_tarihi.setEnabled(False)
        self.chk_donus.stateChanged.connect(self._donus_ayar_degistir)

        self.cb_ulasim_tipi = QComboBox()
        self.cb_ulasim_tipi.addItems(["✈️ Uçak", "🚌 Otobüs", "🚆 Tren", "🚗 Özel Araç", "🛳️ Gemi"])
        self.cb_ulasim_tipi.setStyleSheet(style_input())
        self.cb_ulasim_tipi.setCursor(Qt.PointingHandCursor)

        self.inp_ulasim_fiyat = QDoubleSpinBox()
        self.inp_ulasim_fiyat.setSuffix(" ₺")
        self.inp_ulasim_fiyat.setMaximum(999999)
        self.inp_ulasim_fiyat.setStyleSheet(style_input())

        grid_temel.addWidget(QLabel("Gidilecek Ülke:"), 0, 0)
        grid_temel.addWidget(self.cb_ulke, 1, 0)
        grid_temel.addWidget(QLabel("Şehir (Seçin veya Yazın):"), 0, 1)
        grid_temel.addWidget(self.cb_sehir, 1, 1)
        grid_temel.addWidget(QLabel("Gidiş Tarihi:"), 0, 2)
        grid_temel.addWidget(self.inp_tarih, 1, 2)
        
        grid_temel.addWidget(self.chk_donus, 2, 0)
        grid_temel.addWidget(self.inp_donus_tarihi, 3, 0)
        grid_temel.addWidget(QLabel("Ulaşım Tipi Seçin:"), 2, 1)
        grid_temel.addWidget(self.cb_ulasim_tipi, 3, 1)
        grid_temel.addWidget(QLabel("Bilet / Yol Masrafı:"), 2, 2)
        grid_temel.addWidget(self.inp_ulasim_fiyat, 3, 2)

        detay_lay.addLayout(grid_temel)

        # Konaklama
        ozet1 = QLabel("🏨 Konaklama")
        ozet1.setStyleSheet(f"color: {C['success']}; font-weight: bold; margin-top: 10px;")
        detay_lay.addWidget(ozet1)

        row_fiyat = QHBoxLayout()
        self.inp_otel = QLineEdit()
        self.inp_otel.setPlaceholderText("Otel Adı (Opsiyonel)")
        self.inp_otel.setStyleSheet(style_input())
        self.inp_gece = QSpinBox()
        self.inp_gece.setSuffix(" Gece")
        self.inp_gece.setMinimum(1)
        self.inp_gece.setStyleSheet(style_input())
        self.inp_fiyat = QDoubleSpinBox()
        self.inp_fiyat.setSuffix(" ₺ /Gece")
        self.inp_fiyat.setMaximum(999999)
        self.inp_fiyat.setStyleSheet(style_input())
        
        row_fiyat.addWidget(self.inp_otel, 2)
        row_fiyat.addWidget(self.inp_gece, 1)
        row_fiyat.addWidget(self.inp_fiyat, 1)
        detay_lay.addLayout(row_fiyat)

        # Plan
        ozet2 = QLabel("🎯 Plan & Rota")
        ozet2.setStyleSheet(f"color: {C['accent']}; font-weight: bold; margin-top: 10px;")
        detay_lay.addWidget(ozet2)

        self.inp_rota = QLineEdit()
        self.inp_rota.setPlaceholderText("Rota (Şehir girildiğinde otomatik dolar)")
        self.inp_rota.setStyleSheet(style_input())
        detay_lay.addWidget(self.inp_rota)

        self.inp_akt = QLineEdit()
        self.inp_akt.setPlaceholderText("Aktiviteler (Virgülle ayırın)")
        self.inp_akt.setStyleSheet(style_input())
        detay_lay.addWidget(self.inp_akt)

        lay.addWidget(kart_detay)

        btn_kaydet = QPushButton("✔ Bileti ve Planı Kaydet")
        btn_kaydet.setStyleSheet(style_btn(C['success']))
        btn_kaydet.setCursor(Qt.PointingHandCursor)
        btn_kaydet.clicked.connect(self._seyahat_ekle)
        lay.addWidget(btn_kaydet)
        
        lay.addStretch()
        scroll.setWidget(icerik)
        ana_v_lay.addWidget(scroll)
        return sayfa

    def _ulke_degisti(self, ulke):
        self.cb_sehir.clear()
        if ulke == "Türkiye":
            iller = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak"]
            self.cb_sehir.addItems(sorted(iller))
        elif ulke == "İtalya":
            self.cb_sehir.addItems(["Roma", "Milano", "Venedik", "Floransa", "Napoli"])
        elif ulke == "Fransa":
            self.cb_sehir.addItems(["Paris", "Marsilya", "Lyon", "Nice", "Cannes"])
        elif ulke == "BAE":
            self.cb_sehir.addItems(["Dubai", "Abu Dabi", "Şarika"])
        elif ulke == "Almanya":
            self.cb_sehir.addItems(["Berlin", "Münih", "Frankfurt", "Hamburg", "Köln"])
        elif ulke == "İngiltere":
            self.cb_sehir.addItems(["Londra", "Manchester", "Liverpool", "Birmingham"])
        elif ulke == "Kıbrıs":
            self.cb_sehir.addItems(["Lefkoşa", "Girne", "Gazimağusa", "Baf"])
        elif ulke == "Amerika":
            self.cb_sehir.addItems(["New York", "Los Angeles", "Miami", "Chicago", "Las Vegas"])

        self.cb_sehir.setCurrentText("") 

    def _rota_otomatik_doldur(self, metin):
        hedef = metin.strip().lower()
        if not hedef:
            return

        havalimanlari = {
            "antalya": "İst -> Antalya Havalimanı -> Otele Transfer",
            "izmir": "İst -> Adnan Menderes Havalimanı -> Otele Transfer",
            "bodrum": "İst -> Milas-Bodrum Havalimanı -> Otele Transfer",
            "trabzon": "İst -> Trabzon Havalimanı -> Otele Transfer",
            "kapadokya": "İst -> Nevşehir Kapadokya Hvl. -> Göreme Transfer",
            "nevşehir": "İst -> Nevşehir Kapadokya Hvl. -> Otel",
            "roma": "İst -> Roma Fiumicino Hvl. -> Şehir Merkezi",
            "paris": "İst -> Paris CDG Hvl. -> Şehir Merkezi",
            "dubai": "İst -> Dubai Uluslararası Hvl. -> Otele Transfer",
            "kıbrıs": "İst -> Ercan Havalimanı -> Otele Transfer",
            "gaziantep": "İst -> Gaziantep Oğuzeli Hvl. -> Otele Transfer",
            "ankara": "İst -> Esenboğa Havalimanı -> Şehir Merkezi",
            "milano": "İst -> Milano Malpensa Hvl. -> Şehir Merkezi",
            "londra": "İst -> Londra Heathrow Hvl. -> Merkez"
        }
        
        for sehir, rota in havalimanlari.items():
            if sehir in hedef:
                self.inp_rota.setText(rota)
                self.cb_ulasim_tipi.setCurrentIndex(0) # Uçağı seç
                return

    def _donus_ayar_degistir(self, durum):
        self.inp_donus_tarihi.setEnabled(durum == Qt.Checked)
        if durum == Qt.Checked:
            self.inp_donus_tarihi.setDate(self.inp_tarih.date().addDays(self.inp_gece.value() if self.inp_gece.value() > 0 else 7))

    # ══════════════════════════════════════════════════════════
    #  SAYFA 2: ÖNERİLEN ROTALAR (6 Paket Tam Sürüm)
    # ══════════════════════════════════════════════════════════
    def _sayfa_onerilen_rotalar(self):
        sayfa = QWidget()
        ana_v_lay = QVBoxLayout(sayfa)
        ana_v_lay.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        icerik = QWidget()
        icerik.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(icerik)
        lay.setContentsMargins(40, 30, 40, 30)
        lay.setSpacing(20)

        baslik = QLabel("🌟 Sizin İçin Önerilen Paket Rotalar")
        baslik.setStyleSheet(f"color: {C['sidebar']}; font-size: 28px; font-weight: bold;")
        lay.addWidget(baslik)

        kisi_kart = QFrame()
        kisi_kart.setStyleSheet(f"background-color: {C['card_alt']}; border-radius: 12px; border: 1px solid {C['border']};")
        shadow(kisi_kart)
        k_lay = QVBoxLayout(kisi_kart)
        k_lay.setContentsMargins(30, 20, 30, 20)
        
        lbl_info = QLabel("Bilet için Yolcu Bilgilerini Girin:")
        lbl_info.setStyleSheet(f"color: {C['sidebar']}; font-weight: bold; font-size: 16px;")
        k_lay.addWidget(lbl_info)

        grid_yolcu_hazir = QGridLayout()
        self.inp_y_ad_hazir = QLineEdit()
        self.inp_y_ad_hazir.setStyleSheet(style_input())
        self.inp_y_mail_hazir = QLineEdit()
        self.inp_y_mail_hazir.setStyleSheet(style_input())
        self.inp_y_tel_hazir = QLineEdit()
        self.inp_y_tel_hazir.setPlaceholderText("05...")
        self.inp_y_tel_hazir.setStyleSheet(style_input())
        
        grid_yolcu_hazir.addWidget(QLabel("Ad Soyad:"), 0, 0)
        grid_yolcu_hazir.addWidget(self.inp_y_ad_hazir, 1, 0)
        grid_yolcu_hazir.addWidget(QLabel("E-Posta:"), 0, 1)
        grid_yolcu_hazir.addWidget(self.inp_y_mail_hazir, 1, 1)
        grid_yolcu_hazir.addWidget(QLabel("Telefon (05...):"), 0, 2)
        grid_yolcu_hazir.addWidget(self.inp_y_tel_hazir, 1, 2)

        k_lay.addLayout(grid_yolcu_hazir)
        lay.addWidget(kisi_kart)

        paketler = [
            {"baslik": "🎈 Kapadokya Otobüs Turu (3 Gece)", "hedef": "Nevşehir, Türkiye", "otel": "Peri Cave Hotel", "fiyat": 3500.0, "gece": 3, "ulasim_fiyat": 800.0, "ulasim_tipi": "🚌 Otobüs", "rota": "İst -> Nevşehir Otogar -> Göreme", "akt": "Balon Turu, Çömlek Yapımı"},
            {"baslik": "🍕 Romantik Roma Kaçamağı (4 Gece)", "hedef": "Roma, İtalya", "otel": "Colosseum Inn", "fiyat": 5500.0, "gece": 4, "ulasim_fiyat": 4500.0, "ulasim_tipi": "✈️ Uçak", "rota": "İst -> Roma Fiumicino -> Merkez", "akt": "Kolezyum, Trevi Çeşmesi"},
            {"baslik": "🌲 Karadeniz Yayla Turu (5 Gece)", "hedef": "Rize, Türkiye", "otel": "Ayder Doğa Tesisleri", "fiyat": 2000.0, "gece": 5, "ulasim_fiyat": 2200.0, "ulasim_tipi": "✈️ Uçak", "rota": "Trabzon Hvl -> Ayder -> Karagöl", "akt": "Rafting, Zipline"},
            {"baslik": "🐪 Büyüleyici Dubai (4 Gece)", "hedef": "Dubai, BAE", "otel": "Burj Al Arab Yakını", "fiyat": 8500.0, "gece": 4, "ulasim_fiyat": 6000.0, "ulasim_tipi": "✈️ Uçak", "rota": "İst -> Dubai Hvl -> Palm Jumeirah", "akt": "Çöl Safarisi, Burj Khalifa"},
            {"baslik": "🗼 Aşıklar Şehri Paris (3 Gece)", "hedef": "Paris, Fransa", "otel": "Montmartre Butik Otel", "fiyat": 6500.0, "gece": 3, "ulasim_fiyat": 5200.0, "ulasim_tipi": "✈️ Uçak", "rota": "İst -> Paris CDG -> Şehir Merkezi", "akt": "Eyfel Kulesi, Louvre Müzesi"},
            {"baslik": "🏖️ Antalya Özel Araç Rotası (6 Gece)", "hedef": "Antalya, Türkiye", "otel": "Kaş Resort Hotel", "fiyat": 4200.0, "gece": 6, "ulasim_fiyat": 2500.0, "ulasim_tipi": "🚗 Özel Araç", "rota": "İstanbul -> Burdur -> Kaş", "akt": "Kaputaş Plajı, Antik Kent"}
        ]

        for paket in paketler:
            kart = QFrame()
            kart.setStyleSheet(f"background-color: {C['card']}; border-left: 6px solid {C['accent']}; border-radius: 10px;")
            shadow(kart)
            h_lay = QHBoxLayout(kart)
            h_lay.setContentsMargins(25, 20, 25, 20)

            bilgi_lay = QVBoxLayout()
            lbl_baslik = QLabel(paket["baslik"])
            lbl_baslik.setStyleSheet(f"color: {C['sidebar']}; font-size: 18px; font-weight: bold;")
            
            lbl_detay = QLabel(f"🏨 Otel: {paket['otel']}   |   {paket['ulasim_tipi']}: {paket['ulasim_fiyat']:,.0f} ₺\n🗺️ Rota: {paket['rota']}\n🎯 Aktiviteler: {paket['akt']}")
            lbl_detay.setStyleSheet(f"color: {C['text_sub']}; font-size: 13px; line-height: 1.5;")
            
            bilgi_lay.addWidget(lbl_baslik)
            bilgi_lay.addWidget(lbl_detay)
            h_lay.addLayout(bilgi_lay)

            fiyat_lay = QVBoxLayout()
            toplam = (paket['fiyat'] * paket['gece']) + paket['ulasim_fiyat']
            lbl_fiyat = QLabel(f"Toplam Bütçe:\n{toplam:,.0f} ₺")
            lbl_fiyat.setStyleSheet(f"color: {C['success']}; font-weight: bold; font-size: 16px;")
            lbl_fiyat.setAlignment(Qt.AlignCenter)
            
            btn_sec = QPushButton("Paketi Seç & Bilet Kes")
            btn_sec.setStyleSheet(style_btn(C['accent']))
            btn_sec.setCursor(Qt.PointingHandCursor)
            btn_sec.clicked.connect(lambda ch, veri=paket: self._onerilen_kaydet(veri))

            fiyat_lay.addWidget(lbl_fiyat)
            fiyat_lay.addWidget(btn_sec)
            h_lay.addLayout(fiyat_lay)
            lay.addWidget(kart)

        lay.addStretch()
        scroll.setWidget(icerik)
        ana_v_lay.addWidget(scroll)
        return sayfa

    # ══════════════════════════════════════════════════════════
    #  SAYFA 3: SEYAHAT LİSTESİ VE İPTAL İŞLEMİ
    # ══════════════════════════════════════════════════════════
    def _sayfa_seyahatlerim(self):
        sayfa = QWidget()
        lay = QVBoxLayout(sayfa)
        lay.setContentsMargins(40, 30, 40, 30)
        lay.setSpacing(15)

        baslik_lay = QHBoxLayout()
        baslik = QLabel("🌍 Kaydedilmiş Tüm Seyahatler")
        baslik.setStyleSheet(f"color: {C['sidebar']}; font-size: 28px; font-weight: bold;")
        
        self.lbl_sayac = QLabel("Toplam 0 Seyahat")
        self.lbl_sayac.setStyleSheet(f"background-color: {C['border']}; color: {C['text_dark']}; padding: 8px 15px; border-radius: 12px; font-weight: bold;")
        
        baslik_lay.addWidget(baslik)
        baslik_lay.addStretch()
        baslik_lay.addWidget(self.lbl_sayac)
        lay.addLayout(baslik_lay)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7) 
        self.tablo.setHorizontalHeaderLabels(["Durum", "Yolcu", "Seyahat Yeri", "Tarihler", "Konaklama", "Toplam Bütçe", "Aksiyon"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.verticalHeader().setDefaultSectionSize(70) 
        self.tablo.setAlternatingRowColors(True)
        self.tablo.setStyleSheet(f"""
            QTableWidget {{ background-color: {C['card']}; border: none; border-radius: 10px; font-size: 13px; }}
            QTableWidget::item {{ border-bottom: 1px solid {C['border']}; padding-left: 10px; }}
            QHeaderView::section {{ background-color: #E5E7EB; color: {C['text_dark']}; padding: 15px; font-weight: bold; border: none; font-size: 14px; }}
        """)
        shadow(self.tablo)
        lay.addWidget(self.tablo)

        return sayfa

    # ══════════════════════════════════════════════════════════
    #  FONKSİYONLAR
    # ══════════════════════════════════════════════════════════
    def _tabloyu_guncelle(self):
        seyahatler = self.sistem.tum_seyahatleri_getir()
        self.tablo.setRowCount(0)
        self.lbl_sayac.setText(f"Toplam {len(seyahatler)} Bilet")

        for s in seyahatler:
            r = self.tablo.rowCount()
            self.tablo.insertRow(r)
            
            durum_metni = s.get_durum()
            if "Tamamlandı" in durum_metni:
                durum_ikon = f"⚪ {durum_metni}"
                renk = QColor(C['text_sub'])
            else:
                durum_ikon = f"🟢 {durum_metni}"
                renk = QColor(C['accent'])
            
            durum_item = QTableWidgetItem(durum_ikon)
            durum_item.setForeground(renk)
            f = QFont(); f.setBold(True); durum_item.setFont(f)
            self.tablo.setItem(r, 0, durum_item)
            
            yolcu_ad = f"👤 {s.yolcu_ad}\n📞 {s.yolcu_tel}" if s.yolcu_ad else "👤 Belirtilmemiş"
            self.tablo.setItem(r, 1, QTableWidgetItem(yolcu_ad))
            
            gidis_ulasim = f"📍 {s.gidis_yeri}\n{s.ulasim_tipi}"
            self.tablo.setItem(r, 2, QTableWidgetItem(gidis_ulasim))
            
            g_tarihi = s.tarih.strftime('%d.%m.%Y')
            tarih_str = f"G: {g_tarihi}\nD: {s.donus_tarihi}" if s.donus_tarihi else f"G: {g_tarihi}\n(Sadece Gidiş)"
            self.tablo.setItem(r, 3, QTableWidgetItem(tarih_str))
            
            k = s.get_konaklama()
            otel = f"🏨 {k.otel_adi}\n🌙 {k.gece_sayisi} Gece" if k else "🏨 Yok"
            self.tablo.setItem(r, 4, QTableWidgetItem(otel))

            bütce = s.bütce_hesapla()
            bütce_str = f"💰 {bütce:,.0f} ₺" if bütce > 0 else "-"
            self.tablo.setItem(r, 5, QTableWidgetItem(bütce_str))
            
            # --- DETAY VE İPTAL BUTONLARI BURADA ---
            btn_w = QWidget()
            btn_lay = QHBoxLayout(btn_w)
            btn_lay.setContentsMargins(5, 5, 5, 5)
            
            btn_detay = QPushButton("🔍")
            btn_detay.setToolTip("Bilet Detayı")
            btn_detay.setStyleSheet(f"background-color: {C['sidebar']}; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
            btn_detay.setCursor(Qt.PointingHandCursor)
            btn_detay.clicked.connect(lambda ch, sey=s: self._seyahat_detayi_goster(sey))
            
            btn_iptal = QPushButton("🗑️")
            btn_iptal.setToolTip("Seyahati İptal Et")
            btn_iptal.setStyleSheet(f"background-color: {C['danger']}; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
            btn_iptal.setCursor(Qt.PointingHandCursor)
            btn_iptal.clicked.connect(lambda ch, sey=s: self._seyahat_iptal_onay(sey))

            btn_lay.addWidget(btn_detay)
            btn_lay.addWidget(btn_iptal)
            self.tablo.setCellWidget(r, 6, btn_w)

    def _seyahat_iptal_onay(self, s):
        cevap = QMessageBox.question(self, "İptal Onayı", f"Sayın {s.yolcu_ad},\n\n'{s.gidis_yeri}' varışlı seyahat biletinizi iptal etmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            ok, msj = self.sistem.seyahat_iptal_et(s)
            if ok:
                QMessageBox.information(self, "Başarılı", "Bilet başarıyla iptal edildi ve sistemden kaldırıldı.")
                self._tabloyu_guncelle()
            else:
                QMessageBox.warning(self, "Hata", msj)

    def _seyahat_detayi_goster(self, s):
        plan = s.get_plan()
        rota_str = f"🗺️ Rota:\n{plan.rota}" if plan and plan.rota else "🗺️ Rota belirtilmemiş"
        akt_str = f"🎯 Aktiviteler:\n{', '.join(plan.aktiviteler)}" if plan and plan.aktiviteler else "🎯 Aktivite belirtilmemiş"
        donus = f"🔙 Dönüş: {s.donus_tarihi}" if s.donus_tarihi else f"{s.ulasim_tipi} Yön: Sadece Gidiş"
        
        k_tutar = s.get_konaklama().get_toplam_maliyet() if s.get_konaklama() else 0.0

        mesaj = f"""
--- YOLCU VE İLETİŞİM ---
👤 Ad Soyad: {s.yolcu_ad}
✉️ E-Posta: {s.yolcu_email}
📞 Telefon: {s.yolcu_tel}

--- SEYAHAT VE TARİH BİLGİSİ ---
📍 Gidiş Yeri: {s.gidis_yeri}
🛫 Gidiş Tarihi: {s.tarih.strftime('%d.%m.%Y')}
{donus}

--- TUR PLANI ---
{rota_str}

{akt_str}

--- BÜTÇE DAĞILIMI ---
{s.ulasim_tipi} Bilet/Masraf: {s.ulasim_fiyati:,.2f} ₺
🏨 Konaklama: {k_tutar:,.2f} ₺
💰 Toplam Tutar: {s.bütce_hesapla():,.2f} ₺
"""
        QMessageBox.information(self, f"Bilet Detayı - {s.yolcu_ad}", mesaj.strip())

    def _seyahat_ekle(self):
        ad = self.inp_y_ad_yeni.text().strip()
        mail = self.inp_y_mail_yeni.text().strip()
        tel = self.inp_y_tel_yeni.text().strip().replace(" ", "")
        
        ulke = self.cb_ulke.currentText().strip()
        sehir = self.cb_sehir.currentText().strip()

        if not ad or not mail or not tel or not sehir:
            QMessageBox.warning(self, "Hata", "Lütfen Yolcu Adı, Email, Telefon ve Şehir bilgilerini eksiksiz doldurun!")
            return
            
        if "@" not in mail:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir e-posta adresi girin.")
            return

        if not tel.isdigit() or not tel.startswith("05") or len(tel) != 11:
            QMessageBox.warning(self, "Geçersiz Telefon Numarası", "Lütfen geçerli bir telefon numarası girin.\nNumara sadece rakamlardan oluşmalı, '05' ile başlamalı ve 11 haneli olmalıdır.")
            return

        hedef = f"{sehir}, {ulke}"

        t = self.inp_tarih.date()
        s_tarih = date(t.year(), t.month(), t.day())
        
        donus_str = ""
        if self.chk_donus.isChecked():
            dt = self.inp_donus_tarihi.date()
            d_tarih = date(dt.year(), dt.month(), dt.day())
            if d_tarih < s_tarih:
                QMessageBox.warning(self, "Hata", "Dönüş tarihi, gidiş tarihinden önce olamaz!")
                return
            donus_str = d_tarih.strftime('%d.%m.%Y')
        
        ulasim_tipi = self.cb_ulasim_tipi.currentText()
        ulasim_fiyati = self.inp_ulasim_fiyat.value()
        otel_adi = self.inp_otel.text().strip()
        fiyat = self.inp_fiyat.value()
        gece = self.inp_gece.value()
        rota = self.inp_rota.text().strip()
        akt = self.inp_akt.text().strip()

        self.sistem.seyahat_kaydet(hedef, s_tarih, otel_adi, fiyat, gece, rota, akt, ad, mail, tel, donus_str, ulasim_fiyati, ulasim_tipi)
        
        self.inp_y_ad_yeni.clear()
        self.inp_y_mail_yeni.clear()
        self.inp_y_tel_yeni.clear()
        self.cb_ulke.setCurrentIndex(0) 
        self.cb_sehir.setCurrentText("")
        self.chk_donus.setChecked(False)
        self.cb_ulasim_tipi.setCurrentIndex(0)
        self.inp_otel.clear()
        self.inp_ulasim_fiyat.setValue(0)
        self.inp_fiyat.setValue(0)
        self.inp_gece.setValue(1)
        self.inp_rota.clear()
        self.inp_akt.clear()
        
        QMessageBox.information(self, "Başarılı", f"Biletiniz oluşturuldu Sayın {ad}!\nİyi tatiller dileriz.")
        self._sayfa_degistir(2)

    def _onerilen_kaydet(self, veri):
        ad = self.inp_y_ad_hazir.text().strip()
        mail = self.inp_y_mail_hazir.text().strip()
        tel = self.inp_y_tel_hazir.text().strip().replace(" ", "")
        
        if not ad or not mail or not tel:
            QMessageBox.warning(self, "Hata", "Lütfen paketi seçmeden önce yukarıdaki alana Ad Soyad, E-Posta ve Telefon girin.")
            return
            
        if "@" not in mail:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir e-posta adresi girin.")
            return

        if not tel.isdigit() or not tel.startswith("05") or len(tel) != 11:
            QMessageBox.warning(self, "Geçersiz Telefon Numarası", "Lütfen geçerli bir telefon numarası girin.\nNumara sadece rakamlardan oluşmalı, '05' ile başlamalı ve 11 haneli olmalıdır.")
            return

        plan_tarihi = date.today() + timedelta(days=15)
        donus_tarihi = plan_tarihi + timedelta(days=veri["gece"])
        donus_str = donus_tarihi.strftime('%d.%m.%Y')
        
        self.sistem.seyahat_kaydet(
            gidis_yeri=veri["hedef"],
            tarih=plan_tarihi,
            otel_adi=veri["otel"],
            fiyat=veri["fiyat"],
            gece=veri["gece"],
            rota=veri["rota"],
            aktiviteler=veri["akt"],
            yolcu_ad=ad,
            yolcu_email=mail,
            yolcu_tel=tel,
            donus_tarihi=donus_str,
            ulasim_fiyati=veri["ulasim_fiyat"],
            ulasim_tipi=veri["ulasim_tipi"]
        )
        
        self.inp_y_ad_hazir.clear()
        self.inp_y_mail_hazir.clear()
        self.inp_y_tel_hazir.clear()
        
        QMessageBox.information(self, "Bilet Onaylandı", f"Sayın {ad},\n'{veri['baslik']}' paketiniz onaylandı!\n\nGidiş: {plan_tarihi.strftime('%d.%m.%Y')}\nDönüş: {donus_str}")
        self._sayfa_degistir(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = SeyahatGUI()
    pencere.show()
    sys.exit(app.exec_())