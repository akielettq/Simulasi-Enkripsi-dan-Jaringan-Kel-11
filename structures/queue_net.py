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