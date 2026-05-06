"""
============================================================
  SEYAHAT PLANLAMA SİSTEMİ - İptal Özellikli İş Mantığı
============================================================
"""
import sqlite3
from datetime import date

class Konaklama:
    def __init__(self, otel_adi: str, gecelik_fiyat: float, gece_sayisi: int = 1):
        self.otel_adi = otel_adi
        self.gecelik_fiyat = gecelik_fiyat
        self.gece_sayisi = gece_sayisi

    def get_toplam_maliyet(self) -> float:
        return self.gecelik_fiyat * self.gece_sayisi

class Plan:
    def __init__(self, rota: str, aktiviteler: list = None):
        self.rota = rota
        self.aktiviteler = aktiviteler if aktiviteler else []

class Seyahat:
    def __init__(self, seyahat_id: int, gidis_yeri: str, tarih: date, yolcu_ad: str = "", yolcu_email: str = "", yolcu_tel: str = "", donus_tarihi: str = "", ulasim_fiyati: float = 0.0, ulasim_tipi: str = "✈️ Uçak"):
        self.seyahat_id = seyahat_id
        self.gidis_yeri = gidis_yeri
        self.tarih = tarih
        self.yolcu_ad = yolcu_ad
        self.yolcu_email = yolcu_email
        self.yolcu_tel = yolcu_tel
        self.donus_tarihi = donus_tarihi
        self.ulasim_fiyati = ulasim_fiyati
        self.ulasim_tipi = ulasim_tipi
        self.__konaklama = None
        self.__plan = None

    def konaklama_ata(self, konaklama: Konaklama):
        self.__konaklama = konaklama

    def plan_ata(self, plan: Plan):
        self.__plan = plan

    def get_konaklama(self) -> Konaklama:
        return self.__konaklama

    def get_plan(self) -> Plan:
        return self.__plan

    def bütce_hesapla(self) -> float:
        toplam = self.ulasim_fiyati
        if self.__konaklama:
            toplam += self.__konaklama.get_toplam_maliyet()
        return toplam

    def get_durum(self) -> str:
        bugun = date.today()
        if self.tarih < bugun:
            return "Tamamlandı"
        elif self.tarih == bugun:
            return "Bugün!"
        else:
            kalan_gun = (self.tarih - bugun).days
            return f"{kalan_gun} gün kaldı"

class SeyahatUygulamasi:
    def __init__(self):
        self.db_yol = "seyahat_veritabani.db"
        self.seyahatler = []
        self.db_kur()
        self.verileri_yukle()

    def db_kur(self):
        with sqlite3.connect(self.db_yol) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS seyahatler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gidis_yeri TEXT, tarih TEXT, otel_adi TEXT, 
                otel_fiyat REAL, gece INTEGER, rota TEXT, aktiviteler TEXT,
                yolcu_ad TEXT, yolcu_email TEXT, yolcu_tel TEXT, donus_tarihi TEXT,
                ulasim_fiyati REAL, ulasim_tipi TEXT
            )""")
            conn.commit()

    def verileri_yukle(self):
        self.seyahatler = []
        with sqlite3.connect(self.db_yol) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM seyahatler")
            for row in cursor.fetchall():
                s_id, gidis, tarih_str, otel, fiyat, gece, rota, akt, y_ad, y_email, y_tel, d_tarih, u_fiyat, u_tipi = row
                yil, ay, gun = map(int, tarih_str.split('-'))
                tarih_obj = date(yil, ay, gun)
                yeni_s = Seyahat(s_id, gidis, tarih_obj, y_ad, y_email, y_tel, d_tarih, u_fiyat, u_tipi)
                if otel: yeni_s.konaklama_ata(Konaklama(otel, fiyat, gece))
                if rota or akt: yeni_s.plan_ata(Plan(rota, akt.split(",") if akt else []))
                self.seyahatler.append(yeni_s)

    def seyahat_kaydet(self, gidis_yeri, tarih, otel_adi, fiyat, gece, rota, aktiviteler, yolcu_ad, yolcu_email, yolcu_tel, donus_tarihi, ulasim_fiyati, ulasim_tipi):
        with sqlite3.connect(self.db_yol) as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO seyahatler (gidis_yeri, tarih, otel_adi, otel_fiyat, gece, rota, aktiviteler, yolcu_ad, yolcu_email, yolcu_tel, donus_tarihi, ulasim_fiyati, ulasim_tipi) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                           (gidis_yeri, str(tarih), otel_adi, fiyat, gece, rota, aktiviteler, yolcu_ad, yolcu_email, yolcu_tel, donus_tarihi, ulasim_fiyati, ulasim_tipi))
            conn.commit()
            self.verileri_yukle()

    def tum_seyahatleri_getir(self):
        return sorted(self.seyahatler, key=lambda s: s.tarih)

    # --- YENİ EKLENEN İPTAL FONKSİYONU ---
    def seyahat_iptal_et(self, seyahat: Seyahat):
        try:
            with sqlite3.connect(self.db_yol) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM seyahatler WHERE id = ?", (seyahat.seyahat_id,))
                conn.commit()
                self.verileri_yukle()
                return True, "Seyahat planı iptal edildi."
        except Exception as e:
            return False, f"İptal hatası: {e}"