class MesinEnkripsi:
    def __init__(self):
        self.kunci_matriks = [
            [2, 1], 
            [1, 1]
        ]
        self.kunci_invers = [
            [1, -1], 
            [-1, 2]
        ]

    def hitung_perkalian_matriks(self, matriks, angka_1, angka_2):
        hasil_atas = (matriks[0][0] * angka_1) + (matriks[0][1] * angka_2)
        hasil_bawah = (matriks[1][0] * angka_1) + (matriks[1][1] * angka_2)
        return [hasil_atas, hasil_bawah]

    def acak_pesan(self, teks_asli):
        if len(teks_asli) % 2 != 0: 
            teks_asli = teks_asli + " "
            
        hasil_acak = []
        for i in range(0, len(teks_asli), 2):
            huruf_pertama = ord(teks_asli[i])
            huruf_kedua = ord(teks_asli[i+1])
            
            hasil_kali = self.hitung_perkalian_matriks(self.kunci_matriks, huruf_pertama, huruf_kedua)
            
            hasil_acak.append(hasil_kali[0])
            hasil_acak.append(hasil_kali[1])
            
        return hasil_acak
        
    def kembalikan_pesan(self, kumpulan_angka):
        teks_kembali = ""
        for i in range(0, len(kumpulan_angka), 2):
            angka_pertama = kumpulan_angka[i]
            angka_kedua = kumpulan_angka[i+1]
            
            hasil_kali = self.hitung_perkalian_matriks(self.kunci_invers, angka_pertama, angka_kedua)
            
            teks_kembali = teks_kembali + chr(int(round(hasil_kali[0])))
            teks_kembali = teks_kembali + chr(int(round(hasil_kali[1])))
            
        return teks_kembali.strip()