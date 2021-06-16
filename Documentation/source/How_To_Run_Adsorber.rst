
.. _How_To_Run_Adsorber:

*Run_Adsorber.py* - Running Adsorber
####################################

In this article, we will look at how to run the genetic algorithm. This program is run though the **Run_Adsorber.py** script, which includes all the information on what cluster to globally optimise and the genetic algorithm settings to use. You can find other examples of ``Run_Adsorber.py`` files at `github.com/GardenGroupUO/Organisms <https://github.com/GardenGroupUO/Organisms>`_ under ``Examples\Playground`` and ``Examples\Example_Run_Files``. Also, you can try out this program by running an example script through a Jupyter notebook. See Examples_of_Running_GA to get access to examples of running Organisms through this Jupyter notebook!

.. contents::
    :depth: 2
    :local:

Running the Adsorber Program
****************************

We will explain how the ``Run_Adsorber.py`` code works by running though the example shown below:

.. literalinclude:: Run_Adsorber.py
	:language: python
	:caption: Run_Adsorber.py
	:name: Run_Adsorber.py
	:tab-width: 4
	:linenos:

Lets go through each part of the Run_Adsorber.py file one by one to understand how to use it. 

1) Things to import into this script
====================================

First you will want to import the ``Adsorber`` program, as well as any other methods that you want to use to import atoms and molecules to adsorb upon your cluster or surface. Here, we have imported the ``molecule`` method from the ``ase.build`` module.

.. literalinclude:: Run_Adsorber.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 1
	:lines: 1-2

2) Initial inputs for ``Adsorber``
==================================

To begin, there are three inputs you will need to give to Adsorber. These are:

* **system_name** (*str.*): The name of the file of the cluster or the surface model that you will like to import into Adsorber. This file should be a ``.xyz`` or ``.traj`` file. 
* **cluster_or_surface_model** (*str.*): This tells ``Adsorber`` if you are wanting to adsorb atoms and clusters to the surface of a cluster or a surface model. If you are dealing with a cluster, set ``cluster_or_surface_model = 'cluster'``, else if you are dealing with a surface model, set ``cluster_or_surface_model = 'surface model'`` and make sure that the normal to the surface points in the z direction. 
* **cutoff** (*float* or *dict.*): This is the maximum distance between atoms to be considered ``bonded`` or ``neighbouring``. This is used to determine bridging, three-fold, and four-fold sites. This is given as a float for monoatomic cluster and surface systems, or for a multiatomic system if you are happy for the max bonding distance between any two elements to be the same. If you would like different element pairs to have different maximum bonding distances, this is given as a dictionary. For example, for a CuPd system: ``cutoff = {'Cu': 3.2, 'Pd': 3.6, ('Cu','Pd'): 3.4}``
* **surface_atoms** (*list of ints*): This is a list of the indices of all the surface atoms in your cluster or surface model. See :ref:`How_To_Use_Adsorber` for how to determine which of your atoms are surface atoms and to get those clusters indices to add to the ``surface_atoms`` list. Note that if there are surface atoms that you do not want molecules to adsorb to, dont include them in this list. 

This is given in this example as below:

.. literalinclude:: Run_Adsorber.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 5
	:lines: 5-9

.. _add_atoms_and_molecules_on_to_surface_of_model:

3) Add the Atoms and Molecules on to the Surface of your Cluster/Surface Model
==============================================================================

We will now add all the atoms and molecules that you want to adsorb to the surface of your cluster or surface model. We first want to import all of these into this script. In ASE, there are a variety of molecules you can obtain from the ``molecule`` method in the ``ase.build`` module. This is imported into the ``Run_Adsorber.py`` script with the following

.. code-block:: python

	from ase.build import molecule

This is what we have done here. You can also import molecules from other ``.xyz`` or ``.traj`` files with the ``read`` method from ASE:

.. code-block:: python

	from ase.io import read

For each atom and molecule that you make you want to add it to a dictionary that has the following inputs:

* **name** (*str.*): The name you want to give for this atom or molecule
* **molecule** (*ase.Atoms*): The is the ``Atoms`` object for the atom or molecule, as obtained from the ``molecule`` or ``read`` method as mentioned above.
* **distance_of_adatom_from_surface** (*float*): This is the binding distance that you would like the atom or molecule to be initially placed from the cluster or surface model before you perform further optimisation with DFT. 

For single atoms, this is all that is needed. If you want to adsorb molecules that have two or more atoms in it, you want to give two or three additional inputs into this dictionary.

* **index** (*int.*): This is the index of the atom in the molecule to adsorb to the surface for the cluster/surface model. See :ref:`How_To_Use_Adsorber` for more information on how to select the index of the atom in the molecule you would like to be adsorbed to the surface. 
* **axis** (*str./list/tuple*): This is the axis in your molecule that you would like to point away from the surface of the cluster/surface model, as well as to rotate your moleule around (if you would like to rotate your molecule around the axis). See :ref:`How_To_Use_Adsorber` for more information for how to specify this axis. 
* **rotations** (*list/tuple*, optional): These are the angles of rotation that you would like to rotate the molecules around the **axis** on the surface of your cluster/surface model. If you have a linear molecule that is alligned to the **axis** or you do not want to rotate your molecule around the **axis**, you do not need to add this as this is an optional input. See :ref:`How_To_Use_Adsorber` for more information about how to specify how to best rotate your molecule about the **axis** on the surface of your cluster/surface model. 

An example of this is shown below:

.. literalinclude:: Run_Adsorber.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 13
	:lines: 13-18

Once you have made a dictionary for all of the atoms and molecules you would like to adsorb to the surface of your cluster/surface model, you want to add them all to a list, as shown below:

.. literalinclude:: Run_Adsorber.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 100
	:lines: 100

The full example of the atoms and molecules that have been adsorbed to this cluster (called ``15-3-3629.xyz``) is shown below:

.. literalinclude:: Run_Adsorber.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 11
	:lines: 11-100

.. _information_required_to_make_submitsl_siles_for_submitting_files_to_slurm:

4) Information required to make ``submit.sl`` siles for submitting files to Slurm
=================================================================================

``Adsorber`` is able to create folders with the files required to run VASP jobs of your system for all of the adsorbed species and orientations that you would like to consider. Do you this, you will want to include a dictionary called ``slurm_information`` that contains all the information about the ``submit.sl`` file required to submit jobs to the Slurm workload Manager (https://slurm.schedmd.com/documentation.html). The following information is required in the ``slurm_information`` dictionary:

	* ``'project'`` (*str.*): The name of the project to run this on.
	* ``'partition'`` (*str.*): The partition to run this on.
	* ``'time'`` (*str.*): The length of time to give these jobs. This is given in ‘HH:MM:SS’, where HH is the number of hours, MM is the number of minutes, and SS is the number of seconds to run ``Adsorber`` for.
	* ``'nodes'`` (*int*): The number of nodes to use. Best to set this to 1. 
	* ``'ntasks_per_node'`` (*int*): The number of cpus to run these jobs across on a node for a VASP job. 
	* ``'mem-per-cpu'`` (*str.*): This is the memory that is used per cpu by the job.
	* ``'email'`` (*str.*): This is the email address to send slurm messages to about this job. If you do not want to give an email, write here either ``None`` or ``''``.
	* ``'vasp_version'`` (*str.*): This is the version of VASP that you want to use for your VASP job. Default: ``'VASP/5.4.4-intel-2017a'``
	* ``'vasp_execution'`` (*str.*): This is the command that is required to run a VASP job. Default: ``'vasp_std'``

An example of a ``slurm_information`` dictionary in the ``Run_Adsorber.py`` script is shown below:

.. literalinclude:: Run_Adsorber.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 102
	:lines: 102-114

Run the Adsorber Program!
=========================

You have got to the end of all the parameter setting stuff! Now on to the fun stuff! The next part of the ``Run_Adsorber.py`` file will run the Adsorber program. This is written as follows in the ``Run_Adsorber.py`` script:

.. literalinclude:: Run_Adsorber.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 117
	:lines: 117-118
