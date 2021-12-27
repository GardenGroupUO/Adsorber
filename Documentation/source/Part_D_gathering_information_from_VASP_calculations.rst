.. _Part_D_gathering_information_from_VASP_calculations:

Part D: Gathering Information from VASP Calculations
####################################################

At any point during and after your VASP calculations have been running (during Part A and Part C), you can run a python program that will gather information about your VASP calculations, such as the energies of your systems with attached adsorbates, and if your VASP calculations have converged or not. You can run this program by typing ``Run_Adsorber_Part_D_gather_information.py`` into the terminal in the same folder that you ran ``Run_Adosrber.py`` from: 

.. code-block:: bash

   Run_Adsorber_Part_D_gather_information.py

This will create an excel file called ``Part_D_Information_on_VASP_Calculations.xlsx`` that contains various information about your VASP calculations. All adsorbates will be collected together based on their name before any ``_``. For example, if you tried adsorbing ``COOH`` in two ways, called ``COOH_symmetric`` and ``COOH_O_tilted``, ``Run_Adsorber_Part_D_gather_information.py`` will group the information from these two sets of calculations together because they both start with ``COOH`` before the ``_``, telling ``Run_Adsorber_Part_D_gather_information.py`` they both involve adsorbing ``COOH`` to the surface of your model. 

If you only want to get information for a few different adsorbates, include these adsorbates after typing ``Run_Adsorber_Part_D_gather_information.py`` into the terminal. For example, if we only want to gather information on the adsorbates ``CHO`` and ``COOH``, we do the following:

.. code-block:: bash

   Run_Adsorber_Part_D_gather_information.py CHO COOH

The following information is included in the ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet:

* ``'Job'``: The Job ID of the job assign by slurm. 
* ``'Project'``: The name of the project.
* ``'Job Name'``: The name of the job, as given by Adsorber.
* ``'Path'``: The path from the folder that your ``Run_Adsorber.py`` script was run from to the VASP job.
* ``'Description'``: A description of the job.
* ``'Time submitted for'``: The amount of time that the user submitted the job for.
* ``'Date Submitted'``: The date when the job began.
* ``'Date Finished'``: The date when the job ended.
* ``'Time Elapsed (hrs)'``: The amount of time that actually elapsed (will be shorter or the same time as ``'Time submitted for'``).
* ``'Max. Memory (Gb)'``: The maximum amount of memory that was used by VASP for this job.
* ``'Energy (eV)'``: The energy of the system, adsorbate, or system+adsorbate. 
* ``'Rel. Energy (eV)'``: The energy of the system relative to the lowest energy system with that adsorbate (not included in the ``Originals`` tab).
* ``'Converged?'``: Will indicate if the VASP job converged or not.
* ``'Similar to'``: This will indicate if there are any other jobs that finished where the adsorbate moved into similar positions. This is not complete, so expect for some VASP jobs that finished with adsorbates in the same place to not be given here. 
* ``'No of surface atoms adsorbed to'``: This will give the number of atoms thats that the adsorbate is bound to, as well as other information about which atoms in the adsorbate are bound to which surface atoms of your surface/cluster. This is given as ``[adsorbate atom->surface atoms]``. 
* ``'Notes'``: An empty cell for you to write any notes in.

While this excel spreadsheet will tell you if a job converges or not, it doesn't tell you if VASP has done something stupid, unexpected, or unintended. You will want to go though each of your VASP calculations and check to make sure you are happy with those VASP calculations or not. **This excel spreadsheet is intended to assist your analysis, not to replace your analysis**. 

Part D: Supplementary Methods for tightening convergence criteria and resuming VASP jobs
----------------------------------------------------------------------------------------

Often because there are lots of ways that adsorbates can be bound to a cluster, many VASP jobs are required where an adsorbate is bound to various surface sites about a surface or cluster. This means that 200 to 2000+ VASP jobs need to be completed to understand the preferable binding site for an adsorbate upon a surface or cluster. For this reason, I often will perform ``Adsorber`` at a low convergence (for example 0.03 eV) and then once I know which sites are most preferable for an adsorbate to bind to, only perform a tigher convergence (0.01 eV) on those lowest energy sites. 

Furthermore, in some cases, some of your VASP jobs will converge the adsorbate to the same place on the surface as many other VASP jobs (for example, adsorb a COOH to the same top-top site starting at different positions on your surface). You can use the ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet to look to see this, by looking at the columns ``Similar to`` and ``No of surface atoms adsorbed to``. If either of these are the same as other systems (other rows), this may indicate that those systems (rows) are equivalent. 

The following methods can help you figure out if different VASP jobs have converged to the same place and help resume any jobs that you want to tighten the convergence of

``Run_Adsorber_compare_systems_with_same_binding.py``: Comparing systems where adsorbate binds to the same surface atoms
************************************************************************************************************************

As well as using the ``Similar to`` and ``No of surface atoms adsorbed to`` columns of the ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet, you can also use this program to help figure out which systems converged to the same place. This program will look through your ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet, compare those systems that have the same ``No of surface atoms adsorbed to``, and write files to help you analyse those systems that may be similar. 

It is useful to know which system converge to the same place, because if you want to tighten the convergence criteria you don't need to waste computer time resuming calculations for system that have already converged to the same place with looser convergence criteria. Tightening the convergence of these system may run in identical fashions, therefore only wasting computer time. 

To use this program, you want to first move into the same directory as your ``Run_Adsorber.py`` file and then type ``Run_Adsorber_compare_systems_with_same_binding.py`` into the terminal:

.. code-block:: bash

   cd into_the_same_directory_as_your_Run_Adsorber_script
   Run_Adsorber_compare_systems_with_same_binding.py write_similarity_traj_files upper_energy_limit

You can have the following optional inputs:

* ``write_similarity_traj_files`` (*bool*): If true, this program will write all the systems that were identical/similar to the same ``.traj`` file. This is to allow the user to check that all these systems are infact the same or similar enough to be regarded the same ('Default: ``false``'). 
* ``upper_energy_limit`` (*float*): By default, all of the lowest energy version of identical final state systems is written to this system. If you only want to write those that are X.XX eV above the minimum energy system, set this value to X.XX eV. For example, if you only want to record those systems that are 0.5 eV above the minimum energy system, set this value to 0.5. (Default: record all lowenergy energy versions of identical states).

This will create a folder called ``Similar_Systems`` into your ``Part_D_Results_Folder`` directory. This folder will contain subdirectories that are name in the same way as in your ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet (for example, ``1 (C1 [79->25]),1 (O1 [80->66])``. However this will be relabelled so that spaces are changed to ``_``, ``[``, ``]``, ``(``, and ``)`` removed, ``,`` to ``+`` and ``->`` to ``to``, e.g. ``1 (C1 [79->25]),1 (O1 [80->66])`` goes to ``1_C1_79to25__1_O1_80to66``). These alternative names are also give in the ``Part_D_Information_on_VASP_Calculations.xlsx`` excel spreadsheet, in the cell to the right of this cell. In these folders will contain:

* ``similar_systems.txt``: This file contains all the job_names, energies, and paths of VASP jobs that may have converged to the same place
* a ``traj`` file: This contains all the final states of your jobs. The images in this ``traj`` are ordered in the same manor as given in ``similar_systems.txt``. The images in this ``traj`` may all look the same, because these jobs may have converged to the same place.
* ``xyz`` files: These are xyz files of the final states that jobs had reached before finishing. These ``xyz`` files may all look the same, because these jobs may have converged to the same place.

``Run_Adsorber_prepare_unconverged_VASP_jobs.py``: Prepare Jobs for resubmission
********************************************************************************

You may want to rerun some of your jobs, either because they finished with errors, did not converge, or because you want to change the convergence criteria for that job (either by tightening or loosening the convergence criteria). See :ref:`Part_C_Run_Adsorber_prepare_unconverged_VASP_jobs_PY` for information about how to prepare jobs for being resubmitted to slurm. 

``Run_Adsorber_Tidy_Finished_Jobs.py``: Clean up the files for jobs that you are happy with
*******************************************************************************************

VASP makes lots of files after it has run. These can be annoying to keep if you are transferring files about. The ``Run_Adsorber_Tidy_Finished_Jobs.py`` script will get rid of all the unnecessary files that are created from all subdirectories. The files that are removed are: ``CHG``, ``CHGCAR``, ``CONTCAR``, ``DOSCAR``, ``EIGENVAL``, ``fe.dat``, ``IBZKPT``, ``OSZICAR``, ``PCDAT``, ``POTCAR``, ``REPORT``, ``vasprun.xml``, ``vaspout.eps``, ``WAVECAR``, ``XDATCAR``, and ``vdw_kernel.bindat``. The ``INCAR``, ``KPOINTS``, ``OUTCAR``, ``POSCAR``, and ``submit.sl`` files are not removed, as well as any output and error files that are created by slurm during the VASP optimsation, are **NOT** removed by this script. To perform this script, move into the folders that can all the subfolders you wish to tidy up and enter ``Run_Adsorber_Tidy_Finished_Jobs.py`` into the terminal:

.. code-block:: bash

   Run_Adsorber_Tidy_Finished_Jobs.py

If you do want to remove all ``INCAR``, ``KPOINTS``, and ``submit.sl`` files in these folders as well,  move into the folders that can all the subfolders you wish to tidy up and enter ``Run_Adsorber_Tidy_Finished_Jobs.py full`` into the terminal: 

.. code-block:: bash

   Run_Adsorber_Tidy_Finished_Jobs.py full

Note: the ``Run_Adsorber_Tidy_Finished_Jobs.py`` program will not change or remove any files that are in your ``VASP_Files`` folder. 