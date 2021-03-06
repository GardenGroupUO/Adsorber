class CLICommand:
    """Will determine which jobs have converged or not based on your INCAR input.
    """

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('write_job_directory', nargs='*', help='Write the paths and other information of the VASP jobs that have not yet converged. Asnwer can be either True or False. Default: True.')

    @staticmethod
    def run(args):
        Run_method(args)

def Run_method(args_method):
	'''
	Geoffrey Weal, Run_Adsorber_determine_converged_VASP_jobs.py, 21/08/2021

	This program is designed to indicate which VASP jobs have converged or not

	'''
	import os
	from Adsorber.Adsorber.Part_D_Methods import determine_convergence_of_output

	true_statements = ['true','t']
	false_statements = ['false','f']
	args_method_write_job_directory = args_method.write_job_directory
	if len(args_method.write_job_directory) == 1:
		if args_method_write_job_directory[0].lower() in true_statements+false_statements:
			if args_method_write_job_directory[0].lower() in true_statements:
				write_job_directory = True
			else:
				write_job_directory = False
		else:
			print('Error: Input for "check_unconverged" must be either True ("T","t","TRUE","True","true") or False ("F","f","FALSE","False","false")')
			print('Check your input, which is: '+str(args_method_write_job_directory[0]))
			exit('Check this. This program will close without starting.')
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
	Did_not_converge_but_repeat_did = []
	Did_not_converge = []
	Did_not_converge_and_repeat_did_not_converge = []
	files_have_not_begun = []
	for root, dirs, files in os.walk(os.getcwd()):
		if ('_repeat' in root):
			dirs[:] = []
			files[:] = []
			continue
		if (submission_folder_name in root):
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
				files_have_not_begun.append(job_details)
				continue
			converged = determine_convergence_of_output(path_to_output)
			repeat_converged = None
			all_repeat_paths_to_output = []
			if not converged:
				counter = 1
				repeat_path_to_output = path_to_output+'_repeat'
				current_repeat_path_to_output = repeat_path_to_output
				while os.path.exists(current_repeat_path_to_output):
					repeat_converged = determine_convergence_of_output(current_repeat_path_to_output)
					if repeat_converged:
						break
					all_repeat_paths_to_output.append(current_repeat_path_to_output)
					counter += 1
					current_repeat_path_to_output = repeat_path_to_output+'_'+str(counter)
			if converged:
				Did_converged.append(job_details)
			elif (not converged) and repeat_converged:
				Did_not_converge_but_repeat_did.append(job_details+[current_repeat_path_to_output])
			elif (not converged) and (repeat_converged is None):
				Did_not_converge.append(job_details)
			elif (not converged) and (not repeat_converged):
				Did_not_converge_and_repeat_did_not_converge.append(job_details+[all_repeat_paths_to_output])
			else:
				exit('huh how did you get here? Debug this using import pdb; pdb.set_trace()')

	Did_converged.sort()
	Did_not_converge_but_repeat_did.sort()
	Did_not_converge.sort()
	Did_not_converge_and_repeat_did_not_converge.sort()
	files_have_not_begun.sort()

	print('==============================================')
	if (len(Did_converged)+len(Did_not_converge_but_repeat_did)+len(Did_not_converge)+len(Did_not_converge_and_repeat_did_not_converge)+len(files_have_not_begun)) > 0:
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
		if len(Did_not_converge_but_repeat_did) > 0:
			print("The following VASP jobs DID NOT CONVERGE BUT IT'S REPEAT DID CONVERGE")
			for name, path, repeat_path_to_output in Did_not_converge_but_repeat_did:
				if write_job_directory:
					print(name+' ('+repeat_path_to_output+')')
				else:
					print(name)
			print('No of completed repeated jobs: '+str(len(Did_not_converge_but_repeat_did)))
		else:
			print('All jobs found had converged')
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
		if len(Did_not_converge_and_repeat_did_not_converge) > 0:
			print('The following VASP jobs DID NOT CONVERGE AND ITS REPEAT(S) HAS(VE) NOT CONGERVED')
			for name, path, all_repeat_paths_to_output in Did_not_converge_and_repeat_did_not_converge:
				if write_job_directory:
					print(name+' ('+path+')')
					for repeated_path in all_repeat_paths_to_output:
						print(' --> ('+repeated_path+')')
				else:
					print(name)
			print('No of uncompleted jobs: '+str(len(Did_not_converge_and_repeat_did_not_converge)))
		else:
			print('All jobs found had converged')
		print('==============================================')
		if len(files_have_not_begun) > 0:
			print('The following VASP jobs HAVE NOT STARTED')
			for name, path in files_have_not_begun:
				if write_job_directory:
					print(name+' ('+path+')')
				else:
					print(name)
			print('No of jobs that had not started: '+str(len(files_have_not_begun)))
			print('==============================================')
	else:
		print('No jobs were found in this directory and subdirectories')
	print('==============================================')

	def write_to_TXTfile(did_not_converge,Did_not_converge_and_repeat_did_not_converge):
		with open('unconverged_systems.txt','w') as unconverged_systemsTXT:
			for name, path in did_not_converge:
				unconverged_systemsTXT.write(str(path)+'\t'+str(name)+'\n')
			if len(Did_not_converge_and_repeat_did_not_converge) > 0:
				unconverged_systemsTXT.write('\n')
				for name, path, all_repeat_paths_to_output in Did_not_converge_and_repeat_did_not_converge:
					unconverged_systemsTXT.write(str(path)+'\t'+str(name)+'\n')
					for counter in range(len(all_repeat_paths_to_output)):
						unconverged_systemsTXT.write(str(path)+'\t'+str(name)+'_repeat_'+str(counter)+'\n')
	write_to_TXTfile(Did_not_converge,Did_not_converge_and_repeat_did_not_converge)