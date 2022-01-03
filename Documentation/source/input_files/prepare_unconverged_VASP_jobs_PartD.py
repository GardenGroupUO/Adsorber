from Adsorber import Run_Adsorber_prepare_unconverged_VASP_jobs

# If you want to resubmit certain adsorbate+systems given in a text file. 
# There are two ways you can do this, as a single path or a list of paths 
# Example 1. Single path
path_to_resubmission_list_file = 'Part_D_Results_Folder/Similar_Systems_COH_extra.txt'
# Example 1. List of paths
path_to_resubmission_list_file = []
for system in ['C','CH','CH2','CH3','CH2O','CH2OH','CH3O','CHOH','O','OH']:
        path_to_resubmission_list_file.append('Part_D_Results_Folder/Similar_Systems_'+str(system)+'.txt')

# A switch that determines what type of resubmnission scheme you would like to perform
prepare_jobs_switch = 'text' # 'folder' # text
# Information required to prepare jobs
main_information = {'path_to_resubmission_list_file': path_to_resubmission_list_file}

# if you would like to prepare jobs even if they have already converged, change this to True
force_prepare = True # MAKE SURE THIS IS SET TO TRUE
# If you want to also update the VASP files while performing this task
update_VASP_files = True # MAKE SURE THIS IS SET TO TRUE

slurm_information = {}
slurm_information['project'] = 'uoo02568'
slurm_information['partition'] = 'large'
slurm_information['time'] = '72:00:00'
slurm_information['nodes'] = 1
slurm_information['ntasks_per_node'] = 12
slurm_information['mem-per-cpu'] = '1200MB'
slurm_information['email'] = 'geoffreywealslurmnotifications@gmail.com'
slurm_information['vasp_version'] = 'VASP/5.3.5-intel-2017a-VTST-BEEF'
slurm_information['vasp_execution'] = 'vasp_cd'

Run_Adsorber_prepare_unconverged_VASP_jobs(prepare_jobs_switch,main_information=main_information,slurm_information=slurm_information,force_prepare=force_prepare,update_VASP_files=update_VASP_files)
