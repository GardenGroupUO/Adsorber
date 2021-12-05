import numpy as np

from ase import Atom
from ase.io import write

from Adsorber.Adsorber.other_methods import make_folder, get_unit_vector, Rodrigues_Rotation_formula
from Adsorber.Adsorber.Part_B_automated_rotation_methods import get_automatic_rotations, get_distance

# ================================================================================================================
# The main method for adsorbing adsorbates to a system at a binding site

def adsorb_single_species_to_cluster(cluster, surface_atoms, binding_site_datum, cutoff, an_adsorbed_species, binding_sites_name, sub_name, main_path_name):

	len_of_cluster = len(cluster)

	dummy_adsorption_site, centre_of_binding_origin, indices_of_atoms_involved = binding_site_datum
	distance_of_adatom_from_surface = an_adsorbed_species['distance_of_adatom_from_surface']
	adsorption_site = get_extended_adsorption_site(distance_of_adatom_from_surface, dummy_adsorption_site, centre_of_binding_origin)

	adsorbed_molecule_name = an_adsorbed_species['name']
	adsorbed_molecule = an_adsorbed_species['molecule'].copy()

	path_name = main_path_name+'/'+adsorbed_molecule_name+'/'+binding_sites_name
	make_folder(path_name)
	cluster_with_adsorbed_molecule_name = adsorbed_molecule_name+'_'+str(binding_sites_name).lower()+'_'+str(sub_name)+'_'+str(len(cluster)-1+sub_name)
	path_to_file = path_name+'/'+cluster_with_adsorbed_molecule_name

	if len(adsorbed_molecule) == 1:
		cluster_with_adsorbed_molecule = cluster.copy()
		if isinstance(adsorbed_molecule,Atom):
			# move index atom to the binding position
			adsorbed_molecule.x = adsorption_site[0]
			adsorbed_molecule.y = adsorption_site[1]
			adsorbed_molecule.z = adsorption_site[2]
			cluster_with_adsorbed_molecule.append(np.transpose(adsorbed_molecule))
		else:
			# move index atom to the binding position
			adsorbed_molecule[0].x = adsorption_site[0]
			adsorbed_molecule[0].y = adsorption_site[1]
			adsorbed_molecule[0].z = adsorption_site[2]
			cluster_with_adsorbed_molecule += adsorbed_molecule
		write(path_to_file+'.xyz',cluster_with_adsorbed_molecule)
	elif len(adsorbed_molecule) > 1:
		adsorbed_molecule = an_adsorbed_species['molecule'].copy()
		binding_atom_index = an_adsorbed_species['index']
		adsorbed_molecule_axis = get_unit_vector(return_vector(an_adsorbed_species['axis']))
		position_of_index_atom = adsorbed_molecule[binding_atom_index].position
		center_index_atom = np.array((0,0,0)) - position_of_index_atom
		direction_to_point_molecule_along = get_unit_vector(adsorption_site - centre_of_binding_origin)
		Rotation_matrix = Rodrigues_Rotation_formula(adsorbed_molecule_axis, direction_to_point_molecule_along)
		#######################################################################################################################
		# Rotate and move the adsorbate into positions
		adsorbed_molecule = an_adsorbed_species['molecule'].copy()
		#-----------------------------------------------------------------------------
		# rotate the molecule to allign correctly
		# 1. center the index_atom at (0,0,0)
		adsorbed_molecule.set_positions(adsorbed_molecule.get_positions() + center_index_atom)		
		# 2. determine the angles required to rotate the molecule based on adsorbed_molecule_axis
		# 3. Perform rotation
		rotate_molecule_into_new_vector(adsorbed_molecule, adsorbed_molecule_axis, direction_to_point_molecule_along, adsorbed_molecule_name, Rotation_matrix=Rotation_matrix)
		#-----------------------------------------------------------------------------
		# move index atom to the binding position
		position_of_index_atom = adsorbed_molecule[binding_atom_index].position
		adsorbed_atom_translation = adsorption_site - position_of_index_atom
		adsorbed_molecule.set_positions(adsorbed_molecule.get_positions() + adsorbed_atom_translation)
		#-----------------------------------------------------------------------------
		#######################################################################################################################
		if 'rotations' in an_adsorbed_species:
			if isinstance(an_adsorbed_species['rotations'],str) and an_adsorbed_species['rotations'].startswith('automatic'):
				rotations = get_automatic_rotations(cluster, surface_atoms, centre_of_binding_origin, indices_of_atoms_involved, direction_to_point_molecule_along, cutoff, adsorbed_molecule, binding_atom_index, binding_sites_name)
				if an_adsorbed_species['rotations'].startswith('automatic with misalignment of ') and an_adsorbed_species['rotations'].startswith(' degrees'):
					rotation_misalignment = float(an_adsorbed_species['rotations'].replace('automatic with misalignment of ','').replace(' degrees',''))
					rotations = get_misaligned_rotations(rotations, rotation_misalignment)
			else:
				rotations = an_adsorbed_species['rotations']
		else:
			rotations = [0.0]

		if len(rotations) == 1:
			cluster_with_adsorbed_molecule = cluster.copy() + adsorbed_molecule.copy()
			write(path_to_file+'.xyz',cluster_with_adsorbed_molecule)
		else:
			systems_rotations = []
			for rotation in sorted(rotations):
				adsorbed_molecule_with_rotation_around_axis = adsorbed_molecule.copy()
				adsorbed_molecule_with_rotation_around_axis.rotate(rotation, direction_to_point_molecule_along, centre_of_binding_origin)
				cluster_with_adsorbed_molecule = cluster.copy() + adsorbed_molecule_with_rotation_around_axis
				for _, a_system in systems_rotations:
					if is_same_system(cluster_with_adsorbed_molecule,a_system,starting_index=len_of_cluster):
						break
				else:
					systems_rotations.append((rotation, cluster_with_adsorbed_molecule))
			# view([cluster_with_adsorbed_molecule for rotation, cluster_with_adsorbed_molecule in systems_rotations]) # for debugging
			for rotation, cluster_with_adsorbed_molecule in systems_rotations:
				write(path_to_file+'_rotation_'+str(rotation)+'.xyz',cluster_with_adsorbed_molecule)

# ================================================================================================================
# Other methods

def get_extended_adsorption_site(distance_of_adatom_from_surface, dummy_adsorption_site, centre_of_binding_origin):
	vector = get_unit_vector(dummy_adsorption_site - centre_of_binding_origin)
	new_adsorption_site = centre_of_binding_origin + distance_of_adatom_from_surface*vector
	return new_adsorption_site

def return_vector(vector):
	if isinstance(vector,tuple) or isinstance(vector,list):
		return vector
	elif isinstance(vector,str):
		if vector == 'x':
			vector = (1,0,0)
		elif vector == 'y':
			vector = (0,1,0)
		elif vector == 'z':
			vector = (0,0,1)
		elif vector == '-x':
			vector = (-1,0,0)
		elif vector == '-y':
			vector = (0,-1,0)
		elif vector == '-z':
			vector = (0,0,-1)
		else:
			exit('error')
		return vector

# ================================================================================================================
# Rotation methods

def rotate_molecule_into_new_vector(molecule, molecule_vector, rotate_molecule_to_this_vector, adsorbed_molecule_name,Rotation_matrix=None):
	if Rotation_matrix is None:
		Rotation_matrix = Rodrigues_Rotation_formula(molecule_vector, rotate_molecule_to_this_vector)
	new_rotated_positions = np.transpose(np.matmul(Rotation_matrix,np.transpose(molecule.get_positions())))
	molecule.set_positions(new_rotated_positions)

# ================================================================================================================
# Methods for determining if systems are structurally equivalant

def is_same_system(new_system,original_system,starting_index=0, maximum_distance_to_be_within = 0.25):
	new_system_positions_of_elements = {}
	original_system_positions_of_elements = {}
	elements = set()
	# Obtain the positions of adsorbate elements in the new and original systems
	for index in range(starting_index,len(new_system)):
		new_atom = new_system[index]
		new_system_positions_of_elements.setdefault(new_atom.symbol,[]).append(new_atom.position)
		elements.add(new_atom.symbol)
		original_atom = original_system[index]
		original_system_positions_of_elements.setdefault(original_atom.symbol,[]).append(original_atom.position)
		elements.add(original_atom.symbol)
	# Determines if the positions of elements overlap. This method works by gathering all the distances of 
	# all atoms of a particular element and comparing them from smallest distance until all atoms are paired together. 
	for element in elements:
		new_positions = new_system_positions_of_elements[element]
		ori_positions = original_system_positions_of_elements[element]
		are_atoms_eithin_eachother = are_positions_within_eachother(new_positions, ori_positions, maximum_distance_to_be_within=maximum_distance_to_be_within)
		if not are_atoms_eithin_eachother:
			return False
	return True


def are_positions_within_eachother(new_positions, ori_positions, maximum_distance_to_be_within = 0.25):
	matrix = np.zeros((len(new_positions),len(ori_positions)))
	for new_index in range(len(new_positions)):
		for ori_index in range(len(ori_positions)):
			matrix[new_index][ori_index] = get_distance(new_positions[new_index], ori_positions[ori_index])
	while not np.all(np.isnan(matrix)):
		smallest_distance = np.nanmin(matrix)
		if smallest_distance > maximum_distance_to_be_within:
			return False
		minimum_new_index, minimum_ori_index = np.where(matrix == smallest_distance)
		minimum_new_index, minimum_ori_index = minimum_new_index[0], minimum_ori_index[0]
		for index in range(len(ori_positions)):
			matrix[minimum_new_index][index] = np.nan
		for index in range(len(new_positions)):
			matrix[index][minimum_ori_index] = np.nan
	return True

# ================================================================================================================
