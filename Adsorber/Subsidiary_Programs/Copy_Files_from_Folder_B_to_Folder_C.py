import os
from shutil import copyfile

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

	binding_sites = [top_sites, bridge_sites, three_fold_sites, four_fold_sites]
	for index in range(len(binding_sites)):
		sites = binding_sites[index]
		if isinstance(sites,str):
			binding_sites[index] = get_indices(sites)
		else:
			for folder_name, indices in list(sites.items()):
				sites[folder_name] = get_indices(indices)

	site_types = ['Top_Sites','Bridge_Sites','Three_Fold_Sites','Four_Fold_Sites']

	def make_folder(c,Part_C_folder,within_path_from,within_path_to,all_sites_to_copy,print_directories):
		path_from = Part_B_folder+'/'+within_path_from
		path_to   = Part_C_folder+'/'+within_path_to
		if not os.path.exists(path_to):
			os.makedirs(path_to)
		for a_site_tested in all_sites_to_copy:
			filename = suffix+str(a_site_tested-number_difference)+'_'+str(a_site_tested)+'.xyz'
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
		for site_type, all_sites_to_copy in zip(site_types,binding_sites):
			within_path_from = str(adsorbate)+'/'+str(site_type)
			path_from = Part_B_folder+'/'+within_path_from
			if not os.path.exists(path_from):
				continue
			a_filename = os.listdir(path_from)[0]
			suffix = str(adsorbate)+'_'+str(site_type).lower()+'_'
			a_filename = a_filename.replace('.xyz','').replace(suffix,'')
			dummy_atom_position, dummy_atom_index = a_filename.split('_')
			dummy_atom_position, dummy_atom_index = int(dummy_atom_position), int(dummy_atom_index)
			number_difference = dummy_atom_index - dummy_atom_position
			within_path_to   = str(adsorbate)+'/'+str(site_type)
			if isinstance(sites,str):
				make_folder(Part_B_folder,Part_C_folder,within_path_from,within_path_to,all_sites_to_copy,False)
			else:
				for folder_name, indices in all_sites_to_copy.items():
					new_within_path_to = within_path_to+'/'+str(folder_name)
					make_folder(Part_B_folder,Part_C_folder,within_path_from,new_within_path_to,indices,True)
	print()
	print('Completed copying selected xyz files')
	print('From: '+str(Part_B_folder))
	print('To: '+str(Part_C_folder))
	print('=======================================')