'''
Geoffrey Weal, Run_Adsorber_prepare_unconverged_VASP_jobs.py, 21/08/2021

This program is designed to prepare unconvverged VASP jobs for resubmission. 

'''

import os

from Adsorber.Subsidiary_Programs.prepare_jobs_scripts.prepare_unconverged_VASP_jobs_from_folders  import prepare_unconverged_VASP_jobs_from_folders
from Adsorber.Subsidiary_Programs.prepare_jobs_scripts.prepare_unconverged_VASP_jobs_from_textfile import prepare_unconverged_VASP_jobs_from_textfile

from tqdm import tqdm
from Adsorber.Subsidiary_Programs.prepare_jobs_scripts.prepare_unconverged_VASP_jobs_methods import already_reset, copy_files_from_VASP_files_folder, prepare_VASP_files_for_resubmission
from Adsorber.Subsidiary_Programs.Part_D_Methods import determine_convergence_of_output
from Adsorber.Adsorber.Part_C_Create_adsorbed_VASP_Files import make_individual_submitSL_files

class Run_Adsorber_prepare_unconverged_VASP_jobs:

	def __init__(self,prepare_jobs_switch,main_information,slurm_information,force_prepare=False,update_VASP_files=False):

		self.prepare_jobs_switch = prepare_jobs_switch
		self.force_prepare = force_prepare
		self.update_VASP_files = update_VASP_files

		information_required_for = {'folder': ['files_with_VASP_calcs', 'options'], 'text': ['path_to_resubmission_list_file']}

		# -------------------------------------------------------------------------------------------------------------------------------

		for key in information_required_for.keys():
			if self.prepare_jobs_switch == key:
				information_to_look_for = information_required_for[self.prepare_jobs_switch]
				check_if_not_exists = [(not does_exist in main_information) for does_exist in information_to_look_for]
				if any(check_if_not_exists):
					print('Problem with Run_Adsorber_prepare_unconverged_VASP_jobs.py')
					print('You are missing main_information in the main_information dictionary that is required to run this program with prepare_jobs_switch = '+str(self.prepare_jobs_switch))
					print('This missing main_information is: ')
					for index in range(len(check_if_not_exists)):
						is_not_there = check_if_not_exists[index]
						if is_not_there:
							print('\t* '+str(information_to_look_for[index]))
					print()
					print("You have given main_information = "+str(main_information))
					print('Check this out. This program will stop without having begun')
					exit()
				break
		else:
			print('Problem with Run_Adsorber_prepare_unconverged_VASP_jobs.py')
			print('You have not entered a valid input for prepare_jobs_switch')
			print('The prepare_jobs_switch variable can either be: ')
			print("\t* 'folder': Prepare jobs that are found in a folder and it's subfolders.")
			print("\t* 'text': Prepare jobs that are given in a text file.")
			print()
			print("You have set prepare_jobs_switch = "+str(self.prepare_jobs_switch))
			print('Check this out. This program will stop without having begun')
			exit()

		# -------------------------------------------------------------------------------------------------------------------------------

		self.Run_AdsorberPY_name = 'Run_Adsorber.py'

		# -------------------------------------------------------------------------------------------------------------------------------

		if self.prepare_jobs_switch == 'folder':
			self.files_with_VASP_calcs = main_information['files_with_VASP_calcs']
			self.options = main_information['options']
		elif self.prepare_jobs_switch == 'text':
			self.path_to_resubmission_list_file = main_information['path_to_resubmission_list_file']
			self.vasp_files_folder = 'VASP_Files'
		
		self.OUTCAR_file = 'OUTCAR'
		self.submission_folder_name = 'Submission_Folder'
		self.slurm_information = slurm_information
		
		print('------------------------------------------------------------')
		print('Collecting path to VASP jobs for resubmission')
		if self.prepare_jobs_switch == 'folder':
			self.paths_to_VASP_job_to_prepare = prepare_unconverged_VASP_jobs_from_folders(self.files_with_VASP_calcs, self.OUTCAR_file, self.submission_folder_name)
		elif self.prepare_jobs_switch == 'text':
			self.paths_to_VASP_job_to_prepare = prepare_unconverged_VASP_jobs_from_textfile(self.path_to_resubmission_list_file, self.OUTCAR_file, self.submission_folder_name)
		print('Finished collecting path to VASP jobs for resubmission')
		print('------------------------------------------------------------')
		#for test in self.paths_to_VASP_job_to_prepare:
			#print(test)
		print('Preparing VASP jobs for resubmission')
		self.prepare_VASP_jobs()
		print('Finished preparing VASP jobs for resubmission')
		print('------------------------------------------------------------')

		# -------------------------------------------------------------------------------------------------------------------------------

	def prepare_VASP_jobs(self):
		resubmitted_VASP_jobs_that_had_issues = []
		pbar = tqdm(self.paths_to_VASP_job_to_prepare)
		for path_to_output in pbar:
			pbar.set_description('')
			if already_reset(path_to_output):
				continue
			converged = determine_convergence_of_output(path_to_output)
			if self.force_prepare or not converged:
				jobname = os.path.basename(os.path.normpath(path_to_output))
				pbar.set_description(jobname)
				could_OUTCAR_CONTCAR_be_loaded = prepare_VASP_files_for_resubmission(path_to_output, self.submission_folder_name)
				# If there was a problem with preparation
				if (could_OUTCAR_CONTCAR_be_loaded is not None) and (could_OUTCAR_CONTCAR_be_loaded == False):
					resubmitted_VASP_jobs_that_had_issues.append((jobname,path_to_output))
				#Copy the VASP files (like INCAR, KPOINTS, etc) from the VASP files folder to this folder.
				if self.update_VASP_files:
					copy_files_from_VASP_files_folder(path_to_output, self.vasp_files_folder)
				# If slurm_information given, update it to that given in script.
				if not self.slurm_information == None:
					make_individual_submitSL_files(path_to_output, jobname, self.slurm_information)
		if len(resubmitted_VASP_jobs_that_had_issues) > 0:
			print('==============================================')
			print('The following VASP jobs had issues with either/both the OUTCAR and CONTCAR files.')
			print('These VASP jobs have been prepared for resubmission with the original POSCAR.')
			print('The old files have been placed in submission folders and marked with "Issue"')
			for VASP_job_name, VASP_job_path in resubmitted_VASP_jobs_that_had_issues:
				print(str(VASP_job_name)+' ('+str(VASP_job_path)+')')
			print('==============================================')
