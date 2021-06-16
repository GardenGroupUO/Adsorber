#!/usr/bin/env python3

import os
from shutil import copyfile
from ase.io import read, write

def make_VASP_folders(system,adsorbed_species,look_through_folder='System_with_Adsorbed_Species',vasp_files_folder='VASP_Files',folder_name='VASP_for_System_with_Adsorbed_Species',slurm_information={}):
	"""

	"""
	elements = get_elements(system,adsorbed_species)
	check_VASP_files(vasp_files_folder,elements)
	if not os.path.exists(folder_name):
		os.makedirs(folder_name)
	for root, dirs, files in os.walk(look_through_folder):
		dirs.sort()
		files.sort()
		for file in files:
			if file.endswith('.xyz'):
				print(root)
				dirs[:] = []
				break
		for file in files:
			if file.endswith('.xyz'):
				system = read(root+'/'+file)
				file_name = file.replace('.xyz','')
				folder_to_save_to = folder_name+root.replace(look_through_folder,'')+'/'+file_name
				if not os.path.exists(folder_to_save_to):
					os.makedirs(folder_to_save_to)
				write(folder_to_save_to+'/POSCAR',system)
				for vasp_file in os.listdir(vasp_files_folder):
					if not vasp_file == 'POTCARs':
						copyfile(vasp_files_folder+'/'+vasp_file,folder_to_save_to+'/'+vasp_file)
				make_overall_potcar(folder_to_save_to,vasp_files_folder)
				make_individual_submitSL_files(folder_to_save_to,file_name,slurm_information)

def get_elements(system,adsorbed_species):
	elements = []
	elements += list(system.get_chemical_symbols())
	for molecule_dict in adsorbed_species:
		elements += list(molecule_dict['molecule'].get_chemical_symbols())
	elements = tuple(set(elements))
	return elements

def make_overall_potcar(folder_to_save_to,vasp_files_folder):
	with open(folder_to_save_to+'/POSCAR') as POSCAR_file:
		elements = POSCAR_file.readline().split()
	with open(folder_to_save_to+'/POTCAR', "w") as out_POTCAR:
		for element in elements:
			with open(vasp_files_folder+'/POTCARs/POTCAR_'+str(element), "r") as in_POTCAR:
				out_POTCAR.write(in_POTCAR.read())

def check_VASP_files(vasp_files_folder,elements):
	"""

	"""
	if not os.path.exists(vasp_files_folder):
		print('Error in copying VASP files to cluster folder')
		print('There is no folder called "VASP_Files" in your working directory.')
		print('This folder is where you should place your VASP files in for DFT local optimisations.')
		print('Make this folder and place your "POTCAR" files for each element in your system and all adsorbed species, INCAR", "KPOINTS" files for VASP local optimisations')
		print('This program will exit without completing.')
		exit()
	VASP_Files_files = os.listdir(vasp_files_folder)
	have_INCAR   = 'INCAR'   in VASP_Files_files
	have_KPOINTS = 'KPOINTS' in VASP_Files_files
	if not (have_INCAR and have_KPOINTS):
		print('Error in copying VASP files to cluster folder')
		print('You need the following files when you are performing VASP calculations:')
		print()
		print('\tINCAR  :\t'  +('You have this' if have_INCAR   else 'You do not have this'))
		print('\tKPOINTS:\t'+('You have this' if have_KPOINTS else 'You do not have this'))
		print()
		print('Check this out. This program will now end without completing.')
		exit()
	potcar_folder_name = 'POTCARs'
	have_POTCARs = (potcar_folder_name in VASP_Files_files) and os.path.isdir(vasp_files_folder+'/'+potcar_folder_name)
	if not have_POTCARs:
		print('Error in copying VASP files to cluster folder')
		print('You need the following folders when you are performing VASP calculations:')
		print()
		print('\tPOTCARs:\t' +('You have this' if have_POTCARs  else 'You do not have this'))
		print()
		print('Check this out. This program will now end without completing.')
		exit()
	not_got_elements = []
	for element in elements:
		if not os.path.exists(vasp_files_folder+'/'+potcar_folder_name+'/'+'POTCAR_'+str(element)):
			not_got_elements.append(element)
	if not len(not_got_elements) == 0:
		print('Error in copying VASP files to cluster folder')
		print('You need to include the following POTCAR files in '+str(potcar_folder_name)+' to perform VASP calculations:')
		print()
		for element in not_got_elements:
			print('POTCAR_'+str(element))
		print()
		print('Check this out. This program will now end without completing.')
		exit()

def make_individual_submitSL_files(root,file_name,slurm_information):
	"""

	"""
	project = slurm_information['project']
	time = slurm_information['time']
	nodes = slurm_information['nodes']
	ntasks_per_node = slurm_information['ntasks_per_node']
	mem_per_cpu = slurm_information['mem-per-cpu']
	partition = slurm_information['partition']
	email = slurm_information['email']
	vasp_version = slurm_information['vasp_version']
	vasp_execution = slurm_information['vasp_execution']
	make_submitSL(file_name,root,project,time,nodes,ntasks_per_node,mem_per_cpu,partition=partition,email=email,vasp_version=vasp_version,vasp_execution=vasp_execution)

def make_submitSL(file_name,local_path,project,time,nodes,ntasks_per_node,mem_per_cpu,partition='large',email='',vasp_version='VASP/5.4.4-intel-2017a',vasp_execution='vasp_std'):
    # create name for job
    #print("creating submit.sl for "+str(file_name))
    name = 'Adsorber_Run_'+str(file_name)
    # writing the submit.sl script
    with open(local_path+"/submit.sl", "w") as submitSL:
        submitSL.write('#!/bin/bash -e\n')
        submitSL.write('#SBATCH -J ' + str(name) + '\n')
        submitSL.write('#SBATCH -A ' + str(project) + '         # Project Account\n')
        submitSL.write('#SBATCH --partition ' + str(partition) + '\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --time=' + str(time) + '     # Walltime\n')
        submitSL.write('#SBATCH --nodes=' + str(nodes) + '\n')
        submitSL.write('#On VASP, Ben Roberts recommends using the same number\n')
        submitSL.write('#of tasks on all nodes, even if this makes scheduling\n')
        submitSL.write('#a little more difficult\n')
        submitSL.write('#SBATCH --ntasks-per-node=' + str(ntasks_per_node) + '\n')
        submitSL.write('#SBATCH --mem-per-cpu=' + str(mem_per_cpu) + '\n')
        submitSL.write('\n')
        #submitSL.write("#SBATCH --hint=nomultithread    # don't use hyperthreading"+'\n')
        submitSL.write('#SBATCH --output=slurm-%j.out      # %x and %j are replaced by job name and ID'+'\n')
        submitSL.write('#SBATCH --error=slurm-%j.err'+'\n')
        if not email == '':
            submitSL.write('#SBATCH --mail-user=' + str(email) + '\n')
            submitSL.write('#SBATCH --mail-type=ALL\n')
        submitSL.write('#SBATCH --hint nomultithread\n')
        submitSL.write('\n')
        submitSL.write('module load '+str(vasp_version)+'\n')
        submitSL.write('srun -K '+str(vasp_execution)+'\n')