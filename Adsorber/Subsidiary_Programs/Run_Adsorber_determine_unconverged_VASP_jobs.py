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
submitSL_file = 'submit.sl'
INCAR_file = 'INCAR'
submission_folder_name = 'Submission_Folder'
Did_converged = []
Did_not_converge = []
files_have_not_begun = []
for root, dirs, files in os.walk(os.getcwd()):
	if submission_folder_name in root:
		dirs[:] = []
		files[:] = []
		continue
	for index in range(len(dirs)-1,-1,-1):
		dirname = dirs[index]
		if dirname.startswith(submission_folder_name):
			del dirs[index]
	if (submitSL_file in files) and (INCAR_file in files):
		jobname = os.path.basename(os.path.normpath(root))
		job_details = jobname
		if not (OUTCAR_file in files):
			files_have_not_begun.append(job_details)
			continue
		path_to_output = root #+'/'+OUTCAR_file
		converged = determine_convergence_of_output(path_to_output)
		if write_job_directory:
			job_details += ' ('+path_to_output+')'
		if converged:
			Did_converged.append(job_details)
		else:
			Did_not_converge.append(job_details)

Did_converged.sort()
Did_not_converge.sort()
files_have_not_begun.sort()

print('==============================================')
if (len(Did_converged)+len(Did_not_converge)+len(files_have_not_begun)) > 0:
	print('==============================================')
	if len(Did_converged) > 0:
		print('The following VASP jobs CONVERGED')
		for VASP_job in Did_converged:
			print(VASP_job)
		print('No of completed jobs: '+str(len(Did_converged)))
	else:
		print('No jobs found had converged')
	print('==============================================')
	if len(Did_not_converge) > 0:
		print('The following VASP jobs DID NOT CONVERGE')
		for VASP_job in Did_not_converge:
			print(VASP_job)
		print('No of uncompleted jobs: '+str(len(Did_not_converge)))
	else:
		print('All jobs found had converged')
	print('==============================================')
	if len(files_have_not_begun) > 0:
		print('The following VASP jobs HAVE NOT STARTED')
		for VASP_job in files_have_not_begun:
			print(VASP_job)
		print('No of jobs that had not started: '+str(len(files_have_not_begun)))
		print('==============================================')
else:
	print('No jobs were found in this directory and subdirectories')
print('==============================================')