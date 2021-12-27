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
		path_to_output = root
		job_details = [jobname,path_to_output]
		if not (OUTCAR_file in files):
			files_have_not_begun.append(job_details[0])
			continue
		converged = determine_convergence_of_output(path_to_output)
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
		for name, path in Did_converged:
			if write_job_directory:
				print(name+' ('+path+')')
			else:
				print(name)
		print('No of completed jobs: '+str(len(Did_converged)))
	else:
		print('No jobs found had converged')
	print('==============================================')
	if len(Did_not_converge) > 0:
		print('The following VASP jobs DID NOT CONVERGE')
		for name, path in Did_not_converge:
			if write_job_directory:
				print(name+' ('+path+')')
			else:
				print(name)
		print('No of uncompleted jobs: '+str(len(Did_not_converge)))
	else:
		print('All jobs found had converged')
	print('==============================================')
	if len(files_have_not_begun) > 0:
		print('The following VASP jobs HAVE NOT STARTED')
		for VASP_job in files_have_not_begun:
			if write_job_directory:
				print(name+' ('+path+')')
			else:
				print(name)
		print('No of jobs that had not started: '+str(len(files_have_not_begun)))
		print('==============================================')
else:
	print('No jobs were found in this directory and subdirectories')
print('==============================================')

def write_to_TXTfile(did_not_converge):
	#import pdb; pdb.set_trace()
	with open('unconverged_systems.txt','w') as unconverged_systemsTXT:
		for name, path in did_not_converge:
			unconverged_systemsTXT.write(str(path)+'\t'+str(name)+'\n')
write_to_TXTfile(Did_not_converge)