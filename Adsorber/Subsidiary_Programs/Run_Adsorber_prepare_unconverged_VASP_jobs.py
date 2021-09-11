'''
Geoffrey Weal, Run_Adsorber_prepare_unconverged_VASP_jobs.py, 21/08/2021

This program is designed to prepare unconvverged VASP jobs for resubmission. 

'''
import os
from ase.io import read, write
from shutil import copyfile

from Adsorber.Subsidiary_Programs.Part_D_Methods import determine_convergence_of_output

class Run_Adsorber_prepare_unconverged_VASP_jobs:

	def __init__(self,files_with_VASP_calcs = ['Part_A_Non_Adsorbed_Files_For_VASP','Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP'],options={'energies_from_lowest_energy': float('inf')}):

		self.files_with_VASP_calcs = files_with_VASP_calcs
		self.options = options
		
		self.OUTCAR_file = 'OUTCAR'
		self.submission_folder_name = 'Submission_Folder'
		
		self.run()

	def run(self):
		
		print('==============================================')
		print('The following VASP jobs DID NOT CONVERGE and HAVE BEEN PREPARED TO BE RESUMED (i.e. resubmitted to VASP)')
		resubmitted_VASP_jobs_that_had_issues = []
		for initial_VASP_folder in self.files_with_VASP_calcs:
			for root, dirs, files in os.walk(initial_VASP_folder):
				if self.submission_folder_name in root:
					dirs[:] = []
					files[:] = []
					continue
				for index in range(len(dirs)-1,-1,-1):
					dirname = dirs[index]
					if dirname.startswith(self.submission_folder_name):
						del dirs[index]
				if self.OUTCAR_file in files:
					path_to_output = root #+'/'+self.OUTCAR_file
					converged = determine_convergence_of_output(path_to_output)
					if not converged:
						print(root)
						could_OUTCAR_CONTCAR_be_loaded = self.prepare_VASP_files_for_resubmission(root)
						if (could_OUTCAR_CONTCAR_be_loaded is not None) and (could_OUTCAR_CONTCAR_be_loaded == False):
							jobname = os.path.basename(os.path.normpath(root))
							resubmitted_VASP_jobs_that_had_issues.append((jobname,root))
		print('==============================================')
		if len(resubmitted_VASP_jobs_that_had_issues) > 0:
			print('The following VASP jobs had issues with either/both the OUTCAR and CONTCAR files.')
			print('These VASP jobs have been prepared for resubmission with the original POSCAR.')
			print('The old files have been placed in submission folders and marked with "Issue"')
			for VASP_job_name, VASP_job_path in resubmitted_VASP_jobs_that_had_issues:
				print(str(VASP_job_name)+' ('+str(VASP_job_path)+')')
			print('==============================================')

	def get_greatest_folder_number(self,overall_path,folder_name_suffix):
		run_folders = [int(things.replace(folder_name_suffix+'_','')) for things in os.listdir(overall_path) if (os.path.isdir(overall_path+'/'+things) and things.startswith(folder_name_suffix))]
		if len(run_folders) > 0:
			greatest_number = max(run_folders)
			next_folder_number = greatest_number+1
		else:
			next_folder_number = 1
		return next_folder_number

	def prepare_VASP_files_for_resubmission(self,path_to_VASP_files):
		dirname = os.path.basename(os.path.normpath(path_to_VASP_files))
		if dirname.startswith(self.submission_folder_name):
			return None
		####################################################################################
		# get the name of the submission_folder
		next_folder_number = self.get_greatest_folder_number(path_to_VASP_files,self.submission_folder_name)
		next_submission_folder_name = self.submission_folder_name+'_'+str(next_folder_number)
		os.makedirs(path_to_VASP_files+'/'+next_submission_folder_name)
		####################################################################################
		# copy over files to backup
		files_to_copy = ['CONTCAR','INCAR','KPOINTS','OUTCAR','POSCAR','submit.sl']
		for file in os.listdir(path_to_VASP_files):
			if not os.path.isfile(path_to_VASP_files+'/'+file):
				continue
			if (file in files_to_copy) or ('slurm-' in file):
				copyfile(path_to_VASP_files+'/'+file,path_to_VASP_files+'/'+next_submission_folder_name+'/'+file)
		####################################################################################
		# change last OUTCAR image to current POSCAR
		try:
			last_image = read(path_to_VASP_files+'/OUTCAR')
		except Exception:
			try:
				last_image = read(path_to_VASP_files+'/CONTCAR')
			except Exception:
				last_image = None
		path_to_previous_POSCAR = path_to_VASP_files+'/POSCAR'
		could_OUTCAR_CONTCAR_be_loaded = last_image is not None
		if could_OUTCAR_CONTCAR_be_loaded:
			if os.path.exists(path_to_previous_POSCAR):
				os.remove(path_to_previous_POSCAR)
			write(path_to_VASP_files+'/'+'POSCAR',last_OUTCAR_image)
		else:
			issue_folder_name = next_submission_folder_name+'_Issue'
			next_issue_folder_number = self.get_greatest_folder_number(path_to_VASP_files,issue_folder_name)
			next_issue_folder_name = issue_folder_name+'_'+str(next_issue_folder_number)
			os.rename(path_to_VASP_files+'/'+next_submission_folder_name, path_to_VASP_files+'/'+next_issue_folder_name)
		####################################################################################
		# Remove files
		files_to_delete = ['CHG','CHGCAR','CONTCAR','DOSCAR','EIGENVAL','fe.dat','IBZKPT','OSZICAR','OUTCAR','PCDAT','REPORT','vaspout.eps','vasprun.xml','WAVECAR','XDATCAR']
		for file in os.listdir(path_to_VASP_files):
			if not os.path.isfile(path_to_VASP_files+'/'+file):
				continue
			if (file in files_to_delete) or ('slurm-' in file):
				os.remove(path_to_VASP_files+'/'+file)
		return could_OUTCAR_CONTCAR_be_loaded