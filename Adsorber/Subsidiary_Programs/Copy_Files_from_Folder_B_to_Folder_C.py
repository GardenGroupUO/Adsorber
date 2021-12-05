import os, errno
from copy import deepcopy
from shutil import copyfile

from ase import Atoms
from ase.io import read, write

def Copy_Files_from_Folder_B_to_Folder_C(adsorbates, top_sites, bridge_sites, three_fold_sites, four_fold_sites):

	def get_indices(top_sites):
		top_sites = top_sites.split()
		all_top_sites = []
		for top_site in top_sites:
			if top_site.isdigit():
				all_top_sites.append(int(top_site))
			else:
				limits = top_site.split(':')
				lower_limit, upper_limit = limits
				lower_limit, upper_limit = int(lower_limit), int(upper_limit)
				all_top_sites += list(range(lower_limit, upper_limit+1, 1))
		return all_top_sites 

	binding_sites = [deepcopy(top_sites), deepcopy(bridge_sites), deepcopy(three_fold_sites), deepcopy(four_fold_sites)]
	for index in range(len(binding_sites)):
		sites = binding_sites[index]
		if isinstance(sites,str):
			binding_sites[index] = get_indices(sites)
		else:
			for folder_name, indices in list(sites.items()):
				sites[folder_name] = get_indices(indices)

	# =============================================================================================================
	# Make folder that contains models of the places where you have chosen to place H atom on.

	model_folder = 'Part_B_Binding_Site_Locations'
	bonding_models_suffixes = ['top_sites.xyz','bridging_sites.xyz','three_fold_sites.xyz','four_fold_sites.xyz']
	file_names = []
	for bonding_models_suffix in bonding_models_suffixes:
		for file in os.listdir(model_folder):
			if file.endswith(bonding_models_suffix):
				file_names.append(file)
				break

	if len(file_names) > 0:

		chosen_sites_folder_name = 'Part_B_Chosen_Binding_Sites_model'
		print('Making models of selected binding sites and placing it in the folder called: '+str(chosen_sites_folder_name))
		if not os.path.exists(chosen_sites_folder_name):
			os.makedirs(chosen_sites_folder_name)

		system = read(model_folder+'/'+file_names[0]).copy()
		for index in range(len(system)-1,-1,-1):
			if system[index].symbol == 'H':
				del system[index]
			else:
				break

		full_binding_model = Atoms()
		for sites, model_name in zip(binding_sites, file_names):
			if isinstance(sites,dict):
				new_sites = []
				for site in sites.values():
					new_sites += site
				sites = new_sites
			full_model = read(model_folder+'/'+model_name).copy()
			binding_site_model = Atoms()
			for index in range(len(full_model)):
				if index in sites:
					binding_site_model.append(full_model[index])
			xyz_name = model_name.replace('.xyz','')+'_chosen_binding_sites.xyz'
			write(chosen_sites_folder_name+'/'+xyz_name,system+binding_site_model)
			full_binding_model += binding_site_model.copy()
		write(chosen_sites_folder_name+'/Full_Selected_Binding_Site_model.xyz',system+full_binding_model)

	# =============================================================================================================
	# Place adsorbates+system from Part_B_folder to Part_C_folder

	site_types = ['Top_Sites','Bridge_Sites','Three_Fold_Sites','Four_Fold_Sites']

	def make_folder(Part_B_folder,Part_C_folder,within_path_from,within_path_to,all_sites_to_copy,number_difference,print_directories):
		path_from = Part_B_folder+'/'+within_path_from
		path_to   = Part_C_folder+'/'+within_path_to
		if not os.path.exists(path_to):
			os.makedirs(path_to)
		for a_site_tested in all_sites_to_copy:
			filename_prefix = suffix+str(a_site_tested-number_difference)+'_'+str(a_site_tested)
			filenames = []
			for filename in os.listdir(path_from):
				if os.path.isfile(path_from+'/'+filename) and filename.startswith(filename_prefix):
					filenames.append(filename)
			if len(filenames) == 0:
				raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 'No file that begin with '+str(filename_prefix)+' in '+str(path_from))
			filenames.sort()
			for filename in filenames:
				if print_directories:
					print(filename+': '+within_path_from+' -> '+within_path_to)
				else:
					print(filename)
				copyfile(path_from+'/'+filename,path_to+'/'+filename)

	print('=======================================')
	Part_B_folder = 'Part_B_All_Systems_with_Adsorbed_Species'
	Part_C_folder = 'Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files'
	print('Copying selected xyz files')
	print('From: '+str(Part_B_folder))
	print('To: '+str(Part_C_folder))
	print()
	for adsorbate in adsorbates:
		print('Copying selected xyz files involving '+str(adsorbate))
		for site_type, all_sites_to_copy in zip(site_types,binding_sites):
			within_path_from = str(adsorbate)+'/'+str(site_type)
			path_from = Part_B_folder+'/'+within_path_from
			if not os.path.exists(path_from):
				continue
			a_filename = os.listdir(path_from)[0]
			suffix = str(adsorbate)+'_'+str(site_type).lower()+'_'
			a_filename = a_filename.replace('.xyz','').replace(suffix,'')
			a_filename = a_filename.split('_')
			dummy_atom_position, dummy_atom_index = int(a_filename[0]), int(a_filename[1])
			number_difference = dummy_atom_index - dummy_atom_position
			within_path_to   = str(adsorbate)+'/'+str(site_type)
			if isinstance(sites,str):
				make_folder(Part_B_folder,Part_C_folder,within_path_from,within_path_to,all_sites_to_copy,number_difference,False)
			else:
				for folder_name, indices in all_sites_to_copy.items():
					new_within_path_to = within_path_to+'/'+str(folder_name)
					make_folder(Part_B_folder,Part_C_folder,within_path_from,new_within_path_to,indices,number_difference,True)
		print()
	print('Completed copying selected xyz files')
	print('From: '+str(Part_B_folder))
	print('To: '+str(Part_C_folder))
	print('=======================================')