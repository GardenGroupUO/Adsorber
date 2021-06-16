
.. _How_to_submit_files_to_slurm:

How do I submit files to Slurm to perform DFT local optimisations in VASP
#########################################################################

As mentioned in :ref:`How_to_use_output_data_to_obtain_VASP_data_of_systems_with_adsorbed_species`, after running the ``Run_Adsorber.py`` script for a second time you will get a new folder called ``System_with_Adsorbed_Species_for_VASP``. This ``System_with_Adsorbed_Species_for_VASP`` folder will contain your system with all the molecule adsorbed to the various binding sites across the system is the format required to run in VASP. Each folder in ``System_with_Adsorbed_Species_for_VASP`` will contain:

* ``POSCAR``: Contains the structural information for a system with an adsorbed atom or molecule. 
* ``INCAR``: This is a VASP file that contains all the information required to run the VASP job (https://www.vasp.at/wiki/index.php/INCAR and https://cms.mpi.univie.ac.at/vasp/vasp/INCAR_File.html).
* ``KPOINTS``: The KPOINTS file is used to specify the Bloch vectors (k-points) that will be used to sample the Brillouin zone in your calculation (https://www.vasp.at/wiki/index.php/KPOINTS).
* ``POTCAR``: This is the file that contains all the information about the functional that is being used. This ``POTCAR`` file contains each of the individual ``POTCAR`` files for each element that is found in the ``POSCAR`` (https://www.vasp.at/wiki/index.php/POTCAR). 
* ``submit.sl``: This file will allow the VASP job to be submitted to Slurm. 

Now you can submit all your jobs to Slurm. To do this, ``cd`` into the ``System_with_Adsorbed_Species_for_VASP`` folder and enter into the terminal:

.. code-block:: bash

	Run_Adsorber_submitSL_slurm.py

This will run the ``Run_Adsorber_submitSL_slurm.py`` subsidary program that is designed to submit all ``submit.sl``  jobs to Slurm. Just sit back and relax, and let this program do all the submitting for you.