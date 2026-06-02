import os
from models.hash_table import HashTableAkun

class SistemUtama:
    def __init__(self):
        self.database = HashTableAkun()
        self.nama_file = "data/data_pengguna.txt" 
        self.baca_dari_file()

    def baca_dari_file(self):
        if os.path.exists(self.nama_file) == False:
            return 
            
        file = open(self.nama_file, 'r')
        for baris in file:
            data_bersih = baris.strip()
            username, password = data_bersih.split(',')
            self.database.simpan_akun(username, password)
        file.close()

    def daftar_baru(self, username, password):
        cek_user = self.database.cari_akun(username)
        if cek_user is not None:
            return False 
            
        self.database.simpan_akun(username, password)
        
        file = open(self.nama_file, 'a')
        file.write(username + "," + password + "\n")
        file.close()
        return True