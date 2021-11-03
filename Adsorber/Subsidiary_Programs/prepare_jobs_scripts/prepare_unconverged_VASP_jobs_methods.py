'''
Geoffrey Weal, Run_Adsorber_prepare_unconverged_VASP_jobs_methods.py, 21/08/2021

 

'''

import os
from ase.io import read, write
from shutil import copyfile


def prepare_VASP_files_for_resubmission(path_to_VASP_files, submission_folder_name):
	dirname = os.path.basename(os.path.normpath(path_to_VASP_files))
	if dirname.startswith(submission_folder_name):
		return None
	####################################################################################
	# get the name of the submission_folder
	next_folder_number = get_greatest_folder_number(path_to_VASP_files,submission_folder_name)
	next_submission_folder_name = submission_folder_name+'_'+str(next_folder_number)
	os.makedirs(path_to_VASP_files+'/'+next_submission_folder_name)
	####################################################################################
	# copy over files to backup
	files_to_copy = ['CONTCAR','INCAR','KPOINTS','OUTCAR','POSCAR','submit.sl']
	for file in os.listdir(path_to_VASP_files):
		if not os.path.isfile(path_to_VASP_files+'/'+file):
			continue
		if (file in files_to_copy) or ('slurm-' in file):
			copyfile(path_to_VASP_files+'/'+file,path_to_VASP_files+'/'+next_submission_folder_name+'/'+file)
	####################################################################################
	# change last OUTCAR image to current POSCAR
	try:
		last_image = read(path_to_VASP_files+'/OUTCAR')
	except Exception:
		try:
			last_image = read(path_to_VASP_files+'/CONTCAR')
		except Exception:
			last_image = None
	path_to_previous_POSCAR = path_to_VASP_files+'/POSCAR'
	could_OUTCAR_CONTCAR_be_loaded = last_image is not None
	if could_OUTCAR_CONTCAR_be_loaded:
		if os.path.exists(path_to_previous_POSCAR):
			os.remove(path_to_previous_POSCAR)
		write(path_to_VASP_files+'/'+'POSCAR',last_image)
	else:
		issue_folder_name = next_submission_folder_name+'_Issue'
		next_issue_folder_number = get_greatest_folder_number(path_to_VASP_files,issue_folder_name)
		next_issue_folder_name = issue_folder_name+'_'+str(next_issue_folder_number)
		os.rename(path_to_VASP_files+'/'+next_submission_folder_name, path_to_VASP_files+'/'+next_issue_folder_name)
	####################################################################################
	# Remove files
	files_to_delete = ['CHG','CHGCAR','CONTCAR','DOSCAR','EIGENVAL','fe.dat','IBZKPT','OSZICAR','OUTCAR','PCDAT','REPORT','vaspout.eps','vasprun.xml','WAVECAR','XDATCAR']
	for file in os.listdir(path_to_VASP_files):
		if not os.path.isfile(path_to_VASP_files+'/'+file):
			continue
		if (file in files_to_delete) or ('slurm-' in file):
			os.remove(path_to_VASP_files+'/'+file)
	return could_OUTCAR_CONTCAR_be_loaded


def get_greatest_folder_number(overall_path,folder_name_suffix):
	run_folders = [int(things.replace(folder_name_suffix+'_','')) for things in os.listdir(overall_path) if (os.path.isdir(overall_path+'/'+things) and things.startswith(folder_name_suffix))]
	if len(run_folders) > 0:
		greatest_number = max(run_folders)
		next_folder_number = greatest_number+1
	else:
		next_folder_number = 1
	return next_folder_number

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def copy_files_from_VASP_files_folder(path_to_VASP_job, vasp_files_folder):
	for vasp_file in os.listdir(vasp_files_folder):
		if not vasp_file == 'POTCARs':
			copyfile(vasp_files_folder+'/'+vasp_file,path_to_VASP_job+'/'+vasp_file)


def already_reset(path_to_VASP_job):
	list_of_files = [file for file in os.listdir(path_to_VASP_job) if os.path.isfile(path_to_VASP_job+'/'+file)]
	if 'vdw_kernel.bindat' in list_of_files:
		list_of_files.remove('vdw_kernel.bindat')
	has_VASP_job_been_reset = set(list_of_files) == set(['INCAR','KPOINTS','POSCAR','POTCAR','submit.sl'])
	#if has_VASP_job_been_reset == False:
	#	import pdb; pdb.set_trace()
	return has_VASP_job_been_reset