.. _Part_C_Preparing_Adsorbed_Systems_For_VASP:

Part C: Preparing Selected Adsorbed Systems For VASP Optimisation
#################################################################

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
-----------------------------------------

``Run_Adsorber.py`` will take all the ``.xyz`` that you have placed in ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files`` and convert them into files ready to be run in VASP with the Slurm Workload Manager. ``Adsorber`` will create a new folder called ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` that contain VASP folders of your selected systems with adsorbates. Each of these VASP folders contain a ``POSCAR`` of the system with adsorbate, as well as the ``INCAR``, ``KPOINTS``, ``POTCAR``, and ``submit.sl`` files, as well as any other files that you need for your VASP calcuations. If the VASP folder exists and it contains a ``POSCAR``, this ``POSCAR`` will not be replaced as you may have updated the ``POSCAR`` if your VASP job entered prematurally without converging. If you do want to force override all ``POSCAR`` files, you will want to set ``part_c_force_create_original_POSCAR = True`` in your ``Run_Adsorber.py`` script. 

Note: This ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder may get big, so just check the amount of space that the newly created ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` is taking up as it is being created. 

.. _How_to_submit_files_to_slurm:

How to submit VASP jobs to Slurm
--------------------------------

Once you have run the ``Run_Adsorber.py`` script with ``Step_to_Perform = 'Part C'``, you can submit your jobs. If you use a computer cluster that run the Slurm Workload Manager, you can submit all your jobs at the same time by changing directory into the ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder and running a script called ``Run_Adsorber_submitSL_slurm.py``.

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP
   Run_Adsorber_submitSL_slurm.py

Running the ``Run_Adsorber_submitSL_slurm.py`` script in the terminal will submit all your VASP jobs. **This script will only submit jobs to slurm that do not have an OUTCAR file.** Any jobs that are currently running or have finished running will not be resubmitted, as they will have created an OUTCAR file. 

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

NOTE: You **CAN** enter more than 1000 jobs into the slurm queue with ``Run_Adsorber_submitSL_slurm.py``. If you reach 1000 jobs queued in slurm, ``Run_Adsorber_submitSL_slurm.py`` will patiently wait for current running jobs to complete and add more of your jobs into the slurm queue as current jobs are completed. 


What to do if some jobs have not finished/converged
---------------------------------------------------

If some of your jobs have not converged or have not finished, you will need to go though them and resubmit those jobs that have not finished. You can use the ``vfin.pl`` and ``vef.pl`` scripts in the ``VTST`` toolset to do this (see https://theory.cm.utexas.edu/vtsttools/ for more information about the ``VTST`` toolset for VASP and how to download it). However, there are also programs included in ``Adsorber`` that can help you do this with ease. These programs are described below:

``Run_Adsorber_determine_unconverged_VASP_jobs.py``: Determine which jobs have converged and which have not
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This program is designed to inform you of which VASP jobs have converge and which have not. To run this, move into the folder that you would like to examine all jobs that are within subdirectories of. Then run this program in the terminal. For example, if you want to examine if all VASP jobs from Part A have converged, perform the following in the terminal:

.. code-block:: bash

   cd Part_A_Non_Adsorbed_Files_For_VASP
   Run_Adsorber_determine_unconverged_VASP_jobs.py

If you want to check if all VASP jobs from Part C have converged, perform the following in the terminal:

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP
   Run_Adsorber_determine_unconverged_VASP_jobs.py

If you want to just want to check if the VASP jobs for a particular adsorbate from Part C have converged, for example if all systems that had CO adsorbed to its surface, perform the following in the terminal:

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/CO
   Run_Adsorber_determine_unconverged_VASP_jobs.py

This will give you a list of VASP jobs that have converged and have not converged:

.. code-block:: bash

   ==============================================
   The following VASP jobs CONVERGED
   CO_top_sites_53_130 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_53_130)
   CO_top_sites_42_119 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_42_119)
   CO_top_sites_30_107 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_30_107)
   CO_top_sites_32_109 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_32_109)
   CO_top_sites_31_108 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_31_108)
   CO_top_sites_36_113 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_36_113)
   CO_top_sites_47_124 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_47_124)
   CO_top_sites_35_112 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_35_112)
   CO_top_sites_29_106 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_29_106)
   CO_top_sites_41_118 (./CO/Top_Sites/Ico_Sites_Green/CO_top_sites_41_118)
   ==============================================
   The following VASP jobs DID NOT CONVERGE
   CO_top_sites_49_126 (./CO/Top_Sites/5_Fold_Vertex_Site_Red/CO_top_sites_49_126)
   CO_top_sites_27_104 (./CO/Top_Sites/5_Fold_Vertex_Site_Red/CO_top_sites_27_104)
   CO_top_sites_58_135 (./CO/Top_Sites/Weird_Sites_Yellow/CO_top_sites_58_135)
   CO_top_sites_12_89 (./CO/Top_Sites/Weird_Sites_Yellow/CO_top_sites_12_89)
   CO_top_sites_19_96 (./CO/Top_Sites/Weird_Sites_Yellow/CO_top_sites_19_96)
   CO_top_sites_21_98 (./CO/Top_Sites/Weird_Sites_Yellow/CO_top_sites_21_98)
   CO_top_sites_44_121 (./CO/Top_Sites/Weird_Sites_Yellow/CO_top_sites_44_121)
   ==============================================

If you just want the names of the jobs and not the directories printed, type ``Run_Adsorber_determine_unconverged_VASP_jobs.py False`` into the terminal. This will give the following:

.. code-block:: bash

   ==============================================
   The following VASP jobs CONVERGED
   CO_top_sites_53_130
   CO_top_sites_42_119
   CO_top_sites_30_107
   CO_top_sites_32_109
   CO_top_sites_31_108
   CO_top_sites_36_113
   CO_top_sites_47_124
   CO_top_sites_35_112
   CO_top_sites_29_106
   CO_top_sites_41_118
   ==============================================
   The following VASP jobs DID NOT CONVERGE
   CO_top_sites_49_126
   CO_top_sites_27_104
   CO_top_sites_58_135
   CO_top_sites_12_89
   CO_top_sites_19_96
   CO_top_sites_21_98
   CO_top_sites_44_121
   ==============================================

.. _Part_C_Run_Adsorber_prepare_unconverged_VASP_jobs_PY:

``Run_Adsorber_prepare_unconverged_VASP_jobs.py``: Prepare VASP jobs for resubmission, either with the same or a new convergence criteria
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If not all your VASP jobs converged, or you want to tighten your convergence criteria (i.e. change your value of ``EDIFFG`` in your ``INCAR`` file so it is closer to 0.0 eV or 0.0 eV/Ang), you can setup your VASP calculations to be resubmitted to VASP from the last geometry optimisation step. To do this, you first need to prepare a new python script in the same place on your computer as your ``Run_Adsorber.py`` called ``prepare_unconverged_VASP_jobs.py``. An example of this ``prepare_unconverged_VASP_jobs.py`` python script is as follows:

.. code-block:: python

   from Adsorber import Run_Adsorber_prepare_unconverged_VASP_jobs

   #files_with_VASP_calcs = ['Part_A_Non_Adsorbed_Files_For_VASP','Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP']
   files_with_VASP_calcs = ['Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/CHO']

   options = {'energies_from_lowest_energy': float('inf')}

   Run_Adsorber_prepare_unconverged_VASP_jobs(files_with_VASP_calcs,options)

The settings for this script are:

   * ``files_with_VASP_calcs`` (*list of file paths strings*): This is a list that contains all the directories of all the jobs you would like to resubmit. Only jobs that have not converged will be resubmitted, unless ``force_resubmit_all_VASP_jobs_found`` is set to ``True``. 
   * ``options`` (*dict.*): This dictionary allow you to pick options for resubmitting certain VASP jobs for resubmission. This is particularly useful if you want to resubmit only specific VASP jobs when you are tightening your convergence critera. Some of these options that are available are: 

      * ``'max_energy_from_lowest_energy'`` (*float*): This is the maximum energy for VASP jobs that have run within each folder in ``files_with_VASP_calcs`` to have obtained from the lowest energy configuration. To figure out.

You can then run this program by typing the following into the terminal:

.. code-block:: bash

   python Run_Adsorber_prepare_unconverged_VASP_jobs.py

For each job that is setup for resubmission, the ``CONTCAR``, ``INCAR``, ``KPOINT``, ``OUTCAR``, ``POSCAR``, and ``submit.sl`` files , as well as any output and error files created by slurm during the VASP optimisation, are moved to a folder called ``Submission_Folder``. The ``CHG``, ``CHGCAR``, ``DOSCAR``, ``EIGENVAL``, ``IBZKPT``, ``OSZICAR``, ``PCDAT``, ``PCDAT``, ``REPORT``, ``vasprun.xml``, ``WAVECAR``, ``XDATCAR`` files are deleted, the last image written in the ``OUTCAR`` is used as the new ``POSCAR``, and the old ``OUTCAR`` is deleted. ``Run_Adsorber_prepare_unconverged_VASP_jobs.py`` **will also prepare any VASP jobs for resubmission that had issues, because the** ``OUTCAR`` **or** ``CONTCAR`` **could not be loaded.** In this case, the POSCAR used will be the original POSCAR. Files from the previous VASP job run will  be stored in a folder called ``Submission_Folder`` with ``Issue`` included in the label. 

**Second, if you want to change the** ``INCAR`` **,** ``KPOINT`` **, or** ``submit.sl`` **files used for these resubmitted VASP jobs**, you need to rerun your ``Run_Adsorber.py`` script again, running it in ``Part C`` mode. To do this:

1. Make the necessary changes to your ``INCAR`` and/or ``KPOINT`` files in your ``VASP_Files`` folder.
2. Make the necessary changes to your ``submit.sl`` script by making changes to your ``slurm_information`` dictionary in your ``Run_Adsorber.py`` script. 
3. Make sure that the ``part_to_perform`` variable in your ``Run_Adsorber.py`` script is set to ``'Part C'`` (``part_to_perform = 'Part C'``).
4. Run your ``Run_Adsorber.py`` script in the terminal:

.. code-block:: bash

   python Run_Adsorber.py

**=> If you want to change the convergence criteria**, perform the steps as above, making sure you change the ``EDIFFG`` tag in the ``INCAR`` file suppied in the ``VASP_Files`` folder.

``Run_Adsorber_Tidy_Finished_Jobs.py``: Clean up the files for jobs that you are happy with
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

VASP makes lots of files after it has run. These can be annoying to keep if you are transferring files about. The ``Run_Adsorber_Tidy_Finished_Jobs.py`` script will get rid of all the unnecessary files that are created from all subdirectories. The files that are removed are: ``CHG``, ``CHGCAR``, ``CONTCAR``, ``DOSCAR``, ``EIGENVAL``, ``fe.dat``, ``IBZKPT``, ``OSZICAR``, ``PCDAT``, ``POTCAR``, ``REPORT``, ``vasprun.xml``, ``vaspout.eps``, ``WAVECAR``, ``XDATCAR``, and ``vdw_kernel.bindat``. The ``INCAR``, ``KPOINTS``, ``OUTCAR``, ``POSCAR``, and ``submit.sl`` files are not removed, as well as any output and error files that are created by slurm during the VASP optimsation, are **NOT** removed by this script. To perform this script, move into the folders that can all the subfolders you wish to tidy up and enter ``Run_Adsorber_Tidy_Finished_Jobs.py`` into the terminal:

.. code-block:: bash

   Run_Adsorber_Tidy_Finished_Jobs.py

If you do want to remove all ``INCAR``, ``KPOINTS``, and ``submit.sl`` files in these folders as well,  move into the folders that can all the subfolders you wish to tidy up and enter ``Run_Adsorber_Tidy_Finished_Jobs.py full`` into the terminal: 

.. code-block:: bash

   Run_Adsorber_Tidy_Finished_Jobs.py full

Note: the ``Run_Adsorber_Tidy_Finished_Jobs.py`` program will not change or remove any files that are in your ``VASP_Files`` folder. 