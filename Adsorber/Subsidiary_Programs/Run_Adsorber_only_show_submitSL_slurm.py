#!/usr/bin/env python3
'''
Geoffrey Weal, Run_Adsorber_submitSL_slurm.py, 16/06/2021

This program is designed to submit all sl files called submit.sl to slurm

'''
print('###########################################################################')
print('###########################################################################')
print('Run_Adsorber_only_show_submitSL_slurm.py')
print('###########################################################################')
print('This program will show you what VASP files will be submitted to slurm by Run_Adsorber_submitSL_slurm.py')
print('This program WILL NOT submit VASP files.')
print('###########################################################################')
print('###########################################################################')

import os

print('*****************************************************************************')
print('The following VASP files will be submitted to slurm by Run_Adsorber_submitSL_slurm.py')
path = os.getcwd()
counter = 0
for (dirpath, dirnames, filenames) in os.walk(path):
    dirnames.sort()
    filenames.sort()
    if 'submit.sl' in filenames:
        if 'OUTCAR' in filenames: # if OUTCAR is found, the VASP files have already been run or are running, so don't want to submit this!
            dirnames[:] = []
            filenames[:] = []
            continue
        name = dirpath.replace(path, '').split('/', -1)[1:]
        name = "_".join(str(x) for x in name)
        counter += 1
        print(str(counter)+": Submit " + str(name) + " to slurm "+'(Submission .sl file found in: '+str(dirpath)+')')
        dirnames[:] = []
        filenames[:] = []
print('*****************************************************************************')
print('No of VASP files that will be submitted to slurm: '+str(counter))
print('*****************************************************************************')