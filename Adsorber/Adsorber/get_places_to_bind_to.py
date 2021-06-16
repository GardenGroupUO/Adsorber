import numpy as np
from ase import Atom
from ase.optimize import FIRE
from ase.constraints import FixAtoms, FixBondLengths

from Adsorber.Adsorber.coulomb_potential import coulomb_potential
from Adsorber.Adsorber.other_methods import get_distance, get_unit_vector

def get_the_centre(atom_indices,cluster_positions):
	vectors = [cluster_positions[index] for index in atom_indices]
	centre_of_shape = sum(vectors)/float(len(atom_indices))
	return centre_of_shape

def coulomb_repulsion_potential_optimisation(cluster,binding_point,surface_atoms_to_bind_to):
	new_cluster = cluster.copy()
	# fix every atom in the cluster
	const1 = FixAtoms(indices=[atom.index for atom in new_cluster])
	# append a dummy adsorption atom and fix its bond distance with surface atoms
	new_cluster.append(Atom('H',binding_point))
	# fix bond length ot atoms of interest to bond to on surface
	bonds_to_fix = [(surface_atom,len(new_cluster)-1) for surface_atom in surface_atoms_to_bind_to]
	const2 = FixBondLengths(bonds_to_fix)
	# set constraints
	new_cluster.set_constraint([const1,const2])
	new_cluster.set_calculator(coulomb_potential())
	opt = FIRE(new_cluster) #,trajectory='qn.traj')
	opt.run(fmax=0.02,steps=100)
	binding_point = new_cluster[-1].position
	return binding_point

def get_origin_position(cluster_or_surface_model,cluster_center_of_mass,surface_atom_position):
	if cluster_or_surface_model == 'cluster':
		origin_position = cluster_center_of_mass
	elif cluster_or_surface_model == 'surface model':
		origin_position = np.copy(surface_atom_position)
		origin_position[2] = -9999999999999999.9 #-float('inf')
	return origin_position

# ------------------------------------------------------------------------------------------------------------------------------------ #
# Adatom above atom

def get_above_atom_adsorption_site(surface_atom,cluster,cluster_positions,distance_of_adatom_from_surface,origin_position):
	# get cluster positions
	surface_atom_position = cluster_positions[surface_atom]
	# get line from centre of mass of cluster to the surface atom of interest
	AB = surface_atom_position - origin_position
	AB_unit_vector = get_unit_vector(AB)
	#get new binding postion for the adsorbed atom
	binding_point = surface_atom_position + distance_of_adatom_from_surface*AB_unit_vector
	# to make sure it is as far away from every other atom as possible, perform a coulomb repulsion potential optimisation
	surface_atoms_to_bind_to = [surface_atom]
	binding_point = coulomb_repulsion_potential_optimisation(cluster,binding_point,surface_atoms_to_bind_to)
	return (binding_point,surface_atom_position)


def get_above_atom_sites(cluster,surface_atoms,distance_of_adatom_from_surface,cluster_or_surface_model):
	binding_point_data = []
	cluster_center_of_mass = cluster.get_center_of_mass()
	cluster_positions = cluster.get_positions()
	original_no_of_atoms = len(cluster)
	for surface_atom in surface_atoms:
		origin_position = get_origin_position(cluster_or_surface_model,cluster_center_of_mass,cluster_positions[surface_atom])
		binding_point_datum = get_above_atom_adsorption_site(surface_atom,cluster,cluster_positions,distance_of_adatom_from_surface,origin_position)
		binding_point_data.append(binding_point_datum)
	return binding_point_data

# ------------------------------------------------------------------------------------------------------------------------------------ #
# Adatom on bridging site

def get_above_bridge_adsorption_site(surface_atoms_to_bind_to,cluster,cluster_positions,distance_of_adatom_from_surface,origin_position):
	# get the centre of the bridge
	centre_of_pair = get_the_centre(surface_atoms_to_bind_to,cluster_positions)
	# get line from centre of mass of cluster to the surface atom of interest
	AB = centre_of_pair - origin_position
	AB_unit_vector = get_unit_vector(AB)
	# make a plane with the normal vector as the atom_to_atom_vector
	atom_to_atom_vector = [cluster_positions[index] for index in surface_atoms_to_bind_to]
	atom_to_atom_vector = atom_to_atom_vector[1] - atom_to_atom_vector[0]
	atom_to_atom_unit_vector = get_unit_vector(atom_to_atom_vector)
	# project the point from the AB_unit_vector onto a plane with normal vector atom_to_atom_unit_vector
	# This will give a point that is perp to atom_to_atom_unit_vector and is point away from the centre of mass of the cluster
	# https://stackoverflow.com/questions/9605556/how-to-project-a-point-onto-a-plane-in-3d
	orig = np.array([0.0,0.0,0.0]) # centre of unit vector plane is the origin.
	point = AB_unit_vector - orig
	normal = atom_to_atom_unit_vector
	distance = np.dot(point,normal)
	projected_point = point - distance*normal
	perp_vector_to_bond_unit_vector = get_unit_vector(projected_point)
	# get new binding postion for the adsorbed atom
	binding_point = centre_of_pair + distance_of_adatom_from_surface*perp_vector_to_bond_unit_vector
	# to make sure it is as far away from every other atom as possible, perform a coulomb repulsion potential optimisation
	binding_point = coulomb_repulsion_potential_optimisation(cluster,binding_point,surface_atoms_to_bind_to)
	return (binding_point,centre_of_pair)

def get_bridge_sites(cluster,neighbour_list_original,distance_of_adatom_from_surface,cluster_or_surface_model):
	neighbour_list = dict(neighbour_list_original)
	binding_point_data = []
	cluster_center_of_mass = cluster.get_center_of_mass()
	cluster_positions = cluster.get_positions()
	for surface_index1, indices2 in sorted(neighbour_list.items(),key=lambda x:x[0]):
		for surface_index2 in sorted(indices2):
			surface_atoms_to_bind_to = (surface_index1,surface_index2)
			centre_of_pair = get_the_centre(surface_atoms_to_bind_to,cluster_positions)
			origin_position = get_origin_position(cluster_or_surface_model,cluster_center_of_mass,centre_of_pair)
			binding_point_datum = get_above_bridge_adsorption_site(surface_atoms_to_bind_to,cluster,cluster_positions,distance_of_adatom_from_surface,origin_position)
			binding_point_data.append(binding_point_datum)
			neighbour_list[surface_index2].remove(surface_index1)
	return binding_point_data

# ------------------------------------------------------------------------------------------------------------------------------------ #
# Adatom on triangle site

def get_three_or_four_adsorption_site(shape_indices,cluster_positions,distance_of_adatom_from_surface,origin_position):

	# Find the centre of the triangle
	centre_of_shape = get_the_centre(shape_indices,cluster_positions)
	'''
	###### NOT USED ANYMORE ######
	# find distance to add the adatom to above the triangle to give a distance of distance_of_adatom_from_surface_atom from each atom. Assuming equillatoral triangle.
	distance_in_triangle = get_distance(centre_of_triangle,cluster_positions[triangle_indices[0]])
	distance_from_triangle = (distance_of_adatom_from_surface_atom**2.0 - distance_in_triangle**2.0)*0.5
	'''
	# Get the normal vector to the plane that the triangle is in
	AB = cluster_positions[shape_indices[1]] - cluster_positions[shape_indices[0]]
	AC = cluster_positions[shape_indices[2]] - cluster_positions[shape_indices[0]]
	normal_vector = np.cross(AB,AC)
	normal_unit_vector = get_unit_vector(normal_vector)
	# Determine the position of the adatom bonding site. Could be two positions, use centre of mass to use the point that is furest away.
	vector_to_add_to_centre_of_triangle = normal_unit_vector*distance_of_adatom_from_surface
	adsorption_site_1 = centre_of_shape + vector_to_add_to_centre_of_triangle
	adsorption_site_2 = centre_of_shape - vector_to_add_to_centre_of_triangle
	distance_from_COM_to_site_1 = get_distance(origin_position,adsorption_site_1)
	distance_from_COM_to_site_2 = get_distance(origin_position,adsorption_site_2)
	if distance_from_COM_to_site_1 > distance_from_COM_to_site_2:
		return (adsorption_site_1,centre_of_shape)
	else:
		return (adsorption_site_2,centre_of_shape)

def get_three_fold_sites(cluster,neighbour_list,distance_of_adatom_from_surface_atom,cluster_or_surface_model):
	# find neighbouring sets of triangles
	triangles = []
	for index1, indices2 in neighbour_list.items():
		for index2 in indices2:
			neighbours_of_1_as_set = set(indices2)
			neighbours_of_2_as_set = set(neighbour_list[index2])
			intersections = neighbours_of_1_as_set & neighbours_of_2_as_set
			for index3 in intersections:
				triangles.append(tuple(sorted([index1,index2,index3])))
	triangles = sorted(list(set(triangles)))
	# get binding points
	binding_point_data = []
	cluster_positions = cluster.get_positions()
	cluster_center_of_mass = cluster.get_center_of_mass()
	bottom_of_z_axis = np.array((0.0,0.0,-9999999999999999.9))
	for triangle_indices in triangles:
		origin_position = get_origin_position(cluster_or_surface_model,cluster_center_of_mass,bottom_of_z_axis)
		binding_point_datum = get_three_or_four_adsorption_site(triangle_indices,cluster_positions,distance_of_adatom_from_surface_atom,origin_position)
		binding_point_data.append(binding_point_datum)
	return binding_point_data

# ------------------------------------------------------------------------------------------------------------------------------------ #
# Adatom on square site

def get_four_fold_sites(cluster,neighbour_list,distance_of_adatom_from_surface_atom,cluster_or_surface_model):
	# find neighbouring sets of squares
	squares = []
	for index1, indices2 in sorted(neighbour_list.items(),key=lambda x:x[0]):
		for ii in range(len(indices2)):
			first_neighbour_to_index1 = indices2[ii]
			neighbours_of_2_as_set = set(neighbour_list[first_neighbour_to_index1])
			for jj in range(ii+1,len(indices2)):
				second_neighbour_to_index1 = indices2[ii]
				neighbours_of_3_as_set = set(neighbour_list[second_neighbour_to_index1])
				intersections = neighbours_of_2_as_set & neighbours_of_3_as_set
				for index4 in intersections:
					square = tuple(sorted([index1,first_neighbour_to_index1,index4,second_neighbour_to_index1]))
					if not len(set(square)) == len(square):
						continue
					position_1 = neighbour_list[index1]
					position_4 = neighbour_list[index4]
					distance14 = get_distance(position_1,position_4)
					position_2 = neighbour_list[first_neighbour_to_index1]
					position_3 = neighbour_list[second_neighbour_to_index1]
					distance23 = get_distance(position_2,position_3)
					if (distance14 <= distance_of_adatom_from_surface_atom*(2.0)) and (distance23 <= distance_of_adatom_from_surface_atom*(2.0)):
						squares.append()
	squares = sorted(list(set(squares)))
	# get binding points
	binding_point_data = []
	cluster_positions = cluster.get_positions()
	cluster_center_of_mass = cluster.get_center_of_mass()
	bottom_of_z_axis = np.array((0.0,0.0,9999999999999999.9))
	for square_indices in squares:
		origin_position = get_origin_position(cluster_or_surface_model,cluster_center_of_mass,bottom_of_z_axis)
		binding_point_datum = get_three_or_four_adsorption_site(square_indices,cluster_positions,distance_of_adatom_from_surface_atom,origin_position)
		binding_point_data.append(binding_point_datum)
	return binding_point_data

# ------------------------------------------------------------------------------------------------------------------------------------ #
