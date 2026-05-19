import os
import time

# ==========================================
# 1. STACK & QUEUE (Inbox, Draft & Antrean Jaringan)
# ==========================================
class Stack:
    def __init__(self): self.items = []
    def push(self, item): self.items.append(item)
    def pop(self): return self.items.pop() if self.items else None
    def is_empty(self): return len(self.items) == 0

class Queue:
    def __init__(self): self.items = []
    def enqueue(self, item): self.items.append(item)
    def dequeue(self): return self.items.pop(0) if self.items else None
    def is_empty(self): return len(self.items) == 0

# ==========================================
# 2. HASH TABLE & FILE HANDLER (Login Sistem & Inbox)
# ==========================================
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return sum(ord(char) for char in key) % self.size

    def insert(self, username, password):
        index = self._hash(username)
        while self.table[index] is not None:
            if self.table[index][0] == username:
                # Update password tapi biarkan inbox tetap utuh
                self.table[index][1] = password
                return
            index = (index + 1) % self.size
        # Menyimpan: [Username, Password, Kotak Masuk (Stack)]
        self.table[index] = [username, password, Stack()]

    def get(self, username):
        """Mencari user dan mengembalikan seluruh data [user, pw, inbox]"""
        index = self._hash(username)
        start_index = index
        while self.table[index] is not None:
            if self.table[index][0] == username:
                return self.table[index]
            index = (index + 1) % self.size
            if index == start_index: break
        return None

class UserSystem:
    def __init__(self):
        self.users_db = HashTable()
        self.filename = "database_user.txt"
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename): return
        with open(self.filename, 'r') as file:
            for line in file:
                user, pw = line.strip().split(',')
                self.users_db.insert(user, pw)

    def register(self, username, password):
        if self.users_db.get(username):
            return False
        self.users_db.insert(username, password)
        with open(self.filename, 'a') as file:
            file.write(f"{username},{password}\n")
        return True

    def login(self, username, password):
        user_data = self.users_db.get(username)
        if user_data and user_data[1] == password:
            return True
        return False

# ==========================================
# 3. LINKED LISTS (Log, Navigasi, Load Balance)
# ==========================================
class NodeDLL:
    def __init__(self, data):
        self.data = data
        self.prev = self.next = None

class HistoryNavigasi: 
    def __init__(self):
        self.head = self.tail = self.current = None

    def tambah_log(self, data):
        baru = NodeDLL(data)
        if not self.head:
            self.head = self.tail = self.current = baru
        else:
            self.tail.next = baru
            baru.prev = self.tail
            self.tail = self.current = baru

class NodeCLL:
    def __init__(self, nama):
        self.nama = nama
        self.next = None

class LoadBalancer: 
    def __init__(self):
        self.head = self.tail = self.current = None

    def tambah_server(self, nama):
        baru = NodeCLL(nama)
        if not self.head:
            self.head = self.tail = self.current = baru
            baru.next = self.head
        else:
            self.tail.next = baru
            self.tail = baru
            self.tail.next = self.head

    def get_server(self):
        if not self.head: return None
        terpilih = self.current.nama
        self.current = self.current.next
        return terpilih

# ==========================================
# 4. GRAPH & TREE (Topologi & Struktur Enkripsi)
# ==========================================
class JaringanGraph:
    def __init__(self): self.rute = {}
    def tambah_koneksi(self, asal, tujuan, ping):
        if asal not in self.rute: self.rute[asal] = []
        if tujuan not in self.rute: self.rute[tujuan] = []
        self.rute[asal].append((tujuan, ping))
        self.rute[tujuan].append((asal, ping))

class NodeTree:
    def __init__(self, data):
        self.data = data
        self.kiri = self.kanan = None

def telusuri_tree(node, level=0):
    if node:
        telusuri_tree(node.kiri, level + 1)
        print("   " * level + f"-> {node.data}")
        telusuri_tree(node.kanan, level + 1)

# ==========================================
# 5. KRIPTOGRAFI ALJABAR LINEAR
# ==========================================
class MatriksKripto:
    def __init__(self):
        self.K = [[2, 1], [1, 1]]
        self.K_inv = [[1, -1], [-1, 2]]

    def _kali(self, m, v):
        return [(m[0][0]*v[0]) + (m[0][1]*v[1]), (m[1][0]*v[0]) + (m[1][1]*v[1])]

    def enkripsi(self, teks):
        if len(teks) % 2 != 0: teks += " "
        cipher = []
        for i in range(0, len(teks), 2):
            v = [ord(teks[i]), ord(teks[i+1])]
            cipher.extend(self._kali(self.K, v))
        return cipher
        
    def dekripsi(self, cipher_angka):
        teks_asli = ""
        for i in range(0, len(cipher_angka), 2):
            v = [cipher_angka[i], cipher_angka[i+1]]
            hasil = self._kali(self.K_inv, v)
            teks_asli += chr(hasil[0]) + chr(hasil[1])
        return teks_asli.strip()

# ==========================================
# PROGRAM UTAMA (INTEGRASI SELURUH MODUL)
# ==========================================
def main():
    sistem = UserSystem()
    log_admin = HistoryNavigasi()
    antrean_jaringan = Queue()
    kripto = MatriksKripto()
    
    # Setup Circular LL & Graph
    balancer = LoadBalancer()
    for srv in ["Proxy-JKT", "Proxy-SGP", "Proxy-TYO"]: balancer.tambah_server(srv)
    
    peta = JaringanGraph()
    peta.tambah_koneksi("Pusat", "Proxy-JKT", 10)
    peta.tambah_koneksi("Proxy-JKT", "Proxy-SGP", 15)

    # Setup Tree
    root_enkripsi = NodeTree("Root Kunci Kripto")
    root_enkripsi.kiri = NodeTree("Kunci Publik (Node Kiri)")
    root_enkripsi.kanan = NodeTree("Kunci Privat (Node Kanan)")

    while True:
        print("\n" + "="*45)
        print(" SIMULATOR JARINGAN KRIPTOGRAFI (DENGAN INBOX)")
        print("="*45)
        print("1. Registrasi Akun")
        print("2. Login (Cek Kotak Masuk & Kirim Pesan)")
        print("3. Cek Navigasi Log (Double LL)")
        print("4. Cek Peta Server (Graph & Tree)")
        print("5. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            user = input("Username baru: ")
            pw = input("Password baru: ")
            if sistem.register(user, pw):
                print("[+] Pendaftaran berhasil!")
                log_admin.tambah_log(f"User baru mendaftar: {user}")
            else:
                print("[-] Username sudah ada.")

        elif pilihan == '2':
            user = input("Username: ")
            pw = input("Password: ")
            if sistem.login(user, pw):
                print(f"\n[Login Sukses] Selamat datang, {user}!")
                log_admin.tambah_log(f"User login: {user}")
                
                # CEK KOTAK MASUK (INBOX) PADA SAAT LOGIN
                user_data = sistem.users_db.get(user)
                inbox_user = user_data[2] # Indeks 2 adalah Stack Kotak Masuk
                
                if not inbox_user.is_empty():
                    print("\n🔔 ANDA MEMILIKI PESAN BARU!")
                    # Ambil pesan teratas dari tumpukan (Stack pop)
                    pesan_masuk = inbox_user.pop()
                    print(f"[-] Pesan Acak Diterima (Cipher): {pesan_masuk}")
                    print("[Membuka Gembok... Dekripsi Matriks]")
                    time.sleep(1)
                    pesan_asli = kripto.dekripsi(pesan_masuk)
                    print(f"[*] ISI PESAN ASLI: {pesan_asli}")
                else:
                    print("\nKotak Masuk kosong.")

                # MENU KIRIM PESAN
                kirim = input("\nKirim pesan ke pengguna lain? (Y/N): ").upper()
                if kirim == 'Y':
                    target = input("Masukkan username penerima: ")
                    data_target = sistem.users_db.get(target)
                    
                    if data_target:
                        stack_draft = Stack()
                        pesan = input("Ketik pesan rahasia: ")
                        stack_draft.push(pesan)
                        
                        if input("Ketik 'Z' untuk Batal/Undo, atau 'Enter' untuk kirim: ").upper() == 'Z':
                            print(f"[Undo] Pesan batal dikirim: {stack_draft.pop()}")
                            continue
                        
                        pesan_final = stack_draft.pop()
                        cipher = kripto.enkripsi(pesan_final)
                        print(f"\n[ENKRIPSI] Pesan diacak menjadi: {cipher}")
                        
                        antrean_jaringan.enqueue(cipher)
                        print("[ANTREAN] Paket masuk Queue jaringan...")
                        time.sleep(1)
                        
                        paket = antrean_jaringan.dequeue()
                        server_aktif = balancer.get_server()
                        print(f"[TRANSMISI] Paket dialihkan melalui {server_aktif} (Circular LL)")
                        
                        # MASUKKAN PESAN KE KOTAK MASUK PENERIMA
                        inbox_target = data_target[2]
                        inbox_target.push(paket)
                        
                        log_admin.tambah_log(f"{user} mengirim pesan rahasia ke {target}")
                        print(f"\n[BERHASIL] Pesan terkirim dan masuk ke inbox {target}!")
                    else:
                        print("[-] Username tujuan tidak ditemukan di database.")
            else:
                print("[-] Login gagal. Username/Password salah.")

        elif pilihan == '3':
            print("\n--- NAVIGASI LOG ADMIN ---")
            if not log_admin.current:
                print("Log masih kosong.")
                continue
            while True:
                print(f"Log Aktif: {log_admin.current.data}")
                nav = input("Pencet 'A' (Prev), 'D' (Next), 'Q' (Keluar): ").upper()
                if nav == 'A' and log_admin.current.prev: log_admin.current = log_admin.current.prev
                elif nav == 'D' and log_admin.current.next: log_admin.current = log_admin.current.next
                elif nav == 'Q': break

        elif pilihan == '4':
            print("\n--- TOPOLOGI GRAPH ---")
            for node, conns in peta.rute.items():
                jalur = ", ".join([f"{t}({p}ms)" for t, p in conns])
                print(f"[{node}] <--> {jalur}")
                
            print("\n--- STRUKTUR TREE REKURSIF ---")
            telusuri_tree(root_enkripsi)

        elif pilihan == '5':
            print("Mematikan sistem... Sampai jumpa!")
            break

if __name__ == "__main__":
    main()