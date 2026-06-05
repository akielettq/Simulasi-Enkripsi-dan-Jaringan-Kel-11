import time
import random
from utils.layar import bersihkan_layar
from structures.stack import StackPesan
from structures.queue_net import QueueJaringan
from structures.singular_linked_list import SinglyLinkedList
from structures.doubly_linked_list import DoublyLinkedList
from structures.circular_linked_list import CircularLinkedList
from models.graph import PetaJaringan
from models.tree import BSTSensor
from sistem.sistem_utama import SistemUtama
from sistem.kriptografi import MesinEnkripsi

def jalankan_aplikasi():
    # ========================================================
    # [INISIALISASI SISTEM] 
    # Memanggil semua cetakan (Class) dari folder lain 
    # ========================================================
    
    # Mengelola Hash Table & File txt
    sistem = SistemUtama()                 
    
    # Mengelola log riwayat admin
    log_buku = DoublyLinkedList()          
    
    # Mengelola Traffic pesan
    antrean = QueueJaringan()              
    
    # Mengelola perhitungan aljabar linear
    mesin_sandi = MesinEnkripsi()          
    
    # [CIRCULAR LINKED LIST] Mengatur server dengan konsep perputaran
    pengatur_server = CircularLinkedList()
    pengatur_server.add_server("Proxy-Jakarta")
    pengatur_server.add_server("Proxy-Singapore")
    pengatur_server.add_server("Proxy-Tokyo")
    
    # [GRAPH] Membuat topologi rute server (Pusat ke Cabang)
    peta = PetaJaringan()
    
    # Jalur dengan Ping 12ms
    peta.sambungkan_kabel("Pusat", "Proxy-Jakarta", 12)   
    # Jalur dengan Ping 25ms
    peta.sambungkan_kabel("Pusat", "Proxy-Singapore", 25) 
    # Jalur dengan Ping 45ms
    peta.sambungkan_kabel("Pusat", "Proxy-Tokyo", 45)     

# [TREE] Inisialisasi BST untuk Sensor Kata Kasar
    pohon_sensor = BSTSensor()
    pohon_sensor.tambah_kata_kotor("anjing")
    pohon_sensor.tambah_kata_kotor("babi")
    pohon_sensor.tambah_kata_kotor("bodoh")
    pohon_sensor.tambah_kata_kotor("kampang")

    # ========================================================
    # [MAIN LOOP] Antarmuka CLI Interaktif
    # ========================================================
    while True:
        # --- KODE WARNA ANSI (Memberikan efek visual ala Hacker) ---
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        RESET = '\033[0m'
        BOLD = '\033[1m'

        bersihkan_layar()
        
        # --- ASCII ART BANNER ---
        print(CYAN + BOLD + r"""
   _____                            ______          __ 
  / ___/___  _______  __________   / ____/ /_  ____/ /_
  \__ \/ _ \/ ___/ / / / ___/ _ \ / /   / __ \/ __  / __/
 ___/ /  __/ /__/ /_/ / /  /  __// /___/ / / / /_/ / /_  
/____/\___/\___/\__,_/_/   \___/ \____/_/ /_/\__,_/\__/  
        """ + RESET)
        
        print(YELLOW + "=================================================" + RESET)
        print(GREEN + "      SISTEM JARINGAN RAHASIA - KELOMPOK 11      " + RESET)
        print(YELLOW + "=================================================" + RESET)
        print(CYAN + "[1]" + RESET + " Daftar Akun Baru")
        print(CYAN + "[2]" + RESET + " Masuk (Login) & Kirim Pesan")
        print(CYAN + "[3]" + RESET + " Cek Buku Riwayat Admin")
        print(CYAN + "[4]" + RESET + " Cek Peta Server & Daftar Sensor")
        print(RED   + "[5]" + RESET + " Matikan Aplikasi")
        print(YELLOW + "=================================================" + RESET)
        
        pilihan = input(BOLD + "Masukkan kode akses (1-5) ❯ " + RESET)

        # --- MENU 1: DAFTAR AKUN ---
        if pilihan == '1':
            # Tambahkan .strip() di ujungnya biar membersihkan spasi
            nama = input("Masukkan Username baru: ").strip()
            kata_sandi = input("Masukkan Password baru: ").strip()
            
            # [QC] Validasi input kosong dan karakter ilegal
            if nama.strip() == "" or kata_sandi.strip() == "":
                print(">> Gagal: Username dan Password tidak boleh kosong!")
                input("\n[Tekan Enter untuk kembali...]")
                continue
            
            # [QC] Validasi panjang karakter
            if len(nama) > 20:
                print(">> Gagal: Username maksimal 20 karakter!")
                input("\n[Tekan Enter untuk kembali...]")
                continue
                
            if "," in nama or "," in kata_sandi:
                print(">> Gagal: Username dan Password tidak boleh memakai simbol koma (,).")
                input("\n[Tekan Enter untuk kembali...]")
                continue

            # [HASH TABLE] O(1) Insertion: Menyimpan data langsung ke indeks hash
            sukses = sistem.daftar_baru(nama, kata_sandi)
            
            if sukses == True:
                print(">> Pendaftaran berhasil!")
                # [DOUBLY LL] Mencatat kejadian ke dalam node log
                log_buku.append_log("Ada user baru daftar namanya: " + nama)
            else:
                print(">> Gagal, nama itu sudah ada yang punya.")
                
            input("\n[Tekan Enter untuk kembali ke menu utama...]")

        # --- MENU 2: LOGIN & CHAT ---
        elif pilihan == '2':
            # [QC] Mencegah login jika database masih kosong
            semua_user = sistem.database.ambil_semua_username()
            if len(semua_user) == 0:
                bersihkan_layar()
                print(">> Gagal: Belum ada satupun akun yang terdaftar di sistem!")
                print(">> Silakan daftar akun baru (Pilih Menu 1) terlebih dahulu.")
                input("\n[Tekan Enter untuk kembali ke menu utama...]")
                continue 

            nama = input("Username kamu: ").strip()
            kata_sandi = input("Password kamu: ").strip()
            
            # [HASH TABLE] O(1) Search: Mengecek kecocokan username
            data_user = sistem.database.cari_akun(nama)
            
            if data_user is not None and data_user[1] == kata_sandi:
                bersihkan_layar() 
                print(">> BERHASIL MASUK! Halo " + nama)
                log_buku.append_log(nama + " baru saja login.")
                
                kotak_masuk_saya = data_user[2]
                
                # [STACK] Proses membaca Inbox dengan prinsip LIFO (Last In, First Out)
                if len(kotak_masuk_saya.daftar_pesan) > 0:
                    jumlah_pesan = len(kotak_masuk_saya.daftar_pesan)
                    print("\n[!] KAMU PUNYA " + str(jumlah_pesan) + " PESAN BARU [!]")
                    print("Membuka pesan dari yang paling baru (Konsep LIFO)...")
                    
                    urutan = 1
                    while len(kotak_masuk_saya.daftar_pesan) > 0:
                        # Mengambil (Pop) paket dari tumpukan teratas
                        paket_masuk = kotak_masuk_saya.ambil_pesan_terakhir()
                        nama_pengirim = paket_masuk[0]
                        pesan_masuk = paket_masuk[1]
                        
                        # [KRIPTOGRAFI] Dekripsi pesan masuk menggunakan Invers Matriks 2x2
                        pesan_asli = mesin_sandi.kembalikan_pesan(pesan_masuk)
                        
                        print("\n--- Pesan ke-" + str(urutan) + " (Dari: 👤 " + nama_pengirim + ") ---")
                        print("Sandi Asli :", pesan_masuk)
                        time.sleep(0.5)
                        print("Isi Pesan  : " + pesan_asli)
                        urutan += 1
                    print("------------------------------")
                else:
                    print("\nKotak pesanmu masih kosong.")

                # Proses Pengiriman Pesan
                while True:
                    print("\n" + "="*40)
                    kirim_jawab = input("Mau kirim pesan ke teman? (Y/N): ")
                    if kirim_jawab.upper() != 'Y':
                        print(">> Selesai ngobrol. Mengakhiri sesi login...")
                        break 
                    
                    bersihkan_layar()
                    
                    print("\n--- DAFTAR KONTAK TERSEDIA (A-Z) ---")
                    daftar_kontak = SinglyLinkedList()
                    ada_teman = False
                    
                    # 1. Masukkan semua user (kecuali diri sendiri) ke Singly Linked List
                    for teman in semua_user:
                        if teman != nama: 
                            daftar_kontak.tambah_kontak(teman)
                            ada_teman = True
                            
                    # 2. Panggil algoritma Sorting (Bubble Sort manual)
                    daftar_kontak.urutkan_abjad()
                    
                    # 3. Tampilkan hasil yang sudah terurut
                    kontak_terurut = daftar_kontak.ambil_semua()
                    for teman_rapi in kontak_terurut:
                        print("👤 " + teman_rapi)
                            
                    if not ada_teman:
                        print("Belum ada user lain yang mendaftar.")
                        print(">> Tidak ada target. Sesi chat dibatalkan...")
                        break 
                    else:
                        print("------------------------------")
                        nama_tujuan = input("Tulis username tujuan: ")
                        
                        # [QC] Mencegah mengirim pesan ke diri sendiri
                        if nama_tujuan == nama:
                            print(">> Tidak bisa mengirim pesan ke diri sendiri!")
                            continue
                            
                        data_teman = sistem.database.cari_akun(nama_tujuan)
                        
                        if data_teman is not None:
                            draf_pesan = StackPesan()
                            isi_pesan = input("Ketik pesanmu di sini: ")
                            
                            # [QC] Mencegah pesan kosong (Spasi doang)
                            if isi_pesan.strip() == "":
                                print(">> Gagal: Pesan tidak boleh kosong!")
                                continue
                                
                            draf_pesan.tambah_pesan(isi_pesan)
                            
                            batal = input("Pencet 'Z' kalau mau Batal/Undo, atau 'Enter' untuk kirim: ")
                            
                            # [STACK] Implementasi fitur Undo (Membatalkan draft)
                            if batal.upper() == 'Z':
                                # POP Stack
                                pesan_batal = draf_pesan.ambil_pesan_terakhir() 
                                print(">> Oke, pesan '" + pesan_batal + "' batal dikirim.")
                            else:
                                pesan_jadi = draf_pesan.ambil_pesan_terakhir()
                                
                                # [KRIPTOGRAFI] Enkripsi Plaintext menjadi array Ciphertext
                                pesan_sandi = mesin_sandi.acak_pesan(pesan_jadi)
                                
                            # [TREE] Validasi kata kasar via Binary Search Tree
                                if pohon_sensor.cek_kata_kotor(isi_pesan):
                                    print("\n>> PERINGATAN SISTEM: Pesan Anda mengandung kata terlarang!")
                                    print(">> Pesan diblokir dan gagal dikirim.")
                                    continue
                                
                                print("\n>> PROSES 1: Mengacak pesan jadi =", pesan_sandi)
                                
                                paket_data = [nama, pesan_sandi] 
                                antrean.masuk_antrean(paket_data)
                                
                                server_bertugas = pengatur_server.get_next_server()
                                
                                # [GRAPH] Menghitung delay berdasarkan jarak server
                                ping = peta.cari_ping("Pusat", server_bertugas)
                                print(f">> PROSES 2: Antrean masuk server {server_bertugas} (Ping: {ping}ms)")
                                
                                # Simulasi delay jaringan (ping dibagi 10 agar jadi detik)
                                time.sleep(ping / 10.0) 
                                
                                paket_jalan = antrean.keluar_antrean()
                                print(">> PROSES 3: Pesan berhasil melewati jaringan.")
                                
                                kotak_masuk_teman = data_teman[2]
                                kotak_masuk_teman.tambah_pesan(paket_jalan)
                                
                                log_buku.append_log(nama + " mengirim pesan ke " + nama_tujuan)
                                print("\n>> BERHASIL! Pesan sudah masuk ke inbox " + nama_tujuan)
                        else:
                            print(">> Gagal, username tujuan tidak ketemu.")
            else:
                print(">> Login Gagal! Password salah atau akun tidak ada.")
                
            input("\n[Tekan Enter untuk kembali ke menu utama...]")

        # --- MENU 3: BUKU RIWAYAT ---
        elif pilihan == '3':
            bersihkan_layar()
            print("\n--- BUKU CATATAN ADMIN ---")
            if log_buku.current is None:
                print("Belum ada kejadian apa-apa.")
                input("\n[Tekan Enter untuk kembali...]")
            else:
                while True:
                    bersihkan_layar()
                    print("--- BUKU CATATAN ADMIN ---")
                    print("Kejadian saat ini: " + log_buku.current.event)
                    print("-" * 30)
                    
                    # [DOUBLY LL] Navigasi traversal dua arah (Next & Prev pointer)
                    tombol = input("Pencet A (Mundur), D (Maju), Q (Keluar Menu): ")
                    if tombol.upper() == 'A' and log_buku.current.prev is not None:
                        log_buku.current = log_buku.current.prev
                    elif tombol.upper() == 'D' and log_buku.current.next is not None:
                        log_buku.current = log_buku.current.next
                    elif tombol.upper() == 'Q':
                        break

        # --- MENU 4: PETA JARINGAN & TREE SENSOR ---
        elif pilihan == '4':
            bersihkan_layar()
            print("\n--- DATA PETA SERVER (GRAPH) ---")
            
            # [GRAPH] Membaca relasi antarkota/server di dalam Adjacency List
            for nama_server, daftar_koneksi in peta.titik_rute.items():
                print("Lokasi: " + nama_server)
                for tujuan in daftar_koneksi:
                    print("  -> Nyambung ke " + tujuan[0] + " (Jarak " + str(tujuan[1]) + "ms)")
                
            print("\n--- DATA SILSILAH SENSOR KATA KASAR (BST) ---")
            # [TREE] Menampilkan isi Binary Search Tree menggunakan In-Order Traversal
            if pohon_sensor.root is None:
                print("Daftar sensor kata kasar masih kosong.")
            else:
                pohon_sensor.cetak_inorder(pohon_sensor.root, 0)
            
            input("\n[Tekan Enter untuk kembali ke menu utama...]")

        # --- MENU 5: KELUAR ---
        elif pilihan == '5':
            bersihkan_layar()
            print("Mematikan program... Dadah!")
            break
            
        # [QC] Menangani jika input user di luar angka 1-5
        else:
            print(">> Pilihan tidak valid! Silakan masukkan angka 1 sampai 5.")
            time.sleep(1.5)