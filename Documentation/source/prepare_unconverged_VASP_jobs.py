from Adsorber import Run_Adsorber_prepare_unconverged_VASP_jobs

#files_with_VASP_calcs = ['Part_A_Non_Adsorbed_Files_For_VASP','Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP']
files_with_VASP_calcs = ['Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/CHO']

options = {'energies_from_lowest_energy': float('inf')}

Run_Adsorber_prepare_unconverged_VASP_jobs(files_with_VASP_calcs,options)
