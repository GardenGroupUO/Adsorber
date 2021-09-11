#!/usr/bin/env python3
'''
Geoffrey Weal, Run_Adsorber_determine_similar_adsorption_sites.py, 5/09/2021

This program is designed to determine which VASP local optimisations have localised adsorbates to the same position

'''
import os, sys
import numpy as np
from scipy.spatial.transform import Rotation

from ase.io import read
from ase.visualize import view

from Adsorber.Subsidiary_Programs.Part_D_Methods import determine_convergence_of_output

System_Adsorbate_VASP_Jobs_folder_name = 'Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP'
if not System_Adsorbate_VASP_Jobs_folder_name in os.listdir('.'):
    print('Error: Could not find the folder: '+str(System_Adsorbate_VASP_Jobs_folder_name))
    print('You need to execute Run_Adsorber_determine_unconverged_VASP_jobs.py in the same place as your '+System_Adsorbate_VASP_Jobs_folder_name+' folder is.')
    print('This program will finish without beginning.')
    exit()

Run_AdsorberPY_name = 'Run_Adsorber.py'
if not Run_AdsorberPY_name in os.listdir('.'):
    print('Error: Could not find the folder: '+str(Run_AdsorberPY_name))
    print('You need to execute Run_Adsorber_determine_unconverged_VASP_jobs.py in the same place as your '+Run_AdsorberPY_name+' script is.')
    print('This program will finish without beginning.')
    exit()

a_line_to_look_for = ['from', 'Adsorber', 'import', 'Adsorber_Program']
def get_cluster_name_from_Run_AdsorberPY_script():
    program_name = None
    with open(Run_AdsorberPY_name) as Run_AdsorberPY:
        for line in Run_AdsorberPY:
            line_split = line.rstrip().split()
            if len(line_split) >= 4 and line_split[0:4] == a_line_to_look_for:
                if 'as' in line:
                    program_name = line_split[5]
                else:
                    program_name = a_line_to_look_for[3]
            if (program_name is not None) and (program_name+'(' in line):
                line = line.rstrip().replace(program_name+'(','').replace(')','')
                inputs_from_line = line.split(',')
                system_filename = inputs_from_line[2]
                break
        with open(Run_AdsorberPY_name) as Run_AdsorberPY:
            for line in Run_AdsorberPY:
                if system_filename in line:
                    line = line.rstrip()
                    name_of_xyz_file = line.replace('system_filename','').replace('=','')
                    name_of_xyz_file = eval(name_of_xyz_file)
                    return name_of_xyz_file

name_of_xyz_file = get_cluster_name_from_Run_AdsorberPY_script()
bare_system_xyz = read(name_of_xyz_file)
no_of_atoms_in_bare_system_xyz = len(bare_system_xyz)

folders_to_look_through = tuple(folder for folder in os.listdir(System_Adsorbate_VASP_Jobs_folder_name) if os.path.isdir(System_Adsorbate_VASP_Jobs_folder_name+'/'+folder))


OUTCAR_file = 'OUTCAR'
submission_folder_name = 'Submission_Folder'
def get_all_completed_OUTCARS(overall_folder):
    converged_jobs = []
    for root, dirs, files in os.walk(overall_folder):
        if submission_folder_name in root:
            dirs[:] = []
            files[:] = []
            continue
        for index in range(len(dirs)-1,-1,-1):
            dirname = dirs[index]
            if dirname.startswith(submission_folder_name):
                del dirs[index]
        if OUTCAR_file in files:
            converged = determine_convergence_of_output(root)
            #if converged:
            converged_jobs.append(root)
            dirs[:] = []
            files[:] = []
    return converged_jobs

def get_OUTCAR_Atoms_files(path_to_OUTCAR):
    print(path_to_OUTCAR)
    first_system_adsorbate = read(path_to_OUTCAR+'/OUTCAR')
    first_system_only = first_system_adsorbate[:no_of_atoms_in_bare_system_xyz]
    centre_translation_matrix = first_system_only.get_center_of_mass()
    first_system_adsorbate.set_positions(first_system_adsorbate.get_positions() - centre_translation_matrix)
    first_system_only.set_positions(first_system_only.get_positions() - centre_translation_matrix)
    first_system_only_positions = first_system_only.get_positions()
    return first_system_adsorbate, first_system_only, first_system_only_positions, os.path.basename(path_to_OUTCAR), path_to_OUTCAR

# ============================================================================================================
'''
maximum_distance_to_be_within = 0.25
def are_positions_within_eachother(new_positions, ori_positions):
    matrix = np.zeros((len(new_positions),len(ori_positions)))
    for new_index in range(len(new_positions)):
        for ori_index in range(len(ori_positions)):
            matrix[new_index][ori_index] = get_distance(new_positions[new_index], ori_positions[ori_index])
    while not np.all(np.isnan(matrix)):
        smallest_distance = np.nanmin(matrix)
        if smallest_distance > maximum_distance_to_be_within:
            return False
        minimum_new_index, minimum_ori_index = np.where(matrix == smallest_distance)
        minimum_new_index, minimum_ori_index = minimum_new_index[0], minimum_ori_index[0]
        for index in range(len(ori_positions)):
            matrix[minimum_new_index][index] = np.nan
        for index in range(len(new_positions)):
            matrix[index][minimum_ori_index] = np.nan
    return True

def is_same_system_including_adsorbate_attachment_site(new_system,original_system,len_of_cluster):
    new_system_positions_of_elements = {}
    original_system_positions_of_elements = {}
    elements = set()
    # Obtain the positions of adsorbate elements in the new and original systems
    for index in range(len_of_cluster,len(new_system)):
        new_atom = new_system[index]
        new_system_positions_of_elements.setdefault(new_atom.symbol,[]).append(new_atom.position)
        elements.add(new_atom.symbol)
        original_atom = original_system[index]
        original_system_positions_of_elements.setdefault(original_atom.symbol,[]).append(original_atom.position)
        elements.add(original_atom.symbol)
    # Determines if the positions of elements overlap. This method works by gathering all the distances of 
    # all atoms of a particular element and comparing them from smallest distance until all atoms are paired together. 
    for element in elements:
        new_positions = new_system_positions_of_elements[element]
        ori_positions = original_system_positions_of_elements[element]
        are_atoms_eithin_eachother = are_positions_within_eachother(new_positions, ori_positions)
        if not are_atoms_eithin_eachother:
            return False
    return True
'''
# ============================================================================================================

def checkConsecutive(ori_system_indices,sort=False):
    if sort:
        ori_system_indices_copy = sorted(ori_system_indices)
        return sorted(ori_system_indices_copy) == list(range(min(ori_system_indices_copy), max(ori_system_indices_copy)+1))
    else:
        return sorted(ori_system_indices) == list(range(min(ori_system_indices), max(ori_system_indices)+1))

system_atom_maximum_distance_to_be_within = 0.2
from Adsorber.Adsorber.Part_B_automated_rotation_methods import get_distance
from time import time
def compare_positions_in_cluster(new_system,original_system,len_of_cluster):
    positions_of_atoms = []
    len_of_original_system = len(original_system)
    new_indices = np.repeat(range(len_of_original_system), len_of_original_system, axis=0)
    ori_indices = list(range(len_of_original_system))*len_of_original_system
    new_symbols = np.repeat(new_system.get_chemical_symbols(), len_of_original_system, axis=0)
    ori_symbols = original_system.get_chemical_symbols()*len_of_original_system
    new_positions = np.repeat(new_system.positions, len_of_original_system, axis=0)
    ori_positions = np.tile(original_system.positions, [len_of_original_system, 1])
    distances = np.sum((new_positions-ori_positions)**2,axis=1)**0.5
    positions_of_atoms = list(inputs for inputs in zip(distances,new_indices,ori_indices,new_symbols,ori_symbols) if inputs[0] <= system_atom_maximum_distance_to_be_within and inputs[3] == inputs[4])
    if len(positions_of_atoms) < len_of_cluster:
        return False, None
    positions_of_atoms.sort()
    counter = 0
    corresponding_indices_ori_to_new = {index: None for index in range(len_of_original_system)}
    for distance, new_index, ori_index, new_symbol, ori_symbols in positions_of_atoms:
        if corresponding_indices_ori_to_new[ori_index] is None:
            corresponding_indices_ori_to_new[ori_index] = new_index
            counter += 1
            if counter == len_of_original_system:
                break
    ori_system_indices = tuple(corresponding_indices_ori_to_new.values())
    if any(xx is None for xx in ori_system_indices):
        return False, None
    if   checkConsecutive(ori_system_indices,sort=False): # needs to be false 
        return True, 'Consecutive'
    elif checkConsecutive(ori_system_indices,sort=True):
        return True, corresponding_indices_ori_to_new
    else:
        return False, None

'''
def rearrange_cluster(system_adsorbate,indices_to_rearrange_into):
    indices_to_rearrange_into += range(len(indices_to_rearrange_into),len(system_adsorbate),1)
    new_system_adsorbate = system_adsorbate.copy()
    for NOTUSED in range(len(system_adsorbate)):
        del new_system_adsorbate[0]
    for index in indices_to_rearrange_into:
        new_system_adsorbate.append(system_adsorbate[index])
    return new_system_adsorbate
'''

from ase.data import covalent_radii, atomic_numbers
def nnd_and_half_distance(atom1_symbol,atom2_symbol):
    cr1 = covalent_radii[atomic_numbers[atom1_symbol]]
    cr2 = covalent_radii[atomic_numbers[atom2_symbol]]
    bd = cr1 + cr2
    bd_2nn = bd * (2.0)**0.5
    diff = bd_2nn - bd
    bd_and_a_half = bd + 0.5*diff
    return bd_and_a_half

import networkx as nx
attached_atom_distance = 1.0
graphs_of_system_adsorbates = []
def adatoms_attached_to_a_system(system_adsorbate,len_of_cluster):
    graph = nx.Graph()
    sys_atom_positions = system_adsorbate.get_positions()[:len_of_cluster]
    # get nodes
    for abs_index in range(len_of_cluster,len(system_adsorbate)):
        adsorbate_atom = system_adsorbate[abs_index]
        system_neighbours = []
        for sys_index in range(len(sys_atom_positions)):
            distance = get_distance(adsorbate_atom.position,sys_atom_positions[sys_index])
            if distance <= nnd_and_half_distance(adsorbate_atom.symbol,system_adsorbate[sys_index].symbol):
                system_neighbours.append(sys_index)
        graph.add_node(abs_index,symbol=adsorbate_atom.symbol,position=tuple(adsorbate_atom.position),system_neighbours=tuple(system_neighbours))
    # get edges
    for abs_index_1 in range(len_of_cluster,len(system_adsorbate)):
        atom1 = system_adsorbate[abs_index_1]
        for abs_index_2 in range(abs_index_1+1,len(system_adsorbate)):
            atom2 = system_adsorbate[abs_index_2]
            distance = get_distance(atom1.position,atom2.position)
            if distance <= nnd_and_half_distance(atom1.symbol,atom2.symbol):
                graph.add_edge(abs_index_1, abs_index_2)
    return graph

maximum_distance_to_be_within_node_match = 1.0
def node_match(g1_n1,g2_n2):
    if not g1_n1['symbol'] == g2_n2['symbol']:
        return False
    if not g1_n1['system_neighbours'] == g2_n2['system_neighbours']:
        return False
    distance = get_distance(g1_n1['position'],g2_n2['position'])
    if not (distance <= maximum_distance_to_be_within_node_match):
        return False
    return True

def adatoms_attached_to_same_system_atoms(graph1, graph2, indices_compared):
    if not indices_compared == 'Consecutive':
        for index in graph2.nodes:
            import pdb; pdb.set_trace()
            neighbours = tuple(indices_compared[neighbour] for neighbour in graph2.nodes[index]['system_neighbours'])
            graph2.nodes[index]['system_neighbours'] = neighbours
    are_graphs_isomorphic = nx.is_isomorphic(graph1, graph2, node_match=node_match)
    return are_graphs_isomorphic

from Adsorber.Adsorber.Part_B_adsorb_single_species_to_cluster import is_same_system
def compare_position_of_adsorbates(index1,first_system_adsorbate,first_system_only,index2,second_system_adsorbate,second_system_only,len_of_cluster):
    # First, determine if the positions of atoms in each cluster are roughly in the same place as each other
    systems_atoms_in_same_position, indices_compared = compare_positions_in_cluster(first_system_only,second_system_only,len_of_cluster)
    #systems_atoms_in_same_position, indices_compared = True, None
    if not systems_atoms_in_same_position:
        return False
    elif not adatoms_attached_to_same_system_atoms(graphs_of_system_adsorbates[index1],graphs_of_system_adsorbates[index2],indices_compared):
        return False
    #view([first_system_adsorbate,second_system_adsorbate])
    #import pdb; pdb.set_trace()
    #if not is_same_system_including_adsorbate_attachment_site(first_system_adsorbate,second_system_adsorbate_copy,len_of_cluster):
    #    return False
    return True
    
    #return is_same_system(first_system_adsorbate,second_system_adsorbate,no_of_atoms_in_bare_system_xyz)
    

# ============================================================================================================

for folder in folders_to_look_through:
    print('====================================================================')
    print('Getting system+adsorbate objects from '+str(folder))
    all_completed_outcar_files = get_all_completed_OUTCARS(System_Adsorbate_VASP_Jobs_folder_name+'/'+folder)
    all_outcar_objects = [get_OUTCAR_Atoms_files(path_to_OUTCAR) for path_to_OUTCAR in all_completed_outcar_files]
    print(len(all_completed_outcar_files))
    print('====================================================================')
    # make graphs of plots
    for system_adsorbate, system_only, system_only_positions, name, path in all_outcar_objects:
        graph = adatoms_attached_to_a_system(system_adsorbate,no_of_atoms_in_bare_system_xyz)
        graphs_of_system_adsorbates.append(graph)
    similar_system_adsorbates = {}
    for index1 in range(len(all_outcar_objects)):
        first_system_adsorbate, first_system_only, first_system_only_positions, first_name, first_path = all_outcar_objects[index1]
        masses = first_system_only.get_masses()
        print(all_completed_outcar_files[index1])
        for index2 in range(index1+1,len(all_outcar_objects)):
            second_system_adsorbate, second_system_only, second_system_only_positions, second_name, second_path = all_outcar_objects[index2]
            estimated_rotation, rmsd = Rotation.align_vectors(first_system_only_positions,second_system_only_positions,masses)
            rotation_matrix = estimated_rotation.as_matrix()
            second_system_adsorbate.set_positions(np.dot(rotation_matrix,second_system_adsorbate.get_positions().T).T)
            if compare_position_of_adsorbates(index1,first_system_adsorbate,first_system_only,index2,second_system_adsorbate,second_system_only,no_of_atoms_in_bare_system_xyz):
                similar_system_adsorbates.setdefault(first_name,[]).append(second_name)
                similar_system_adsorbates.setdefault(second_name,[]).append(first_name)
    print(similar_system_adsorbates)
    import pdb; pdb.set_trace()