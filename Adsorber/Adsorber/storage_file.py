import numpy as np

def write_data_file(data_storage_file,bind_site_data_types,above_atom_binding_sites,above_bridge_binding_sites,above_three_fold_sites,above_four_fold_sites):
    def write_to_datafileTXT(datafileTXT,binding_sites,description):
        counter = 1
        datafileTXT.write('The following sites are binding sites for '+str(description)+'.\n')
        datafileTXT.write('Site\t\t\tBinding Position\t\t\t\t\t\tSurface Position\n')
        for binding_position, surface_position in binding_sites:
            datafileTXT.write('Site '+str(counter)+'\t'+str(binding_position)+' \t'+str(surface_position)+'\n')
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
            if line.startswith('Site\t\t\tBinding Position\t\t\t\t\t\tSurface Position'):
                continue
            elif line.startswith('The following sites are binding sites for '+str(bind_site_data_types[index])+'.'):
                write_to_list = True
            elif line.startswith('--------------------------------------------------------------') and write_to_list == True:
                write_to_list = False
                index += 1
            elif write_to_list:
                line = line.rstrip()
                index2 = 0
                datum = ['','']
                write_to_second_list = False
                for character in line:
                    if character == '[':
                        write_to_second_list = True
                    elif character == ']':
                        datum[index2] = datum[index2].split()
                        for index_sub in range(len(datum[index2])):
                            datum[index2][index_sub] = float(datum[index2][index_sub])
                        write_to_second_list = False
                        index2 += 1
                    elif write_to_second_list:
                        datum[index2] += character
                binding_position, surface_position = datum
                binding_position = np.array(binding_position)
                surface_position = np.array(surface_position)
                datum = (binding_position,surface_position)
                data[index].append(datum)
    above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites = data
    return above_atom_binding_sites, above_bridge_binding_sites, above_three_fold_sites, above_four_fold_sites