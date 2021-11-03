'''
Geoffrey Weal, Run_Adsorber_prepare_unconverged_VASP_jobs.py, 21/08/2021



'''

import os

def prepare_unconverged_VASP_jobs_from_textfile(path_to_resubmission_list_file, OUTCAR_file, submission_folder_name):
	vasp_jobs_to_resubmit = []
	with open(path_to_resubmission_list_file,'r') as FILE:
		for line in FILE:
			path = line.rstrip().split()[0]
			if not os.path.exists(path):
				continue
			if submission_folder_name in root:
				dirs[:] = []
				files[:] = []
				continue
			for index in range(len(dirs)-1,-1,-1):
				dirname = dirs[index]
				if dirname.startswith(submission_folder_name):
					del dirs[index]
			#if OUTCAR_file in files:
			#	paths_to_VASP_job_to_prepare.append(root)
			vasp_jobs_to_resubmit.append(path)

	vasp_jobs_to_resubmit.sort()
	return vasp_jobs_to_resubmit
