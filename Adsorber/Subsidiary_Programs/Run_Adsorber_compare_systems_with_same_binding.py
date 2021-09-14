#!/usr/bin/env python3
'''
Geoffrey Weal, Run_Adsorber_compare_sytems_with_same_binding.py, 14/09/2021

This program is designed to allow you to look at different VASP jobs with adsorbates in different positions that have converged to similar places.

This program is designed to allow you to see if they have converged to the same place. 

'''
import os
from ase.io import read, write

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def make_dir(save_folder_name):
	if not os.path.exists(save_folder_name):
		os.makedirs(save_folder_name)

System_Adsorbate_VASP_Jobs_folder_name = 'Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP'
if not System_Adsorbate_VASP_Jobs_folder_name in os.listdir('.'):
    print('Error: Could not find the folder: '+str(System_Adsorbate_VASP_Jobs_folder_name))
    print('You need to execute Run_Adsorber_determine_unconverged_VASP_jobs.py in the same place as your '+System_Adsorbate_VASP_Jobs_folder_name+' folder is.')
    print('This program will finish without beginning.')
    exit()

Run_AdsorberPY_name = 'Run_Adsorber.py'
if not Run_AdsorberPY_name in os.listdir('.'):
    print('Error: Could not find the folder: '+str(Run_AdsorberPY_name))
    print('You need to execute Run_Adsorber_determine_unconverged_VASP_jobs.py in the same place as your '+Run_AdsorberPY_name+' script is.')
    print('This program will finish without beginning.')
    exit()

save_folder_name = 'Part_D_Results_Folder'    
excel_name = "Part_D_Information_on_VASP_Calculations.xlsx"
workbook = load_workbook(save_folder_name+'/'+excel_name)

sheetnames = workbook.sheetnames
if 'Originals' in sheetnames:
	sheetnames.remove('Originals')

def get_key_name(key):
	key_split = key.replace(' ','_')
	key_split = key_split.rstrip().split('(,')
	for index in range(len(key_split)):
		key_split_part = key_split[index].replace('[','')
		key_split_part = key_split_part.replace(']','')
		key_split_part = key_split_part.replace('(','')
		key_split_part = key_split_part.replace(')','')
		key_split_part = key_split_part.replace('->','to')
		key_split[index] = key_split_part.replace(',','+')
	key_name = '__'.join(key_split)
	return key_name

similar_systems_name = 'Similar_Systems'
saving_suffix_path = save_folder_name+'/'+similar_systems_name
for sheetname in sheetnames:
	sheet = workbook[sheetname]
	print(sheetname)
	similar_systems = {}
	for row_index in range(2,sheet.max_row+1):
		job_name = sheet.cell(row=row_index, column=3).value
		job_path = sheet.cell(row=row_index, column=4).value
		energy = sheet.cell(row=row_index, column=11).value
		binding_surface_atoms = sheet.cell(row=row_index, column=15).value
		similar_systems.setdefault(binding_surface_atoms,[]).append((energy,job_name,job_path))
	for key in sorted(similar_systems.keys()):
		if len(similar_systems[key]) > 1:
			similar_systems[key].sort()
			key_name = get_key_name(key)
			saving_path = saving_suffix_path+'/'+sheetname+'/'+key_name
			print(key_name)
			make_dir(saving_path)
			file = open(saving_path+'/similar_systems.txt','w')
			file.write('name\tenergy (eV)')
			all_outcar_files = []
			for energy, job_name, job_path in similar_systems[key]:
				try:
					final_image = read(job_path+'/OUTCAR')
				except Exception as ee:
					try:
						final_image = read(job_path+'/CONTCAR')
					except Exception as ef:
						raise ef
				write(saving_path+'/'+job_name+'.xyz',final_image)
				all_outcar_files.append(final_image)
				file.write(job_name+'\t'+str(round(float(energy.replace('=','')),5)))
			write(saving_path+'/'+key_name+'.traj',all_outcar_files)
