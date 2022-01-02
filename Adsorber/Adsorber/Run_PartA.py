
class CLICommand:
    """Adsorber will create VASP files for the system and adsorbates, as well as any other molecules you would like to optimise using VASP. The system should be optimised with VASP, as well as any other adsorbates or molecules that will help you with your calculations.
    """

    @staticmethod
    def add_arguments(parser):
    	pass
        #parser.add_argument('filename', nargs='*', help='Name of file to determine format for.')

    @staticmethod
    def run(args):
        Run_PartA()

import os
import numpy as np
from shutil import copyfile

from ase import Atom
from ase.io import write

from Adsorber.Adsorber.import_settings import import_general_settings, import_adsorbate_settings, import_PartA_settings
from Adsorber.Adsorber.program_information import introductory_remarks, finish_up
from Adsorber.Adsorber.general_methods import make_folder, get_system, return_vector
from Adsorber.Adsorber.make_VASP_files_methods import make_overall_potcar, make_individual_submitSL_files

def Run_PartA():
	"""
	Adsorber will create VASP files for the system and adsorbates, as well as any other molecules you would like to optimise using VASP. 

	The system should be optimised with VASP, as well as any other adsorbates or molecules that will help you with your calculations.

	"""
	# Introduction
	introductory_remarks()
	# Get input varables from scripts
	cluster_or_surface_model, system_filename, name_without_suffix, add_vacuum, vasp_files_folder, systems_to_convert_for_VASP_name = import_general_settings()
	adsorbed_species = import_adsorbate_settings()
	slurm_information_system, other_molecules_to_obtain_VASP_energies_for, slurm_information_adsorbates_and_other, part_A_folder_name = import_PartA_settings()
	cluster = get_system(system_filename,add_vacuum=add_vacuum,save_vacuum_system=True)
	save_adsorbates(adsorbed_species)
	save_adsorbates_with_rotation_axis(adsorbed_species)
	# Run program
	print('=================================')
	print('Adsorber will create VASP files of your system as well as molecules you want to adsorb to your system.')
	print('No adsorbed modelled are created yet. That happens in Part B.')
	print('=================================')
	Part_A_make_VASP_files_of_system_and_molecules(part_A_folder_name, cluster, adsorbed_species, other_molecules_to_obtain_VASP_energies_for, vasp_files_folder, slurm_information_system, slurm_information_adsorbates_and_other)
	print('=================================')
	print('Finished creating VASP files of your system and adsorbates.')
	print('Perform VASP optimisations of these.')
	print('=================================')
	# Finish program
	finish_up()

# ============================================================================================
# Input programs, save the adsorbate files.
def save_adsorbates(adsorbed_species):
	adsorbates = []
	for an_adsorbed_species in adsorbed_species:
		adsorbate = an_adsorbed_species['molecule'].copy()
		adsorbates.append(adsorbate)
	write('adsorbates.traj',adsorbates)

def save_adsorbates_with_rotation_axis(adsorbed_species):
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

# ============================================================================================
# Main Part A programs
def Part_A_make_VASP_files_of_system_and_molecules(part_A_folder_name, cluster, adsorbed_species, other_molecules_to_obtain_VASP_energies_for, vasp_files_folder, slurm_information_system, slurm_information_adsorbates_and_other):
	"""
	Part A main program: Runs all the methods required to make VASP files of your system, adsorbates, and other molecules
	"""
	# will create VASP files of the system
	make_VASP_files_of_only_system(part_A_folder_name, cluster, vasp_files_folder, slurm_information_system)
	print('=================================')
	# will create VASP files of all adsorbates
	make_VASP_files_of_only_adsorbates(part_A_folder_name, adsorbed_species, vasp_files_folder, slurm_information_adsorbates_and_other, 'adsorbates')
	print('=================================')
	# will create VASP files of all molecules that you want energies for but dont want to adsorb to your system (cluster/surface model)
	make_VASP_files_of_only_adsorbates(part_A_folder_name, other_molecules_to_obtain_VASP_energies_for, vasp_files_folder, slurm_information_adsorbates_and_other, 'molecules')

def make_VASP_files_of_only_system(part_A_folder_name, cluster, vasp_files_folder, slurm_information_system):
	"""
	Make VASP files of your system
	"""
	print('Make VASP files for System')
	name = 'system'
	path_name = part_A_folder_name+'/'+name
	make_VASP_files_of_species(path_name,cluster,vasp_files_folder,name,slurm_information_system)

def make_VASP_files_of_only_adsorbates(part_A_folder_name, adsorbed_species, vasp_files_folder, slurm_information_adsorbates_and_other,to_print):
	"""
	Make VASP files of your adsorbate
	"""
	print('Make VASP files for '+str(to_print))
	for an_adsorbed_species in adsorbed_species:
		name = an_adsorbed_species['name']
		adsorbate = an_adsorbed_species['molecule']
		path_name = part_A_folder_name+'/'+name
		make_VASP_files_of_species(path_name,adsorbate,vasp_files_folder,name,slurm_information_adsorbates_and_other)

def make_VASP_files_of_species(path_name,chemical,vasp_files_folder,name,slurm_information):
	"""
	Make VASP files of the system, adosrbate, or molecule you want to write files of
	"""
	print('Making VASP files for '+str(name))
	make_folder(path_name)
	write(path_name+'/POSCAR',chemical)
	# This for loop copies all the VASP files in VASP_Files into each folder with a POSCAR
	for vasp_file in os.listdir(vasp_files_folder):
		if not vasp_file == 'POTCARs':
			copyfile(vasp_files_folder+'/'+vasp_file,path_name+'/'+vasp_file)
	#os.chmod(path_name, 0o0777)
	# Make POTCAR for the system
	make_overall_potcar(path_name,vasp_files_folder)
	# Make submit.sl file
	make_individual_submitSL_files(path_name,name,slurm_information)