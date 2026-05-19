import os
import time

# =======================================================
# 1. STACK & QUEUE (Tumpukan Pesan & Antrean Jaringan)
# =======================================================
class StackPesan:
    def __init__(self):
        self.daftar_pesan = []
        
    def tambah_pesan(self, pesan):
        self.daftar_pesan.append(pesan)
        
    def ambil_pesan_terakhir(self):
        if len(self.daftar_pesan) == 0:
            return None
        else:
            return self.daftar_pesan.pop()

class QueueJaringan:
    def __init__(self):
        self.antrean = []
        
    def masuk_antrean(self, paket):
        self.antrean.append(paket)
        
    def keluar_antrean(self):
        if len(self.antrean) == 0:
            return None
        else:
            return self.antrean.pop(0) # Ambil indeks paling depan

# =======================================================
# 2. HASH TABLE & FILE HANDLER (Database Akun)
# =======================================================
class HashTableAkun:
    def __init__(self):
        self.ukuran_tabel = 100
        # Bikin list kosong sebanyak 100 slot
        self.tabel = []
        for i in range(self.ukuran_tabel):
            self.tabel.append(None)

    def ubah_nama_jadi_angka(self, nama):
        # Ini adalah Algoritma Hashing sederhana
        total_angka = 0
        for huruf in nama:
            total_angka = total_angka + ord(huruf)
        return total_angka % self.ukuran_tabel

    def simpan_akun(self, username, password):
        indeks = self.ubah_nama_jadi_angka(username)
        
        # Cek kalau slotnya kepakai, geser ke slot sebelahnya
        while self.tabel[indeks] is not None:
            if self.tabel[indeks][0] == username:
                self.tabel[indeks][1] = password # Update password
                return
            indeks = (indeks + 1) % self.ukuran_tabel
            
        # Simpan: [Username, Password, Kotak Masuk]
        kotak_masuk = StackPesan()
        self.tabel[indeks] = [username, password, kotak_masuk]

    def cari_akun(self, username):
        indeks = self.ubah_nama_jadi_angka(username)
        indeks_awal = indeks
        
        while self.tabel[indeks] is not None:
            if self.tabel[indeks][0] == username:
                return self.tabel[indeks] # Ketemu! Kembalikan datanya
            
            indeks = (indeks + 1) % self.ukuran_tabel
            if indeks == indeks_awal:
                break
        return None # Kalau tidak ketemu

class SistemUtama:
    def __init__(self):
        self.database = HashTableAkun()
        self.nama_file = "data_pengguna.txt"
        self.baca_dari_file()

    def baca_dari_file(self):
        if os.path.exists(self.nama_file) == False:
            return # Kalau file belum ada, biarkan saja
            
        file = open(self.nama_file, 'r')
        for baris in file:
            data_bersih = baris.strip()
            username, password = data_bersih.split(',')
            self.database.simpan_akun(username, password)
        file.close()

    def daftar_baru(self, username, password):
        cek_user = self.database.cari_akun(username)
        if cek_user is not None:
            return False # Gagal, nama sudah dipakai
            
        self.database.simpan_akun(username, password)
        
        file = open(self.nama_file, 'a')
        file.write(username + "," + password + "\n")
        file.close()
        return True

# =======================================================
# 3. LINKED LISTS (Buku Riwayat & Server Berputar)
# =======================================================
class NodeRiwayat:
    def __init__(self, kejadian):
        self.kejadian = kejadian
        self.sebelumnya = None
        self.selanjutnya = None

class NavigasiRiwayatAdmin: # Double Linked List
    def __init__(self):
        self.kepala = None
        self.ekor = None
        self.posisi_sekarang = None

    def catat_kejadian(self, kejadian):
        node_baru = NodeRiwayat(kejadian)
        
        if self.kepala is None:
            self.kepala = node_baru
            self.ekor = node_baru
            self.posisi_sekarang = node_baru
        else:
            self.ekor.selanjutnya = node_baru
            node_baru.sebelumnya = self.ekor
            self.ekor = node_baru
            self.posisi_sekarang = node_baru

class NodeServer:
    def __init__(self, nama_server):
        self.nama_server = nama_server
        self.selanjutnya = None

class LoadBalancerServer: # Circular Linked List
    def __init__(self):
        self.kepala = None
        self.ekor = None
        self.posisi_sekarang = None

    def tambah_server_baru(self, nama_server):
        node_baru = NodeServer(nama_server)
        
        if self.kepala is None:
            self.kepala = node_baru
            self.ekor = node_baru
            self.posisi_sekarang = node_baru
            node_baru.selanjutnya = self.kepala # Muter balik
        else:
            self.ekor.selanjutnya = node_baru
            self.ekor = node_baru
            self.ekor.selanjutnya = self.kepala # Ekor selalu nunjuk kepala

    def ambil_giliran_server(self):
        if self.kepala is None:
            return None
            
        server_terpilih = self.posisi_sekarang.nama_server
        # Geser giliran untuk pesan berikutnya
        self.posisi_sekarang = self.posisi_sekarang.selanjutnya 
        return server_terpilih

# =======================================================
# 4. GRAPH & TREE (Peta & Silsilah Keamanan)
# =======================================================
class PetaJaringan:
    def __init__(self):
        self.titik_rute = {}
        
    def sambungkan_kabel(self, lokasi_a, lokasi_b, jarak_ping):
        # Bikin lokasi baru kalau belum ada
        if lokasi_a not in self.titik_rute:
            self.titik_rute[lokasi_a] = []
        if lokasi_b not in self.titik_rute:
            self.titik_rute[lokasi_b] = []
            
        # Hubungkan timbal balik
        self.titik_rute[lokasi_a].append([lokasi_b, jarak_ping])
        self.titik_rute[lokasi_b].append([lokasi_a, jarak_ping])

class NodeSilsilah:
    def __init__(self, nama_data):
        self.nama_data = nama_data
        self.cabang_kiri = None
        self.cabang_kanan = None

def buka_folder_rekursif(node_sekarang, jarak_spasi):
    # Fungsi Rekursif (Memanggil diri sendiri)
    if node_sekarang is not None:
        buka_folder_rekursif(node_sekarang.cabang_kiri, jarak_spasi + 1)
        
        spasi = "   " * jarak_spasi
        print(spasi + "-> " + node_sekarang.nama_data)
        
        buka_folder_rekursif(node_sekarang.cabang_kanan, jarak_spasi + 1)

# =======================================================
# 5. KRIPTOGRAFI ALJABAR LINEAR (Matriks 2x2)
# =======================================================
class MesinEnkripsi:
    def __init__(self):
        # Kunci Matriks: Baris 1 [2, 1], Baris 2 [1, 1]
        self.kunci_matriks = [
            [2, 1], 
            [1, 1]
        ]
        # Kunci Pembuka (Invers Matriks)
        self.kunci_invers = [
            [1, -1], 
            [-1, 2]
        ]

    def hitung_perkalian_matriks(self, matriks, angka_1, angka_2):
        # Rumus aljabar linear manual yang sangat jelas
        hasil_atas = (matriks[0][0] * angka_1) + (matriks[0][1] * angka_2)
        hasil_bawah = (matriks[1][0] * angka_1) + (matriks[1][1] * angka_2)
        return [hasil_atas, hasil_bawah]

    def acak_pesan(self, teks_asli):
        # Tambah spasi di akhir kalau jumlah hurufnya ganjil
        if len(teks_asli) % 2 != 0: 
            teks_asli = teks_asli + " "
            
        hasil_acak = []
        
        # Proses per 2 huruf
        for i in range(0, len(teks_asli), 2):
            huruf_pertama = ord(teks_asli[i])
            huruf_kedua = ord(teks_asli[i+1])
            
            hasil_kali = self.hitung_perkalian_matriks(self.kunci_matriks, huruf_pertama, huruf_kedua)
            
            hasil_acak.append(hasil_kali[0])
            hasil_acak.append(hasil_kali[1])
            
        return hasil_acak
        
    def kembalikan_pesan(self, kumpulan_angka):
        teks_kembali = ""
        
        # Proses per 2 angka
        for i in range(0, len(kumpulan_angka), 2):
            angka_pertama = kumpulan_angka[i]
            angka_kedua = kumpulan_angka[i+1]
            
            hasil_kali = self.hitung_perkalian_matriks(self.kunci_invers, angka_pertama, angka_kedua)
            
            teks_kembali = teks_kembali + chr(hasil_kali[0])
            teks_kembali = teks_kembali + chr(hasil_kali[1])
            
        return teks_kembali.strip()

# =======================================================
# MENU APLIKASI UTAMA
# =======================================================
def main():
    sistem = SistemUtama()
    log_buku = NavigasiRiwayatAdmin()
    antrean = QueueJaringan()
    mesin_sandi = MesinEnkripsi()
    
    # 1. Siapkan Server Keliling
    pengatur_server = LoadBalancerServer()
    pengatur_server.tambah_server_baru("Proxy-Jakarta")
    pengatur_server.tambah_server_baru("Proxy-Singapore")
    pengatur_server.tambah_server_baru("Proxy-Tokyo")
    
    # 2. Siapkan Peta Google Maps (Graph)
    peta = PetaJaringan()
    peta.sambungkan_kabel("Pusat", "Proxy-Jakarta", 10)
    peta.sambungkan_kabel("Proxy-Jakarta", "Proxy-Singapore", 15)

    # 3. Siapkan Silsilah Kemanan (Tree)
    akar_tree = NodeSilsilah("Sistem Keamanan Utama")
    akar_tree.cabang_kiri = NodeSilsilah("Data Public Key")
    akar_tree.cabang_kanan = NodeSilsilah("Data Private Key")

    # ================= LOOOPING MENU =================
    while True:
        print("\n===========================================")
        print(" PROGRAM CHAT RAHASIA (KELOMPOK 2) ")
        print("===========================================")
        print("1. Daftar Akun Baru")
        print("2. Masuk (Login) & Kirim Pesan")
        print("3. Cek Buku Riwayat Admin")
        print("4. Cek Peta Server & Tree Keamanan")
        print("5. Matikan Aplikasi")
        print("===========================================")
        pilihan = input("Mau pilih nomor berapa? : ")

        # --- MENU 1: DAFTAR ---
        if pilihan == '1':
            nama = input("Masukkan Username baru: ")
            kata_sandi = input("Masukkan Password baru: ")
            sukses = sistem.daftar_baru(nama, kata_sandi)
            
            if sukses == True:
                print(">> Pendaftaran berhasil!")
                log_buku.catat_kejadian("Ada user baru daftar namanya: " + nama)
            else:
                print(">> Gagal, nama itu sudah ada yang punya.")

        # --- MENU 2: LOGIN & CHAT ---
        elif pilihan == '2':
            nama = input("Username kamu: ")
            kata_sandi = input("Password kamu: ")
            
            data_user = sistem.database.cari_akun(nama)
            
            # Cek apakah akun ketemu dan passwordnya sama
            if data_user is not None and data_user[1] == kata_sandi:
                print("\n>> BERHASIL MASUK! Halo " + nama)
                log_buku.catat_kejadian(nama + " baru saja login.")
                
                # Cek Inbox (Kotak Masuk)
                kotak_masuk_saya = data_user[2]
                
                if len(kotak_masuk_saya.daftar_pesan) > 0:
                    print("\n[!] ADA PESAN BARU UNTUKMU [!]")
                    pesan_masuk = kotak_masuk_saya.ambil_pesan_terakhir()
                    print("Bentuk Asli (Angka Acak) :", pesan_masuk)
                    
                    time.sleep(1)
                    pesan_asli = mesin_sandi.kembalikan_pesan(pesan_masuk)
                    print("Setelah Dibuka Sandinya  : " + pesan_asli)
                else:
                    print("\nKotak pesanmu masih kosong.")

                # Mulai Kirim Pesan
                kirim_jawab = input("\nMau kirim pesan ke teman? (Y/N): ")
                if kirim_jawab.upper() == 'Y':
                    nama_tujuan = input("Tulis username tujuan: ")
                    data_teman = sistem.database.cari_akun(nama_tujuan)
                    
                    if data_teman is not None:
                        draf_pesan = StackPesan()
                        isi_pesan = input("Ketik pesanmu di sini: ")
                        draf_pesan.tambah_pesan(isi_pesan)
                        
                        batal = input("Pencet 'Z' kalau mau Batal/Undo, atau 'Enter' untuk kirim: ")
                        
                        if batal.upper() == 'Z':
                            pesan_batal = draf_pesan.ambil_pesan_terakhir()
                            print(">> Oke, pesan '" + pesan_batal + "' batal dikirim.")
                        else:
                            # 1. Ambil Pesan
                            pesan_jadi = draf_pesan.ambil_pesan_terakhir()
                            
                            # 2. Acak Pakai Matematika
                            pesan_sandi = mesin_sandi.acak_pesan(pesan_jadi)
                            print("\n>> PROSES 1: Mengacak pesan jadi =", pesan_sandi)
                            
                            # 3. Masuk Antrean Jaringan
                            antrean.masuk_antrean(pesan_sandi)
                            print(">> PROSES 2: Menunggu antrean jaringan...")
                            time.sleep(1)
                            
                            # 4. Dikirim Lewat Server
                            paket_jalan = antrean.keluar_antrean()
                            server_bertugas = pengatur_server.ambil_giliran_server()
                            print(">> PROSES 3: Dikirim lewat " + server_bertugas)
                            
                            # 5. Sampai di Kotak Masuk Teman
                            kotak_masuk_teman = data_teman[2]
                            kotak_masuk_teman.tambah_pesan(paket_jalan)
                            
                            log_buku.catat_kejadian(nama + " mengirim pesan ke " + nama_tujuan)
                            print("\n>> BERHASIL! Pesan sudah masuk ke inbox " + nama_tujuan)
                    else:
                        print(">> Gagal, username tujuan tidak ketemu.")
            else:
                print(">> Login Gagal! Password salah atau akun tidak ada.")

        # --- MENU 3: BUKU RIWAYAT ---
        elif pilihan == '3':
            print("\n--- BUKU CATATAN ADMIN ---")
            if log_buku.posisi_sekarang is None:
                print("Belum ada kejadian apa-apa.")
            else:
                while True:
                    print("Kejadian saat ini: " + log_buku.posisi_sekarang.kejadian)
                    tombol = input("Pencet A (Mundur), D (Maju), Q (Keluar Menu): ")
                    
                    if tombol.upper() == 'A' and log_buku.posisi_sekarang.sebelumnya is not None:
                        log_buku.posisi_sekarang = log_buku.posisi_sekarang.sebelumnya
                    elif tombol.upper() == 'D' and log_buku.posisi_sekarang.selanjutnya is not None:
                        log_buku.posisi_sekarang = log_buku.posisi_sekarang.selanjutnya
                    elif tombol.upper() == 'Q':
                        break

        # --- MENU 4: PETA JARINGAN ---
        elif pilihan == '4':
            print("\n--- DATA PETA SERVER (GRAPH) ---")
            for nama_server, daftar_koneksi in peta.titik_rute.items():
                print("Lokasi: " + nama_server)
                for tujuan in daftar_koneksi:
                    # tujuan[0] itu nama, tujuan[1] itu jarak ping
                    print("  -> Nyambung ke " + tujuan[0] + " (Jarak " + str(tujuan[1]) + "ms)")
                
            print("\n--- DATA SILSILAH KEAMANAN (TREE) ---")
            buka_folder_rekursif(akar_tree, 0)

        # --- MENU 5: KELUAR ---
        elif pilihan == '5':
            print("Mematikan program... Dadah!")
            break

if __name__ == "__main__":
    main()