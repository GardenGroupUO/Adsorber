from Adsorber import Run_Adsorber_prepare_unconverged_VASP_jobs

# if you want to resubmit all adsorbate+systems that have an energy above the current minimum energy system.
files_with_VASP_calcs = ['Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/CHO']
options = {'energies_from_lowest_energy': float('inf')}

# If you want to resubmit certain adsorbate+systems given in a text file. 
path_to_resubmission_list_file = 'Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/unconverged_systems.txt'

# A switch that determines what type of resubmnission scheme you would like to perform
prepare_jobs_switch = 'text' # 'folder' # text
# Information required to prepare jobs with selected switch
#main_information = {'files_with_VASP_calcs': files_with_VASP_calcs, 'options': options}
main_information = {'path_to_resubmission_list_file': path_to_resubmission_list_file}

# if you would like to prepare jobs even if they have already converged, change this to True
force_prepare = False
# If you want to also update the VASP files while performing this task
update_VASP_files = False

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
