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