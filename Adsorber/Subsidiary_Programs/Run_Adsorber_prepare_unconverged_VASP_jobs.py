#!/usr/bin/env python3
'''
Geoffrey Weal, Run_Adsorber_prepare_unconverged_VASP_jobs.py, 21/08/2021

This program is designed to prepare unconvverged VASP jobs for resubmission. 

'''
import os
from ase.io import read, write
from shutil import copyfile

from Adsorber.Subsidiary_Programs.convergence_methods import determine_convergence_of_output

submission_folder_name = 'Submission_Folder'
def prepare_VASP_files_for_resubmission(path_to_VASP_files):
	dirname = os.path.basename(os.path.normpath(path_to_VASP_files))
	if dirname.startswith(submission_folder_name):
		return
	####################################################################################
	# get the name of the submission_folder
	run_folders = [] 
	for things in os.listdir(path_to_VASP_files):
		if os.path.isdir(path_to_VASP_files+'/'+things) and things.startswith(submission_folder_name):
			things = int(things.replace(submission_folder_name+'_',''))
			run_folders.append(things)
	if len(run_folders) > 0:
		greatest_number = max(run_folders)
		next_folder_number = greatest_number+1
	else:
		next_folder_number = 1
	next_submission_folder_name = submission_folder_name+'_'+str(next_folder_number)
	os.makedirs(path_to_VASP_files+'/'+next_submission_folder_name)
	####################################################################################
	# copy over files to backup
	files_to_copy = ['INCAR','KPOINTS','OUTCAR','POSCAR','submit.sl']
	for file in os.listdir(path_to_VASP_files):
		if not os.path.isfile(path_to_VASP_files+'/'+file):
			continue
		if (file in files_to_copy) or ('slurm-' in file):
			copyfile(path_to_VASP_files+'/'+file,path_to_VASP_files+'/'+next_submission_folder_name+'/'+file)
	####################################################################################
	# change last OUTCAR image to current POSCAR
	path_to_previous_POSCAR = path_to_VASP_files+'/POSCAR'
	if os.path.exists(path_to_previous_POSCAR):
		os.remove(path_to_previous_POSCAR)
	last_OUTCAR_image = read(path_to_VASP_files+'/OUTCAR')
	write(path_to_VASP_files+'/'+'POSCAR',last_OUTCAR_image)
	####################################################################################
	# Remove files
	files_to_delete = ['CHG','CHGCAR','CONTCAR','DOSCAR','EIGENVAL','IBZKPT','OSZICAR','PCDAT','OUTCAR','PCDAT','REPORT','vasprun.xml','WAVECAR','XDATCAR']
	for file in os.listdir(path_to_VASP_files):
		if not os.path.isfile(path_to_VASP_files+'/'+file):
			continue
		if (file in files_to_delete) or ('slurm-' in file):
			os.remove(path_to_VASP_files+'/'+file)

print('==============================================')
print('The following VASP jobs DID NOT CONVERGE and HAVE BEEN PREPARED TO BE RESUMED (i.e. resubmitted to VASP)')
#print('Processed VASP files: ')
OUTCAR_file = 'OUTCAR'
for root, dirs, files in os.walk('.'):
	for index in range(len(dirs)-1,-1,-1):
		dirname = dirs[index]
		if dirname.startswith(submission_folder_name):
			del dirs[index]

	if OUTCAR_file in files:
		path_to_output = root+'/'+OUTCAR_file
		converged = determine_convergence_of_output(path_to_output)
		jobname = os.path.basename(os.path.normpath(root))
		if not converged:
			print(jobname)
			prepare_VASP_files_for_resubmission(root)

