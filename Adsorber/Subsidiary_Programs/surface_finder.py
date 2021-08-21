import numpy as np
from math import sqrt, cos, radians, atan, tan, atan2, degrees, acos, pi
from ase import Atom, Atoms
from ase.io import read, write
from ase.visualize import view

def get_unit_vector(non_normalised_vector):
	return non_normalised_vector/np.linalg.norm(non_normalised_vector)

name = '15-3-3629.xyz'
cluster = read(name)
cluster_positions = cluster.get_positions()
# Center center of mass of the cluster at the origin
cluster_center_of_mass = cluster.get_center_of_mass()
# Calculate the radial vectors of all of the atoms in the cluster, from the center --> call this vector AC
cluster_radial_vectors = cluster_positions - cluster_center_of_mass
# Calculate the vector between the atom of interest (atom i) and all other atoms in the system. --> call this vector AB
# Then dot product this with the radial vector for the atom of interest (atom i)
angle_of_cones_between_vectors = {}
for index1 in range(len(cluster_positions)):
	cluster_radial_vector_1_unit_vector = get_unit_vector(cluster_radial_vectors[index1])
	position1 = cluster_positions[index1]
	for index2 in range(index1+1,len(cluster_positions)):
		position2 = cluster_positions[index2]
		vector_from_1_to_2 = position2 - position1 # getting AB
		## take dot product of the vector AB and the radial vector 
		angle_of_cone = np.dot(get_unit_vector(vector_from_1_to_2),cluster_radial_vector_1_unit_vector)
		angle_of_cones_between_vectors.setdefault(index1,[]).append((index2,angle_of_cone))
		angle_of_cones_between_vectors.setdefault(index2,[]).append((index1,angle_of_cone))
#Check to see whether there are any other vectors (all vectors AB) that sit within a (in this case, currently, 40 degree cone). 
surface_atoms = []
for index1, cones in angle_of_cones_between_vectors.items():
	max_index, max_cone = max(cones,key=lambda x:x[1])
	if max_cone < cos(radians(40)): 
		cluster[index1].tag = 1
		print(index1)
	else:
		cluster[index1].tag = 0

write('surface_'+name,cluster)











# import numpy as np
# from math import sqrt, cos, radians, atan, tan, atan2, degrees, acos, pi

# nAt = 110

# header = []

# num_lines = sum(1 for line in open('XDAT_1'))
# iter = (num_lines-7)/(nAt+1)

# all_atoms = []
# # Read in the coordinates from the XDAT_1 file
# with open("XDAT_1", "r") as ofile:
# 	for i in range(7):
# 		x = ofile.readline()
# 		header.append(x)
# 	for j in range(iter):
# 		ind_atoms = []
# 		for k in range(nAt+1):
# 			x = ofile.readline()
# 			if not "Direct" in x:
# 				geometry_coords = []
# 				each_atom_coords = x.split()
# 				for l in range(3):
# 					geometry_coords.append(float(each_atom_coords[l])*40)
# 				ind_atoms.append(geometry_coords)
# 		all_atoms.append(ind_atoms)			

# center = []	

# #Center center of mass of the cluster at the origin

# for k in all_atoms:
# 	com = np.mean(k, axis = 0)
# 	center.append(com)

# #Calculate the radial vectors of all of the atoms in the cluster, from the center --> call this vector AC
	
# radial_vectors = []

# for k in range(len(all_atoms)):
# 	rv_iter = []
# 	for b in range(len(all_atoms[k])):
# 		rv_atom = []
# 		for i in range(3):
# 			rv = (all_atoms[k][b][i] - center[k][i])
# 			rv_atom.append(rv)
# 		rv_iter.append(rv_atom)
# 	radial_vectors.append(rv_iter)

# ab_v = []

# fw = open('chk.xyz', 'w')

# #Calculate the vector between the atom of interest (atom i) and all other atoms in the system. --> call this vector AB

# master_indices = []
# surface_atoms = []
# for m in range(len(all_atoms)):
# 	all_indices = []
# 	surf_at = []
# 	for a in range(len(all_atoms[m])):
# 		atom_index = []
# 		ab_v_atoms = []
# 		for b in range(nAt):
# 			ab_v = []	
# 			if b != a:
# 				for l in range(3):
# 					ab_vector = all_atoms[m][b][l] - all_atoms[m][a][l] ## calculate length of vector ab
# 					ab_v.append(ab_vector)
#                                 ## This part is to calculate the angle between vector AB and vector AC
# 				numerator = ((ab_v[0])*(radial_vectors[m][a][0]) + (ab_v[1])*(radial_vectors[m][a][1]) + (ab_v[2])*(radial_vectors[m][a][2])) ## take dot product of the vector AB and the radial vector 
# 				denominator = ((((ab_v[0])**2 + (ab_v[1])**2 + (ab_v[2])**2) ** 0.5) * (((radial_vectors[m][a][0])**2 + (radial_vectors[m][a][1])**2 + (radial_vectors[m][a][2])**2) ** 0.5)) ## magnitude of vector AB * magnitude of vector AC 
# 				index = numerator/denominator # index = cos(theta) 
# 				atom_index.append(index)
# 		all_indices.append(atom_index)
# 	master_indices.append(all_indices)

# #Check to see whether there are any other vectors (all vectors AB) that sit within a (in this case, currently, 40 degree cone). 

# for h in range(len(master_indices)):
# 	fw.write(str(nAt) +  '\nblah \n')
# 	for y in range(len(master_indices[h])):
# 		for p in master_indices[h][y]: ## You can change the angle of the cone that look for atoms within, to make the algorithm more or less selective. Bigger angle = more selective. 
# 		#	if max(master_indices[h][y]) < 0.5: #cos 60
# 	#		if max(master_indices[h][y]) < ((sqrt(2))/2): #cos 45
# 			#if max(master_indices[h][y]) < ((sqrt(3))/2): #cos 30
# 			if max(master_indices[h][y]) < cos(radians(40)): #cos 40
# 				lbl = 'Bi'
# 			else:
# 				lbl = 'Ga'
# 				print(h, y)
# 		outstr = '%s   %10.5f   %10.5f  %10.5f\n' % (lbl, all_atoms[h][y][0], all_atoms[h][y][1], all_atoms[h][y][2])
# 		fw.write(outstr)
 
