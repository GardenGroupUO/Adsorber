.. _Part_D_supplementary_methods:

Part D: Supplementary Methods
#############################

Often because there are lots of ways that adsorbates can be bound to a cluster, many VASP jobs are required where an adsorbate is bound to various surface sites about a surface or cluster. This means that 200 to 2000+ VASP jobs need to be completed to understand the preferable binding site for an adsorbate upon a surface or cluster. For this reason, I often will perform ``Adsorber`` at a low convergence (for example 0.03 eV) and then once I know which sites are most preferable for an adsorbate to bind to, only perform a tigher convergence (0.01 eV) on those lowest energy sites. 

Furthermore, in some cases, some of your VASP jobs will converge the adsorbate to the same place on the surface as many other VASP jobs (for example, adsorb a COOH to the same top-top site starting at different positions on your surface). You can use the ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet to look to see this, by looking at the columns ``Similar to`` and ``No of surface atoms adsorbed to``. If either of these are the same as other systems (other rows), this may indicate that those systems (rows) are equivalent. 

The following methods can help you figure out if different VASP jobs have converged to the same place and help resume any jobs that you want to tighten the convergence of

``Adsorber compare``: Comparing systems where adsorbate binds to the same surface atoms
************************************************************************************************************************

As well as using the ``Similar to`` and ``No of surface atoms adsorbed to`` columns of the ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet, you can also use this program to help figure out which systems converged to the same place. This program will look through your ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet, compare those systems that have the same ``No of surface atoms adsorbed to``, and write files to help you analyse those systems that may be similar. 

It is useful to know which system converge to the same place, because if you want to tighten the convergence criteria you don't need to waste computer time resuming calculations for system that have already converged to the same place with looser convergence criteria. Tightening the convergence of these system may run in identical fashions, therefore only wasting computer time. 

To use this program, you want to first move into the same directory as your ``general.py``, ``adsorbate.py``, ``partA.py``, ``partB.py``, and ``partC.py`` scripts, and then type ``Adsorber compare`` into the terminal:

.. code-block:: bash

   cd into_the_same_directory_as_your_Run_Adsorber_script
   Adsorber compare write_similarity_traj_files upper_energy_limit

You can have the following optional inputs:

* ``write_similarity_traj_files`` (*bool*): If true, this program will write all the systems that were identical/similar to the same ``.traj`` file. This is to allow the user to check that all these systems are infact the same or similar enough to be regarded the same ('Default: ``false``'). 
* ``upper_energy_limit`` (*float*): By default, all of the lowest energy version of identical final state systems is written to this system. If you only want to write those that are X.XX eV above the minimum energy system, set this value to X.XX eV. For example, if you only want to record those systems that are 0.5 eV above the minimum energy system, set this value to 0.5. (Default: record all lowenergy energy versions of identical states).

This will create a folder called ``Similar_Systems`` into your ``Part_D_Results_Folder`` directory. This folder will contain subdirectories that are name in the same way as in your ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet (for example, ``1 (C1 [79->25]),1 (O1 [80->66])``. However this will be relabelled so that spaces are changed to ``_``, ``[``, ``]``, ``(``, and ``)`` removed, ``,`` to ``+`` and ``->`` to ``to``, e.g. ``1 (C1 [79->25]),1 (O1 [80->66])`` goes to ``1_C1_79to25__1_O1_80to66``). These alternative names are also give in the ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet, in the cell to the right of this cell. In these folders will contain:

* ``similar_systems.txt``: This file contains all the job_names, energies, and paths of VASP jobs that may have converged to the same place
* a ``traj`` file: This contains all the final states of your jobs. The images in this ``traj`` are ordered in the same manor as given in ``similar_systems.txt``. The images in this ``traj`` may all look the same, because these jobs may have converged to the same place.
* ``xyz`` files: These are xyz files of the final states that jobs had reached before finishing. These ``xyz`` files may all look the same, because these jobs may have converged to the same place.

What to do once you have performed ``Adsorber compare`` and want to tighten the convergence criteria for selected unique states
-------------------------------------------------------------------------------------------------------------------------------

Once you have performed ``Adsorber compare``, a file called ``similar_systems.txt`` will be created. You can run your ``prepare_unconverged_VASP_jobs.py`` script again if you want to tighten your convergence critera. In this example, we will call this script ``prepare_unconverged_VASP_jobs_PartD.py``. This is what you need to do in order to tighten the convergence criteria:

1. Change the ``EDIFF`` tag in your ``INCAR`` file in your ``VASP_Files`` folder to a tighter convergence criteria

2. You then want to change ``path_to_resubmission_list_file`` in your ``prepare_unconverged_VASP_jobs_PartD.py`` file to the ``similar_systems.txt`` file you have just created. For example, if you want to resubmit those unique states for CHO adsorbates adsorbed to your system, the following code could be used:

**Notes about this** ``prepare_unconverged_VASP_jobs_PartD.py`` **script:**

* You can give ``path_to_resubmission_list_file`` as a single path or a list of paths.
* **MAKE SURE THAT THE** ``force_prepare`` **VARIABLE IS SET TO** ``True``.
* **MAKE SURE THAT THE** ``update_VASP_files`` **VARIABLE IS SET TO** ``True``.

.. literalinclude:: input_files/prepare_unconverged_VASP_jobs_PartD.py
   :language: python
   :caption: prepare_unconverged_VASP_jobs_PartD.py
   :name: prepare_unconverged_VASP_jobs_PartD.py
   :tab-width: 4
   :linenos:

3. Run the ``prepare_unconverged_VASP_jobs_PartD.py`` script

.. code-block:: bash

   python prepare_unconverged_VASP_jobs_PartD.py

This will prepare your unique states to be reoptimised with VASP using a tighter convergence criteria. See :ref:`Part_C1_Submitting_Jobs_to_Slurm` to learn how to submit your VASP jobs to slum. 

If you need more information about ``prepare_unconverged_VASP_jobs.py``, see :ref:`Part_C_Run_Adsorber_prepare_unconverged_VASP_jobs_PY`. This ``prepare_unconverged_VASP_jobs.py`` script has been written for preparing unconverged jobs for resubmission, but by setting ``force_prepare = True`` and ``update_VASP_files = True`` we can use this same script for preparing jobs to tighten the convergence criteria. 

``Adsorber tidy``: Clean up the files for jobs that you are happy with
**********************************************************************

VASP makes lots of files after it has run. These can be annoying to keep if you are transferring files about. The ``Run_Adsorber_Tidy_Finished_Jobs.py`` script will get rid of all the unnecessary files that are created from all subdirectories. The files that are removed are: ``CHG``, ``CHGCAR``, ``CONTCAR``, ``DOSCAR``, ``EIGENVAL``, ``fe.dat``, ``IBZKPT``, ``OSZICAR``, ``PCDAT``, ``POTCAR``, ``REPORT``, ``vasprun.xml``, ``vaspout.eps``, ``WAVECAR``, ``XDATCAR``, and ``vdw_kernel.bindat``. The ``INCAR``, ``KPOINTS``, ``OUTCAR``, ``POSCAR``, and ``submit.sl`` files are not removed, as well as any output and error files that are created by slurm during the VASP optimsation, are **NOT** removed by this script. To perform this script, move into the folders that can all the subfolders you wish to tidy up and enter ``Run_Adsorber_Tidy_Finished_Jobs.py`` into the terminal:

.. code-block:: bash

   Adsorber tidy

If you do want to remove all ``INCAR``, ``KPOINTS``, and ``submit.sl`` files in these folders as well,  move into the folders that can all the subfolders you wish to tidy up and enter ``Run_Adsorber_Tidy_Finished_Jobs.py full`` into the terminal: 

.. code-block:: bash

   Adsorber tidy full

Note: the ``Adsorber tidy`` command will not change or remove any files that are in your ``VASP_Files`` folder. 