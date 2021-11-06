import os
import numpy as np

from datetime import datetime, timedelta

from Adsorber import __version__

# ================================================================================================================================================

# https://stackoverflow.com/questions/2301789/how-to-read-a-file-in-reverse-order
def reverse_readline(filename, buf_size=8192):
    """A generator that returns the lines of a file in reverse order"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # The first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # If the previous chunk starts right from the beginning of line
                # do not concat the segment to the last line of new chunk.
                # Instead, yield the segment first 
                if buffer[-1] != '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if lines[index]:
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment

# ================================================================================================================================================

def get_version_number():
    version = __version__
    return version

def version_no():
    """
    Will provide the version of the Adsorber program
    """
    version = get_version_number() 
    return version

def introductory_remarks():
    print('=================================')
    print()
    print('       Adsorber: Part D          ')
    print()
    print('         Version: '+str(version_no()))
    print()
    print('=================================')
    print()

# ================================================================================================================================================
# Combined methods

seconds_in_week   = 60 * 60 * 24 * 7
seconds_in_day    = 60 * 60 * 24
seconds_in_hour   = 60 * 60
seconds_in_minute = 60

def convert_seconds_to_human_readable_time(time_in_seconds):
    time_str = ''
    writing = False
    weeks, remainder = divmod(time_in_seconds,seconds_in_week)
    if (not weeks == 0):
        time_str += str(weeks)+' weeks, '
    days, remainder = divmod(remainder,seconds_in_day)
    if writing or (not days == 0):
        time_str += str(days)+' days, '
    hours, remainder = divmod(remainder,seconds_in_hour)
    if writing or (not hours == 0):
        time_str += str(hours)+' hrs, '
    minutes, seconds = divmod(remainder,seconds_in_minute)
    if writing or (not minutes == 0):
        time_str += str(minutes)+' mins, '
    time_str += str(round(seconds,0))+' secs'
    return time_str

def get_job_id(path_to_OUTCAR):
    for file in os.listdir(path_to_OUTCAR):
        if os.path.isfile(path_to_OUTCAR+'/'+file) and file.startswith('slurm-') and file.endswith('.out'):
            job_id = int(file.replace('slurm-','').replace('.out',''))
            return job_id
    return 'None'

def get_start_date_from_OUTCAR(root):
    with open(root+'/OUTCAR','r') as OUTCAR:
        for line in OUTCAR:
            if 'executed on' in line:
                line = line.rstrip().split()
                start_date_from_vasp, start_time_from_vasp = line[4], line[5]
                start_time_timestamp = datetime.strptime(start_date_from_vasp+' '+start_time_from_vasp, "%Y.%m.%d %H:%M:%S")
                start_time_timestamp = datetime.timestamp(start_time_timestamp)
                return start_date_from_vasp+' '+start_time_from_vasp, start_time_timestamp
            elif '------------------------------------------------------------------------------' in line:
                return None, None

def get_finish_time(date_submitted,time_elapsed):
    date_finished = date_submitted + time_elapsed
    date_finished = datetime.fromtimestamp(date_finished)
    date_finished = date_finished.strftime('%Y.%m.%d %H:%M:%S')
    return date_finished

def get_EDIFFG_from_OUTCAR(root):
    with open(root+'/OUTCAR','r') as OUTCAR:
        for line in OUTCAR:
            if 'EDIFFG' in line:
                line = line.rstrip().split()
                EDIFFG = float(line[2])
                return EDIFFG
    return '---'

def get_project_id_and_time_from_slurm(root):
    project_id = None
    time = None
    with open(root+'/submit.sl','r') as submitSL:
        for line in submitSL:
            if '--time' in line:
                time = line.rstrip().split()[1].replace('--time=','')
                if (project_id is not None) and (time is not None):
                    break
            if '#SBATCH -A' in line:
                project_id = line.rstrip().split()[2]
                if (project_id is not None) and (time is not None):
                    break
    return project_id, time

def determine_convergence_and_time_elapsed_and_date_finished_and_Max_mem_Gb_and_energy_of_output(path_to_output,start_time_timestamp):
    convergence = None
    time_elapsed_seconds = None; time_elapsed = None; date_finished = None
    Max_mem_Gb = None
    energy = None
    for line in reverse_readline(path_to_output+'/OUTCAR'):
        if 'force has converged' in line:
            convergence = True
            if (convergence is not None) and (time_elapsed_seconds is not None) and (Max_mem_Gb is not None) and (energy is not None):
                break
        elif 'Elapsed time' in line:
            time_elapsed_seconds = float(line.rstrip().split()[3])
            if (convergence is not None) and (time_elapsed_seconds is not None) and (Max_mem_Gb is not None) and (energy is not None):
                break
        elif 'Maximum memory used' in line:
            Max_mem_kb = float(line.rstrip().split()[4])
            Max_mem_Gb = round(Max_mem_kb/1048576,2) #(1024*1024)
            if (convergence is not None) and (time_elapsed_seconds is not None) and (Max_mem_Gb is not None) and (energy is not None):
                break
        elif ('energy(sigma->0)' in line):
            line = line.rstrip().split()
            if convergence:
                energy = float(line[6])
                if (convergence is not None) and (time_elapsed_seconds is not None) and (Max_mem_Gb is not None) and (energy is not None):
                    break
            elif len(line) == 7:
                energy = float(line[6])
                break
            elif len(line) == 8:
                energy = float(line[7])
                break
            else:
                break
        elif 'FREE ENERGIE OF THE ION-ELECTRON SYSTEM' in line:
            break
    convergence = False if convergence is None else True
    if time_elapsed_seconds is not None:
        date_finished = get_finish_time(start_time_timestamp, time_elapsed_seconds)
        time_elapsed = convert_seconds_to_human_readable_time(time_elapsed_seconds)
    return convergence, time_elapsed, date_finished, Max_mem_Gb, energy

force_has_converged = 'force has converged'
end_message = 'FREE ENERGIE OF THE ION-ELECTRON SYSTEM' 
def determine_convergence_of_output(path_to_output):
    for line in reverse_readline(path_to_output+'/OUTCAR'):
        if force_has_converged in line:
            return True
        elif end_message in line:
            break
    return False

got_energy = 'energy(sigma->0)' 
def determine_convergence_and_energy_of_output(path_to_output):
    convergence = False; energy = None
    for line in reverse_readline(path_to_output+'/OUTCAR'):
        if force_has_converged in line:
            convergence = True
            if energy is not None:
                break
        elif got_energy in line:
            line = line.rstrip().split()
            energy = float(line[-1])
            if convergence:
                break
        elif end_message in line:
            break
    return convergence, energy

# ================================================================================================================================================
# ================================================================================================================================================
# ================================================================================================================================================
# ================================================================================================================================================

a_line_to_look_for = ['from', 'Adsorber', 'import', 'Adsorber_Program']
def get_cluster_name_from_Run_AdsorberPY_script(Run_AdsorberPY_name):
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

from ase.io import read
Submission_Folder = 'Submission_Folder'
def get_OUTCAR_Atoms_files(path_to_OUTCAR,files_in_submission_folder,no_of_atom_in_system):
    path_to = path_to_OUTCAR
    if files_in_submission_folder is not None:
        path_to += '/'+files_in_submission_folder
    try:
        first_system_adsorbate = read(path_to+'/CONTCAR')
    except Exception as ee: 
        try:
            first_system_adsorbate = read(path_to+'/OUTCAR')
        except Exception as ff:
            return None
    first_system_only = first_system_adsorbate[:no_of_atom_in_system]
    centre_translation_matrix = first_system_only.get_center_of_mass()
    first_system_adsorbate.set_positions(first_system_adsorbate.get_positions() - centre_translation_matrix)
    first_system_only.set_positions(first_system_only.get_positions() - centre_translation_matrix)
    if os.path.basename(path_to_OUTCAR).startswith(Submission_Folder):
        name = path_to_OUTCAR.split('/')[-2]
    else:
        name = os.path.basename(path_to_OUTCAR)
    return first_system_adsorbate, name, path_to_OUTCAR

# ================================================================================================================================================

# Are two system+adsorbates combinations the same methods

def checkConsecutive(ori_system_indices,sort=False):
    if sort:
        ori_system_indices_copy = sorted(ori_system_indices)
        return sorted(ori_system_indices_copy) == list(range(min(ori_system_indices_copy), max(ori_system_indices_copy)+1))
    else:
        return sorted(ori_system_indices) == list(range(min(ori_system_indices), max(ori_system_indices)+1))

system_atom_maximum_distance_to_be_within = 0.2
def compare_positions_in_system_without_adsorbate(new_system,original_system,len_of_system_without_adsorbate):
    positions_of_atoms = []
    new_indices = np.repeat(range(len_of_system_without_adsorbate), len_of_system_without_adsorbate, axis=0)
    ori_indices = list(range(len_of_system_without_adsorbate))*len_of_system_without_adsorbate
    new_symbols = np.repeat(new_system.get_chemical_symbols()[:len_of_system_without_adsorbate], len_of_system_without_adsorbate, axis=0)
    ori_symbols = original_system.get_chemical_symbols()[:len_of_system_without_adsorbate]*len_of_system_without_adsorbate
    new_positions = np.repeat(new_system.get_positions()[:len_of_system_without_adsorbate], len_of_system_without_adsorbate, axis=0)
    ori_positions = np.tile(original_system.get_positions()[:len_of_system_without_adsorbate], [len_of_system_without_adsorbate, 1])
    distances = np.sum((new_positions-ori_positions)**2,axis=1)**0.5
    positions_of_atoms = list(inputs for inputs in zip(distances,new_indices,ori_indices,new_symbols,ori_symbols) if inputs[0] <= system_atom_maximum_distance_to_be_within and inputs[3] == inputs[4])
    if len(positions_of_atoms) < len_of_system_without_adsorbate:
        return False, None
    positions_of_atoms.sort()
    counter = 0
    corresponding_indices_ori_to_new = {index: None for index in range(len_of_system_without_adsorbate)}
    for distance, new_index, ori_index, new_symbol, ori_symbols in positions_of_atoms:
        if corresponding_indices_ori_to_new[ori_index] is None:
            corresponding_indices_ori_to_new[ori_index] = new_index
            counter += 1
            if counter == len_of_system_without_adsorbate:
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


# ================================================================================================================================================

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
from Adsorber.Adsorber.Part_B_automated_rotation_methods import get_distance
attached_atom_distance = 1.0
def make_graph_of_adsorbate(system_adsorbate,len_of_cluster,attach_edges=True):
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
    if attach_edges:
        for abs_index_1 in range(len_of_cluster,len(system_adsorbate)):
            atom1 = system_adsorbate[abs_index_1]
            for abs_index_2 in range(abs_index_1+1,len(system_adsorbate)):
                atom2 = system_adsorbate[abs_index_2]
                distance = get_distance(atom1.position,atom2.position)
                if distance <= nnd_and_half_distance(atom1.symbol,atom2.symbol):
                    graph.add_edge(abs_index_1, abs_index_2)
    return graph

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

maximum_distance_to_be_within_node_match = 1.0
def node_match_1(g1_n1,g2_n2):
    if not g1_n1['symbol'] == g2_n2['symbol']:
        return False
    if not g1_n1['system_neighbours'] == g2_n2['system_neighbours']:
        return False
    distance = get_distance(g1_n1['position'],g2_n2['position'])
    if not (distance <= maximum_distance_to_be_within_node_match):
        return False
    return True
def node_match_2(g1_n1,g2_n2):
    if not g1_n1['symbol'] == g2_n2['symbol']:
        return False
    distance = get_distance(g1_n1['position'],g2_n2['position'])
    if not (distance <= maximum_distance_to_be_within_node_match):
        return False
    return True

def compare_adsorbate_positions(graph1, graph2, second_system, indices_compared, compare_neighbours=True):
    graph_2_copy = graph2.copy()
    second_system_positions = second_system.get_positions()
    # Change positions in graph due to previous rotation of second_system before this method in Run_Adsorber_Part_D_gather_information.py
    for index in graph_2_copy.nodes:
        graph_2_copy.nodes[index]['positions'] = tuple(second_system_positions[index])
    # update neighbour indices in graph2 if atoms are misalligned to atom indices in the first_system
    if compare_neighbours:
        if not indices_compared == 'Consecutive':
            for index in graph_2_copy.nodes:
                import pdb; pdb.set_trace()
                neighbours = tuple(indices_compared[neighbour] for neighbour in graph_2_copy.nodes[index]['system_neighbours'])
                graph_2_copy.nodes[index]['system_neighbours'] = neighbours
        are_graphs_isomorphic = nx.is_isomorphic(graph1, graph_2_copy, node_match=node_match_1)
    else:
        are_graphs_isomorphic = nx.is_isomorphic(graph1, graph_2_copy, node_match=node_match_2)
    return are_graphs_isomorphic

# ================================================================================================================================================

from scipy.spatial.transform import Rotation
def rotation_second_system(first_system_adsorbate,second_system_adsorbate,no_of_atoms_in_bare_system_xyz,masses):
    estimated_rotation, rmsd = Rotation.align_vectors(first_system_adsorbate.get_positions()[:no_of_atoms_in_bare_system_xyz],second_system_adsorbate.get_positions()[:no_of_atoms_in_bare_system_xyz],masses[:no_of_atoms_in_bare_system_xyz])
    rotation_matrix = estimated_rotation.as_matrix()
    second_system_adsorbate_copy = second_system_adsorbate.copy()
    second_system_adsorbate_copy.set_positions(np.dot(rotation_matrix,second_system_adsorbate_copy.get_positions().T).T)
    return second_system_adsorbate_copy

def compare_position_of_adsorbates(first_system,first_graph,second_system,second_graph,len_of_cluster,compare_neighbours=True):
    # First, determine if the positions of atoms in each cluster are roughly in the same place as each other
    systems_atoms_in_same_position, indices_compared = compare_positions_in_system_without_adsorbate(first_system,second_system,len_of_cluster)
    if not systems_atoms_in_same_position:
        return False
    #import pdb; pdb.set_trace()
    if not compare_adsorbate_positions(first_graph,second_graph,second_system,indices_compared,compare_neighbours=compare_neighbours):
        return False
    return True
    
# ================================================================================================================================================

