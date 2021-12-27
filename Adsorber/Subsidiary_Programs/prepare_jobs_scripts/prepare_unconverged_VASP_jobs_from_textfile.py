'''
Geoffrey Weal, Run_Adsorber_prepare_unconverged_VASP_jobs.py, 21/08/2021



'''

import os

def prepare_unconverged_VASP_jobs_from_textfile(path_to_resubmission_list_file, OUTCAR_file, submission_folder_name):
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

	vasp_jobs_to_resubmit.sort()
	return vasp_jobs_to_resubmit
