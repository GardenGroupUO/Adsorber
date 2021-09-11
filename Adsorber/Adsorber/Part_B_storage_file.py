import numpy as np

title = 'Site\t\tBinding Position\t\t\tSurface Position\t\tIndices of atoms involved'

def write_data_file(data_storage_file,bind_site_data_types,above_atom_binding_sites,above_bridge_binding_sites,above_three_fold_sites,above_four_fold_sites):
    def write_to_datafileTXT(datafileTXT,binding_sites,description):
        counter = 1
        datafileTXT.write('The following sites are binding sites for '+str(description)+'.\n')
        datafileTXT.write(title+'\n')
        for binding_position, surface_position, atoms_involved in binding_sites:
            datafileTXT.write('Site '+str(counter)+'\t'+str(binding_position)+'\t'+str(surface_position)+'\t'+str(atoms_involved)+'\n')
            counter += 1
        datafileTXT.write('--------------------------------------------------------------\n')
    with open(data_storage_file,'w') as datafileTXT:
        datafileTXT.write('--------------------------------------------------------------\n')
        datafileTXT.write('--------------------------------------------------------------\n')
        datafileTXT.write('The following data gives the positions of possible binding sites for adatoms and admolecules across a cluster or surface.\n\n')
        write_to_datafileTXT(datafileTXT,above_atom_binding_sites,bind_site_data_types[0])
        write_to_datafileTXT(datafileTXT,above_bridge_binding_sites,bind_site_data_types[1])
        write_to_datafileTXT(datafileTXT,above_three_fold_sites,bind_site_data_types[2])
        write_to_datafileTXT(datafileTXT,above_four_fold_sites,bind_site_data_types[3])

def load_data_file(data_storage_file,bind_site_data_types):
    index = 0
    write_to_list = False
    data = [[],[],[],[]]
    with open(data_storage_file,'r') as datafileTXT:
        for line in datafileTXT:
            if line.startswith(title):
                continue
            elif line.startswith('The following sites are binding sites for '+str(bind_site_data_types[index])+'.'):
                write_to_list = True
            elif line.startswith('--------------------------------------------------------------') and write_to_list == True:
                write_to_list = False
                index += 1
            elif write_to_list:
                line = line.rstrip().split('[')
                datum = (convert_to_list(line[1],True,False),convert_to_list(line[2],True,False),convert_to_list(line[3],False,True))
                data[index].append(datum)
    above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites = data
    return above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites

def convert_to_list(a_string, turn_into_array, commas_and_int):
    if a_string.endswith('\t'):
        a_string = a_string[:-1]
    a_string = a_string.replace(']','')
    a_string = a_string.lstrip()
    if commas_and_int:
        a_list = [int(number) for number in a_string.split(',')]
    else:
        a_list = [float(number) for number in a_string.split()]
    if turn_into_array:
        a_list = np.array(a_list)
    return a_list