class NodeKata:
    def __init__(self, kata):
        self.kata = kata
        self.left = None
        self.right = None

class BSTSensor:
    def __init__(self):
        self.root = None
        
    def tambah_kata_kotor(self, kata):
        if self.root is None:
            self.root = NodeKata(kata)
        else:
            self._insert(self.root, kata)
            
    def _insert(self, node, kata):
        if kata < node.kata:
            if node.left is None:
                node.left = NodeKata(kata)
            else:
                self._insert(node.left, kata)
        elif kata > node.kata:
            if node.right is None:
                node.right = NodeKata(kata)
            else:
                self._insert(node.right, kata)
                
    def cek_kata_kotor(self, pesan):
        # Memecah kalimat menjadi kata-kata, lalu cek satu-satu ke dalam Tree
        kata_kata = pesan.lower().split()
        for kata in kata_kata:
            if self._search(self.root, kata):
                return True # Ditemukan kata kotor
        return False
        
    def _search(self, node, kata):
        if node is None:
            return False
        if node.kata == kata:
            return True
        if kata < node.kata:
            return self._search(node.left, kata)
        return self._search(node.right, kata)
        
    def cetak_inorder(self, node, depth=0):
        if node is not None:
            self.cetak_inorder(node.left, depth + 1)
            print("   " * depth + f"-> Kata disensor: '{node.kata}'")
            self.cetak_inorder(node.right, depth + 1)