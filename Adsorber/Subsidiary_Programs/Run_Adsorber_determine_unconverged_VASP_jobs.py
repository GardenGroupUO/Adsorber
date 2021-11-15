#!/usr/bin/env python3
'''
Geoffrey Weal, Run_Adsorber_determine_converged_VASP_jobs.py, 21/08/2021

This program is designed to indicate which VASP jobs have converged or not

'''
import os, sys
from Adsorber.Subsidiary_Programs.Part_D_Methods import determine_convergence_of_output

if len(sys.argv) == 2:
	write_job_directory = bool(sys.argv[1])
else:
	write_job_directory = True

print('==============================================')
print('Currently processes VASP Jobs: Determining which jobs have converged or not.')
#print('Processed VASP files: ')
OUTCAR_file = 'OUTCAR'
submission_folder_name = 'Submission_Folder'
Did_converged = []
Did_not_converge = []
for root, dirs, files in os.walk(os.getcwd()):
	if submission_folder_name in root:
		dirs[:] = []
		files[:] = []
		continue
	for index in range(len(dirs)-1,-1,-1):
		dirname = dirs[index]
		if dirname.startswith(submission_folder_name):
			del dirs[index]
	if OUTCAR_file in files:
		path_to_output = root #+'/'+OUTCAR_file
		converged = determine_convergence_of_output(path_to_output)
		jobname = os.path.basename(os.path.normpath(root))
		job_details = jobname
		if write_job_directory:
			job_details += ' ('+path_to_output+')'
		if converged:
			Did_converged.append(job_details)
		else:
			Did_not_converge.append(job_details)

Did_converged.sort()
Did_not_converge.sort()

print('==============================================')
if (len(Did_converged)+len(Did_not_converge)) > 0:
	if len(Did_converged) > 0:
		print('The following VASP jobs CONVERGED')
		for VASP_job in Did_converged:
			print(VASP_job)
	else:
		print('No jobs found had converged')
	print('==============================================')
	if len(Did_not_converge) > 0:
		print('The following VASP jobs DID NOT CONVERGE')
		for VASP_job in Did_not_converge:
			print(VASP_job)
	else:
		print('All jobs found had converged')
else:
	print('No jobs were found in this directory and subdirectories')
print('==============================================')