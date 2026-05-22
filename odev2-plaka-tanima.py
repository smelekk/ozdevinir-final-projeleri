class TuringMakinesi:
    def __init__(self, plaka):
        self.bant = list(plaka) + ['B']
        self.kafa = 0

        self.durum = 'q0'
        self.kabul = 'qKABUL'
        self.red = 'qRED'   # qRED durumu 
        self.adim = 1

        self.rakamlar = "0123456789"
        self.harfler = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.gecisler = self.gecis_fonk() #geçiş fonksiyonu oluştur

    def gecis_fonk(self):
        gecis = {}
        for r in self.rakamlar:
            gecis[('q0', r)] = ('q1', r, 'R') #ilk rakam
        for r in self.rakamlar:
            gecis[('q1', r)] = ('q2', r, 'R') #ikinci rakam
        for h in self.harfler:
            gecis[('q2', h)] = ('q3', h, 'R') #birinci harf
        for h in self.harfler:
            gecis[('q3', h)] = ('q4', h, 'R') #ikinci harf
        for r in self.rakamlar:
            gecis[('q4', r)] = ('q5', r, 'R') #üçüncü rakam
        for r in self.rakamlar:
            gecis[('q5', r)] = ('q6', r, 'R') #dördüncü rakam
        for r in self.rakamlar:
            gecis[('q6', r)] = ('q7', r, 'R') #beşinci rakam
        gecis[('q7', 'B')] = (self.kabul, 'B', 'S')  #kabul durumu
        return gecis
    
    def bant_yazdir(self, okunan, yazilan, yon):
        bant_gorunum = "".join(self.bant)
        bilgi = (
            f"Adım: {self.adim} | "
            f"Durum: {self.durum} | "
            f"Okunan: {okunan} | "
            f"Yazılan: {yazilan} | "
            f"Hareket: {yon}"
        )
        print(bilgi)
        print("Bant :", bant_gorunum)
        print("       " + " " * self.kafa + "^")

    def calistir(self):
        print("TURING MAKİNESİ PLAKA TANIYICI (NNLLNNN)")
        print("Girdi:", "".join(self.bant).replace("_", ""))
        print("\n" + "-" * 60)

        while self.durum not in [self.kabul, self.red]:
            # Bant sonuna çıkılırsa boşluk oku
            if self.kafa >= len(self.bant):
                okunan = 'B'
            else:
                okunan = self.bant[self.kafa]

            anahtar = (self.durum, okunan)

            if anahtar in self.gecisler:
                yeni_durum, yazilan, yon = self.gecisler[anahtar]
                self.bant[self.kafa] = yazilan  #banda yazar
                self.bant_yazdir(okunan, yazilan, yon)  #adımı yazdırır
                self.durum = yeni_durum #durum güncellenir

                if yon == 'R': #kafayı sağa hareket ettir
                    self.kafa += 1
                elif yon == 'L':
                    self.kafa -= 1
            else:
                # qRED durumuna geçiş
                self.durum = self.red
                self.bant_yazdir(okunan, okunan, 'S')
            self.adim += 1
        if self.durum == self.kabul:
            print("SONUÇ: KABUL")
        else:
            print("SONUÇ: RED")

if __name__ == "__main__":
    while True:
        plaka = input("Plaka giriniz: ")
        
        tm = TuringMakinesi(plaka)
        tm.calistir()
        print("\n")
        break
