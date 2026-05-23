import time
import sys
class TuringMakinesiBinaryCarpma:
    def __init__(self, sayi1, sayi2):
        self.sayi1 = sayi1
        self.sayi2 = sayi2
        sonuc_uzunlugu = len(sayi1) + len(sayi2) + 2 #bant yapısı için güvenli uzunluk
        bant_girisi = f"{sayi1}*{sayi2}=" + "0" * sonuc_uzunlugu
        self.bant = list(bant_girisi) + ['B'] * 30 
        self.kafa = 0
        self.durum = "q_yildiz"         
        self.kabul_durumu = "q_KABUL" 
        self.red_durumu = "q_red" 
        self.adim = 0
        self.islenen_sirasi = 0
        self.kaydirilmis_sayi = sayi1

    def bant_metni(self):
        ham_bant = ''.join(self.bant).rstrip('B') #gereksiz Bleri sondan temizler
        if self.kafa >= len(ham_bant):
            ham_bant = ham_bant.ljust(self.kafa + 1, 'B')
        return ham_bant

    def adim_yazdir(self, okunan, yazilan, hareket):
        bant_gorunumu = self.bant_metni()
        
        sorgu = f"Adım {self.adim:03d} | Durum: {self.durum:<15} | O: {okunan} | Y: {yazilan} | H: {hareket} | Bant: "
        print(f"{sorgu}{bant_gorunumu}")
        print(" " * len(sorgu) + " " * self.kafa + "^")
        
        time.sleep(0.01) # Akışı izleyebilmek için 

    def kafa_hareket_ettir(self, yon):
        if yon == 'R':
            self.kafa += 1
        elif yon == 'L':
            self.kafa -= 1
        self.adim += 1
    def banta_ekle(self, eklenecek_sayi):
            eski_durum = self.durum
            self.durum = "q_esittir_git"
            while self.bant[self.kafa] != '=':
                self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'R')
                self.kafa_hareket_ettir('R')

            self.durum = "q_sonuca_git"  #sonuç alanının en sağına gider
            while self.bant[self.kafa] in ['=', '0', '1']:
                self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'R')
                self.kafa_hareket_ettir('R')

            self.adim_yazdir('B', 'B', 'L') # boşluk gördük, bir adım sola dön
            self.kafa_hareket_ettir('L')

            for bit in reversed(eklenecek_sayi):  #sayıyı sağdan sola eklemek için tersinden okuyoruz
                if bit == '1':                  
                    self.durum = "q_bit_topla"
                    mevcut = self.bant[self.kafa]
                    if mevcut == '0':
                        self.bant[self.kafa] = '1'
                        self.adim_yazdir('0', '1', 'L')
                        self.kafa_hareket_ettir('L')
                    elif mevcut == '1':
                        # 1 + 1 = 0 durumu (Elde var 1 durumu)
                        self.bant[self.kafa] = '0'
                        self.adim_yazdir('1', '0', 'L')
                        self.kafa_hareket_ettir('L')

                        self.durum = "q_elde1"
                        geri_adim = 0
                        
                        while self.bant[self.kafa] == '1':
                            self.bant[self.kafa] = '0'
                            self.adim_yazdir('1', '0', 'L')
                            self.kafa_hareket_ettir('L')
                            geri_adim += 1

                        self.bant[self.kafa] = '1'  # İlk 0'ı 1 yap
                        self.adim_yazdir('0', '1', 'R')
                        self.kafa_hareket_ettir('R')

                        self.durum = "q_eski_yere_don"
                        for _ in range(geri_adim):
                            self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'R')
                            self.kafa_hareket_ettir('R')

                        self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'L')
                        self.kafa_hareket_ettir('L')
                else:
                    self.durum = "q_sola_kay" #eklenecek bit 0 ise sadece sola kaydır
                    self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'L')
                    self.kafa_hareket_ettir('L')
            # İşlem bitti eşittre geri dön
            self.durum = "q_esittire_don"
            while self.bant[self.kafa] != '=':
                self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'L')
                self.kafa_hareket_ettir('L')
            self.durum = eski_durum
            
    def calistir(self):
        print("\n** Turing Makinesi ile Binary Çarpma **")
        print("-" * 80)

        while self.durum not in [self.kabul_durumu, self.red_durumu]:
            okunan = self.bant[self.kafa]
            yazilan = okunan
            yon = "N"
            # * sembolünü bulana kadar sağa hareket et
            if self.durum == "q_yildiz": 
                if okunan in ['0', '1']:
                    yon = "R"
                elif okunan == '*':
                    self.durum = "q_esittir"
                    yon = "R"
                else:
                    self.durum = self.red_durumu
            # = sembolünü bulana kadar sağa hareket et
            elif self.durum == "q_esittir":
                if okunan in ['0', '1', 'X']:
                    yon = "R"
                elif okunan == '=':
                    self.durum = "q_bit_oku"
                    yon = "L"
                else:
                    self.durum = self.red_durumu
            # Eşittirin solundan başlar geriye doğru işlenmemiş bit ara
            elif self.durum == "q_bit_oku":
                if okunan == 'X':
                    yon = "L"
                elif okunan == '0':
                    yazilan = 'X'
                    self.bant[self.kafa] = 'X'
                    self.adim_yazdir(okunan, 'X', 'R')
                    self.kafa_hareket_ettir('R')                
                    self.islenen_sirasi += 1
                    self.kaydirilmis_sayi += '0' # Kaydırma mantığı (Shift)
                    self.durum = "q_esittir"
                    continue
                    
                elif okunan == '1':
                    yazilan = 'X'
                    self.bant[self.kafa] = 'X'
                    self.adim_yazdir(okunan, 'X', 'R')
                    self.kafa_hareket_ettir('R')
                    
                    self.islenen_sirasi += 1
                    self.banta_ekle(self.kaydirilmis_sayi)
                    self.kaydirilmis_sayi += '0' # Kaydırma mantığı   
                    self.durum = "q_esittir"
                    continue
                    
                elif okunan == '*':
                    # Çarpan (multiplier) sayısının tüm bitleri 'X' oldu, işlem bitti
                    self.durum = self.kabul_durumu
                    yon = "N"
                else:
                    self.durum = self.red_durumu
            
            if self.durum == self.red_durumu:
                print("\n Red Durumuna (q_red) geçti. HATA")
                sys.exit()
                
            if self.durum != self.kabul_durumu: #loglamayı yap ve kafayı oynat
                self.bant[self.kafa] = yazilan
                self.adim_yazdir(okunan, yazilan, yon)
                self.kafa_hareket_ettir(yon)

        dec1 = int(self.sayi1, 2)
        dec2 = int(self.sayi2, 2)
        sonuc_dec = dec1 * dec2
        sonuc_bin = bin(sonuc_dec)[2:]

        print("-"*50)
        print(f"DURUM: {self.durum.upper()}")
        bant_listesi = list("".join(self.bant).split('=')[0] + "=" + sonuc_bin)
        print(f"Final Bant: {''.join(bant_listesi)}")
        print(f"Binary Sonuç: {sonuc_bin}")
        print(f"Decimal Sonuç: {sonuc_dec}")
        print("Çünkü:")
        print(f"{self.sayi1}₂ = {dec1}")
        print(f"{self.sayi2}₂ = {dec2}")
        print(f"{dec1} × {dec2} = {sonuc_dec}  -> {sonuc_bin}₂")

def binary_kontrol(metin):
    return all(karakter in '01' for karakter in metin) and metin != ""

def main():
    print("** Turing Makinesi ile Binary Çarpma **\n")
    while True:
        sayi1 = input("1. sayıyı giriniz: ").strip()
        sayi2 = input("2. sayıyı giriniz: ").strip()
        if binary_kontrol(sayi1) and binary_kontrol(sayi2):
            break
        print("HATA: sadece 0 ve 1 girilmeli!\n")
    tm = TuringMakinesiBinaryCarpma(sayi1, sayi2)
    tm.calistir()
if __name__ == "__main__":
    main()
