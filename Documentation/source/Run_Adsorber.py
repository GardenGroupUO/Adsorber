from ase.build import molecule
from Adsorber import Adsorber_Program

# ------------------------------------------------------------------------------------------------------------------------------------
# Initial inputs for the Adsorber program
part_to_perform = 'Part B'

# General Variables
cluster_or_surface_model = 'cluster'

# Part A information
system_filename = '15-3-3629_with_vacuum_6.0_Ang.xyz'

# Part B information
path_to_VASP_optimised_non_adsorbate_system = 'Part_A_Non_Adsorbed_Files_For_VASP/system/OUTCAR'
cutoff = 3.5
surface_atoms = [11,25,28,13,3,8,6,23,22,59,34,62,66,1,0,4,30,15,14,16,5,12,29,2,7,10,24,26,70,35,47,50,60,63,48,39,41,44,54,68,76,71,32,31,74,42,56,52,43,40,46,61,53,45,57,72,73,77]

# ------------------------------------------------------------------------------------------------------------------------------------
# Give the Atoms objects for the atoms and molecules you want to adsorb to your cluster or surface model
adsorbed_species = []

COOH_symmetric = molecule('HCOOH') # note the carbon is index 1
COOH_symmetric.center(vacuum=10.0)
del COOH_symmetric[4] # remove the hydrogen atom
COOH_symmetric_axis = (0.1,-1,0)
distance_of_adatom_from_surface = 1.5
rotations = 'automatic' #range(0,360,10)
COOH_symmetric_adsorbed_species = {'name': 'COOH_symmetric', 'molecule': COOH_symmetric, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 1, 'axis': COOH_symmetric_axis, 'rotations': rotations, 'sites_to_bind_adsorbate_to': ['Top_Sites','Bridge_Sites','Three_Fold_Sites']}
adsorbed_species.append(COOH_symmetric_adsorbed_species)

COOH_O_tilted = molecule('HCOOH') # note the carbon is index 1
COOH_O_tilted.center(vacuum=10.0)
del COOH_O_tilted[4] # remove the hydrogen atom
COOH_O_tilted_axis = (-0.4,-1,0)
distance_of_adatom_from_surface = 1.5
rotations = 'automatic' #range(0,360,10)
COOH_O_tilted_adsorbed_species = {'name': 'COOH_O_tilted', 'molecule': COOH_O_tilted, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 1, 'axis': COOH_O_tilted_axis, 'rotations': rotations, 'sites_to_bind_adsorbate_to': 'Top_Sites'}
#adsorbed_species.append(COOH_O_tilted_adsorbed_species)

CO = molecule('CO') # note the carbon is index 1
CO.center(vacuum=10.0)
CO_axis = 'z'
distance_of_adatom_from_surface = 1.5
CO_adsorbed_species = {'name': 'CO', 'molecule': CO, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 1, 'axis': CO_axis}
#adsorbed_species.append(CO_adsorbed_species)

# --------------------------------------------
# option1
COH = molecule('H2COH') # note the carbon is index 0
COH.center(vacuum=10.0)
del COH[4] # remove the hydrogen atom
del COH[3] # remove the hydrogen atom
COH_axis = '-x'
distance_of_adatom_from_surface = 1.5
rotations = 'automatic' #range(0,360,10)
COH_adsorbed_species = {'name': 'COH', 'molecule': COH, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': COH_axis, 'rotations': rotations}
#adsorbed_species.append(COH_adsorbed_species)

#option2
CHO = molecule('HCO') # note the carbon is index 0
CHO.center(vacuum=10.0)
CHO_axis = (-(3.0**0.5)/2.0,-1.0/2.0,0)
rotations = 'automatic' #range(0,360,10)
CHO_adsorbed_species = {'name': 'CHO', 'molecule': CHO, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CHO_axis, 'rotations': rotations}
#adsorbed_species.append(CHO_adsorbed_species)
# --------------------------------------------
# option1
CH2O = molecule('H2CO') # note the carbon is index 1
CH2O.center(vacuum=10.0)
CH2O_axis = 'x'
distance_of_adatom_from_surface = 1.5
rotations = 'automatic' #range(0,360,10)
CH2O_adsorbed_species = {'name': 'CH2O', 'molecule': CH2O, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 1, 'axis': CH2O_axis, 'rotations': rotations}
#adsorbed_species.append(CH2O_adsorbed_species)

# option1
CHOH = molecule('H2COH') # note the carbon is index 0
CHOH.center(vacuum=10.0)
del CHOH[3]
CHOH_axis = (-1,-1,0)
distance_of_adatom_from_surface = 1.5
rotations = 'automatic' #range(0,360,10)
CHOH_adsorbed_species = {'name': 'CHOH', 'molecule': CHOH, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CHOH_axis, 'rotations': rotations}
#adsorbed_species.append(CHOH_adsorbed_species)
# --------------------------------------------
# new option 1
CH3O = molecule('CH3O') # note the oxygen is index 1
CH3O.center(vacuum=10.0)
CH3O_axis = '-y'
distance_of_adatom_from_surface = 1.5
CH3O_adsorbed_species = {'name': 'CH3O', 'molecule': CH3O, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 1, 'axis': CH3O_axis}
#adsorbed_species.append(CH3O_adsorbed_species)

# new option 2
CH2OH = molecule('CH3OH') # carbon is index 0
CH2OH.center(vacuum=10.0)
del CH2OH[2] # remove the hydrogen atom
CH2OH_axis = (1,-1,0)
distance_of_adatom_from_surface = 1.5
rotations = 'automatic' #range(0,360,10)
CH2OH_adsorbed_species = {'name': 'CH2OH', 'molecule': CH2OH, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CH2OH_axis, 'rotations': rotations}
#adsorbed_species.append(CH2OH_adsorbed_species)
# --------------------------------------------
# new new option 1
CH2 = molecule('CH4') # carbon is index 0
CH2.center(vacuum=10.0)
del CH2[4] # remove the hydrogen atom
del CH2[3] # remove the hydrogen atom
CH2_axis = 'z'
distance_of_adatom_from_surface = 1.5
rotations = 'automatic' #range(0,180,10)
CH2_adsorbed_species = {'name': 'CH2', 'molecule': CH2, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CH2_axis, 'rotations': rotations}
#adsorbed_species.append(CH2_adsorbed_species)

CH3 = molecule('CH4') # carbon is index 0
CH3.center(vacuum=10.0)
del CH3[4] # remove the hydrogen atom
CH3_axis = (1,-1,1)
distance_of_adatom_from_surface = 1.5
rotations = 'automatic' #range(0,120,10)
CH3_adsorbed_species = {'name': 'CH3', 'molecule': CH3, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CH3_axis, 'rotations': rotations}
#adsorbed_species.append(CH3_adsorbed_species)

# new new option 2
O = molecule('O')
O.center(vacuum=10.0)
distance_of_adatom_from_surface = 1.5
O_adsorbed_species = {'name': 'O', 'molecule': O, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface}
#adsorbed_species.append(O_adsorbed_species)

OH = molecule('OH') # note the oxygen is index 0
OH.center(vacuum=10.0)
OH_axis = '-z'
distance_of_adatom_from_surface = 1.5
OH_adsorbed_species = {'name': 'OH', 'molecule': OH, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': OH_axis}
#adsorbed_species.append(OH_adsorbed_species)

C = molecule('C')
C.center(vacuum=10.0)
distance_of_adatom_from_surface = 1.5
C_adsorbed_species = {'name': 'C', 'molecule': C, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface}
#adsorbed_species.append(C_adsorbed_species)

# ------------------------------------------------------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------------------------------------------------------
# Run the Adsorber program
Adsorber_Program(part_to_perform,cluster_or_surface_model,system_filename,path_to_VASP_optimised_non_adsorbate_system,cutoff,surface_atoms,adsorbed_species,slurm_information)
