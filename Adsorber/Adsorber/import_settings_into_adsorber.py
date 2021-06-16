from ase.io import read

def import_settings(self,name,cluster_or_surface_model,cutoff,surface_atoms,adsorbed_species,slurm_information):
	# General data about the cluster
	self.name = name
	self.cluster = read(name)
	import_cluster_or_surface_model_setting(self,cluster_or_surface_model)
	self.name_without_suffix = self.name.split('.')[0]
	# information about the surface of the cluster/surface model
	self.surface_atoms = sorted(surface_atoms)
	import_cutoff_setting(self,cutoff)
	# information about the atoms and molecules that will be adsorbed, as well sa their binding sites
	self.distance_of_adatom_from_surface = 1.25 # Angstroms #vdw_radii[atomic_numbers[self.cluster[0].symbol]] + vdw_radii[atomic_numbers['H']]
	self.adsorbed_species = adsorbed_species
	self.bind_site_data_types = ['above atom sites','above bridge sites','above three-fold sites','above four-fold sites']
	# information about where data from this program is stored
	self.data_storage_file = 'adsorber_data.txt'
	self.system_folder_name = 'System_with_Adsorbed_Species'
	# Information about making VASP file of system with adsorbed species
	self.vasp_files_folder = 'VASP_Files' 
	self.VASP_folder_name = 'System_with_Adsorbed_Species_for_VASP' 
	self.slurm_information = slurm_information

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