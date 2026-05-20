class HashTableAkun:

    def _init_(self):

        self.ukuran_tabel = 100
        self.tabel = [None] * self.ukuran_tabel

    # Fungsi hash
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

        kotak_masuk = StackPesan()

        self.tabel[indeks] = [username, password, kotak_masuk]

        return True

    # Mencari akun
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


