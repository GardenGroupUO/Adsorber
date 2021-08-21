#!/usr/bin/env python3
'''
Geoffrey Weal, Run_Adsorber_determine_converged_VASP_jobs.py, 21/08/2021

This program is designed to indicate which VASP jobs have converged or not

'''
import os
from Adsorber.Subsidiary_Programs.convergence_methods import determine_convergence_of_output

print('==============================================')
print('Currently processes VASP Jobs: Determining if they have converged or not')
#print('Processed VASP files: ')
OUTCAR_file = 'OUTCAR'
Did_converged = []
Did_not_converge = []
for root, dirs, files in os.walk('.'):
	if OUTCAR_file in files:
		path_to_output = root+'/'+OUTCAR_file
		converged = determine_convergence_of_output(path_to_output)
		jobname = os.path.basename(os.path.normpath(root))
        #print(jobname)
		if converged:
			Did_converged.append(jobname)
		else:
			Did_not_converge.append(jobname)

print('==============================================')
print('The following VASP jobs CONVERGED')
for VASP_job in Did_converged:
	print(VASP_job)
print('==============================================')
print('The following VASP jobs DID NOT CONVERGE')
for VASP_job in Did_not_converge:
	print(VASP_job)
print('==============================================')