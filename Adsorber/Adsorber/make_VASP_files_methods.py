import os

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

# ===========================================================

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

# ===========================================================

def check_VASP_files(vasp_files_folder,elements):
    """
    Will check the VASP_files folder to make sure everything is in order
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

# ===========================================================