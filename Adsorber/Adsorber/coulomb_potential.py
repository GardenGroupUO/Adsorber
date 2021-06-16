import numpy as np

from ase.calculators.calculator import Calculator
from ase.neighborlist import neighbor_list

from ase.constraints import FixAtoms, FixBondLengths

def get_unit_vector(vector):
	unit_vector = vector / np.linalg.norm(vector)
	return unit_vector

class coulomb_potential(Calculator):
	implemented_properties = ['energy', 'forces']
	# k from https://en.wikipedia.org/wiki/Coulomb_constant in units eV·Å·e−2
	default_parameters = {'k': 14.3996,'Q': 1.0,'q': 1.0,'rcut': 20.0}
	
	def __init__(self, **kwargs):
		Calculator.__init__(self, **kwargs)
		self.previous_energy = float('inf')

	def calculate(self, atoms=None, properties=['energy'],system_changes=['positions', 'numbers', 'cell', 'pbc', 'charges', 'magmoms']):
		Calculator.calculate(self, atoms, properties, system_changes)

		k = self.parameters.k
		Q = self.parameters.Q
		q = self.parameters.q
		rcut = self.parameters.rcut

		forces = np.zeros((len(self.atoms), 3))
		coefficient = k*Q*q

		ii, jj, dd, DD = neighbor_list('ijdD', atoms, rcut)
		dhat = (DD / dd[:, None]).T

		energy = (coefficient / dd).sum()
		F = -((coefficient / dd**2.0) * dhat).T
		for dim in range(3):
			forces[:, dim] = np.bincount(ii, weights=F[:, dim],minlength=len(atoms))
		'''
		# ------------------------------------------------------------
		# remove component of force that is parallel to the sum of vectors of FixBondLength, FixBondLengths
		bonding_pairs_indices = []
		for constraints in atoms.constraints:
			if isinstance(constraints,FixBondLengths):
				for pair in constraints.pairs:
					bonding_pairs_indices.append(tuple(pair))
		pointing_vector = np.array([0.0,0.0,0.0])
		bonding_pairs_indices = tuple(set(bonding_pairs_indices))
		for bonding_pair_indices in bonding_pairs_indices:
			bonding_pair_indices = sorted(bonding_pair_indices)
			vector = atoms[bonding_pair_indices[1]].position - atoms[bonding_pair_indices[0]].position
			pointing_vector += vector
		pointing_vector = get_unit_vector(pointing_vector)
		force_on_hydrogen = forces[-1, :]
		# get vector projection onto unit vector: https://en.wikipedia.org/wiki/Vector_projection
		project_vector = np.dot(force_on_hydrogen,pointing_vector)*pointing_vector
		forces[-1, :] -= project_vector
		#import pdb; pdb.set_trace()
		'''
		# ------------------------------------------------------------
		# turn off forces for atoms that are fixed in position
		'''
		fixed_atom_indices = []
		for constraints in atoms.constraints:
			if isinstance(constraints,FixAtoms):
				fixed_atom_indices += tuple(constraints.get_indices())
		fixed_atom_indices = tuple(set(fixed_atom_indices))
		for index in fixed_atom_indices:
			forces[index, :] = np.array([0.0, 0.0, 0.0])
		'''
		#print(forces)
		# ------------------------------------------------------------
		self.results['energy'] = energy
		self.results['forces'] = forces