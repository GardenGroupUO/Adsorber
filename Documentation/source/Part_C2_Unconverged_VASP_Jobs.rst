.. _Part_C2_Unconverged_VASP_Jobs:

Part C2: What To Do If Some Jobs Have Not Finished/Converged
#############################################################

In many cases, some of your jobs may have not converged, may not have finished due to an error, or you may want to restart your job with a tigher convergence criteria. In these cases you will want to reset your jobs to be resubmitted. There are way to do this (for example, using the ``vfin.pl`` and ``vef.pl`` scripts in the ``VTST`` toolset, https://theory.cm.utexas.edu/vtsttools/). In Adsorber, we have written a few programs and have set up a few protocols to 

1. Find out which jobs have converged or not.
2. To resubmit all jobs or (specific jobs) to slurm.

These programs/protocols are described below. 

.. _Part_C_Run_Adsorber_determine_unconverged_VASP_jobs:

``Adsorber check_unconverged``: Determine which jobs have converged and which have not
--------------------------------------------------------------------------------------

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
------------------------------------------------

There are two programs that you can use for preparing jobs for resubmission to slurm, depending on what you want to do. The first thing to do is to make any changes to your convergence criteria or other VASP settings. Once you are happy, move on to one of the two pro before that is most suited to what you want to do. 


Before preparing jobs for resubmission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before using either of these programs, you want to first make any changes to the settings that you want to change in your ``INCAR`` file (and make any corrections that you need to make to your ``KPOINTS`` and ``POTCAR`` files if required). For example, if you want to change the geometric convergence criteria you want to change the ``EDIFF`` tag in your ``INCAR`` file now. 

If you dont need to make any changes to your ``INCAR``, do not worry about any of this. 


``prepare_unconverged_VASP_jobs.py``: Prepare unconverged VASP jobs for resubmission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If not all your VASP jobs converged, you can setup your VASP calculations to be resubmitted to VASP from the last geometry optimisation step. To do this, you first need to prepare a new python script in the same place on your computer as your ``general.py``, ``adsorbate.py``, ``partA.py``, ``partB.py``, and ``partC.py`` scripts called ``prepare_unconverged_VASP_jobs_PartC.py``. An example of this ``prepare_unconverged_VASP_jobs_PartC.py`` python script is as follows:

.. literalinclude:: input_files/prepare_unconverged_VASP_jobs_PartC.py
   :language: python
   :caption: prepare_unconverged_VASP_jobs_PartC.py
   :name: prepare_unconverged_VASP_jobs_PartC.py
   :tab-width: 4
   :linenos:

There are five main variables that are need in this script. These are :

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

* ``slurm_information`` (*dict.*): This dictionary contains all the information required to create the ``submit.sl`` scripts. See :ref:`Part_C1_Preparing_Adsorbed_Systems_For_VASP` for more information about the settings to place in this dictionary. 

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


What should I do if I do not want to use ``prepare_unconverged_VASP_jobs.py`` to prepare jobs for resubmission but want to just resubmit certain jobs: ``Adsorber prep_single_resub``
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

In some cases you may have manually looked through some jobs and find you want to resubmit some jobs to give them longer to run. You can do this using ``Adsorber prep_single_resub``. 

To use ``Adsorber prep_single_resub``, first move into the folder of the job you want to prepare for resubmission. Then in the terminal type

.. code-block:: bash

   Adsorber prep_single_resub

``Adsorber prep_single_resub`` will take all the files and place the important ones in a new ``Submission`` folder, leaving only the ``INCAR``, ``POTCAR``, ``KPOINTS``, ``submit.sl``, and any other input files. A new ``POSCAR`` will be created that is the previous ``CONTCAR`` or if this file does not exist the last image in the ``OUTCAR``.


What to do if some of my calculations are not converging and you want to repeat them from the beginning: ``Adsorber repeat``
----------------------------------------------------------------------------------------------------------------------------

In some cases you may find that when you look at a job manually that you want to restart the job from the beginning. You can do this using ``Adsorber repeat``. To use this, in the folder of tyhe job you want to restart, type in the terminal: 

.. code-block:: bash

   Adsorber repeat

``Adsorber repeat`` will take all the files from your ``Submission_1`` folder (or if you dont have this directory from your folder) and copy them into a new folder that ends with ``_repeat``. This will include your original ``POSCAR``, ``INCAR``, ``POTCAR``, ``KPOINTS``, ``submit.sl``, and any other input files. The ``submit.sl`` will have its job name changed to include the ``_repeat`` tag in its name. ``Adsorber repeat``  will not touch your current job folder

You can use this as many times as you want. 
The first time you use it a new folder ending with ``_repeat`` will be made. 
The second time you use it a new folder ending with ``_repeat_2`` will be made. 
The third time you use it a new folder ending with ``_repeat_3`` will be made. 
And so on and so on.


What to do when you are ready to resubmit VASP jobs to slurm
------------------------------------------------------------

When you are ready to resubmit these jobs, see :ref:`Part_C1_Submitting_Jobs_to_Slurm` for information about the ``Run_Adsorber_submitSL_slurm.py``, a program for automatically resubmitting jobs to slurm.
