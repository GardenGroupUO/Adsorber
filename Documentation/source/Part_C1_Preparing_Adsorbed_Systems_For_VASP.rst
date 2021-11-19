.. _Part_C1_Preparing_Adsorbed_Systems_For_VASP:

Part C.1: Preparing Selected Adsorbed Systems For VASP Optimisation
###################################################################

After you have selected the binding sites to adsorb adsorbates onto and have placed their associated ``xyz`` files into ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files`` (with the desired orientations/rotations), we can proceed to preparing the VASP files for these systems with adsorbates. To do this, **set the** ``Step_to_Perform`` **variable in the** ``Run_Adsorber.py`` **script to** ``'Part C'``:

.. code-block:: python

   Step_to_Perform = 'Part C'

As mentioned previously in :ref:`Part_A_Optimising_System_Initially`, You also need to create a folder called ``VASP_Files`` that contains the following files and folders:

* ``INCAR``: This is a VASP file that contains all the information required to run the VASP job (https://www.vasp.at/wiki/index.php/INCAR and https://cms.mpi.univie.ac.at/vasp/vasp/INCAR_File.html).
* ``KPOINTS``: The KPOINTS file is used to specify the Bloch vectors (k-points) that will be used to sample the Brillouin zone in your calculation (https://www.vasp.at/wiki/index.php/KPOINTS).
* ``POTCARs``: This is a folder that contains all of the ``POTCAR`` files for all of the different elements in your models. Each of the ``POTCAR`` files in this folder need to be labelled as ``POTCAR_XX``, where ``XX`` is the symbol for the particular element. For example, for the POTCAR to describe Cu, you want to name the POTCAR as ``POTCAR_Cu``, the POTCAR for C should be called ``POTCAR_C``, the POTCAR for H should be called ``POTCAR_H``, .... 

You want to also include any other files that will be needed. For example, if you are running VASP with the BEEF functional, you need to include the ``vdw_kernel.bindat`` file in the ``VASP_Files`` folder. An example of ``VASP_Files`` folders can be found in `Adsorber Examples on Github <https://github.com/GardenGroupUO/Adsorber/tree/main/Example>`_. 

You also want to make sure that your ``Run_Adsorber.py`` script also includes the ``slurm_information`` dictionary that contains the information required to make the ``submit.sl`` file. The ``submit.sl`` file is used to submit a VASP job to Slurm. The information required in the ``slurm_information`` dictionary can be found at :ref:`Information required to make submit.sl siles for submitting files to Slurm <information_required_to_make_submitsl_siles_for_submitting_files_to_slurm>`.

Once you have done all of these requirements, you can then run the ``Run_Adsorber.py`` script in the terminal:

.. code-block:: bash

   python Run_Adsorber.py

What will ``Run_Adsorber.py``: Part C do?
=========================================

``Run_Adsorber.py`` will take all the ``.xyz`` that you have placed in ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files`` and convert them into files ready to be run in VASP with the Slurm Workload Manager. 

``Adsorber`` will create a new folder called ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` that contain VASP folders of your selected systems with adsorbates. Each of these VASP folders contain a ``POSCAR`` of the system with adsorbate, as well as the ``INCAR``, ``KPOINTS``, ``POTCAR``, and ``submit.sl`` files, as well as any other files that you need for your VASP calcuations. 

If the VASP folder exists and it contains a ``POSCAR``, this ``POSCAR`` will not be replaced as you may have updated the ``POSCAR`` if your VASP job entered prematurally without converging. If you do want to force override all ``POSCAR`` files, you will want to set ``part_c_force_create_original_POSCAR = True`` in your ``Run_Adsorber.py`` script. 

Note: This ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder may get big, so just check the amount of space that the newly created ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` is taking up as it is being created. 

I accidentally gave wrong settings in the ``INCAR`` or ``submit.sl`` files, or something about my ``KPOINTS`` or ``POTCAR``. What should I do? 
==============================================================================================================================================

If you realise you have entered in wrong settings in the ``INCAR`` or ``submit.sl`` files, or your ``KPOINTS`` or ``POTCAR`` files are wrong, no problem! Make the changes to these files and then rerun your ``Run_Adsorber.py`` script again. Only those jobs that have not begun to run (i.e. dont have an ``OUTCAR``) will have their VASP files ``INCAR``, ``submit,sl``, ``KPOINTS``, ``POTCAR``, and other vast files (not the ``POSCAR`` though) copied over. Adsorber will not touch those jobs that have an ``OUTCAR`` that are assumed to be running/have finished running. 

I want to add more new places that adsorbates can bind to on the surface of the cluster/surface model in Part B, what do I do here?
===================================================================================================================================

Run your ``Run_Adsorber.py`` script once you have included all the new binding sites to your ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files`` folder. Running your your ``Run_Adsorber.py`` script again will add new folders and VASP files of these new arrangements of adsorbates on the surface of your cluster/surface model in your ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder. Your original ``POSCAR`` will not be changed (unless you have set ``part_c_force_create_original_POSCAR = True``. We recommend you not to do this here). Only those jobs that have not begun to run (i.e. dont have an ``OUTCAR``) will have their VASP files ``INCAR``, ``submit,sl``, ``KPOINTS``, ``POTCAR``, and other vast files (not the ``POSCAR`` though) copied over. Adsorber will not touch those jobs that have an ``OUTCAR`` that are assumed to be running/have finished running. 


.. _How_to_submit_files_to_slurm:

How to submit VASP jobs to Slurm: The ``Run_Adsorber_submitSL_slurm.py`` program
================================================================================

Once you have run the ``Run_Adsorber.py`` script with ``Step_to_Perform = 'Part C'``, you can submit your jobs. If you use a computer cluster that run the Slurm Workload Manager, you can submit all your jobs at the same time by changing directory into the ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder and running a script called ``Run_Adsorber_submitSL_slurm.py``.

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP
   Run_Adsorber_submitSL_slurm.py

Running the ``Run_Adsorber_submitSL_slurm.py`` script in the terminal will submit all your VASP jobs. The ``Run_Adsorber_submitSL_slurm.py`` program works by looking through all subdirectories that this program is executed from and looks for folders that contain a ``'submit.sl'`` file. 

* **This program will not submit VASP jobs that are currently running or have been run**. **This program will only submit VASP jobs that do not contain a ``OUTCAR`` file**. Any job that is running or has already run will contain an ``OUTCAR`` file, which tells ``Run_Adsorber_submitSL_slurm.py`` that that VASP job is currently running or has already been run.
* ``Run_Adsorber_submitSL_slurm.py`` will execute all folders that contain a ``'submit.sl'`` file. However, ``Run_Adsorber_submitSL_slurm.py`` will not run any ``'submit.sl'`` files from previously run calculations, which are found in the ``Submission_Folder`` folders. 

If you dont want to run all the jobs in ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` but just a select few, you want to move into that folder and then type ``Run_Adsorber_submitSL_slurm.py`` into the terminal. For example, lets say that I only want to run the jobs that are in the directory ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/COOH_symmetric/Bridge_Sites/Other_5_fold_Sites_Blue``, then we want to move into this directory and then type ``Run_Adsorber_submitSL_slurm.py`` into the terminal:

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/COOH_symmetric/Bridge_Sites/Other_5_fold_Sites_Blue
   Run_Adsorber_submitSL_slurm.py

``Run_Adsorber_submitSL_slurm.py`` is set up to only allow 1000 jobs to be running or in the queue in slurm. You can change this value in the ``Run_Adsorber_submitSL_slurm.py``, however by default slurm usually only allows for 1000 jobs to be running or in the queue at any one time. Before you run ``Run_Adsorber_submitSL_slurm.py`` you can see how many jobs you are submitting to the queue by running typing ``no_of_submitSL_files`` into the terminal in the directory you are in. To use this command, you need to include the alias in your ``~/.bashrc``:

.. code-block:: bash

   alias no_of_submitSL_files='find . -name "submit.sl" -type f -not -path "*Submission_Folder_*" | wc -l'

For example, if I want to find out all the jobs in ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP``, I move into this directory and type ``no_of_submitSL_files`` into the terminal:

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP
   no_of_submitSL_files

If I want to find out all the jobs in ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/COOH_symmetric/Bridge_Sites/Other_5_fold_Sites_Blue``, I move into this directory and type ``no_of_submitSL_files`` into the terminal:

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/COOH_symmetric/Bridge_Sites/Other_5_fold_Sites_Blue
   no_of_submitSL_files

To find out the number of jobs that are running or are waiting in the queue in slurm, you can type ``no_of_jobs_running_or_queued`` into the terminal. To use this command, you need to enter this alias into your ``~/.bashrc``:

.. code-block:: bash

   alias no_of_jobs_running_or_queued='squeue -u $USER | wc -l'

Note: This will give you the number of jobs you have in your slurm queue, plus 1. So whatever number you get from ``no_of_jobs_running_or_queued``, minus 1 from it to get the actual number of jobs in your queue. Not suer how to fix this yet. 

NOTE: You **CAN** enter more than 1000 jobs into the slurm queue with ``Run_Adsorber_submitSL_slurm.py``. If you reach 1000 jobs queued in slurm, ``Run_Adsorber_submitSL_slurm.py`` will patiently wait for current running jobs to complete and add more of your jobs into the slurm queue as current jobs are completed. 



What to do if some jobs need to be resubmit for some reason
===========================================================

If you would like to resubmit one or many jobs for some particualy reason, see :ref:`Part_C2_Subsidiary_Programs` for information about the programs for doing this. 