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
from shutil import copy, copytree

def Run_method():
	path_to_folder = os.getcwd()
	path_to_submission_process = path_to_folder+'/Submission_Folder_1'
	if not os.path.exists(path_to_submission_process):
		print('Error: Could not find the Submission_Folder_1 folder.')
		print('Will finish without beginning')
		return
	repeat_path_to_output = path_to_folder+'_repeat'
	current_repeat_path_to_output = repeat_path_to_output
	counter = 1
	while os.path.exists(current_repeat_path_to_output):
		counter += 1
		current_repeat_path_to_output = repeat_path_to_output+'_'+str(counter)
	print('Repeating new '+str(os.path.basename(path_to_folder))+' as '+str(os.path.basename(current_repeat_path_to_output)))
	path_to_new_repeat = os.path.join(path_to_folder,'..',current_repeat_path_to_output)
	print('Path: '+str(path_to_new_repeat))
	if os.path.exists(path_to_new_repeat):
		print('Error: The above path to the repeat folder already exists.')
		print('Will finish without beginning')
		return
	copytree(path_to_submission_process,path_to_new_repeat)
	for file in ['CONTCAR','OUTCAR']:
		if os.path.exists(path_to_new_repeat+'/'+file):
			os.remove(path_to_new_repeat+'/'+file)
	for file in os.listdir(path_to_new_repeat):
		if file.startswith('slurm-'):
			os.remove(path_to_new_repeat+'/'+file)
	if os.path.exists(path_to_folder+'/POTCAR'):
		copy(path_to_folder+'/POTCAR',path_to_new_repeat+'/POTCAR')
	else:
		print('WARNING: Could not find the POTCAR in '+str(path_to_folder))
		print('Make sure you copy a valid POTCAR before you submit your repeated job, otherwise VASP will not run')
	submit_filename = 'submit.sl'
	old_submit_path = path_to_new_repeat+'/'+submit_filename
	new_submit_path = path_to_new_repeat+'/'+submit_filename+'.tmp'
	with open(new_submit_path,'w') as NEW_SUBMIT:
		with open(old_submit_path,'r') as OLD_SUBMIT:
			for line in OLD_SUBMIT:
				if line.startswith('#SBATCH -J'):
					line = line.rstrip()
					line += '_repeat' + ('' if counter == 1 else ('_'+str(counter)))+'\n'
				NEW_SUBMIT.write(line)
	os.remove(old_submit_path)
	os.rename(new_submit_path,old_submit_path)
	print('Finished copying repeat file')