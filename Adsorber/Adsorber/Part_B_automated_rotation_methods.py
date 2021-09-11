import numpy as np
from math import pi

from Adsorber.Adsorber.other_methods import get_unit_vector

def get_automatic_rotations(cluster, surface_atoms, centre_of_binding_origin, indices_of_atoms_involved, direction_to_point_molecule_along, cutoff_to_figure_out, adsorbed_molecule, binding_atom_index, binding_sites_name):
	cutoff = 3.5 # figure this out later
	# ------------------------------------------------
	# get atoms and rotation sites about adsorption site on cluster, involving indices_of_atoms_involved
	nearby_atoms_positions = [cluster[index].position for index in indices_of_atoms_involved]
	# ------------------------------------------------
	# 1. get indices and positions of nearby atoms
	index_of_atoms = []
	nearby_directions = []
	for index in surface_atoms:
		if (binding_sites_name == 'Top_Sites') and (index in indices_of_atoms_involved):
			continue
		position = cluster[index].position
		if all([(get_distance(position,nearby_position) <= cutoff) for nearby_position in nearby_atoms_positions]):
			index_of_atoms.append(index)
			perpendicular_direction = get_prependicular_unit_vector(position,centre_of_binding_origin,direction_to_point_molecule_along)
			nearby_directions.append(perpendicular_direction)
	# the bottom is for debugging purposes, able to see the vectors in ase.gui
	'''
	if indices_of_atoms_involved == [7]:
		for index in index_of_atoms:
			cluster[index].symbol = 'Fe'
		for perpendicular_direction in nearby_directions:
			for number in range(1,6):
				cluster.append(Atom('X',position=centre_of_binding_origin + number*perpendicular_direction))
		view(cluster)
		import pdb; pdb.set_trace()
		exit()
	'''
	# ------------------------------------------------
	# 2. get positions inbetween near-by atoms
	for i1 in range(len(index_of_atoms)):
		index1 = index_of_atoms[i1]
		position1 = cluster[index1].position
		for index2 in index_of_atoms[i1+1:]:
			if (binding_sites_name == 'Bridge_Sites') and (set([index1,index2]) == set(indices_of_atoms_involved)):
				continue
			position2 = cluster[index2].position
			if get_distance(position1,position2) <= cutoff:
				halfway_position = (position1+position2)/2.0
				perpendicular_direction = get_prependicular_unit_vector(halfway_position,centre_of_binding_origin,direction_to_point_molecule_along)
				if np.isnan(perpendicular_direction).all():
					import pdb; pdb.set_trace()
				nearby_directions.append(perpendicular_direction)
	# the bottom is for debugging purposes, able to see the vectors in ase.gui
	#if (binding_sites_name == 'Bridge_Sites'):
	'''
	if indices_of_atoms_involved == [35, 70]:
		for index in index_of_atoms:
			cluster[index].symbol = 'Fe'
		for perpendicular_direction in nearby_directions:
			for number in range(1,6):
				cluster.append(Atom('X',position=centre_of_binding_origin + number*perpendicular_direction))
		view(cluster)
		import pdb; pdb.set_trace()
		exit()
	'''
	# ------------------------------------------------
	# get rotation axes of adsorbate
	adsorbate_levers = []
	for index in range(len(adsorbed_molecule)):
		if index == binding_atom_index:
			continue
		perpendicular_direction = get_prependicular_unit_vector(adsorbed_molecule[index].position, adsorbed_molecule[binding_atom_index].position, direction_to_point_molecule_along)
		if not any([vectors_are_time_same(perpendicular_direction, adsorbate_lever) for adsorbate_lever in adsorbate_levers]):
			adsorbate_levers.append(perpendicular_direction)
	# the bottom is for debugging purposes, able to see the vectors in ase.gui
	#for adsorbate_lever in adsorbate_levers:
	#	for number in range(1,6):
	#		adsorbed_molecule.append(Atom('X',position=adsorbed_molecule[binding_atom_index].position + number*adsorbate_lever))
	#view(adsorbed_molecule)
	# ------------------------------------------------
	# get rotations acount axis from adsorbate_levers to nearby_directions
	angles_of_rotation = [] #[0.0]
	for adsorbate_lever in adsorbate_levers:
		angles_of_rotation_for_lever = []
		initial_angle_of_rotation = 0.0 #get_anticlockwise_rotation(adsorbate_lever,adsorbate_levers[0],direction_to_point_molecule_along)
		for nearby_direction in nearby_directions:
			angle_of_rotation = get_anticlockwise_rotation(nearby_direction,adsorbate_lever,direction_to_point_molecule_along) + initial_angle_of_rotation
			if np.isnan(angle_of_rotation):
				import pdb; pdb.set_trace()
			angle_of_rotation = round(angle_of_rotation,1)
			angles_of_rotation_for_lever.append(angle_of_rotation)
		angles_of_rotation_for_lever.sort()
		angles_of_rotation += angles_of_rotation_for_lever

	# for debugging, you can see each of the rotations you have chosen
	'''
	movie = []
	for angle_of_rotation in angles_of_rotation:
		print(angle_of_rotation)
		adsorbed_molecule_with_rotation_around_axis = adsorbed_molecule.copy()
		adsorbed_molecule_with_rotation_around_axis.rotate(angle_of_rotation, direction_to_point_molecule_along, centre_of_binding_origin)
		cluster_with_adsorbed_molecule = cluster.copy()
		cluster_with_adsorbed_molecule += adsorbed_molecule_with_rotation_around_axis
		movie.append(cluster_with_adsorbed_molecule.copy())
	view(movie)
	'''	
	# ------------------------------------------------
	# remove any rotations that are too similar to each other
	angles_of_rotation.sort()
	#angles_of_rotation = remove_similar_rotation_angles(angles_of_rotation)
	return angles_of_rotation

# -----------------------------------------------------------------------------------------------------------------
# These methods are all used for automating rotations of adsorbate about the binding sites on a system. 

def get_distance(vector_1 ,vector_2):
	distance = (sum([(p1 - p2)**2.0 for p1, p2 in zip(vector_1 ,vector_2)])) ** 0.5
	return distance

def get_prependicular_unit_vector(position, origin, adsorbed_molecule_axis_unit_vector):
	nearby_atom_position = position - origin
	parallel_direction = np.dot(nearby_atom_position,adsorbed_molecule_axis_unit_vector)*adsorbed_molecule_axis_unit_vector
	perpendicular_direction = get_unit_vector(nearby_atom_position - parallel_direction)
	return perpendicular_direction

# https://stackoverflow.com/questions/14066933/direct-way-of-computing-clockwise-angle-between-2-vectors/16544330
# https://math.stackexchange.com/questions/878785/how-to-find-an-angle-in-range0-360-between-2-vectors/879474
def get_anticlockwise_rotation(p1, p2, nn):
	dot = np.dot(p1,p2)
	det = np.dot(nn,np.cross(p1,p2))
	angle = -np.arctan2(det, dot)*(180.0/pi)
	if angle < 0.0:
		angle += 360.0
	return angle

def vectors_are_time_same(vector1, vector2):
	for value1, value2 in zip(vector1, vector2):
		if abs(value1 - value2) > 0.0000000001:
			return False
	return True

angle_within_eachother = 5.0
def remove_similar_rotation_angles(angles_of_rotation):
	index1 = 0
	while index1 < len(angles_of_rotation):
		for index2 in range(len(angles_of_rotation)-1,index1,-1):
			if abs(angles_of_rotation[index1] - angles_of_rotation[index2]) < angle_within_eachother:
				del angles_of_rotation[index2]
		index1 += 1
















def is_within_other_angles(a_rotation, new_rotations):
	for new_rotation in new_rotations:
		if (new_rotation-angle_within_eachother) < a_rotation < (new_rotation+angle_within_eachother):
			return True
	return False

def get_misaligned_rotations(rotations, rotation_misalignment):
	new_rotations = []
	for rotation in sorted(rotations):
		a_rotation = rotation+rotation_misalignment
		if a_rotation >= 360.0:
			a_rotation -= 360.0
		if not is_within_other_angles(a_rotation, new_rotations):
			new_rotations.append(a_rotation)
		a_rotation = rotation-rotation_misalignment
		if a_rotation < 0:
			a_rotation += 360.0
		if not is_within_other_angles(a_rotation, new_rotations):
			new_rotations.append(a_rotation)
	return new_rotations