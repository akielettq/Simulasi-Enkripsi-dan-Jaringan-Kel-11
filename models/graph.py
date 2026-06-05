class PetaJaringan:
    def __init__(self):
        # [Dictionary]
        self.titik_rute = {}
        
    def sambungkan_kabel(self, lokasi_a, lokasi_b, jarak_ping):
        if lokasi_a not in self.titik_rute:
            self.titik_rute[lokasi_a] = []
        if lokasi_b not in self.titik_rute:
            self.titik_rute[lokasi_b] = []
        
        # [Tuple]
        self.titik_rute[lokasi_a].append((lokasi_b, jarak_ping))
        self.titik_rute[lokasi_b].append((lokasi_a, jarak_ping))

    def cari_ping(self, asal, tujuan):
        if asal in self.titik_rute:
            for tetangga in self.titik_rute[asal]:
                if tetangga[0] == tujuan:
                    return tetangga[1]
        return 10 # Default ping kalau tidak ketemu