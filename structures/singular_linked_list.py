class NodeKontak:
    def __init__(self, nama):
        self.nama = nama
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def tambah_kontak(self, nama):
        node_baru = NodeKontak(nama)
        if self.head is None:
            self.head = node_baru
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node_baru

    # [SORTING] Implementasi Bubble Sort manual pada Linked List
    def urutkan_abjad(self):
        if self.head is None or self.head.next is None:
            return

        ditukar = True
        while ditukar:
            ditukar = False
            current = self.head
            while current.next is not None:
                # Membandingkan string secara alfabetis
                if current.nama > current.next.nama:
                    # Tukar datanya doang
                    current.nama, current.next.nama = current.next.nama, current.nama
                    ditukar = True
                current = current.next

    def ambil_semua(self):
        hasil = []
        current = self.head
        while current is not None:
            hasil.append(current.nama)
            current = current.next
        return hasil