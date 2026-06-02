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