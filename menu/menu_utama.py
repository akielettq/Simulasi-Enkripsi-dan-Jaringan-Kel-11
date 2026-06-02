import time
from utils.layar import bersihkan_layar
from structures.stack import StackPesan
from structures.queue_net import QueueJaringan
from structures.doubly_linked_list import DoublyLinkedList
from structures.circular_linked_list import CircularLinkedList
from models.graph import PetaJaringan
from models.tree import TreeNode, inorder_traversal
from sistem.sistem_utama import SistemUtama
from sistem.kriptografi import MesinEnkripsi

def jalankan_aplikasi():
    # ========================================================
    # [INISIALISASI SISTEM] 
    # Memanggil semua cetakan (Class) dari folder lain 
    # ========================================================
    
    sistem = SistemUtama()                 # Mengelola Hash Table & File txt
    log_buku = DoublyLinkedList()          # Mengelola log riwayat admin
    antrean = QueueJaringan()              # Mengelola Traffic pesan
    mesin_sandi = MesinEnkripsi()          # Mengelola perhitungan aljabar linear
    
    # [CIRCULAR LINKED LIST] Mengatur server dengan konsep perputaran
    pengatur_server = CircularLinkedList()
    pengatur_server.add_server("Proxy-Jakarta")
    pengatur_server.add_server("Proxy-Singapore")
    pengatur_server.add_server("Proxy-Tokyo")
    
    # [GRAPH] Membuat topologi rute server menggunakan Adjacency List
    peta = PetaJaringan()
    peta.sambungkan_kabel("Pusat", "Proxy-Jakarta", 10)
    peta.sambungkan_kabel("Proxy-Jakarta", "Proxy-Singapore", 15)

    # [TREE] Membuat silsilah keamanan (Binary Tree)
    akar_tree = TreeNode("Sistem Keamanan Utama")
    akar_tree.left = TreeNode("Data Public Key")
    akar_tree.right = TreeNode("Data Private Key")

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
        print(CYAN + "[4]" + RESET + " Cek Peta Server & Tree Keamanan")
        print(RED   + "[5]" + RESET + " Matikan Aplikasi")
        print(YELLOW + "=================================================" + RESET)
        
        pilihan = input(BOLD + "Masukkan kode akses (1-5) ❯ " + RESET)

        # --- MENU 1: DAFTAR AKUN ---
        if pilihan == '1':
            nama = input("Masukkan Username baru: ")
            kata_sandi = input("Masukkan Password baru: ")
            
            # [QC] Validasi input kosong dan karakter ilegal
            if nama.strip() == "" or kata_sandi.strip() == "":
                print(">> Gagal: Username dan Password tidak boleh kosong!")
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

            nama = input("Username kamu: ")
            kata_sandi = input("Password kamu: ")
            
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
                    
                    print("\n--- DAFTAR KONTAK TERSEDIA ---")
                    ada_teman = False
                    for teman in semua_user:
                        if teman != nama: 
                            print("👤 " + teman)
                            ada_teman = True
                            
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
                                pesan_batal = draf_pesan.ambil_pesan_terakhir() # POP Stack
                                print(">> Oke, pesan '" + pesan_batal + "' batal dikirim.")
                            else:
                                pesan_jadi = draf_pesan.ambil_pesan_terakhir()
                                
                                # [KRIPTOGRAFI] Enkripsi Plaintext menjadi array Ciphertext
                                pesan_sandi = mesin_sandi.acak_pesan(pesan_jadi)
                                print("\n>> PROSES 1: Mengacak pesan jadi =", pesan_sandi)
                                
                                # [QUEUE] Memasukkan paket ke antrean jaringan (FIFO)
                                paket_data = [nama, pesan_sandi] 
                                antrean.masuk_antrean(paket_data)
                                print(">> PROSES 2: Menunggu antrean jaringan...")
                                time.sleep(1)
                                
                                # Mengeluarkan paket yang pertama kali antre
                                paket_jalan = antrean.keluar_antrean()
                                
                                # [CIRCULAR LL] Menentukan server pengirim menggunakan Round-Robin
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

        # --- MENU 4: PETA JARINGAN & TREE KEAMANAN ---
        elif pilihan == '4':
            bersihkan_layar()
            print("\n--- DATA PETA SERVER (GRAPH) ---")
            # [GRAPH] Membaca relasi antarkota/server di dalam Adjacency List
            for nama_server, daftar_koneksi in peta.titik_rute.items():
                print("Lokasi: " + nama_server)
                for tujuan in daftar_koneksi:
                    print("  -> Nyambung ke " + tujuan[0] + " (Jarak " + str(tujuan[1]) + "ms)")
                
            print("\n--- DATA SILSILAH KEAMANAN (TREE) ---")
            # [TREE] Membaca node Tree dengan urutan In-Order Traversal (Kiri-Akar-Kanan)
            inorder_traversal(akar_tree, 0)
            
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