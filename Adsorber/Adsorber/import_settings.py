import os

# =================================================================================================================

def get_variable(script,setting,default='NG'): # (NG = Not Given)
	if (default == 'NG') or (setting in script.__dict__.keys()):
		return script.__dict__[setting]
	else:
		return default

# =================================================================================================================

general_script_name = 'general.py'
adsorbates_script_name = 'adsorbates.py'
partA_script_name = 'partA.py'
partB_script_name = 'partB.py'
partC_script_name = 'partC.py'

def import_general_settings():
	if not os.path.exists(general_script_name):
		print('Error: You do not have a '+str(general_script_name)+' file.')
		print('This is required to provide the general settings for Adsorber.')
		print('See documentation for details on how to write a '+str(general_script_name)+' file.')
		exit('This program will finish without beginning.')
	import general
	cluster_or_surface_model = import_cluster_or_surface_model_setting(get_variable(general,'cluster_or_surface_model'))
	system_filename = get_variable(general,'system_filename')
	name_without_suffix = system_filename.split('.')[0]
	add_vacuum = get_variable(general,'add_vacuum',default=None)
	vasp_files_folder = 'VASP_Files'
	systems_to_convert_for_VASP_name = 'Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files'
	return cluster_or_surface_model, system_filename, name_without_suffix, add_vacuum, vasp_files_folder, systems_to_convert_for_VASP_name

def import_cluster_or_surface_model_setting(cluster_or_surface_model):
	if not isinstance(cluster_or_surface_model,str):
		print('Error in Adsorber')
		print('The "cluster_or_surface_model" variable must be a string')
		print('"cluster_or_surface_model" = '+str(cluster_or_surface_model))
		print('Check this out. The Adsorber program will finish without completing')
		exit()
	elif cluster_or_surface_model.lower() in ['cluster','surface model']:
		return cluster_or_surface_model
	else:
		print('Error in Adsorber')
		print('The "cluster_or_surface_model" variable must be either "cluster" or "surface model"')
		print('"cluster_or_surface_model" = '+str(cluster_or_surface_model))
		print('Check this out. The Adsorber program will finish without completing')
		exit()

# =================================================================================================================

def import_adsorbate_settings():
	if not os.path.exists(adsorbates_script_name):
		print('Error: You do not have a '+str(adsorbates_script_name)+' file.')
		print('This is required to provide the settings reguarding the adsorbate for Adsorber.')
		print('See documentation for details on how to write a '+str(adsorbates_script_name)+'file.')
		exit('This program will finish without beginning.')
	import adsorbates
	adsorbed_species = get_variable(adsorbates,'adsorbed_species')
	return adsorbed_species

# =================================================================================================================

def import_PartA_settings():
	if not os.path.exists(partA_script_name):
		print('Error: You do not have a '+str(partA_script_name)+' file.')
		print('This is required to provide the settings reguarding Part A for Adsorber.')
		print('See documentation for details on how to write a '+str(partA_script_name)+'file.')
		exit('This program will finish without beginning.')
	import partA
	slurm_information_system = get_variable(partA,'slurm_information_system')
	other_molecules_to_obtain_VASP_energies_for = get_variable(partA,'other_molecules_to_obtain_VASP_energies_for')
	slurm_information_adsorbates_and_other = get_variable(partA,'slurm_information_adsorbates_and_other')
	part_A_folder_name = 'Part_A_Non_Adsorbed_Files_For_VASP'
	return slurm_information_system, other_molecules_to_obtain_VASP_energies_for, slurm_information_adsorbates_and_other, part_A_folder_name

# =================================================================================================================

from Adsorber.Adsorber.general_methods import get_system
def import_PartB_settings():
	if not os.path.exists(partB_script_name):
		print('Error: You do not have a '+str(partB_script_name)+' file.')
		print('This is required to provide the settings reguarding Part B for Adsorber.')
		print('See documentation for details on how to write a '+str(partB_script_name)+'file.')
		exit('This program will finish without beginning.')
	import partB
	path_to_VASP_optimised_non_adsorbate_system = get_variable(partB,'path_to_VASP_optimised_non_adsorbate_system')
	cluster = get_system(path_to_VASP_optimised_non_adsorbate_system)
	surface_atoms = get_variable(partB,'surface_atoms')
	cutoff = import_cutoff_setting(get_variable(partB,'cutoff'),cluster,surface_atoms)
	data_storage_file = 'adsorber_data.txt'
	# ===========================================================================================
	# information about the atoms and molecules that will be adsorbed, as well sa their binding sites
	distance_of_dummy_adatom_from_surface = 1.1 # Angstroms #vdw_radii[atomic_numbers[self.cluster[0].symbol]] + vdw_radii[atomic_numbers['H']]
	bind_site_data_types = ['top sites','bridge sites','three-fold sites','four-fold sites']
	# ===========================================================================================
	system_folder_name = 'Part_B_All_Systems_with_Adsorbed_Species'
	return path_to_VASP_optimised_non_adsorbate_system, cluster, surface_atoms, cutoff, data_storage_file, distance_of_dummy_adatom_from_surface, bind_site_data_types, system_folder_name

def import_cutoff_setting(cutoff,cluster,surface_atoms):
	surface_atom_symbols = list(set([cluster[index].symbol for index in surface_atoms]))
	new_cutoff = {}
	if isinstance(cutoff,float):
		for element1 in surface_atom_symbols:
			for element2 in surface_atom_symbols:
				new_cutoff[(element1, element2)] = cutoff
	elif isinstance(cutoff,dict):
		issues = []
		for element in surface_atom_symbols:
			if not element in new_cutoff.keys():
				issues.append(element)
		for index1 in range(len(surface_atom_symbols)):
			element1 = surface_atom_symbols[index1]
			for index2 in range(index1+1,len(surface_atom_symbols)):
				element2 = surface_atom_symbols[index2]
				if (not (element1, element2) in new_cutoff.keys()) or (not (element2, element1) in new_cutoff.keys()):
					issues.append((element1, element2))
		if len(issues) == 0:
			for key, value in cutoff.items():
				if isinstance(key,str):
					new_cutoff[(key,key)] = value
				elif isinstance(key,tuple) and len(key) == 2:
					element1, element2 = key
					new_cutoff[(element1, element2)] = value
					new_cutoff[(element2, element1)] = value
		else:
			print('Error in Adsorber')
			print('You are missing the following from the "cutoff" variable dictionary:')
			print(str(issues))
			print('Make sure to add these cutoff values to your dictionary')
			print('Check this out. The Adsorber program will finish without completing')
			exit()
	else:
		print('Error in Adsorber')
		print('The "cutoff" variable must be either a float or a dictionary')
		print('"cutoff" = '+str(cutoff))
		print('"cutoff" is a '+str(type(cutoff)))
		print('Check this out. The Adsorber program will finish without completing')
		exit()
	return new_cutoff

# =================================================================================================================

def import_PartC_settings():
	if not os.path.exists(partC_script_name):
		print('Error: You do not have a '+str(partC_script_name)+' file.')
		print('This is required to provide the settings reguarding Part C for Adsorber.')
		print('See documentation for details on how to write a '+str(partC_script_name)+'file.')
		exit('This program will finish without beginning.')
	import partC
	VASP_folder_name = 'Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP' 
	part_c_force_create_original_POSCAR = False # part_c_force_create_original_POSCAR
	# Other settings
	path_to_VASP_optimised_non_adsorbate_system = get_variable(partC,'path_to_VASP_optimised_non_adsorbate_system')
	cluster = get_system(path_to_VASP_optimised_non_adsorbate_system)
	slurm_information = get_variable(partC,'slurm_information')
	return VASP_folder_name, part_c_force_create_original_POSCAR, cluster, slurm_information
