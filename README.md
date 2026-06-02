# 🔐 Sistem Chat Rahasia (Secure Chat Simulator)

Proyek ini adalah simulasi aplikasi pengiriman pesan rahasia berbasis *Command Line Interface* (CLI). Dibangun sebagai pemenuhan tugas mata kuliah **Struktur Data dan Algoritma**, program ini mengimplementasikan 7 jenis struktur data fundamental dan algoritma kriptografi berbasis Aljabar Linear (Matriks 2x2) dalam satu arsitektur perangkat lunak yang utuh (Modular).

---

## 🚀 Fitur Utama & Implementasi Struktur Data

Sistem ini dirancang tidak sekadar untuk berfungsi, tetapi juga untuk mendemonstrasikan penggunaan struktur data yang optimal di setiap fiturnya:

1. **Sistem Akun & Autentikasi (`Hash Table`)**
   - Menggunakan *Hash Table* dengan metode *Linear Probing* untuk menyimpan dan mencari data *username* dan *password* dengan efisiensi waktu **O(1)**.
2. **Manajemen Pesan & Fitur Undo (`Stack`)**
   - Kotak masuk (Inbox) dan penulisan draf pesan menggunakan konsep **LIFO** (*Last In, First Out*).
   - Memungkinkan pengguna untuk membatalkan (*Undo*) penulisan pesan sebelum dikirim.
3. **Antrean Jaringan Pengiriman (`Queue`)**
   - Pesan yang sudah dienkripsi akan dimasukkan ke dalam antrean jaringan dengan konsep **FIFO** (*First In, First Out*).
4. **Buku Riwayat Aktivitas Admin (`Doubly Linked List`)**
   - Semua aktivitas (pendaftaran, login, pengiriman pesan) dicatat dalam *node*. Admin dapat menavigasi riwayat ini maju (*Next*) dan mundur (*Prev*) secara dinamis.
5. **Load Balancer Server (`Circular Linked List`)**
   - Pemilihan rute server proksi untuk pengiriman pesan diatur menggunakan algoritma *Round-Robin* yang berputar tiada henti.
6. **Topologi Jaringan Server (`Graph`)**
   - Pemetaan rute antarkota dan *server* menggunakan *Adjacency List* untuk mensimulasikan jarak *Ping* (ms) antar-node.
7. **Hierarki Keamanan Kunci (`Binary Tree`)**
   - Visualisasi silsilah kunci keamanan yang dapat ditelusuri menggunakan algoritma pencarian *In-Order Traversal*.

---

## 🧮 Mesin Kriptografi

Keamanan pesan dijamin menggunakan **Kriptografi Aljabar Linear**. 
Setiap karakter dari pesan asli diubah ke dalam nilai ASCII, kemudian dikalikan secara matriks (2x2) dengan *Public Key* sebelum masuk ke antrean jaringan. Di sisi penerima, algoritma inversi matriks digunakan untuk mengembalikan pesan sandi (*Ciphertext*) menjadi teks asli (*Plaintext*).

---