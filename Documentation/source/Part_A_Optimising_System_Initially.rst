
.. _Part_A_Optimising_System_Initially:

Part A: How to optimise your system, as well as optimise adsorbates and other molecules
#######################################################################################

On this page, we will talk about Part A to using the ``Adsorber`` program. In Part A, the ``Adsorber`` program will create VASP files of your system, be in a cluster or surface model, as well as your adsorbates in vacuum. Your VASP optimised system is then used to adsorb adsorbates to in Part B and C of the ``Adsorber`` program. VASP files of the adsorbates are create if you want to reference your VASP energies to it. You can also create VASP files of any other atoms or molecules that you want to if you want to reference your system to these instead of your adsorbates.

Setting up the  ``partA.py`` input script
-----------------------------------------

To begin, we want to configure the ``partA.py`` script. The ``partA.py`` script looks as follows:

.. literalinclude:: input_files/partA.py
	:language: python
	:caption: partA.py
	:name: partA.py
	:tab-width: 4
	:linenos:

An input variable that is needed is **other_molecules_to_obtain_VASP_energies_for** (*list*). This is a list that contains the information of all the other atoms and molecules that you would like to locally optimise with VASP (using the same VASP settings and POTCAR) for energy calculations later on in your studies. To do this, you want to add your atoms and molecules in the same way as before, such as with ``xyz`` files or using the  ``molecule`` method in the ``ase.build`` module, as shown above. 

For each atom and molecule that you make, you want to add it to a dictionary that has the following inputs:

* **name** (*str.*): The name you want to give for this atom or molecule.
* **molecule** (*ase.Atoms*): The is the ``Atoms`` object for the atom or molecule, as obtained from the ``molecule`` or ``read`` method as mentioned above.

Example of this are shown above for obtaining VASP minimised energies only of H :sub:`2` and H :sub:`2` O:

The other input variables that are needed are **slurm_information_system** (*dict.*) and **slurm_information_adsorbates_and_other** (*dict.*). These are dictionaries that contain all the information about the ``submit.sl`` file required to submit jobs to the Slurm workload Manager (https://slurm.schedmd.com/documentation.html). 
The ``Adsorber`` program will include these ``submit.sl`` in the folders that contain your VASP jobs. 

The other inputs that are required are the ``slurm_information_system`` and the ``slurm_information_adsorbates_and_other``. These dictionaries contain all the information that is needed to create ``submit.sl`` files for your system, as well as for your adsorbates and other molecules you wish to optimise with VASP.

The following information is required in the ``slurm_information_system`` and the ``slurm_information_adsorbates_and_other`` dictionaries are:

	* ``'project'`` (*str.*): The name of the project to run this on.
	* ``'partition'`` (*str.*): The partition to run this on. 
	* ``'time'`` (*str.*): The length of time to give these jobs. This is given in ‘HH:MM:SS’, where HH is the number of hours, MM is the number of minutes, and SS is the number of seconds to run ``Adsorber`` for.
	* ``'nodes'`` (*int*): The number of nodes to use. Best to set this to 1. 
	* ``'ntasks_per_node'`` (*int*): The number of cpus to run these jobs across on a node for a VASP job. 
	* ``'mem-per-cpu'`` (*str.*): This is the memory that is used per cpu by the job.
	* ``'email'`` (*str.*): This is the email address to send slurm messages to about this job. If you do not want to give an email, write here either ``None`` or ``''``.
	* ``'vasp_version'`` (*str.*): This is the version of VASP that you want to use for your VASP job. Default: ``'VASP/5.4.4-intel-2017a'``
	* ``'vasp_execution'`` (*str.*): This is the command that is required to run a VASP job. Default: ``'vasp_std'``

An example of the ``slurm_information_system`` and the ``slurm_information_adsorbates_and_other`` dictionaries are given in the above ``partA.py`` example script. 

Other files you need: The ``VASP_Files`` folder
--------------------------------------------------

You also need to create a folder called ``VASP_Files`` that contains the following files and folders:

* ``INCAR``: This is a VASP file that contains all the information required to run the VASP job (https://www.vasp.at/wiki/index.php/INCAR and https://cms.mpi.univie.ac.at/vasp/vasp/INCAR_File.html).
* ``KPOINTS``: The KPOINTS file is used to specify the Bloch vectors (k-points) that will be used to sample the Brillouin zone in your calculation (https://www.vasp.at/wiki/index.php/KPOINTS).
* ``POTCARs``: This is a folder that contains all of the ``POTCAR`` files for all of the different elements in your models. Each of the ``POTCAR`` files in this folder need to be labelled as ``POTCAR_XX``, where ``XX`` is the symbol for the particular element. For example, for the POTCAR to describe Cu, you want to name the POTCAR as ``POTCAR_Cu``, the POTCAR for C should be called ``POTCAR_C``, the POTCAR for H should be called ``POTCAR_H``, .... 

You want to also include any other files that will be needed. For example, if you are running VASP with the BEEF functional, you need to include the ``vdw_kernel.bindat`` file in the ``VASP_Files`` folder. 

An example of ``VASP_Files`` folders can be found in `Adsorber Examples on Github <https://github.com/GardenGroupUO/Adsorber/tree/main/Example>`_. 

Run ``Adsorber PartA`` 
----------------------

Once you have written your ``general.py``, ``adsorbate.py``, and ``partA.py`` scripts, you can then run ``Adsorber`` in the terminal with the following input:

.. code-block:: bash

	Adsorber PartA

What will ``Adsorber`` do?
--------------------------

This will create a folder called ``Part_A_Non_Adsorbed_Files_For_VASP``. In this folder is another folder called ``system`` that contains all the VASP files required to locally optimise your system in VASP. This ``Part_A_Non_Adsorbed_Files_For_VASP`` folder also contains all the VASP files of your adsorbates that you can also locally optimise in VASP. This is often required to determine in the adsorption energy of your adsorbate onto your system

.. math::

	E_{abs} = E(system+adsorbate) - (E(system) + E(adsorbate))

or if you are defining your adsorption energy with reference species, such as C from graphene, H from H :sub:`2` , and O from H :sub:`2` O: 

.. math::

	E_{abs} = E(system+adsorbate) - (E(system) + E(each\;element\;in\;the\;adsorbate\;in\;stiochiometic\;amounts))

Once you have run VASP on your system and all your adsorbates, proceed to Part B (:ref:`Part_B1_Adsorb_Adsorbates_to_System`).

Note that we have not used this program to get the energy of a C atom in graphene. This is because ``Adsorber`` is not designed to obtain lattice constants. See the ``LatticeFinder`` program to obtain this (see https://github.com/GardenGroupUO/LatticeFinder). 

Note regarding surface models
-----------------------------

This program has not been set up to make layer-converged models of surfaces. You may need to do this yourself. 

