from structures.stack import StackPesan

class HashTableAkun:
    def __init__(self):
        self.ukuran_tabel = 100
        self.tabel = []
        for i in range(self.ukuran_tabel):
            self.tabel.append(None)

    def ubah_nama_jadi_angka(self, nama):
        total_angka = 0
        for huruf in nama:
            total_angka = total_angka + ord(huruf)
        return total_angka % self.ukuran_tabel

    def simpan_akun(self, username, password):
        indeks = self.ubah_nama_jadi_angka(username)
        
        while self.tabel[indeks] is not None:
            if self.tabel[indeks][0] == username:
                self.tabel[indeks][1] = password
                return
            indeks = (indeks + 1) % self.ukuran_tabel
            
        kotak_masuk = StackPesan()
        self.tabel[indeks] = [username, password, kotak_masuk]

    def cari_akun(self, username):
        indeks = self.ubah_nama_jadi_angka(username)
        indeks_awal = indeks
        
        while self.tabel[indeks] is not None:
            if self.tabel[indeks][0] == username:
                return self.tabel[indeks] 
            
            indeks = (indeks + 1) % self.ukuran_tabel
            if indeks == indeks_awal:
                break
        return None

    def ambil_semua_username(self):
        daftar_user = []
        for laci in self.tabel:
            if laci is not None:
                daftar_user.append(laci[0])
        return daftar_user