class CLICommand:
    """This command is designed to remove all the unnecessary files from VASP optimisations once you have finished. This is meant to decease the space of your data as well as the filecount. To be used once you are done and dusted.  
    """

    @staticmethod
    def add_arguments(parser):
        pass
        #parser.add_argument('delete_all_unnecessary_files', nargs='*', help='delete all unnecessary files.')

    @staticmethod
    def run(args):
        Run_method()

import os
from Adsorber.Subsidiary_Programs.prepare_jobs_scripts.prepare_unconverged_VASP_jobs_methods import prepare_VASP_files_for_resubmission

def Run_method():
	path_to_output = os.getcwd()
	submission_folder_name = 'Submission_Folder'
	if os.path.exists(path_to_output+'/POSCAR'):
		could_OUTCAR_CONTCAR_be_loaded = prepare_VASP_files_for_resubmission(path_to_output, submission_folder_name)
		if not could_OUTCAR_CONTCAR_be_loaded:
			print('Error, could not load OUTCAR or CONTCAR')
			return False
		else:
			print('Successfully prepared job for resubmission')
			return True
	else:
		print('Not doing anything, could not find a POSCAR')
		return False