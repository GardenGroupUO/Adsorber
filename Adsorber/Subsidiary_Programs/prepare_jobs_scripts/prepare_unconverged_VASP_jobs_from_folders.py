'''
Geoffrey Weal, Run_Adsorber_prepare_unconverged_VASP_jobs_from_folders.py, 21/08/2021

 

'''

import os

def prepare_unconverged_VASP_jobs_from_folders(files_with_VASP_calcs, OUTCAR_file, submission_folder_name):
	paths_to_VASP_job_to_prepare = []
	for initial_VASP_folder in files_with_VASP_calcs:
		for root, dirs, files in os.walk(initial_VASP_folder):
			if submission_folder_name in root:
				dirs[:] = []
				files[:] = []
				continue
			for index in range(len(dirs)-1,-1,-1):
				dirname = dirs[index]
				if dirname.startswith(submission_folder_name):
					del dirs[index]
			if OUTCAR_file in files:
				paths_to_VASP_job_to_prepare.append(root)

	paths_to_VASP_job_to_prepare.sort()
	return paths_to_VASP_job_to_prepare
