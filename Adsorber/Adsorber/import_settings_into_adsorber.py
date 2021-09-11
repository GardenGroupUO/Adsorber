from ase.io import read

def get_system(system_filename):
	cluster = read(system_filename)
	cluster.set_velocities(cluster.get_velocities())
	cluster.set_pbc(False)
	return cluster

def import_settings(self,part_to_perform,cluster_or_surface_model,system_filename,path_to_VASP_optimised_non_adsorbate_system,cutoff,surface_atoms,adsorbed_species,slurm_information,Other_molecules_to_obtain_VASP_energies_for):
	# ===========================================================================================
	# Determine which Part of Adsorber you want to perform
	self.part_to_perform = part_to_perform
	# General data about the cluster
	self.vasp_files_folder = 'VASP_Files'
	self.surface_atoms = sorted(surface_atoms)
	self.system_filename = system_filename
	self.name_without_suffix = '.'.join(self.system_filename.split('.')[:-1:])
	self.systems_to_convert_for_VASP_name = 'Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files'
	# ===========================================================================================
	# Data for Parts A, B and C.
	if self.part_to_perform == 'Part A':
		# Settings for Part A
		self.Other_molecules_to_obtain_VASP_energies_for = Other_molecules_to_obtain_VASP_energies_for
		# Other settings
		self.cluster = get_system(self.system_filename)
		self.part_A_folder_name = 'Part_A_Non_Adsorbed_Files_For_VASP'
	elif self.part_to_perform == 'Part B':
		# Settings for Part B
		self.path_to_VASP_optimised_non_adsorbate_system = path_to_VASP_optimised_non_adsorbate_system
		# Other settings
		self.cluster = get_system(self.path_to_VASP_optimised_non_adsorbate_system)
		import_cutoff_setting(self,cutoff)
		self.data_storage_file = 'adsorber_data.txt'
		self.system_folder_name = 'Part_B_All_Systems_with_Adsorbed_Species'
		check_saving_binding_sites(adsorbed_species)
	elif self.part_to_perform == 'Part C':
		# Settings for Part C
		self.VASP_folder_name = 'Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP' 
		self.part_c_force_create_original_POSCAR = False # part_c_force_create_original_POSCAR
		# Other settings
		self.path_to_VASP_optimised_non_adsorbate_system = path_to_VASP_optimised_non_adsorbate_system
		self.cluster = get_system(self.path_to_VASP_optimised_non_adsorbate_system)
	else:
		print('=================================')
		print('Error in Adsorber: You have not specified which part of Adsorber you want to perform')
		print('')
		print('You need to set the part_to_perform variable in your Run_Adsorber.py script to either:')
		print('* Part A: ')
		print('* Part B: ')
		print('* Part C: ')
		print('You have set part_to_perform = '+str(self.part_to_perform))
		parts_to_choose = ['Part A', 'Part B', 'Part C']
		print('Set part_to_perform to either: '+str(parts_to_choose))
		print('This program will stop here without running.')
		print('=================================')
		exit()
	import_cluster_or_surface_model_setting(self,cluster_or_surface_model)
	# ===========================================================================================
	# information about the atoms and molecules that will be adsorbed, as well sa their binding sites
	self.distance_of_dummy_adatom_from_surface = 1.1 # Angstroms #vdw_radii[atomic_numbers[self.cluster[0].symbol]] + vdw_radii[atomic_numbers['H']]
	self.adsorbed_species = adsorbed_species
	self.bind_site_data_types = ['top sites','bridge sites','three-fold sites','four-fold sites']
	self.slurm_information = slurm_information
	# ===========================================================================================

def import_cluster_or_surface_model_setting(self,cluster_or_surface_model):
	if not isinstance(cluster_or_surface_model,str):
		print('Error in Adsorber')
		print('The "cluster_or_surface_model" variable must be a string')
		print('"cluster_or_surface_model" = '+str(cluster_or_surface_model))
		print('Check this out. The Adsorber program will finish without completing')
		exit()
	elif cluster_or_surface_model.lower() in ['cluster','surface model']:
		self.cluster_or_surface_model = cluster_or_surface_model
	else:
		print('Error in Adsorber')
		print('The "cluster_or_surface_model" variable must be either "cluster" or "surface model"')
		print('"cluster_or_surface_model" = '+str(cluster_or_surface_model))
		print('Check this out. The Adsorber program will finish without completing')
		exit()

def import_cutoff_setting(self,cutoff):
	surface_atom_symbols = list(set([self.cluster[index].symbol for index in self.surface_atoms]))
	self.cutoff = {}
	if isinstance(cutoff,float):
		for element1 in surface_atom_symbols:
			for element2 in surface_atom_symbols:
				self.cutoff[(element1, element2)] = cutoff
	elif isinstance(cutoff,dict):
		issues = []
		for element in surface_atom_symbols:
			if not element in self.cutoff.keys():
				issues.append(element)
		for index1 in range(len(surface_atom_symbols)):
			element1 = surface_atom_symbols[index1]
			for index2 in range(index1+1,len(surface_atom_symbols)):
				element2 = surface_atom_symbols[index2]
				if (not (element1, element2) in self.cutoff.keys()) or (not (element2, element1) in self.cutoff.keys()):
					issues.append((element1, element2))
		if len(issues) == 0:
			for key, value in cutoff.items():
				if isinstance(key,str):
					self.cutoff[(key,key)] = value
				elif isinstance(key,tuple) and len(key) == 2:
					element1, element2 = key
					self.cutoff[(element1, element2)] = value
					self.cutoff[(element2, element1)] = value
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

all_binding_sites = ['Top_Sites','Bridge_Sites','Three_Fold_Sites','Four_Fold_Sites']
def check_saving_binding_sites(adsorbed_species):
	for adsorbed_speciee in adsorbed_species:
		if 'sites_to_bind_adsorbate_to' in adsorbed_speciee:
			if isinstance(adsorbed_speciee['sites_to_bind_adsorbate_to'],str):
				adsorbed_speciee['sites_to_bind_adsorbate_to'] = [adsorbed_speciee['sites_to_bind_adsorbate_to']]
			if not isinstance(adsorbed_speciee['sites_to_bind_adsorbate_to'],list):
				print('Error importing adsorbed_species into Adsorber for adsorbate: '+str(adsorbed_speciee['name']))
				print('Your entry for "sites_to_bind_adsorbate_to" must be a list')
				print('"sites_to_bind_adsorbate_to": '+str(adsorbed_speciee['sites_to_bind_adsorbate_to']))
				print('Check this out. Adsorber will finishing without beginning.')
				exit()
			adsorbed_speciee['sites_to_bind_adsorbate_to'] = list(set(adsorbed_speciee['sites_to_bind_adsorbate_to']))
			for adsorbed_speciee_binding_site in adsorbed_speciee['sites_to_bind_adsorbate_to']:
				if not adsorbed_speciee_binding_site in all_binding_sites:
					print('Error importing adsorbed_species into Adsorber for adsorbate: '+str(adsorbed_speciee['name']))
					print('Your entry for "sites_to_bind_adsorbate_to" is: '+str(adsorbed_speciee['sites_to_bind_adsorbate_to']))
					print('The entries can only include: '+str(all_binding_sites))
					print('Check this out. Adsorber will finishing without beginning.')
					exit()
		else:
			adsorbed_speciee['sites_to_bind_adsorbate_to'] = all_binding_sites
