import os
from shutil import copyfile
from ase.io import write

from Adsorber.Adsorber.other_methods import make_folder
from Adsorber.Adsorber.Part_C_Create_adsorbed_VASP_Files import make_overall_potcar, make_individual_submitSL_files

def make_VASP_files_of_only_system(part_A_folder_name, cluster, vasp_files_folder, slurm_information):
	print('Make VASP files for System')
	name = 'system'
	path_name = part_A_folder_name+'/'+name
	make_VASP_files_of_species(path_name,cluster,vasp_files_folder,name,slurm_information)

def make_VASP_files_of_only_adsorbates(part_A_folder_name, adsorbed_species, vasp_files_folder, slurm_information):
	for an_adsorbed_species in adsorbed_species:
		name = an_adsorbed_species['name']
		adsorbate = an_adsorbed_species['molecule']
		path_name = part_A_folder_name+'/'+name
		make_VASP_files_of_species(path_name,adsorbate,vasp_files_folder,name,slurm_information)

def make_VASP_files_of_species(path_name,chemical,vasp_files_folder,name,slurm_information):
	print('Making VASP files for '+str(name))
	make_folder(path_name)
	write(path_name+'/POSCAR',chemical)
	# This for loop copies all the VASP files in VASP_Files into each folder with a POSCAR
	for vasp_file in os.listdir(vasp_files_folder):
		if not vasp_file == 'POTCARs':
			copyfile(vasp_files_folder+'/'+vasp_file,path_name+'/'+vasp_file)
	# Make POTCAR for the system
	make_overall_potcar(path_name,vasp_files_folder)
	# Make submit.sl file
	make_individual_submitSL_files(path_name,name,slurm_information)
