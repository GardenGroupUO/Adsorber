from ase.build import molecule
from Adsorber import Adsorber_Program

# ------------------------------------------------------------------------------------------------------------------------------------
# Initial inputs for the Adsorber program
name = '15-3-3629.xyz'
cluster_or_surface_model = 'cluster'
cutoff = 3.2
surface_atoms = [11,25,28,13,3,8,6,23,22,59,34,62,66,1,0,4,30,15,14,16,5,12,29,2,7,10,24,26,70,35,47,50,60,63,48,39,41,44,54,68,76,71,32,31,74,42,56,52,43,40,46,61,53,45,57,72,73,77]
# ------------------------------------------------------------------------------------------------------------------------------------
# Give the Atoms objects for the atoms and molecules you want to adsorb to your cluster or surface model

COOH = molecule('HCOOH') # note the carbon is index 1
del COOH[4] # remove the hydrogen atom
COOH_axis = (0.1,-1,0)
distance_of_adatom_from_surface = 1.25
rotations = range(0,360,10)
COOH_adsorbed_species = {'name': 'COOH', 'molecule': COOH, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 1, 'axis': COOH_axis, 'rotations': rotations}

CO = molecule('CO') # note the carbon is index 1
CO_axis = 'z'
distance_of_adatom_from_surface = 1.25
CO_adsorbed_species = {'name': 'CO', 'molecule': CO, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 1, 'axis': CO_axis}

# --------------------------------------------
# option1
COH = molecule('H2COH') # note the carbon is index 0
del COH[4] # remove the hydrogen atom
del COH[3] # remove the hydrogen atom
COH_axis = '-x'
distance_of_adatom_from_surface = 1.25
rotations = range(0,360,10)
COH_adsorbed_species = {'name': 'COH', 'molecule': COH, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': COH_axis, 'rotations': rotations}

#option2
CHO = molecule('HCO') # note the carbon is index 0
CHO_axis = (-(3.0**0.5)/2.0,-1.0/2.0,0)
rotations = range(0,360,10)
CHO_adsorbed_species = {'name': 'CHO', 'molecule': CHO, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CHO_axis, 'rotations': rotations}
# --------------------------------------------
# option1
CH2O = molecule('H2CO') # note the carbon is index 1
CH2O_axis = 'x'
distance_of_adatom_from_surface = 1.25
rotations = range(0,360,10)
CH2O_adsorbed_species = {'name': 'CH2O', 'molecule': CH2O, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 1, 'axis': CH2O_axis, 'rotations': rotations}

# option1
CHOH = molecule('H2COH') # note the carbon is index 0
del CHOH[3]
CHOH_axis = (-1,-1,0)
distance_of_adatom_from_surface = 1.25
rotations = range(0,360,10)
CHOH_adsorbed_species = {'name': 'CHOH', 'molecule': CHOH, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CHOH_axis, 'rotations': rotations}
# --------------------------------------------
# new option 1
CH3O = molecule('CH3O') # note the oxygen is index 1
CH3O_axis = '-y'
distance_of_adatom_from_surface = 1.25
CH3O_adsorbed_species = {'name': 'CH3O', 'molecule': CH3O, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 1, 'axis': CH3O_axis}

# new option 2
CH2OH = molecule('CH3OH') # carbon is index 0
del CH2OH[2] # remove the hydrogen atom
CH2OH_axis = (1,-1,0)
distance_of_adatom_from_surface = 1.25
rotations = range(0,360,10)
CH2OH_adsorbed_species = {'name': 'CH2OH', 'molecule': CH2OH, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CH2OH_axis, 'rotations': rotations}
# --------------------------------------------
# new new option 1
CH2 = molecule('CH4') # carbon is index 0
del CH2[4] # remove the hydrogen atom
del CH2[3] # remove the hydrogen atom
CH2_axis = 'z'
distance_of_adatom_from_surface = 1.25
rotations = range(0,180,10)
CH2_adsorbed_species = {'name': 'CH2', 'molecule': CH2, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CH2_axis, 'rotations': rotations}

CH3 = molecule('CH4') # carbon is index 0
del CH3[4] # remove the hydrogen atom
CH3_axis = (1,-1,1)
distance_of_adatom_from_surface = 1.25
rotations = range(0,120,10)
CH3_adsorbed_species = {'name': 'CH3', 'molecule': CH3, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': CH3_axis, 'rotations': rotations}

# new new option 2
O = molecule('O')
distance_of_adatom_from_surface = 1.25
O_adsorbed_species = {'name': 'O', 'molecule': O, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface}

OH = molecule('OH') # note the oxygen is index 0
OH_axis = '-z'
distance_of_adatom_from_surface = 1.25
OH_adsorbed_species = {'name': 'OH', 'molecule': OH, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface, 'index': 0, 'axis': OH_axis}

C = molecule('C')
distance_of_adatom_from_surface = 1.25
C_adsorbed_species = {'name': 'C', 'molecule': C, 'distance_of_adatom_from_surface': distance_of_adatom_from_surface}

adsorbed_species = [COOH_adsorbed_species, CO_adsorbed_species, COH_adsorbed_species, CHO_adsorbed_species, CH2O_adsorbed_species, CHOH_adsorbed_species, CH3O_adsorbed_species, CH2OH_adsorbed_species, CH2_adsorbed_species, CH3_adsorbed_species, O_adsorbed_species, OH_adsorbed_species, C_adsorbed_species]
# ------------------------------------------------------------------------------------------------------------------------------------
# slurm informaion for making the submit.sl files for submitting VASP jobs in slurm

slurm_information = {}
slurm_information['project'] = 'uoo02568'
slurm_information['partition'] = 'large'
slurm_information['time'] = '48:00:00'
slurm_information['nodes'] = 1
slurm_information['ntasks_per_node'] = 8
slurm_information['mem-per-cpu'] = '3G'
slurm_information['email'] = 'geoffreywealslurmnotifications@gmail.com'
slurm_information['vasp_version'] = 'VASP/5.4.4-intel-2017a'
slurm_information['vasp_execution'] = 'vasp_std'

# ------------------------------------------------------------------------------------------------------------------------------------
# Run the Adsorber program
Adsorber_Program(name,cluster_or_surface_model,cutoff,surface_atoms,adsorbed_species,slurm_information)
