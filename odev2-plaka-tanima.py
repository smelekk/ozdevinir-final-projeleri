class TuringMakinesi:
    def __init__(self, girdi):
        self.girdi_orjinal = girdi
        self.bant = list(girdi) + ['B']  #bant sonuna boşluk ekleniyor
        self.kafa = 0
        self.durum = 'q0'
        self.kabul_durumu = 'qKABUL'
        self.red_durumu = 'qRED'

        self.gecis_fonksiyonu = {
            'q0': ('rakam', 'q1'),
            'q1': ('rakam', 'q2'),
            'q2': ('harf',  'q3'),
            'q3': ('harf',  'q4'),
            'q4': ('rakam', 'q5'),
            'q5': ('rakam', 'q6'),
            'q6': ('rakam', 'q7')
        }

        self.rakamlar = "0123456789"
        self.harfler = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.sonuc = None

    def karakter_turu(self, karakter):
        if karakter in self.rakamlar:
            return 'rakam'
        elif karakter in self.harfler:
            return 'harf'
        elif karakter == 'B':
            return 'bosluk'
        else:
            return 'gecersiz'

    # Bant görüntüleme

    def bandi_yazdir(self):
        bant_gorunumu = ""
        for i, karakter in enumerate(self.bant):

            if i == self.kafa:
                bant_gorunumu += f"[{karakter}] "
            else:
                bant_gorunumu += f" {karakter}  "
        return bant_gorunumu
    
    def adim_yazdir(self, okunan):
        print(f"Durum: {self.durum}  Okunan Sembol: {okunan}")
        print(f"Bant: {self.bandi_yazdir()}")
        print("-" * 50)

    # Turing Makinesi çalıştırma
    def calistir(self):
        print("\n" + "=" * 50)
        print("TURING MAKİNESİ PLAKA TANIYICI")
        print("=" * 50)
        print(f"Girdi: {self.girdi_orjinal}")
        print()

        while self.sonuc is None:
            if self.kafa >= len(self.bant):
                self.durum = self.red_durumu
                self.sonuc = "RED"
                break
                
            okunan = self.bant[self.kafa]
            
            self.adim_yazdir(okunan)
            if self.durum == 'q7':
                if okunan == 'B':  # Girdi tam 7 karakter ve bitti
                    self.durum = self.kabul_durumu
                    self.sonuc = "KABUL"
                else:  
                    self.durum = self.red_durumu
                    self.sonuc = "RED"
                break

            # GEÇİŞ FONKSİYONU KONTROLÜ (q0 - q6 arası)
            if self.durum in self.gecis_fonksiyonu:
                beklenen_tur, sonraki_durum = self.gecis_fonksiyonu[self.durum]
                guncel_tur = self.karakter_turu(okunan)
                
                if guncel_tur == beklenen_tur:
                    self.durum = sonraki_durum
                    self.kafa += 1  # Geçerli karakterde kafa sağa kayar (R)
                else:
                    # Beklenen dışında
                    self.durum = self.red_durumu
                    self.sonuc = "RED"
                    break
            else:
                self.durum = self.red_durumu
                self.sonuc = "RED"
                break

        # Sonuç çıktısı
        print(f"SONUÇ: {self.sonuc}")
        print("=" * 50)
        return self.sonuc
     
# ANA PROGRAM
if __name__ == "__main__":
    plaka = input("Plaka giriniz: ")
    tm = TuringMakinesi(plaka)
    tm.calistir()
    print()