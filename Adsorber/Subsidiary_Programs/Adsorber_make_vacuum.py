#!/usr/bin/env python3
'''
Geoffrey Weal, Adsorber_make_vacuum.py, 17/08/2021

This program will allow the user to place a vacuum about a system

'''

import sys
from ase.io import read, write

if not len(sys.argv) == 3:
	print('Error in Adsorber_make_vacuum.py')
	print('You need execute this program in the terminal as follows:')
	print('Adsorber_make_vacuum.py SYSTEM_NAME VACUUM')
	print('where SYSTEM_NAME is the filename of your system, and VACUUM is the amount of vacuum to place around your system in Angstroms')
	print('Try this again. Program will now finish without starting.')
	exit()

system_name = sys.argv[1]
vacuum = float(sys.argv[2])
system_name_with_vacuum = '.'.join(system_name.split('.')[:-1:])+'_with_vacuum_'+str(vacuum)+'_Ang.xyz'

system = read(system_name)
system.center(vacuum=vacuum)
write(system_name_with_vacuum,system)

print('Have added '+str(vacuum)+' Ang of vacuum to your system.')
print('This means that replicas of your system under periodic boundary conditions should be at least '+str(2.0*vacuum)+' Ang apart from each other.')
print('Your system with vacuum has been saved as: '+str(system_name_with_vacuum))