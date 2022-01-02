class CLICommand:
    """Will create xyz files of your system with adsorbates bound to all top, bridge, three-fold, and four-fold sites. From these xyz files you should select those that you want to perform VASP optimisations upon in your study. See documentation regarding "Copy_Files_from_Folder_B_to_Folder_C.py" for a program that can help you pick the appropriate xyz files to perform VASP optimisations upon in Part C.
    """

    @staticmethod
    def add_arguments(parser):
        pass
        #parser.add_argument('filename', nargs='*', help='Name of file to determine format for.')

    @staticmethod
    def run(args):
        Run_PartB()

import os
from shutil import copytree

from ase import Atom
from ase.io import write

from Adsorber.Adsorber.import_settings import import_general_settings, import_adsorbate_settings, import_PartB_settings
from Adsorber.Adsorber.program_information import introductory_remarks, finish_up

from Adsorber.Adsorber.Part_B_neighbour_list import get_neighbour_list_for_surface_atoms
from Adsorber.Adsorber.Part_B_get_places_to_bind_to import get_above_atom_sites, get_bridge_sites, get_three_fold_sites, get_four_fold_sites
from Adsorber.Adsorber.Part_B_adsorb_single_species_to_cluster import adsorb_single_species_to_cluster
from Adsorber.Adsorber.Part_B_storage_file import write_data_file, load_data_file

def Run_PartB():
    """
    Will create xyz files of your system with adsorbates bound to all top, bridge, three-fold, and four-fold sites. 

    From these xyz files you should select those that you want to perform VASP optimisations upon in your study. 

    """
    # Introduction
    introductory_remarks()
    # Get input varables from scripts
    cluster_or_surface_model, system_filename, name_without_suffix, add_vacuum, vasp_files_folder, systems_to_convert_for_VASP_name = import_general_settings()
    adsorbed_species = import_adsorbate_settings()
    check_saving_binding_sites(adsorbed_species)
    path_to_VASP_optimised_non_adsorbate_system, cluster, surface_atoms, cutoff, data_storage_file, distance_of_dummy_adatom_from_surface, bind_site_data_types, system_folder_name = import_PartB_settings()
    # Run program
    set_up_cluster(name_without_suffix,cluster,surface_atoms)
    print('=================================')
    print('Adsorber will create systems with adsorbed adsorbates.')
    print('=================================')
    Part_B_make_adsorbed_xyz_files(cluster,cutoff,distance_of_dummy_adatom_from_surface,surface_atoms,data_storage_file,cluster_or_surface_model,bind_site_data_types,name_without_suffix,adsorbed_species,system_folder_name,systems_to_convert_for_VASP_name)
    print('=================================')
    print('Adsorber has finished creating systems with adsorbed adsorbates.')
    print('=================================')
    finish_up()

# ========================================================================================
# Input programs, save the adsorbate files.
all_binding_sites = ['Top_Sites','Bridge_Sites','Three_Fold_Sites','Four_Fold_Sites']
def check_saving_binding_sites(adsorbed_species):
    """
    This method will check if your adsorbed_species is in the correct format.
    """
    for adsorbed_speciee in adsorbed_species:
        if 'sites_to_bind_adsorbate_to' in adsorbed_speciee:
            if isinstance(adsorbed_speciee['sites_to_bind_adsorbate_to'],str):
                adsorbed_speciee['sites_to_bind_adsorbate_to'] = [adsorbed_speciee['sites_to_bind_adsorbate_to']]
            if not isinstance(adsorbed_speciee['sites_to_bind_adsorbate_to'],list):
                print('Error importing adsorbed_species into Adsorber for adsorbate: '+str(adsorbed_speciee['name']))
                print('Your entry for "sites_to_bind_adsorbate_to" must be a list')
                print('"sites_to_bind_adsorbate_to": '+str(adsorbed_speciee['sites_to_bind_adsorbate_to']))
                print('Check this out. Adsorber will finishing without beginning.')
                exit()
            adsorbed_speciee['sites_to_bind_adsorbate_to'] = list(set(adsorbed_speciee['sites_to_bind_adsorbate_to']))
            for adsorbed_speciee_binding_site in adsorbed_speciee['sites_to_bind_adsorbate_to']:
                if not adsorbed_speciee_binding_site in all_binding_sites:
                    print('Error importing adsorbed_species into Adsorber for adsorbate: '+str(adsorbed_speciee['name']))
                    print('Your entry for "sites_to_bind_adsorbate_to" is: '+str(adsorbed_speciee['sites_to_bind_adsorbate_to']))
                    print('The entries can only include: '+str(all_binding_sites))
                    print('Check this out. Adsorber will finishing without beginning.')
                    exit()
        else:
            adsorbed_speciee['sites_to_bind_adsorbate_to'] = all_binding_sites

# ========================================================================================

def set_up_cluster(name_without_suffix,cluster,surface_atoms):
    """
    This method will save a version of the VASP optimised system as an xyz file, as well as with tags denoting the surface atoms you have chosen.
    """
    write(name_without_suffix+'_after_VASP_Opt.xyz',cluster)
    cluster.set_tags(0)
    for surface_atom_index in surface_atoms:
        cluster[surface_atom_index].tag = 1
    write(name_without_suffix+'_after_VASP_Opt_tagged_surface_atoms.xyz',cluster)

# ========================================================================================

def Part_B_make_adsorbed_xyz_files(cluster,cutoff,distance_of_dummy_adatom_from_surface,surface_atoms,data_storage_file,cluster_or_surface_model,bind_site_data_types,name_without_suffix,adsorbed_species,system_folder_name,systems_to_convert_for_VASP_name):
    """
    This method will make xyz files of your system with adsorbates adsorbed to various sites about your system
    """
    # Determine possible top, bridge, three fold, and four fold adsorption sites about your system
    above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites = get_initial_adatom_placements(cluster,cutoff,distance_of_dummy_adatom_from_surface,surface_atoms,data_storage_file,cluster_or_surface_model,bind_site_data_types,name_without_suffix)
    what_to_adsorb = []
    initial_sentence = 'Make System with adsorbates attached upon '
    what_to_adsorb.append((above_atom_binding_sites,'Top_Sites',initial_sentence+'top sites'))
    what_to_adsorb.append((above_bridge_binding_sites,'Bridge_Sites',initial_sentence+'bridge sites'))
    what_to_adsorb.append((above_three_fold_sites,'Three_Fold_Sites',initial_sentence+'three-fold sites'))
    what_to_adsorb.append((above_four_fold_sites,'Four_Fold_Sites',initial_sentence+'four-fold sites'))
    # bind adsorbate to your system about all top, bridge, three fold, and four fold adsorption sites about your system
    print('============================================================================================')
    for binding_sites, binding_sites_name, to_print in what_to_adsorb:
        print(to_print)
        adsorb_species_to_cluster(cluster,surface_atoms,binding_sites,cutoff,adsorbed_species,binding_sites_name,system_folder_name)
    print('============================================================================================')
    # create the folder for xyz files to make VASP files of
    def ig_f(dir, files):
        return [f for f in files if os.path.isfile(os.path.join(dir, f))]
    if not os.path.exists(systems_to_convert_for_VASP_name):
        copytree(system_folder_name, systems_to_convert_for_VASP_name, ignore=ig_f)

def get_initial_adatom_placements(cluster,cutoff,distance_of_dummy_adatom_from_surface,surface_atoms,data_storage_file,cluster_or_surface_model,bind_site_data_types,name_without_suffix):
    """
    Determine possible top, bridge, three fold, and four fold adsorption sites about your system
    """
    if not os.path.exists(data_storage_file):
        # Get the option of top, bridge, three fold, and four fold adsorption sites from system
        print('============================================================================================')
        print('Getting Binding data')
        neighbour_list = get_neighbour_list_for_surface_atoms(cluster,surface_atoms,cutoff)
        print('Getting top binding sites.')
        above_atom_binding_sites = get_above_atom_sites(cluster,surface_atoms,distance_of_dummy_adatom_from_surface,cluster_or_surface_model)
        print('Getting bridging binding sites.')
        above_bridge_binding_sites = get_bridge_sites(cluster,neighbour_list,distance_of_dummy_adatom_from_surface,cluster_or_surface_model)
        print('Getting three-fold binding sites.')
        above_three_fold_sites = get_three_fold_sites(cluster,neighbour_list,distance_of_dummy_adatom_from_surface,cluster_or_surface_model)
        print('Getting four-fold binding sites.')
        above_four_fold_sites = get_four_fold_sites(cluster,neighbour_list,distance_of_dummy_adatom_from_surface,cluster_or_surface_model)
        print('Saving data to '+str(data_storage_file))
        write_data_file(data_storage_file,bind_site_data_types,above_atom_binding_sites,above_bridge_binding_sites,above_three_fold_sites,above_four_fold_sites)
        print('============================================================================================')
    else:
        # Get the option of top, bridge, three fold, and four fold adsorption sites by loading from the data_storage_file Text File. 
        print('============================================================================================')
        print('Loading data from '+str(data_storage_file))
        above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites = load_data_file(data_storage_file,bind_site_data_types)
        print('============================================================================================')

    # Write the xyz file of your system with binding sites given as H atoms.
    def make_full_binding_site_representative_cluster(cluster,above_atom_binding_sites,cluster_file_name):
        representative_cluster = cluster.copy()
        counter = 1
        for binding_position, surface_position, indices_of_atoms_involved in above_atom_binding_sites:
            binding_representative_atom = Atom('H',position=binding_position,charge=counter,tag=2) # These could be symbolised as H or X
            representative_cluster.append(binding_representative_atom)
            counter += 1
        write(cluster_file_name+'.xyz',representative_cluster)
    representative_cluster_folder_name = 'Part_B_Binding_Site_Locations'
    if not os.path.exists(representative_cluster_folder_name):
        os.makedirs(representative_cluster_folder_name)
    prefix_name = representative_cluster_folder_name+'/'+name_without_suffix
    make_full_binding_site_representative_cluster(cluster,above_atom_binding_sites,prefix_name  +'_top_sites')
    make_full_binding_site_representative_cluster(cluster,above_bridge_binding_sites,prefix_name+'_bridging_sites')
    make_full_binding_site_representative_cluster(cluster,above_three_fold_sites,prefix_name    +'_three_fold_sites')
    make_full_binding_site_representative_cluster(cluster,above_four_fold_sites,prefix_name     +'_four_fold_sites')
    return above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites

def adsorb_species_to_cluster(cluster,surface_atoms,binding_site_data,cutoff,adsorbed_species,binding_sites_name,system_folder_name):
    """
    Write the xyz file of adsorbate adsorbed upon various postions upon the surface of your system.
    """
    for an_adsorbed_species in adsorbed_species:
        if binding_sites_name in an_adsorbed_species['sites_to_bind_adsorbate_to']:
            print('Adsorbate Name: '+str(an_adsorbed_species['name']))
            for index in range(len(binding_site_data)):
                binding_site_datum = binding_site_data[index]
                adsorb_single_species_to_cluster(cluster, surface_atoms, binding_site_datum, cutoff, an_adsorbed_species, binding_sites_name, index+1, system_folder_name)
        else:
            print('Adsorbate Name: '+str(an_adsorbed_species['name'])+' --> Will not gather '+binding_sites_name.lower().replace('_',' ')+' models as specified in your Run_Adsorber.py script.')
