import os
import time

# =======================================================
# SIMULASI KRIPTOGRAFI DAN JARINGAN AMAN - KELOMPOK 11
# =======================================================



# =======================================================
# 1. STACK & QUEUE
# Penjelasan: 
# - Stack (LIFO) digunakan sebagai Kotak Masuk/Draf pesan agar pesan terbaru ada di atas.
# - Queue (FIFO) digunakan untuk menyimulasikan antrean paket di jaringan internet.
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
            return self.antrean.pop(0)


# =======================================================
# 2. HASH TABLE & FILE HANDLER (Database Akun)
# Penjelasan:
# - Hash Table dengan Linear Probing untuk pencarian user secara instan O(1).
# - File Handler menyimpan data kredensial secara permanen ke dalam file .txt.
# =======================================================
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

class SistemUtama:
    def __init__(self):
        self.database = HashTableAkun()
        self.nama_file = "data_pengguna.txt"
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


# =======================================================
# 3. LINKED LISTS (Buku Riwayat & Server Berputar)
# Penjelasan:
# - Doubly Linked List: Untuk log aktivitas admin. Punya pointer 'prev' dan 'next' untuk maju-mundur.
# - Circular Linked List: Untuk Load Balancer. Pointer 'next' di Node terakhir kembali ke 'head'.
# =======================================================
class LogNode:
    def __init__(self, event):
        self.event = event
        self.prev = None
        self.next = None

class DoublyLinkedList: 
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def append_log(self, event):
        new_node = LogNode(event)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.current = new_node

class ServerNode:
    def __init__(self, server_name):
        self.server_name = server_name
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_server(self, server_name):
        new_node = ServerNode(server_name)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
            new_node.next = self.head # Circular: pointer kembali ke awal
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head # Circular: Ekor selalu menunjuk Kepala

    def get_next_server(self):
        if self.head is None:
            return None
            
        selected_server = self.current.server_name
        self.current = self.current.next # Geser ke server berikutnya
        return selected_server


# =======================================================
# 4. GRAPH & TREE (Peta & Silsilah Keamanan)
# Penjelasan:
# - Graph (Adjacency List): Menyimpan topologi server & bobot jarak (ping).
# - Binary Tree: Struktur hierarki dengan node 'left' dan 'right', ditelusuri pakai In-Order DFS.
# =======================================================
class PetaJaringan:
    def __init__(self):
        self.titik_rute = {}
        
    def sambungkan_kabel(self, lokasi_a, lokasi_b, jarak_ping):
        if lokasi_a not in self.titik_rute:
            self.titik_rute[lokasi_a] = []
        if lokasi_b not in self.titik_rute:
            self.titik_rute[lokasi_b] = []
            
        self.titik_rute[lokasi_a].append([lokasi_b, jarak_ping])
        self.titik_rute[lokasi_b].append([lokasi_a, jarak_ping])

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def inorder_traversal(current_node, depth):
    # DFS Traversal (Kiri -> Cetak -> Kanan)
    if current_node is not None:
        inorder_traversal(current_node.left, depth + 1)
        
        spasi = "   " * depth
        print(spasi + "-> " + current_node.data)
        
        inorder_traversal(current_node.right, depth + 1)


# =======================================================
# 5. KRIPTOGRAFI ALJABAR LINEAR (Matriks 2x2)
# Penjelasan:
# - Enkripsi pesan dengan perkalian Matriks Utama.
# - Dekripsi pesan dengan perkalian Invers Matriks. Menambahkan padding jika ganjil.
# =======================================================
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
            
            teks_kembali = teks_kembali + chr(hasil_kali[0])
            teks_kembali = teks_kembali + chr(hasil_kali[1])
            
        return teks_kembali.strip()


# =======================================================
# MENU APLIKASI UTAMA
# =======================================================
def main():
    sistem = SistemUtama()
    log_buku = DoublyLinkedList()
    antrean = QueueJaringan()
    mesin_sandi = MesinEnkripsi()
    
    # 1. Siapkan Server Keliling
    pengatur_server = CircularLinkedList()
    pengatur_server.add_server("Proxy-Jakarta")
    pengatur_server.add_server("Proxy-Singapore")
    pengatur_server.add_server("Proxy-Tokyo")
    
    # 2. Siapkan Peta Google Maps (Graph)
    peta = PetaJaringan()
    peta.sambungkan_kabel("Pusat", "Proxy-Jakarta", 10)
    peta.sambungkan_kabel("Proxy-Jakarta", "Proxy-Singapore", 15)

    # 3. Siapkan Silsilah Kemanan (Tree)
    akar_tree = TreeNode("Sistem Keamanan Utama")
    akar_tree.left = TreeNode("Data Public Key")
    akar_tree.right = TreeNode("Data Private Key")

    # ================= LOOOPING MENU =================
    while True:
        print("\n===========================================")
        print(" PROGRAM CHAT RAHASIA (KELOMPOK 11) ")
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
                log_buku.append_log("Ada user baru daftar namanya: " + nama)
            else:
                print(">> Gagal, nama itu sudah ada yang punya.")

        # --- MENU 2: LOGIN & CHAT ---
        elif pilihan == '2':
            nama = input("Username kamu: ")
            kata_sandi = input("Password kamu: ")
            
            data_user = sistem.database.cari_akun(nama)
            
            if data_user is not None and data_user[1] == kata_sandi:
                print("\n>> BERHASIL MASUK! Halo " + nama)
                log_buku.append_log(nama + " baru saja login.")
                
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
                            pesan_jadi = draf_pesan.ambil_pesan_terakhir()
                            
                            pesan_sandi = mesin_sandi.acak_pesan(pesan_jadi)
                            print("\n>> PROSES 1: Mengacak pesan jadi =", pesan_sandi)
                            
                            antrean.masuk_antrean(pesan_sandi)
                            print(">> PROSES 2: Menunggu antrean jaringan...")
                            time.sleep(1)
                            
                            paket_jalan = antrean.keluar_antrean()
                            server_bertugas = pengatur_server.get_next_server()
                            print(">> PROSES 3: Dikirim lewat " + server_bertugas)
                            
                            kotak_masuk_teman = data_teman[2]
                            kotak_masuk_teman.tambah_pesan(paket_jalan)
                            
                            log_buku.append_log(nama + " mengirim pesan ke " + nama_tujuan)
                            print("\n>> BERHASIL! Pesan sudah masuk ke inbox " + nama_tujuan)
                    else:
                        print(">> Gagal, username tujuan tidak ketemu.")
            else:
                print(">> Login Gagal! Password salah atau akun tidak ada.")

        # --- MENU 3: BUKU RIWAYAT ---
        elif pilihan == '3':
            print("\n--- BUKU CATATAN ADMIN ---")
            if log_buku.current is None:
                print("Belum ada kejadian apa-apa.")
            else:
                while True:
                    print("Kejadian saat ini: " + log_buku.current.event)
                    tombol = input("Pencet A (Mundur), D (Maju), Q (Keluar Menu): ")
                    
                    if tombol.upper() == 'A' and log_buku.current.prev is not None:
                        log_buku.current = log_buku.current.prev
                    elif tombol.upper() == 'D' and log_buku.current.next is not None:
                        log_buku.current = log_buku.current.next
                    elif tombol.upper() == 'Q':
                        break

        # --- MENU 4: PETA JARINGAN ---
        elif pilihan == '4':
            print("\n--- DATA PETA SERVER (GRAPH) ---")
            for nama_server, daftar_koneksi in peta.titik_rute.items():
                print("Lokasi: " + nama_server)
                for tujuan in daftar_koneksi:
                    print("  -> Nyambung ke " + tujuan[0] + " (Jarak " + str(tujuan[1]) + "ms)")
                
            print("\n--- DATA SILSILAH KEAMANAN (TREE) ---")
            inorder_traversal(akar_tree, 0)

        # --- MENU 5: KELUAR ---
        elif pilihan == '5':
            print("Mematikan program... Dadah!")
            break

if __name__ == "__main__":
    main()