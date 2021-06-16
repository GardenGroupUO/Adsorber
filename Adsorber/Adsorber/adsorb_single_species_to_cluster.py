import numpy as np

from ase import Atom
from ase.io import write

from Adsorber.Adsorber.other_methods import make_folder, get_unit_vector, Rodrigues_Rotation_formula

def get_extended_adsorption_site(distance_of_adatom_from_surface, adsorption_site, centre_of_binding_origin):
	vector = get_unit_vector(adsorption_site - centre_of_binding_origin)
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

def rotate_molecule_into_new_vector(molecule, molecule_vector, rotate_molecule_to_this_vector, adsorbed_molecule_name,Rotation_matrix=None):
	if Rotation_matrix is None:
		Rotation_matrix = Rodrigues_Rotation_formula(molecule_vector, rotate_molecule_to_this_vector)
	new_rotated_positions = np.transpose(np.matmul(Rotation_matrix,np.transpose(molecule.get_positions())))
	molecule.set_positions(new_rotated_positions)

def adsorb_single_species_to_cluster(cluster, binding_site_datum, an_adsorbed_species, main_path_name, sub_name):

	cluster_with_adsorbed_molecule = cluster.copy()

	adsorption_site, centre_of_binding_origin = binding_site_datum
	distance_of_adatom_from_surface = an_adsorbed_species['distance_of_adatom_from_surface']
	adsorption_site = get_extended_adsorption_site(distance_of_adatom_from_surface,adsorption_site, centre_of_binding_origin)

	adsorbed_molecule_name = an_adsorbed_species['name']
	adsorbed_molecule = an_adsorbed_species['molecule'].copy()

	path_name = main_path_name+'/'+adsorbed_molecule_name
	cluster_with_adsorbed_molecule_name = adsorbed_molecule_name+'_site_'+str(sub_name)
	make_folder(path_name)

	if len(adsorbed_molecule) == 1:
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
		write(path_name+'/'+cluster_with_adsorbed_molecule_name+'.xyz',cluster_with_adsorbed_molecule)
	elif len(adsorbed_molecule) > 1:
		if 'rotations' in an_adsorbed_species:
			rotations = an_adsorbed_species['rotations']
		else:
			rotations = [0.0]
		adsorbed_molecule = an_adsorbed_species['molecule'].copy()
		binding_atom_index = an_adsorbed_species['index']
		adsorbed_molecule_axis = get_unit_vector(return_vector(an_adsorbed_species['axis']))
		position_of_index_atom = adsorbed_molecule[binding_atom_index].position
		center_index_atom = np.array((0,0,0)) - position_of_index_atom
		direction_to_point_molecule_along = get_unit_vector(adsorption_site - centre_of_binding_origin)
		Rotation_matrix = Rodrigues_Rotation_formula(adsorbed_molecule_axis, direction_to_point_molecule_along)
		for rotation in rotations:
			cluster_with_adsorbed_molecule = cluster.copy()
			adsorbed_molecule = an_adsorbed_species['molecule'].copy()
			adsorbed_molecule.rotate(rotation,adsorbed_molecule_axis,adsorbed_molecule[binding_atom_index].position)
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
			cluster_with_adsorbed_molecule += adsorbed_molecule
			if len(rotations) == 1:
				write(path_name+'/'+cluster_with_adsorbed_molecule_name+'.xyz',cluster_with_adsorbed_molecule)
			else:
				write(path_name+'/'+cluster_with_adsorbed_molecule_name+'_rotation_'+str(rotation)+'.xyz',cluster_with_adsorbed_molecule)
