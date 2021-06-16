.. _How_to_use_output_data_to_obtain_VASP_data_of_systems_with_adsorbed_species:

How to obtain VASP files from the ``xyz`` files of your system with adsorbed species
####################################################################################

Once you have remove all unnecessary files and only have the ``xyz`` files that you want in ``System_with_Adsorbed_Species``, you can them rerun the ``Run_Adsorption.py`` script. Instead of making the ``System_with_Adsorbed_Species`` folder again, ``Adsorber`` will recognise that the ``System_with_Adsorbed_Species`` folder already exists. Instead, ``Adsorber`` will look though the ``System_with_Adsorbed_Species`` folder and convert the ``xyz`` files in ``System_with_Adsorbed_Species`` into directories that contain the ``POSCAR`` of the ``xyz`` file, a ``INCAR``, a ``KPOINTS`` file, and a ``POTCAR`` that contains all the ``POTCAR`` information required for each element in your ``xyz`` file. 

To run ``Adsorber`` a second time, you will first need to include in the same directory as your ``Run_Adsorber.py`` script a new folder called ``VASP_Files``. In ``VASP_Files`` you will need to include the following files and folders:

* ``INCAR``: This is a VASP file that contains all the information required to run the VASP job (https://www.vasp.at/wiki/index.php/INCAR and https://cms.mpi.univie.ac.at/vasp/vasp/INCAR_File.html).
* ``KPOINTS``: The KPOINTS file is used to specify the Bloch vectors (k-points) that will be used to sample the Brillouin zone in your calculation (https://www.vasp.at/wiki/index.php/KPOINTS).
* ``POTCARs``: This is a folder that contains all of the ``POTCAR`` files for all of the different elements in your models. Each of the ``POTCAR`` files in this folder need to be labelled as ``POTCAR_XX``, where ``XX`` is the symbol for the particular element. For example, for the POTCAR to describe Cu, you want to name the POTCAR as ``POTCAR_Cu``, the POTCAR for C should be called ``POTCAR_C``, the POTCAR for H should be called ``POTCAR_H``, .... 

An example of ``VASP_Files`` folders can be found in `Adsorber Examples on Github <https://github.com/GardenGroupUO/Adsorber/tree/main/Example>`_. 

You also want to make sure that your ``Run_Adsorber.py`` script also includes the ``slurm_information`` dictionary that contains the information required to make the ``submit.sl`` file. The ``submit.sl`` file is used to submit a VASP job to Slurm. The information required in the ``slurm_information`` dictionary can be found at :ref:`Information required to make submit.sl siles for submitting files to Slurm <information_required_to_make_submitsl_siles_for_submitting_files_to_slurm>`.

Once you have the ``VASP_Files`` folder with all of these files and the ``slurm_information`` dictionary in your ``Run_Adsorber.py`` script, you can then run the ``Run_Adsorber.py`` script. This will create a new folder called ``System_with_Adsorbed_Species_for_VASP`` which will contain all your ``POSCAR`` files of your system with adsorbed molecules, as well as ``INCAR``, ``KPOINTS``, ``POTCAR``, and ``submit.sl`` files. 

This ``System_with_Adsorbed_Species_for_VASP`` folder may get big, so just check the amount of space that the newly created ``System_with_Adsorbed_Species_for_VASP`` is taking up as it is being created. 