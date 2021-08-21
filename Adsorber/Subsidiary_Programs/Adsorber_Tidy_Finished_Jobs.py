#!/usr/bin/env python3
'''
Geoffrey Weal, LatticeFinder_Tidy_Finished_Jobs.py, 30/04/2021

This program is designed to remove the files of jobs that have finished. 

'''
import os
from ase.io import read

files_to_remove = ['CHG','CHGCAR','CONTCAR','DOSCAR','EIGENVAL','fe.dat','IBZKPT','OSZICAR','PCDAT','POTCAR','REPORT','vasprun.xml','vaspout.eps','WAVECAR','XDATCAR','vdw_kernel.bindat'] # 'submit.sl', 'INCAR','KPOINTS','POSCAR',

print('================================================================')
print('Cleaning the following files from completed VASP runs:')
print(files_to_remove)

for root, dirs, files in os.walk("."):
    dirs.sort()
    files.sort()
    if 'OUTCAR' in files:
        try:
            system = read(root+'/'+'OUTCAR')
            system.get_potential_energy()
            system.get_volume()
        except Exception:
            dirs[:] = []
            files[:] = []
            continue
        print(root)
        for file_to_remove in files_to_remove:
            if file_to_remove in files:
                os.remove(root+'/'+file_to_remove)
        '''
        for file in files:
            if file.startswith('slurm-') and file.endswith('.out'):
                os.remove(root+'/'+file)
            elif file.startswith('slurm-') and file.endswith('.err'):
                os.remove(root+'/'+file)
        '''
        dirs[:] = []
        files[:] = []

print('================================================================')