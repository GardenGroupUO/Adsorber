# ----------------------------------------------------------------------------------------------------------------
# Part A Information
# ----------------------------------------------------------------------------------------------------------------
# slurm informaion for making the submit.sl files for submitting VASP jobs in slurm
slurm_information_system = {}
slurm_information_system['project'] = 'uoo02568'
slurm_information_system['partition'] = 'large'
slurm_information_system['time'] = '50:00:00'
slurm_information_system['nodes'] = 1
slurm_information_system['ntasks_per_node'] = 12
slurm_information_system['mem-per-cpu'] = '1200MB'
slurm_information_system['email'] = 'geoffreywealslurmnotifications@gmail.com'
slurm_information_system['vasp_version'] = 'VASP/5.3.5-intel-2017a-VTST-BEEF'
slurm_information_system['vasp_execution'] = 'vasp_cd'
# ----------------------------------------------------------------------------------------------------------------
# Add here any other atoms and molecules that you need to locally optimise in VASP for energy calculations
from ase.build import molecule

other_molecules_to_obtain_VASP_energies_for = []

graphene = molecule('C')
graphene.center(vacuum=10.0)
graphene_optimise_energy = {'name': 'graphene', 'molecule': graphene}
#other_molecules_to_obtain_VASP_energies_for.append(graphene_optimise_energy)

H2 = molecule('H2')
H2.center(vacuum=10.0)
H2_optimised_energy = {'name': 'H2', 'molecule': H2}
other_molecules_to_obtain_VASP_energies_for.append(H2_optimised_energy)

H2O = molecule('H2O')
H2O.center(vacuum=10.0)
H2O_optimised_energy = {'name': 'H2O', 'molecule': H2O}
other_molecules_to_obtain_VASP_energies_for.append(H2O_optimised_energy)

CO2 = molecule('CO2')
CO2.center(vacuum=10.0)
CO2_optimise_energy = {'name': 'CO2', 'molecule': CO2}
other_molecules_to_obtain_VASP_energies_for.append(CO2_optimise_energy)

# ----------------------------------------------------------------------------------------------------------------
# slurm informaion for making the submit.sl files for submitting VASP jobs in slurm
slurm_information_adsorbates_and_other = {}
slurm_information_adsorbates_and_other['project'] = 'uoo02568'
slurm_information_adsorbates_and_other['partition'] = 'large'
slurm_information_adsorbates_and_other['time'] = '5:00:00'
slurm_information_adsorbates_and_other['nodes'] = 1
slurm_information_adsorbates_and_other['ntasks_per_node'] = 12
slurm_information_adsorbates_and_other['mem-per-cpu'] = '1200MB'
slurm_information_adsorbates_and_other['email'] = 'geoffreywealslurmnotifications@gmail.com'
slurm_information_adsorbates_and_other['vasp_version'] = 'VASP/5.3.5-intel-2017a-VTST-BEEF'
slurm_information_adsorbates_and_other['vasp_execution'] = 'vasp_cd'
# ----------------------------------------------------------------------------------------------------------------