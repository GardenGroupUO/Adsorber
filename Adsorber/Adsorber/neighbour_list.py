
def get_distance(atom1,atom2):
	xx_dist = atom1.x - atom2.x
	yy_dist = atom1.y - atom2.y
	zz_dist = atom1.z - atom2.z
	distance = (xx_dist**2.0 + yy_dist**2.0 + zz_dist**2.0)**0.5
	return distance

def get_neighbour_list_for_surface_atoms(cluster,surface_atoms,cutoff_dictionary):
	surface_atom_neighbour_list = {}
	for index1 in range(len(surface_atoms)):
		surface_atom_index_1 = surface_atoms[index1]
		atom1 = cluster[surface_atom_index_1]
		for index2 in range(index1+1,len(surface_atoms)):
			surface_atom_index_2 = surface_atoms[index2]
			atom2 = cluster[surface_atoms[index2]]
			distance = get_distance(atom1,atom2)
			if distance <= cutoff_dictionary[(atom1.symbol,atom2.symbol)]:
				surface_atom_neighbour_list.setdefault(surface_atom_index_1,[]).append(surface_atom_index_2)
				surface_atom_neighbour_list.setdefault(surface_atom_index_2,[]).append(surface_atom_index_1)
	surface_atom_neighbour_list_sorted = {}
	for index in surface_atom_neighbour_list.keys():
		surface_atom_neighbour_list_sorted[index] = sorted(surface_atom_neighbour_list[index])
	return surface_atom_neighbour_list_sorted