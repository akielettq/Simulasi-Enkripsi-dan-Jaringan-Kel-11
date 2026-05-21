import os

# =====================================================
# SISTEM LOGIN & PENYIMPANAN DATA
# Struktur Data: Hash Table & File Handler
# =====================================================


# BAGIAN 1 : MEMBUAT HASH TABLE AKUN

class HashTableAkun:
    def __init__(self):
        self.ukuran_tabel = 100
        self.tabel = [None] * self.ukuran_tabel


    
    # Fungsi hash username (Mengubah username menjadi index tabel)
    def hash_username(self, username):
        total = 0

        for huruf in username:
            total += ord(huruf)
        return total % self.ukuran_tabel


    
    # Menyimpan akun ke hash table
    def simpan_akun(self, username, password):
        indeks = self.hash_username(username)

        while self.tabel[indeks] is not None:
            if self.tabel[indeks][0] == username:
                return False

            indeks = (indeks + 1) % self.ukuran_tabel

        self.tabel[indeks] = [username, password]
        return True


   
    # Fungsi mencari akun (Digunakan saat login)
    def cari_akun(self, username):
        indeks = self.hash_username(username)
        indeks_awal = indeks

        while self.tabel[indeks] is not None:
            if self.tabel[indeks][0] == username:
                return self.tabel[indeks]

            indeks = (indeks + 1) % self.ukuran_tabel

            if indeks == indeks_awal:
                break

        return None



# BAGIAN 2 : SISTEM LOGIN DAN PENYIMPANAN DATA

class SistemLogin:
    def __init__(self):
        self.database = HashTableAkun()
        self.nama_file = "data_pengguna.txt"
        self.baca_file()


    # Membaca data dari file
    def baca_file(self):
        if os.path.exists(self.nama_file):
            file = open(self.nama_file, "r")

            for baris in file:
                data = baris.strip()
                if data != "":
                    username, password = data.split(",")
                    self.database.simpan_akun(username, password)
            file.close()

    # Membuat akun baru
    def daftar(self, username, password):

        berhasil = self.database.simpan_akun(username, password)

        if berhasil: # menyimpan data akun ke file
            file = open(self.nama_file, "a")
            file.write(username + "," + password + "\n")
            file.close()
            return True
        return False
    

    # Fungsi login akun
    def login(self, username, password):
        akun = self.database.cari_akun(username)
        if akun is not None:
            if akun[1] == password:
                return True
        return False
    


sistem = SistemLogin()

sistem.daftar("fufufafa", "saWit43264?")
