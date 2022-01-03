.. _Part_C1_Preparing_Adsorbed_Systems_For_VASP:

Part C1: Preparing Selected Adsorbed Systems For VASP Optimisation
###################################################################

On this page, we will talk about Part C to using the ``Adsorber`` program. After you have selected the binding sites to adsorb adsorbates onto and have placed their associated ``xyz`` files into ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files`` (with the desired orientations/rotations), Part C of the ``Adsorber`` program will preparing the VASP files for your chosen systems with adsorbates. 

This section will discuss the steps you should take in order to create VASP files for your systems withg adsorbed adsorbates.  

Setting up the  ``partC.py`` input script
-----------------------------------------

To begin, we want to configure the ``partC.py`` script. The ``partC.py`` script looks as follows:

.. literalinclude:: input_files/partC.py
   :language: python
   :caption: partC.py
   :name: partC.py
   :tab-width: 4
   :linenos:

A input variables that are needed are:

* **path_to_VASP_optimised_non_adsorbate_system** (*str.*): This is the directory to your surface or cluster model without adsorbate after you have optimised it with VASP. 

   * For clusters, this should be set to ``path_to_VASP_optimised_non_adsorbate_system = 'Part_A_Non_Adsorbed_Files_For_VASP/system/OUTCAR'`` 
   * For surfaces, this should be pointed to the file that you want to bind your adsorbate to. This may be ``path_to_VASP_optimised_non_adsorbate_system = 'Part_A_Non_Adsorbed_Files_For_VASP/system/OUTCAR'``, or if you have surface converged your surface model, then to the file that represents the surface converged model. 

* **slurm_information** (*dict.*): This dictionary contains all the information about the ``submit.sl`` file required to submit jobs to the Slurm workload Manager (https://slurm.schedmd.com/documentation.html). The ``Adsorber`` program will include these ``submit.sl`` in the folders that contain your VASP jobs for your adsorbed adsorbate systems. 

The following information is required in the ``slurm_information`` dictionaries:

   * ``'project'`` (*str.*): The name of the project to run this on.
   * ``'partition'`` (*str.*): The partition to run this on. 
   * ``'time'`` (*str.*): The length of time to give these jobs. This is given in ‘HH:MM:SS’, where HH is the number of hours, MM is the number of minutes, and SS is the number of seconds to run ``Adsorber`` for.
   * ``'nodes'`` (*int*): The number of nodes to use. Best to set this to 1. 
   * ``'ntasks_per_node'`` (*int*): The number of cpus to run these jobs across on a node for a VASP job. 
   * ``'mem-per-cpu'`` (*str.*): This is the memory that is used per cpu by the job.
   * ``'email'`` (*str.*): This is the email address to send slurm messages to about this job. If you do not want to give an email, write here either ``None`` or ``''``.
   * ``'vasp_version'`` (*str.*): This is the version of VASP that you want to use for your VASP job. Default: ``'VASP/5.4.4-intel-2017a'``
   * ``'vasp_execution'`` (*str.*): This is the command that is required to run a VASP job. Default: ``'vasp_std'``

An example of the **slurm_information** dictionary is given in the above ``partC.py`` example script. 

Other files you need: The ``VASP_Files`` folder
--------------------------------------------------

Before proceeding you want to make sure that you are happy with the files in your ``VASP_Files`` folder. You particularly want to make sure that your ``INCAR`` is how you want it, particularly your setting for ``EDIFFG``. This is because your may want to have a low convergence criteria to initially converge your systems, then tighten your convergence criteria for those systems that have the lowest energies. This is the best way to reduce the amount of computational effort you use to perform these calculations. All the files that are in your ``VASP_Files`` folder are:

* ``INCAR``: This is a VASP file that contains all the information required to run the VASP job (https://www.vasp.at/wiki/index.php/INCAR and https://cms.mpi.univie.ac.at/vasp/vasp/INCAR_File.html).
* ``KPOINTS``: The KPOINTS file is used to specify the Bloch vectors (k-points) that will be used to sample the Brillouin zone in your calculation (https://www.vasp.at/wiki/index.php/KPOINTS).
* ``POTCARs``: This is a folder that contains all of the ``POTCAR`` files for all of the different elements in your models. Each of the ``POTCAR`` files in this folder need to be labelled as ``POTCAR_XX``, where ``XX`` is the symbol for the particular element. For example, for the POTCAR to describe Cu, you want to name the POTCAR as ``POTCAR_Cu``, the POTCAR for C should be called ``POTCAR_C``, the POTCAR for H should be called ``POTCAR_H``, .... 

You want to also include any other files that will be needed. For example, if you are running VASP with the BEEF functional, you need to include the ``vdw_kernel.bindat`` file in the ``VASP_Files`` folder. 

An example of ``VASP_Files`` folders can be found in `Adsorber Examples on Github <https://github.com/GardenGroupUO/Adsorber/tree/main/Example>`_. 

Run ``Adsorber PartC`` 
----------------------

Once you have written your ``general.py``, ``adsorbate.py``, and ``PartC.py`` scripts, you can then run ``Adsorber`` in the terminal with the following input:

.. code-block:: bash

   Adsorber PartC

What will ``Adsorber`` do?
--------------------------

``Adsorber`` will take all the ``.xyz`` that you have placed in ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files`` and convert them into files ready to be run in VASP with the Slurm Workload Manager. 

``Adsorber`` will create a new folder called ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` that contain VASP folders of your selected systems with adsorbates. Each of these VASP folders contain a ``POSCAR`` of the system with adsorbate, as well as the ``INCAR``, ``KPOINTS``, ``POTCAR``, and ``submit.sl`` files, as well as any other files that you need for your VASP calcuations. 

If the VASP folder exists and it contains a ``POSCAR``, this ``POSCAR`` will not be replaced as you may have updated the ``POSCAR`` if your VASP job entered prematurally without converging. If you do want to force override all ``POSCAR`` files, you will want to set ``part_c_force_create_original_POSCAR = True`` in your ``Run_Adsorber.py`` script. 

Note: This ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder may get big, so just check the amount of space that the newly created ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` is taking up as it is being created. 

What do you need to do?
-----------------------

Once you have run ``Adsorber partC`` and you are ready to submit jobs to slurm, see :ref:`Part_C1_Submitting_Jobs_to_Slurm` to learn about how to submit ``VASP`` jobs to slurm using the ``Adsorber`` program. 

What to do if you made a mistake that you want to fix before submitting VASP jobs to slurm
------------------------------------------------------------------------------------------

Here is some toubleshooting advice if you need to make a change or correction.

I accidentally gave wrong settings in the ``INCAR`` or ``submit.sl`` files, or something about my ``KPOINTS`` or ``POTCAR``. What should I do? 
==============================================================================================================================================

If you realise you have entered in wrong settings in the ``INCAR`` or ``submit.sl`` files, or your ``KPOINTS`` or ``POTCAR`` files are wrong, no problem! Make the changes to these files and then rerun the ``Adsorber PartC`` command again. Only those jobs that have not begun to run (i.e. dont have an ``OUTCAR``) will have their VASP files ``INCAR``, ``submit,sl``, ``KPOINTS``, ``POTCAR``, and other vast files (not the ``POSCAR`` though) copied over. Adsorber will not touch those jobs that have an ``OUTCAR`` that are assumed to be running/have finished running. 

I want to add more new places that adsorbates can bind to on the surface of the cluster/surface model in Part B, what do I do here?
===================================================================================================================================

Run your ``Adsorber PartC`` command once you have included all the new binding sites to your ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files`` folder. 

Running the ``Adsorber PartC`` command again will add new folders and VASP files of these new arrangements of adsorbates on the surface of your cluster/surface model in your ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder. 

Your original ``POSCAR`` will not be changed. Only those jobs that have not begun to run (i.e. dont have an ``OUTCAR``) will have their VASP files ``INCAR``, ``submit,sl``, ``KPOINTS``, ``POTCAR``, and other vast files (not the ``POSCAR`` though) copied over. 

``Adsorber`` will not touch those jobs that have an ``OUTCAR`` that are assumed to be running/have finished running. 