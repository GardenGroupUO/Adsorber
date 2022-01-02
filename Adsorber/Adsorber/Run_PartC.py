class CLICommand:
    """Will convert the xyz files of adsorbated bounded to selected sites on your system as VASP files for further local optimisation by VASP.
    """

    @staticmethod
    def add_arguments(parser):
        pass
        #parser.add_argument('filename', nargs='*', help='Name of file to determine format for.')

    @staticmethod
    def run(args):
        Run_PartC()

import os
from shutil import copyfile
from ase.io import read, write

from Adsorber.Adsorber.import_settings import import_general_settings, import_adsorbate_settings, import_PartC_settings
from Adsorber.Adsorber.program_information import introductory_remarks, finish_up
from Adsorber.Adsorber.Run_PartB import check_saving_binding_sites
from Adsorber.Adsorber.make_VASP_files_methods import make_overall_potcar, make_individual_submitSL_files, check_VASP_files

def Run_PartC():
    """
    This program will take the xyz files of systems with adsorbates in the chosen binding surface positions and convert them into VASP files to be optimised.
    """
    # Introduction
    introductory_remarks()
    # Get input varables from scripts
    cluster_or_surface_model, system_filename, name_without_suffix, add_vacuum, vasp_files_folder, systems_to_convert_for_VASP_name = import_general_settings()
    adsorbed_species = import_adsorbate_settings()
    check_saving_binding_sites(adsorbed_species)
    VASP_folder_name, part_c_force_create_original_POSCAR, cluster, slurm_information = import_PartC_settings()
    # Run program
    #set_up_cluster(name_without_suffix,cluster,surface_atoms)
    print('=================================')
    print('Adsorber has already created systems with adsorbed atoms and molecules and you have selected systems that you want to run (These are in the "'+str(systems_to_convert_for_VASP_name)+'" folder).')
    print('Adsorber will attempt to create VASP directories of systems with adsorbed molecules from the '+str(systems_to_convert_for_VASP_name)+' folder')
    print('=================================')
    Part_C_make_VASP_files(cluster,adsorbed_species,systems_to_convert_for_VASP_name,vasp_files_folder,VASP_folder_name,slurm_information,part_c_force_create_original_POSCAR)
    print('=================================')
    finish_up()

def Part_C_make_VASP_files(cluster,adsorbed_species,systems_to_convert_for_VASP_name,vasp_files_folder,VASP_folder_name,slurm_information,part_c_force_create_original_POSCAR):
    """
    Will make VASP files of chosen system+adsorbates in certain binding positions
    """
    if slurm_information == {}:
        print('No information give for slurm_information')
        print('VASP files of systems with adsorbed molecules will not be created until a information about the submit.sl files are given in the slurm_information variable.')
        print('Adsorber will finish without making VASP files of systems with adsorbed molecules.')
        exit()
    make_VASP_folders(cluster,adsorbed_species,look_through_folder=systems_to_convert_for_VASP_name,vasp_files_folder=vasp_files_folder,folder_name=VASP_folder_name,slurm_information=slurm_information,part_c_force_create_original_POSCAR=part_c_force_create_original_POSCAR)

# =================================================================================================================

def make_VASP_folders(system,adsorbed_species,look_through_folder='Selected_Systems_to_Convert_for_VASP_Calcs',vasp_files_folder='VASP_Files',folder_name='Selected_Systems_with_Adsorbed_Species_for_VASP',slurm_information={},part_c_force_create_original_POSCAR=False):
    """
    This method will take the xyz files of systems with adsorbates in the chosen binding surface positions and convert them into VASP files to be optimised.
    """
    if not os.path.exists(look_through_folder):
        exit('Error: '+str(look_through_folder)+' folder does not exist. You need to manually create this and place desired systems with adsorbed molecules on it to continue. This program will exit without running.')
    elements = get_elements(system,adsorbed_species)
    check_VASP_files(vasp_files_folder,elements)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    for root, dirs, files in os.walk(look_through_folder):
        dirs.sort()
        files.sort()
        for file in files:
            if file.endswith('.xyz'):
                print(root)
                dirs[:] = []
                break
        for file in files:
            if file.endswith('.xyz'):
                file_name = file.replace('.xyz','')
                folder_to_save_to = folder_name+root.replace(look_through_folder,'')+'/'+file_name
                # ==================================================================================
                # Create the folder to hold the VASP files and make the POSCAR 
                # ==================================================================================
                # only copy over jobs that have not begun, you dont want to change anyting that is currently running. 
                if os.path.exists(folder_to_save_to+'/OUTCAR'):
                    continue
                # begin to make the necessary files
                system = read(root+'/'+file)
                #system, original_positions_of_atoms = system_with_atoms_rearranged_alphabetically(system)
                if not os.path.exists(folder_to_save_to):
                    os.makedirs(folder_to_save_to)
                if not os.path.exists(folder_to_save_to+'/POSCAR') or part_c_force_create_original_POSCAR:
                    write(folder_to_save_to+'/POSCAR',system)
                    # ==============================================================================
                    # Place the files in the VASP_files folder an dplace in your system+adsorbate VASP folder
                    # ==============================================================================
                    # This for loop copies all the VASP files in VASP_Files into each folder with a POSCAR
                    for vasp_file in os.listdir(vasp_files_folder):
                        if not vasp_file == 'POTCARs':
                            copyfile(vasp_files_folder+'/'+vasp_file,folder_to_save_to+'/'+vasp_file)
                    # Make POTCAR for each system
                    make_overall_potcar(folder_to_save_to,vasp_files_folder)
                    # Make submit.sl file
                    make_individual_submitSL_files(folder_to_save_to,file_name,slurm_information)
                    # This will write a file that records the original position of atoms in the system. 
                    # This is because the POSCAR needs to be sorted by atom for the POTCAR. 
                    #write_original_positions_of_atoms_to_disk(original_positions_of_atoms,folder_to_save_to)
                # ==================================================================================
# =================================================================================================================

def get_elements(system,adsorbed_species):
    elements = []
    elements += list(system.get_chemical_symbols())
    for molecule_dict in adsorbed_species:
        elements += list(molecule_dict['molecule'].get_chemical_symbols())
    elements = tuple(set(elements))
    return elements

def system_with_atoms_rearranged_alphabetically(system):
    all_atoms_as_list = []
    for index in range(len(system)):
        atom = system[index]
        all_atoms_as_list.append((atom,index))
    all_atoms_as_list.sort(key=lambda entry:entry[0].symbol)
    system_copy = system.copy()
    while len(system_copy) > 0:
        del system_copy[0]
    original_positions_of_atoms = []
    for atom, index in all_atoms_as_list:
        system_copy.append(atom)
        original_positions_of_atoms.append(index)
    return system_copy, original_positions_of_atoms

def write_original_positions_of_atoms_to_disk(original_positions_of_atoms,folder_to_save_to):
    with open(folder_to_save_to+'/original_positions.txt','w') as original_positionsTXT:
        string_to_enter = ' '.join([str(position) for position in original_positions_of_atoms])
        original_positionsTXT.write(string_to_enter)

# =================================================================================================================