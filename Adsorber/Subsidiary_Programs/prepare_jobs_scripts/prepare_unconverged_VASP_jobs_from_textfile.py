'''
Geoffrey Weal, Run_Adsorber_prepare_unconverged_VASP_jobs.py, 21/08/2021



'''

import os

def read_resubmission_list_file(path_to_resubmission_list_file):
	vasp_jobs_to_resubmit = []
	with open(path_to_resubmission_list_file,'r') as FILE:
		for line in FILE:
			if (not line.strip()) or (line.startswith('#')):
				continue
			path = line.rstrip().split()[0]
			#import pdb; pdb.set_trace()
			if not os.path.exists(path):
				print('Error: The following does not exist: '+str(path))
				continue
			vasp_jobs_to_resubmit.append(path)
	return vasp_jobs_to_resubmit

def prepare_unconverged_VASP_jobs_from_textfile(path_to_resubmission_list_file, OUTCAR_file, submission_folder_name):
	vasp_jobs_to_resubmit = []
	if isinstance(path_to_resubmission_list_file,str):
		vasp_jobs_to_resubmit += read_resubmission_list_file(path_to_resubmission_list_file)
	elif isinstance(path_to_resubmission_list_file,list) or isinstance(path_to_resubmission_list_file,tuple):
		for a_path_to_resubmission_list_file in path_to_resubmission_list_file:
			vasp_jobs_to_resubmit += read_resubmission_list_file(a_path_to_resubmission_list_file)
	else:
		print('Error: path_to_resubmission_list_file must be given as a string, list, or tuple')
		print('type(path_to_resubmission_list_file) = '+str(type(path_to_resubmission_list_file)))
		print('path_to_resubmission_list_file = '+str(path_to_resubmission_list_file))
		print('Check this out and try this again')
		exit('This program will finish without starting.')
	vasp_jobs_to_resubmit.sort()
	return vasp_jobs_to_resubmit
