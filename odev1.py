class TuringMakinesi:
    def __init__(self, bant_metni):
        self.bant = list(bant_metni)
        self.kafa = 0
        self.durum = "q_birinciyi_oku"
        self.adim = 0
        self.shift_sayaci = 0
        self.birinciyi_ayristir = ""

    def banta_ekle(self):
        baslangic_kafa = self.kafa

        # 1. '=' isaretini bul
        self.durum = "q_esittir_bul_topla"
        while self.bant[self.kafa] != '=':
            self.hareket_et("R")
            self.adim += 1
            self.durumu_yazdir(self.bant[self.kafa], self.bant[self.kafa], "R")

        # 2. Banttaki sıfırların en sonuna (en sağa) git
        self.durum = "q_sona_git"
        while self.kafa < len(self.bant) - 1:
            self.hareket_et("R")
            self.adim += 1
            self.durumu_yazdir(self.bant[self.kafa], self.bant[self.kafa], "R")

        # 3. Shift (kaydırma) sayacı kadar sola gel (Basamağı hizala)
        self.durum = "q_sola_hizala"
        for _ in range(self.shift_sayaci):
            self.hareket_et("L")
            self.adim += 1
            self.durumu_yazdir(self.bant[self.kafa], self.bant[self.kafa], "L")

        # 4. Sadece 1. sayıyı sağdan sola banta ekle (Elde hesabı dâhil)
        self.durum = "q_banta_topla"
        for bit in reversed(self.birinciyi_ayristir):
            if bit == '1':
                gecici_kafa = self.kafa
                while True:
                    okunan = self.bant[self.kafa]
                    if okunan == '0':
                        self.bant[self.kafa] = '1'
                        self.adim += 1
                        self.durumu_yazdir('0', '1', "N")
                        break
                    elif okunan == '1':
                        self.bant[self.kafa] = '0'
                        self.adim += 1
                        self.durumu_yazdir('1', '0', "L")
                        self.hareket_et("L")
                    elif okunan == '=':
                        break 

                while self.kafa < gecici_kafa:
                    self.hareket_et("R")

            # Bir sonraki bit için sola kay
            self.hareket_et("L")
            self.adim += 1
            self.durumu_yazdir(self.bant[self.kafa], self.bant[self.kafa], "L")

        # 5. İşlemi bitirip kaldığımız 'X' bitine geri dön
        self.durum = "q_esittire_don"
        while self.kafa > baslangic_kafa:
            self.hareket_et("L")
            self.adim += 1
            self.durumu_yazdir(self.bant[self.kafa], self.bant[self.kafa], "L")

    def durumu_yazdir(self, okunan, yazilan, hareket):
        bant_str = "".join(self.bant)
        prefix = f"Adım {self.adim:03d} | Durum: {self.durum:20} | O: {okunan} | Y: {yazilan} | H: {hareket} | Bant: "
        print(f"{prefix}{bant_str}")
        print(" " * len(prefix) + " " * self.kafa + "^")

    def hareket_et(self, yon):
        if yon == "R":
            self.kafa += 1
            if self.kafa >= len(self.bant):
                self.bant.append(" ")
        elif yon == "L":
            self.kafa -= 1
            if self.kafa < 0:
                self.bant.insert(0, " ")
                self.kafa = 0

    def calistir(self):
        print("\n--- Turing Makinesi Simülasyonu Başladı ---")

        while self.durum not in ["q_kabul", "q_red"]:
            self.adim += 1
            okunan_sembol = self.bant[self.kafa] if self.kafa < len(self.bant) else " "
            yazilan_sembol = okunan_sembol
            yon = "N"

            if self.durum == "q_birinciyi_oku":
                if okunan_sembol in ["0", "1"]:
                    self.birinciyi_ayristir += okunan_sembol
                    yon = "R"
                elif okunan_sembol == "*":
                    self.durum = "q_esittir_bul"
                    yon = "R"
                else:
                    self.durum = "q_red"

            elif self.durum == "q_esittir_bul":
                if okunan_sembol in ["0", "1"]:
                    yon = "R"
                elif okunan_sembol == "=":
                    self.durum = "q_sagdan_oku"
                    yon = "L"
                else:
                    self.durum = "q_red"

            elif self.durum == "q_sagdan_oku":
                if okunan_sembol == "X":
                    yon = "L"
                elif okunan_sembol == "0":
                    yazilan_sembol = "X"
                    self.durum = "q_sadece_kaydir"
                    yon = "N"
                elif okunan_sembol == "1":
                    yazilan_sembol = "X"
                    self.durum = "q_topla_ve_kaydir"
                    yon = "N"
                elif okunan_sembol == "*":
                    self.durum = "q_yazmaya_git"
                    yon = "R"
                else:
                    self.durum = "q_red"

            elif self.durum == "q_sadece_kaydir":
                self.shift_sayaci += 1
                self.durum = "q_sagdan_oku"
                yon = "L"

            elif self.durum == "q_topla_ve_kaydir":
                self.banta_ekle()
                self.shift_sayaci += 1
                self.durum = "q_sagdan_oku"
                yon = "L"

            elif self.durum == "q_yazmaya_git":
                self.durum = "q_kabul"
                yon = "N"

            if self.kafa < len(self.bant):
                self.bant[self.kafa] = yazilan_sembol

            self.durumu_yazdir(okunan_sembol, yazilan_sembol, yon)
            self.hareket_et(yon)

        if self.durum == "q_red":
            print("\n RED Durumu: Geçersiz Girdi")
        else:
            print("\n--- Çarpma İşlemi Tamamlandı ---")


def ikili_sayi_mi(deger):
    return all(karakter in "01" for karakter in deger) and len(deger) > 0

def main():
    print("=== Turing Makinesi ile Binary Çarpma Hesaplayıcı ===\n")
    while True:
        birinci_sayi = input("Birinci sayıyı giriniz (Multiplicand) : ").strip()
        ikinci_sayi = input("İkinci sayıyı giriniz (Multiplier)   : ").strip()

        if ikili_sayi_mi(birinci_sayi) and ikili_sayi_mi(ikinci_sayi):
            break
        print("HATA: Girdiğiniz değerler yalnızca '0' ve '1' içermelidir!\n")

    sifir_dolgu_miktari = len(birinci_sayi) + len(ikinci_sayi) + 1
    bant_formatli = f"{birinci_sayi}*{ikinci_sayi}=" + ("0" * sifir_dolgu_miktari)
    print(f"\nBaşlangıç Bant Formatı: {bant_formatli}")

    tm = TuringMakinesi(bant_formatli)
    tm.calistir()

    dec1 = int(birinci_sayi, 2)
    dec2 = int(ikinci_sayi, 2)
    dec_sonuc = dec1 * dec2
    bin_sonuc = bin(dec_sonuc)[2:]
    bant_sonuc_str = "".join(tm.bant).split('=')[1]
    bant_temiz_sonuc = bant_sonuc_str.lstrip('0') or '0'

    print("\n" + "="*40)
    print("=== NİHAİ SONUÇ EKRANI ===")
    print(f"Çözülen İşlem : {birinci_sayi} * {ikinci_sayi}")
    print(f"Son Bant      : {''.join(tm.bant)}")
    print(f"Banttan Okunan: {bant_temiz_sonuc}")
    print(f"Binary Sonuç  : {bin_sonuc}")
    print(f"Decimal Çözüm : {dec1} x {dec2} = {dec_sonuc}")
    print("="*40)

if __name__ == "__main__":
    main()