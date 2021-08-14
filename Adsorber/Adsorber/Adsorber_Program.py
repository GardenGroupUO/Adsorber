import os, shutil
import numpy as np

from ase import Atom, Atoms
from ase.io import write

from Adsorber.Adsorber.import_settings_into_adsorber import import_settings
from Adsorber.Adsorber.neighbour_list import get_neighbour_list_for_surface_atoms
from Adsorber.Adsorber.get_places_to_bind_to import get_above_atom_sites, get_bridge_sites, get_three_fold_sites, get_four_fold_sites
from Adsorber.Adsorber.adsorb_single_species_to_cluster import adsorb_single_species_to_cluster, no_adsorbed_species_to_cluster
from Adsorber.Adsorber.storage_file import write_data_file, load_data_file
from Adsorber.Adsorber.Create_VASP_Files import make_VASP_folders
from Adsorber import __version__

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

	def __init__(self,system_name,cluster_or_surface_model,cutoff,surface_atoms,adsorbed_species,slurm_information={},force_create_systems=False):
		import_settings(self,system_name,cluster_or_surface_model,cutoff,surface_atoms,adsorbed_species,slurm_information,force_create_systems)
		self.introductory_remarks()
		#self.check_for_cluster_folder(self.system_folder_name)
		self.run()

	# ------------------------------------------------------------------------------------------------------------------------------------------------------

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

	'''
	def check_for_cluster_folder(self,system_folder_name):
		print('=========================================================================================================')
		print('You already have a folder called '+str(system_folder_name))
		print('As it is likely you may remove some of the models from this folder as you decide which models to sample, Adsorber will not run any further.')
		print('If you want to run Adsorber, change the current '+str(system_folder_name)+' folder to a different name.')
		print('Adsorber will finish without starting.')
		print('=========================================================================================================')
		exit()
	'''

	# ------------------------------------------------------------------------------------------------------------------------------------------------------

	def run(self):
		self.set_up_cluster(self.cluster,self.surface_atoms,self.name_without_suffix)
		self.save_adsorbates(self.adsorbed_species)
		def make_systems():
			print('=================================')
			print('Adsorber will create systems with adsorbed atoms and molecules.')
			print('=================================')
			self.run_first_Adsorber_run()
		def make_VASP_systems():
			print('=================================')
			print('Adsorber has already created systems with adsorbed atoms and molecules and you have selected systems that you want to run (These are in the "'+str(self.systems_to_convert_for_VASP_name)+'" folder).')
			print('Adsorber will attempt to create VASP directories of systems with adsorbed molecules from the '+str(self.systems_to_convert_for_VASP_name)+' folder')
			print('=================================')
			self.make_VASP_files()
			print('=================================')
		if self.force_create_systems:
			make_systems()
		elif os.path.exists(self.systems_to_convert_for_VASP_name):
			make_VASP_systems()
		elif not os.path.exists(self.system_folder_name):
			make_systems()
		else:
			print('=================================')
			print('You have run this program once before as you have a "'+str(self.system_folder_name)+'" folder, but you do not have a "'+str(self.systems_to_convert_for_VASP_name)+'" folder that contains the system you want converted into VASP files.')
			print('You need to create a folder called "'+str(self.systems_to_convert_for_VASP_name)+'" and place the versions of your system with adsorbed adatoms into it from the "'+str(self.system_folder_name)+'" folder')
			print('This program will stop here without running.')
			print('=================================')
			exit()

	def make_VASP_files(self):
		if self.slurm_information == {}:
			print('No information give for slurm_information')
			print('VASP files of systems with adsorbed molecules will not be created until a information about the submit.sl files are given in the slurm_information variable.')
			print('Adsorber will finish without making VASP files of systems with adsorbed molecules.')
			exit()
		make_VASP_folders(self.cluster,self.adsorbed_species,look_through_folder=self.systems_to_convert_for_VASP_name,vasp_files_folder=self.vasp_files_folder,folder_name=self.VASP_folder_name,slurm_information=self.slurm_information)

	def run_first_Adsorber_run(self):
		# Just the original system
		no_adsorbed_species_to_cluster(self.cluster, self.system_folder_name)
		# original system + adsorbate
		above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites = self.get_initial_adatom_placements(self.cluster,self.cutoff,self.distance_of_adatom_from_surface,self.surface_atoms)
		what_to_adsorb = []
		what_to_adsorb.append((above_atom_binding_sites,'Above_Atom_Site','Make Clusters/Surfaces with adatoms/admolecules attached above atom sites'))
		what_to_adsorb.append((above_bridge_binding_sites,'Above_Bridge_Site','Make Clusters/Surfaces with adatoms/admolecules attached above bridge sites'))
		what_to_adsorb.append((above_three_fold_sites,'Above_Three_Fold_Site','Make Clusters/Surfaces with adatoms/admolecules attached above three-fold sites'))
		what_to_adsorb.append((above_four_fold_sites,'Above_Four_Fold_Site','Make Clusters/Surfaces with adatoms/admolecules attached above four-fold sites'))
		print('============================================================================================')
		for binding_sites, binding_sites_name, to_print in what_to_adsorb:
			print(to_print)
			self.adsorb_species_to_cluster(self.cluster,binding_sites,self.adsorbed_species,binding_sites_name,self.system_folder_name)
		print('============================================================================================')
		# create the folder for xyz files to make VASP files of
		def ig_f(dir, files):
			return [f for f in files if os.path.isfile(os.path.join(dir, f))]
		shutil.copytree(self.system_folder_name, self.systems_to_convert_for_VASP_name, ignore=ig_f)
		# copy original system to xyz folder to make VASP files of.
		path_name = self.system_folder_name+'/Original_System'
		dest_name = self.systems_to_convert_for_VASP_name+'/Original_System'
		shutil.copytree(path_name, dest_name)

	def set_up_cluster(self,cluster,surface_atoms,name_without_suffix):
		cluster.set_tags(0)
		for surface_atom_index in surface_atoms:
			cluster[surface_atom_index].tag = 1
		write(name_without_suffix+'_tagged_surface_atoms.xyz',cluster)

	def save_adsorbates(self,adsorbed_species):
		adsorbates = []
		for an_adsorbed_species in adsorbed_species:
			adsorbate = an_adsorbed_species['molecule'].copy()
			adsorbates.append(adsorbate)
		write('adsorbates.traj',adsorbates)

	def get_initial_adatom_placements(self,cluster,cutoff,distance_of_adatom_from_surface,surface_atoms):
		if not os.path.exists(self.data_storage_file):
			print('============================================================================================')
			print('Getting Binding data')
			neighbour_list = get_neighbour_list_for_surface_atoms(cluster,surface_atoms,cutoff)
			print('Getting above atoms binding sites.')
			above_atom_binding_sites = get_above_atom_sites(cluster,surface_atoms,distance_of_adatom_from_surface,self.cluster_or_surface_model)
			print('Getting above bridge binding sites.')
			above_bridge_binding_sites = get_bridge_sites(cluster,neighbour_list,distance_of_adatom_from_surface,self.cluster_or_surface_model)
			print('Getting above three-fold binding sites.')
			above_three_fold_sites = get_three_fold_sites(cluster,neighbour_list,distance_of_adatom_from_surface,self.cluster_or_surface_model)
			print('Getting above four-fold binding sites.')
			above_four_fold_sites = get_four_fold_sites(cluster,neighbour_list,distance_of_adatom_from_surface,self.cluster_or_surface_model)
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
			for binding_position, surface_position in above_atom_binding_sites:
				binding_representative_atom = Atom('H',position=binding_position,charge=counter,tag=2)
				representative_cluster.append(binding_representative_atom)
				counter += 1
			write(cluster_file_name+'.xyz',representative_cluster)
		make_full_binding_site_representative_cluster(cluster,above_atom_binding_sites,self.name_without_suffix  +'_above_atom_binding_sites')
		make_full_binding_site_representative_cluster(cluster,above_bridge_binding_sites,self.name_without_suffix+'_above_bridge_binding_sites')
		make_full_binding_site_representative_cluster(cluster,above_three_fold_sites,self.name_without_suffix    +'_above_three_fold_sites')
		make_full_binding_site_representative_cluster(cluster,above_four_fold_sites,self.name_without_suffix     +'_above_four_fold_sites')
		return above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites

	def adsorb_species_to_cluster(self,cluster,binding_site_data,adsorbed_species,binding_sites_name,system_folder_name):
		for an_adsorbed_species in adsorbed_species:
			for index in range(len(binding_site_data)):
				binding_site_datum = binding_site_data[index]
				adsorb_single_species_to_cluster(cluster, binding_site_datum, an_adsorbed_species, binding_sites_name, index+1, system_folder_name)

	# ------------------------------------------------------------------------------------------------------------------------------------------------------
