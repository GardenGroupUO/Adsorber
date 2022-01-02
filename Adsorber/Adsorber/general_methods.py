import os, shutil
import numpy as np

from ase.io import read

def get_system(system_filename,add_vacuum=None,save_vacuum_system=False):
	system = read(system_filename)
	system.set_velocities(system.get_velocities())
	system.set_pbc(False)
	if not add_vacuum is None:
		system.center(vacuum=add_vacuum)
		if save_vacuum_system:
			system_name_with_vacuum = '.'.join(system_filename.split('.')[:-1:])+'_with_vacuum_'+str(add_vacuum)+'_Ang.xyz'
			write(system_name_with_vacuum,system)
			print('Have added '+str(vacuum)+' Ang of vacuum to your system.')
			print('This means that replicas of your system under periodic boundary conditions should be at least '+str(2.0*vacuum)+' Ang apart from each other.')
			print('Your system with vacuum has been saved as: '+str(system_name_with_vacuum))
	return system

def make_new_folder(folder_path):
	if os.path.exists(folder_path):
		shutil.rmtree(folder_path)
	os.makedirs(folder_path)

def remove_folder(folder_path):
	if os.path.exists(folder_path):
		shutil.rmtree(folder_path)

def make_folder(folder_path):
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)

def get_distance(atom_position_1,atom_position_2):
	xx_dist = atom_position_1[0] - atom_position_2[0]
	yy_dist = atom_position_1[1] - atom_position_2[1]
	zz_dist = atom_position_1[2] - atom_position_2[2]
	distance = (xx_dist**2.0 + yy_dist**2.0 + zz_dist**2.0)**0.5
	return distance

def get_unit_vector(v):
	v_hat = v / np.linalg.norm(v)
	return v_hat

def Rodrigues_Rotation_formula(vector, vector_to_rotate_onto):
	# https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
	# https://math.stackexchange.com/questions/2828802/angle-definition-confusion-in-rodrigues-rotation-matrix

	theta = np.arccos(np.dot(vector, vector_to_rotate_onto) / np.linalg.norm(vector)*np.linalg.norm(vector_to_rotate_onto))
	k = np.cross(vector, vector_to_rotate_onto) / np.linalg.norm(np.cross(vector, vector_to_rotate_onto))

	K = np.array([[0, -k[2], k[1]],[k[2], 0, -k[0]],[-k[1], k[0], 0]])
	K2 = np.matmul(K,K)
	I = np.eye(3)

	R = I + np.sin(theta)*K + (1-np.cos(theta))*K2

	return R

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