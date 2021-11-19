import os
from shutil import copyfile
from ase.io import read, write

def make_VASP_folders(system,adsorbed_species,look_through_folder='Selected_Systems_to_Convert_for_VASP_Calcs',vasp_files_folder='VASP_Files',folder_name='Selected_Systems_with_Adsorbed_Species_for_VASP',slurm_information={},part_c_force_create_original_POSCAR=False):
	"""

	"""
	if not os.path.exists(look_through_folder):
		exit('Error: '+str(look_through_folder)+' folder does not exist. You need to manually create this and place desired systems with adsorbed molecules on it to continue. This program will exit without running.')
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
				file_name = file.replace('.xyz','')
				folder_to_save_to = folder_name+root.replace(look_through_folder,'')+'/'+file_name
				# only copy over jobs that have not begun, you dont want to change anyting that is currently running. 
				if os.path.exists(folder_to_save_to+'/OUTCAR'):
					continue
				# begin to make the necessary files
				system = read(root+'/'+file)
				#system, original_positions_of_atoms = system_with_atoms_rearranged_alphabetically(system)
				if not os.path.exists(folder_to_save_to):
					os.makedirs(folder_to_save_to)
				if not os.path.exists(folder_to_save_to+'/POSCAR') or part_c_force_create_original_POSCAR:
					write(folder_to_save_to+'/POSCAR',system)
				# This for loop copies all the VASP files in VASP_Files into each folder with a POSCAR
				for vasp_file in os.listdir(vasp_files_folder):
					if not vasp_file == 'POTCARs':
						copyfile(vasp_files_folder+'/'+vasp_file,folder_to_save_to+'/'+vasp_file)
				# Make POTCAR for each system
				make_overall_potcar(folder_to_save_to,vasp_files_folder)
				# Make submit.sl file
				make_individual_submitSL_files(folder_to_save_to,file_name,slurm_information)
				# This will write a file that records the original position of atoms in the system. 
				# This is because the POSCAR needs to be sorted by atom for the POTCAR. 
				#write_original_positions_of_atoms_to_disk(original_positions_of_atoms,folder_to_save_to)

def system_with_atoms_rearranged_alphabetically(system):
	all_atoms_as_list = []
	for index in range(len(system)):
		atom = system[index]
		all_atoms_as_list.append((atom,index))
	all_atoms_as_list.sort(key=lambda entry:entry[0].symbol)
	system_copy = system.copy()
	while len(system_copy) > 0:
		del system_copy[0]
	original_positions_of_atoms = []
	for atom, index in all_atoms_as_list:
		system_copy.append(atom)
		original_positions_of_atoms.append(index)
	return system_copy, original_positions_of_atoms

def write_original_positions_of_atoms_to_disk(original_positions_of_atoms,folder_to_save_to):
	with open(folder_to_save_to+'/original_positions.txt','w') as original_positionsTXT:
		string_to_enter = ' '.join([str(position) for position in original_positions_of_atoms])
		original_positionsTXT.write(string_to_enter)

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
		no_of_elements = len(elements)
		for index in range(no_of_elements):
			element = elements[index]
			with open(vasp_files_folder+'/POTCARs/POTCAR_'+str(element), "r") as in_POTCAR:
				out_POTCAR.write(in_POTCAR.read())
			if index < no_of_elements-1:
				out_POTCAR.write('\n')


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
	python_version ='Python/3.6.3-gimkl-2017a' # = slurm_information['python_version']
	vasp_version = slurm_information['vasp_version']
	vasp_execution = slurm_information['vasp_execution']
	make_submitSL(file_name,root,project,time,nodes,ntasks_per_node,mem_per_cpu,partition=partition,email=email,python_version=python_version,vasp_version=vasp_version,vasp_execution=vasp_execution)

def make_submitSL(file_name,local_path,project,time,nodes,ntasks_per_node,mem_per_cpu,partition='large',email='',python_version='Python/3.6.3-gimkl-2017a',vasp_version='VASP/5.4.4-intel-2017a',vasp_execution='vasp_std'):
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
        #submitSL.write('module load '+str(python_version)+'\n')
        submitSL.write('\n')
        submitSL.write('#Run VASP job.\n')
        submitSL.write('srun -K '+str(vasp_execution)+'\n')
        #submitSL.write('\n')
        #submitSL.write('# removing files except for OUTCAR as we assume it finished successfully.\n')
        #submitSL.write('Adsorber_Tidy_Finished_Jobs.py')