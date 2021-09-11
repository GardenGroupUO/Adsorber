import os, shutil
import numpy as np

from ase import Atom
from ase.io import write

from Adsorber import __version__
from Adsorber.Adsorber.import_settings_into_adsorber import import_settings
# Imports for Part A
from Adsorber.Adsorber.Part_A_Create_non_adsorbed_VASP_files import make_VASP_files_of_only_system, make_VASP_files_of_only_adsorbates
# Imports for Part B
from Adsorber.Adsorber.Part_B_neighbour_list import get_neighbour_list_for_surface_atoms
from Adsorber.Adsorber.Part_B_get_places_to_bind_to import get_above_atom_sites, get_bridge_sites, get_three_fold_sites, get_four_fold_sites
from Adsorber.Adsorber.Part_B_adsorb_single_species_to_cluster import adsorb_single_species_to_cluster, return_vector
from Adsorber.Adsorber.Part_B_storage_file import write_data_file, load_data_file
# Imports for Part C
from Adsorber.Adsorber.Part_C_Create_adsorbed_VASP_Files import make_VASP_folders

def get_version_number():
	version = __version__
	return version

def version_no():
	"""
	Will provide the version of the Adsorber program
	"""
	version = get_version_number() 
	return version

class Adsorber_Program:

	def __init__(self,part_to_perform,cluster_or_surface_model,system_filename,path_to_VASP_optimised_non_adsorbate_system,cutoff,surface_atoms,adsorbed_species,slurm_information={},Other_molecules_to_obtain_VASP_energies_for=[]):
		import_settings(self,part_to_perform,cluster_or_surface_model,system_filename,path_to_VASP_optimised_non_adsorbate_system,cutoff,surface_atoms,adsorbed_species,slurm_information,Other_molecules_to_obtain_VASP_energies_for)
		self.introductory_remarks()
		#self.check_for_cluster_folder(self.system_folder_name)
		self.run()

	def introductory_remarks(self):
		print('=================================')
		print()
		print('            Adsorber             ')
		print()
		print('         Version: '+str(version_no()))
		print()
		print('=================================')
		print()
		print()
		print()

	def run(self):
		self.save_adsorbates(self.adsorbed_species)
		self.save_adsorbates_with_rotation_axis(self.adsorbed_species)
		# ============================
		if self.part_to_perform == 'Part A':
			print('=================================')
			print('Adsorber will create VASP files of your system as well as molecules you want to adsorb to your system.')
			print('No adsorbed modelled are created yet. That happens in Part B.')
			print('=================================')
			self.Part_A_make_VASP_files_of_system_and_molecules()
			print('=================================')
			print('Finished creating VASP files of your system and adsorbates.')
			print('Perform VASP optimisations of these.')
			print('=================================')
		elif self.part_to_perform == 'Part B':
			self.set_up_cluster(self.cluster,self.surface_atoms)
			print('=================================')
			print('Adsorber will create systems with adsorbed atoms and molecules.')
			print('=================================')
			self.Part_B_make_adsorbed_xyz_files()
		elif self.part_to_perform == 'Part C':
			#self.set_up_cluster(self.cluster,self.surface_atoms)
			print('=================================')
			print('Adsorber has already created systems with adsorbed atoms and molecules and you have selected systems that you want to run (These are in the "'+str(self.systems_to_convert_for_VASP_name)+'" folder).')
			print('Adsorber will attempt to create VASP directories of systems with adsorbed molecules from the '+str(self.systems_to_convert_for_VASP_name)+' folder')
			print('=================================')
			self.Part_C_make_VASP_files()
			print('=================================')
		else:
			print('=================================')
			print('Error in Adsorber: You have not specified which part of Adsorber you want to perform')
			print('This program will stop here without running.')
			print('=================================')
			exit()

	# ==================================================================================================

	def set_up_cluster(self,cluster,surface_atoms):
		write(self.name_without_suffix+'_after_VASP_Opt.xyz',cluster)
		cluster.set_tags(0)
		for surface_atom_index in surface_atoms:
			cluster[surface_atom_index].tag = 1
		write(self.name_without_suffix+'_after_VASP_Opt_tagged_surface_atoms.xyz',cluster)

	def save_adsorbates(self,adsorbed_species):
		adsorbates = []
		for an_adsorbed_species in adsorbed_species:
			adsorbate = an_adsorbed_species['molecule'].copy()
			adsorbates.append(adsorbate)
		write('adsorbates.traj',adsorbates)

	def save_adsorbates_with_rotation_axis(self,adsorbed_species):
		adsorbates = []
		for an_adsorbed_species in adsorbed_species:
			adsorbate = an_adsorbed_species['molecule'].copy()
			if len(adsorbate) > 1:
				central_atom_index = an_adsorbed_species['index']
				centre_of_atom_position = adsorbate[central_atom_index].position
				rotation_axis_vector = np.array(return_vector(an_adsorbed_species['axis']))
				for number in np.arange(0.2,3.1,0.2):
					adsorbate.append(Atom('X',position=centre_of_atom_position + number*rotation_axis_vector))
			adsorbates.append(adsorbate)
		write('adsorbates_with_rotation_axis.traj',adsorbates)

	# ==================================================================================================

	def Part_A_make_VASP_files_of_system_and_molecules(self):
		# will create VASP files of the system
		make_VASP_files_of_only_system(self.part_A_folder_name, self.cluster, self.vasp_files_folder, self.slurm_information)
		# will create VASP files of all adsorbates
		make_VASP_files_of_only_adsorbates(self.part_A_folder_name, self.adsorbed_species, self.vasp_files_folder, self.slurm_information)
		# will create VASP files of all molecules that you want energies for but dont want to adsorb to your system (cluster/surface model)
		make_VASP_files_of_only_adsorbates(self.part_A_folder_name, self.Other_molecules_to_obtain_VASP_energies_for, self.vasp_files_folder, self.slurm_information)

	# ==================================================================================================

	def Part_B_make_adsorbed_xyz_files(self):
		# original system + adsorbate
		above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites = self.get_initial_adatom_placements(self.cluster,self.cutoff,self.distance_of_dummy_adatom_from_surface,self.surface_atoms)
		what_to_adsorb = []
		initial_sentence = 'Make System with adsorbates attached upon '
		what_to_adsorb.append((above_atom_binding_sites,'Top_Sites',initial_sentence+'top sites'))
		what_to_adsorb.append((above_bridge_binding_sites,'Bridge_Sites',initial_sentence+'bridge sites'))
		what_to_adsorb.append((above_three_fold_sites,'Three_Fold_Sites',initial_sentence+'three-fold sites'))
		what_to_adsorb.append((above_four_fold_sites,'Four_Fold_Sites',initial_sentence+'four-fold sites'))
		print('============================================================================================')
		for binding_sites, binding_sites_name, to_print in what_to_adsorb:
			print(to_print)
			self.adsorb_species_to_cluster(self.cluster,self.surface_atoms,binding_sites,self.cutoff,self.adsorbed_species,binding_sites_name,self.system_folder_name)
		print('============================================================================================')
		# create the folder for xyz files to make VASP files of
		def ig_f(dir, files):
			return [f for f in files if os.path.isfile(os.path.join(dir, f))]
		if not os.path.exists(self.systems_to_convert_for_VASP_name):
			shutil.copytree(self.system_folder_name, self.systems_to_convert_for_VASP_name, ignore=ig_f)
		'''
		# copy original system to xyz folder to make VASP files of.\
		# Change in how things are done, this can likely be removed
		path_name = self.system_folder_name+'/Original_System'
		dest_name = self.systems_to_convert_for_VASP_name+'/Original_System'
		shutil.copytree(path_name, dest_name)
		'''

	def get_initial_adatom_placements(self,cluster,cutoff,distance_of_dummy_adatom_from_surface,surface_atoms):
		if not os.path.exists(self.data_storage_file):
			print('============================================================================================')
			print('Getting Binding data')
			neighbour_list = get_neighbour_list_for_surface_atoms(cluster,surface_atoms,cutoff)
			print('Getting top binding sites.')
			above_atom_binding_sites = get_above_atom_sites(cluster,surface_atoms,distance_of_dummy_adatom_from_surface,self.cluster_or_surface_model)
			print('Getting bridging binding sites.')
			above_bridge_binding_sites = get_bridge_sites(cluster,neighbour_list,distance_of_dummy_adatom_from_surface,self.cluster_or_surface_model)
			print('Getting three-fold binding sites.')
			above_three_fold_sites = get_three_fold_sites(cluster,neighbour_list,distance_of_dummy_adatom_from_surface,self.cluster_or_surface_model)
			print('Getting four-fold binding sites.')
			above_four_fold_sites = get_four_fold_sites(cluster,neighbour_list,distance_of_dummy_adatom_from_surface,self.cluster_or_surface_model)
			print('Saving data to '+str(self.data_storage_file))
			write_data_file(self.data_storage_file,self.bind_site_data_types,above_atom_binding_sites,above_bridge_binding_sites,above_three_fold_sites,above_four_fold_sites)
			print('============================================================================================')
		else:
			print('============================================================================================')
			print('Loading data from '+str(self.data_storage_file))
			above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites = load_data_file(self.data_storage_file,self.bind_site_data_types)
			print('============================================================================================')
		def make_full_binding_site_representative_cluster(cluster,above_atom_binding_sites,cluster_file_name):
			representative_cluster = cluster.copy()
			counter = 1
			for binding_position, surface_position, indices_of_atoms_involved in above_atom_binding_sites:
				binding_representative_atom = Atom('H',position=binding_position,charge=counter,tag=2) # These could be symbolised as H or X
				representative_cluster.append(binding_representative_atom)
				counter += 1
			write(cluster_file_name+'.xyz',representative_cluster)

		representative_cluster_folder_name = 'Part_B_Binding_Site_Locations'
		if not os.path.exists(representative_cluster_folder_name):
			os.makedirs(representative_cluster_folder_name)
		prefix_name = representative_cluster_folder_name+'/'+self.name_without_suffix
		make_full_binding_site_representative_cluster(cluster,above_atom_binding_sites,prefix_name  +'_top_sites')
		make_full_binding_site_representative_cluster(cluster,above_bridge_binding_sites,prefix_name+'_bridging_sites')
		make_full_binding_site_representative_cluster(cluster,above_three_fold_sites,prefix_name    +'_three_fold_sites')
		make_full_binding_site_representative_cluster(cluster,above_four_fold_sites,prefix_name     +'_four_fold_sites')
		return above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites

	def adsorb_species_to_cluster(self,cluster,surface_atoms,binding_site_data,cutoff,adsorbed_species,binding_sites_name,system_folder_name):
		for an_adsorbed_species in adsorbed_species:
			if binding_sites_name in an_adsorbed_species['sites_to_bind_adsorbate_to']:
				print('Adsorbate Name: '+str(an_adsorbed_species['name']))
				for index in range(len(binding_site_data)):
					binding_site_datum = binding_site_data[index]
					adsorb_single_species_to_cluster(cluster, surface_atoms, binding_site_datum, cutoff, an_adsorbed_species, binding_sites_name, index+1, system_folder_name)
			else:
				print('Adsorbate Name: '+str(an_adsorbed_species['name'])+' --> Will not gather '+binding_sites_name.lower().replace('_',' ')+' models as specified in your Run_Adsorber.py script.')

	# ==================================================================================================

	def Part_C_make_VASP_files(self):
		if self.slurm_information == {}:
			print('No information give for slurm_information')
			print('VASP files of systems with adsorbed molecules will not be created until a information about the submit.sl files are given in the slurm_information variable.')
			print('Adsorber will finish without making VASP files of systems with adsorbed molecules.')
			exit()
		make_VASP_folders(self.cluster,self.adsorbed_species,look_through_folder=self.systems_to_convert_for_VASP_name,vasp_files_folder=self.vasp_files_folder,folder_name=self.VASP_folder_name,slurm_information=self.slurm_information,part_c_force_create_original_POSCAR=self.part_c_force_create_original_POSCAR)

	# ==================================================================================================