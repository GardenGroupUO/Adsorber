# ----------------------------------------------------------------------------------------------------------------
# Part C Information
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# General settings
path_to_VASP_optimised_non_adsorbate_system = 'Part_A_Non_Adsorbed_Files_For_VASP/system/POSCAR' #OUTCAR'

# slurm informaion for making the submit.sl files for submitting VASP jobs in slurm
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

# ----------------------------------------------------------------------------------------------------------------