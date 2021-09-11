class adsorbate_atom:
    def __init__(self,index,adsorbate_atom):
        self.index = index
        self.adsorbate_atom = adsorbate_atom
        self.adsorbate_neighbours = []
        self.system_indices = []
        self.looked_at = False
    def get_symbol(self):
        return self.adsorbate_atom.symbol
    def get_position(self):
        return self.adsorbate_atom.position
    def connect(self,other_adsorbate_atom):
        self.adsorbate_neighbours.append(other_adsorbate_atom)
        other_adsorbate_atom.adsorbate_neighbours.append(self)
    def add_system_neighbour(self,abs_index):
        self.adsorbate_neighbours.append(abs_index)
    def seen(self):
        self.looked_at = True