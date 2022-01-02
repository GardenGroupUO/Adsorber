.. _Part_C2_Unconverged_VASP_Jobs:

Part C2: What To Do If Some Jobs Have Not Finished/Converged
#############################################################

In many cases, some of your jobs may have not converged, may not have finished due to an error, or you may want to restart your job with a tigher convergence criteria. In these cases you will want to reset your jobs to be resubmitted. There are way to do this (for example, using the ``vfin.pl`` and ``vef.pl`` scripts in the ``VTST`` toolset, https://theory.cm.utexas.edu/vtsttools/). In Adsorber, we have written a few programs and have set up a few protocols to 

1. Find out which jobs have converged or not.
2. To resubmit all jobs or (specific jobs) to slurm.

These programs/protocols are described below. 

.. _Part_C_Run_Adsorber_determine_unconverged_VASP_jobs:

``Adsorber check_unconverged``: Determine which jobs have converged and which have not
======================================================================================

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

What to do if you want to resubmit jobs to slurm
================================================

There are two programs that you can use for preparing jobs for resubmission to slurm, depending on what you want to do. The first thing to do is to make any changes to your convergence criteria or other VASP settings. Once you are happy, move on to one of the two pro before that is most suited to what you want to do. 


Before preparing jobs for resubmission
--------------------------------------

Before using either of these programs, you want to first make any changes to the settings that you want to change in your ``INCAR`` file (and make any corrections that you need to make to your ``KPOINTS`` and ``POTCAR`` files if required). For example, if you want to change the geometric convergence criteria you want to change the ``EDIFF`` tag in your ``INCAR`` file now. 

If you dont need to make any changes to your ``INCAR``, do not worry about any of this. 


``prepare_unconverged_VASP_jobs.py``: Prepare unconverged VASP jobs for resubmission
------------------------------------------------------------------------------------

If not all your VASP jobs converged, you can setup your VASP calculations to be resubmitted to VASP from the last geometry optimisation step. To do this, you first need to prepare a new python script in the same place on your computer as your ``general.py``, ``adsorbate.py``, ``partA.py``, ``partB.py``, and ``partC.py`` scripts called ``prepare_unconverged_VASP_jobs.py``. An example of this ``prepare_unconverged_VASP_jobs.py`` python script is as follows:

.. code-block:: python

   from Adsorber import Run_Adsorber_prepare_unconverged_VASP_jobs

   # A switch that determines what type of resubmnission scheme you would like to perform
   prepare_jobs_switch = 'folder' # text

   # if you want to resubmit all adsorbate+systems that have an energy above the current minimum energy system.
   files_with_VASP_calcs = ['Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/COH']
   options = {'energies_from_lowest_energy': float('inf')}

   # If you want to resubmit certain adsorbate+systems given in a text file. 
   path_to_resubmission_list_file = 'Part_D_Results_Folder/Similar_Systems_CHO.txt' # example of path_to_resubmission_list_file as a string for a single file
   # path_to_resubmission_list_file = ['Part_D_Results_Folder/Similar_Systems_CHO.txt', 'Part_D_Results_Folder/Similar_Systems_COOH.txt', 'Part_D_Results_Folder/Similar_Systems_CO.txt'] # example of path_to_resubmission_list_file as a list of files.

   # Information required to prepare jobs with selected switch
   main_information = {'files_with_VASP_calcs': files_with_VASP_calcs, 'options': options}
   #main_information = {'path_to_resubmission_list_file': path_to_resubmission_list_file}

   # if you would like to prepare jobs even if they have already converged, change this to True
   force_prepare = false
   # If you want to also update the VASP files while performing this task
   update_VASP_files = False

   slurm_information = {}
   slurm_information['project'] = 'uoo02568'
   slurm_information['partition'] = 'large'
   slurm_information['time'] = '72:00:00'
   slurm_information['nodes'] = 1
   slurm_information['ntasks_per_node'] = 12
   slurm_information['mem-per-cpu'] = '1200MB'
   slurm_information['email'] = 'yourslurmnotificationemailaddress@gmail.com'
   slurm_information['vasp_version'] = 'VASP/5.3.5-intel-2017a-VTST-BEEF'
   slurm_information['vasp_execution'] = 'vasp_cd'

   Run_Adsorber_prepare_unconverged_VASP_jobs(prepare_jobs_switch,main_information=main_information,slurm_information=slurm_information,force_prepare=force_prepare,update_VASP_files=update_VASP_files)

There are five variables to specify in this script. These are :

* ``prepare_jobs_switch`` (*str.*): This switch indicates how this program will prepare your jobs. There are two options for this switch:

   * ``'folder'``: This program will go through selected folders that include all the jobs you would like to prepare.
   * ``'text'``: This program will prepare only those jobs that have been included in a given text file. 

* ``main_information`` (*dict.*): This dictionary holds the information required to run this program with ``prepare_jobs_switch = 'folder'`` or ``prepare_jobs_switch = 'text'``. These are:

   * For ``prepare_jobs_switch = 'folder'``: 

      * ``files_with_VASP_calcs`` (*list*): This is the list of directories that contains the jobs you would like to resume. This program will look through the directories in this list as well as all the subdirectories in this list and will resume all the jobs within these directories and subdirectories. 
      * ``energies_from_lowest_energy`` (*float*, optional): This variable allows the user to only prepare those jobs that within ``energies_from_lowest_energy`` eV of the lowest energy adsorbate+system. Any adsorbate+systems that are above ``energies_from_lowest_energy`` eV of the lowest energy adsorbate+system will not be prepared for resuming. Default: ``energies_from_lowest_energy = float('inf')`` (Figure this out, maybe remove)

   * For ``prepare_jobs_switch = 'text'``:

      * ``path_to_resubmission_list_file`` (*str./list/tuple*): This is the path to the text file(s) that contains all the paths the jobs that you want to resume. This can be given as a string to point to a single text file, or as a list that points to many text files. See the above code for an example of ``path_to_resubmission_list_file'' as a list``. NOTE: You can make this list using the ``Run_Adsorber_determine_unconverged_VASP_jobs.py`` program; see :ref:`Part_C_Run_Adsorber_determine_unconverged_VASP_jobs` for more information. 

* ``force_prepare`` (*bool.*): This setting will only prepare those jobs that have not converged. If you set this to ``True``, this program will prepare all files in dictories and subdirectories if they are converged and not converged. Default: ``False``. 

* ``update_VASP_files`` (*bool.*): If this variable is set to ``True``, the files that are in your ``VASP_files`` folder will be copied into the job that are prepared. This allows you to make changes to the files in your ``VASP_files`` folder that you would like to adopt in the jobs you prepare, such as changing the convergence criteria in the ``INCAR``. If you set this to ``False``, the original VASP files from the Job will be used. Default: ``False``. 

* ``slurm_information`` (*dict.*): This dictionary contains all the information required to create the ``submit.sl`` scripts. See XXXXXXXXXXX for more information about the settings to place in this dictionary. 

What will ``prepare_unconverged_VASP_jobs.py`` do?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each job that is setup for resubmission, the ``CONTCAR``, ``INCAR``, ``KPOINT``, ``OUTCAR``, ``POSCAR``, and ``submit.sl`` files , as well as any output and error files created by slurm during the VASP optimisation, are moved to a folder called ``Submission_Folder``. The ``CHG``, ``CHGCAR``, ``DOSCAR``, ``EIGENVAL``, ``IBZKPT``, ``OSZICAR``, ``PCDAT``, ``PCDAT``, ``REPORT``, ``vasprun.xml``, ``WAVECAR``, ``XDATCAR`` files are deleted, the last image written in the ``OUTCAR`` is used as the new ``POSCAR``, and the old ``OUTCAR`` is deleted. ``Run_Adsorber_prepare_unconverged_VASP_jobs.py`` **will also prepare any VASP jobs for resubmission that had issues, because the** ``OUTCAR`` **or** ``CONTCAR`` **could not be loaded.** In this case, the POSCAR used will be the original POSCAR. Files from the previous VASP job run will  be stored in a folder called ``Submission_Folder`` with ``Issue`` included in the label. 

What to do if you have run ``prepare_unconverged_VASP_jobs.py``, but you then want to change the VASP files or the ``submit.sl`` script before resubmitting jobs to slurm 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have already run the ``prepare_unconverged_VASP_jobs.py`` but decide you want to change some of your VASP files, such as using a different convergence criteria or change other parameters in ``INCAR``, ``KPOINT``, or other files, you can do this by rerunning your ``prepare_unconverged_VASP_jobs.py`` script again. To do this:

1. Make the necessary changes to your ``INCAR``, ``KPOINT``, or other files in your ``VASP_Files`` folder.
2. Make the necessary changes to your ``submit.sl`` script by making changes to your ``slurm_information`` dictionary in your ``Run_Adsorber.py`` script. 
3. Rerun your ``prepare_unconverged_VASP_jobs.py`` script in the terminal:

.. code-block:: bash

   python prepare_unconverged_VASP_jobs.py

**=> If you want to change the convergence criteria before you resubmit your unconverged VASP jobs**, perform the steps as above, making sure you change the ``EDIFFG`` tag in the ``INCAR`` file suppied in the ``VASP_Files`` folder. For example, if you want to tighten your convergence criteria, change your value of ``EDIFFG`` in your ``INCAR`` file so it is closer to 0.0 eV or 0.0 eV/Ang. 

What to do when you are ready to resubmit VASP jobs to slurm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you are ready to resubmit these jobs, see :ref:`Part_C1_Submitting_Jobs_to_Slurm` for information about the ``Run_Adsorber_submitSL_slurm.py``, a program for automatically resubmitting jobs to slurm.
