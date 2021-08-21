.. _Part_C_Preparing_Adsorbed_Systems_For_VASP:

Part C: Preparing Selected Adsorbed Systems For VASP Optimisation
#################################################################

After you have selected the binding sites to adsorb adsorbates onto and have placed their associated ``xyz`` files into ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files`` (with the desired orientations/rotations), we can proceed to preparing the VASP files for these systems with adsorbates. To do this, **set the** ``Step_to_Perform`` **in the** ``Run_Adsorber.py`` **script to** ``'Part C'``:

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

This will create a new folder called ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` which contain VASP folders of your selected systems with adsorbates. These VASP folders contain a ``POSCAR`` of the system with adsorbate, as well as the ``INCAR``, ``KPOINTS``, ``POTCAR``, and ``submit.sl`` files, as well as any other files that you need for your VASP calcuations. 

Note: This ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder may get big, so just check the amount of space that the newly created ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` is taking up as it is being created. 

.. _How_to_submit_files_to_slurm:

How to submit VASP jobs to Slurm
--------------------------------

Once you have run the ``Run_Adsorber.py`` script with ``Step_to_Perform = 'Part C'``, you can submit your jobs. If you use a computer cluster that run the Slurm Workload Manager, you can submit all your jobs at the same time by changing directory into the ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder and running a script called ``Run_Adsorber_submitSL_slurm.py``.

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP
   Run_Adsorber_submitSL_slurm.py

Running the ``Run_Adsorber_submitSL_slurm.py`` script in the terminal will submit all your VASP jobs. 

What to do if some jobs have not finished/converged
---------------------------------------------------

If some of your jobs have not converged or have not finished, you will need to go though them and resubmit those jobs that have not finished. You can do this by changing directory into a job that has not completed and running the ``vfin.pl`` script in your terminal:

.. code-block:: bash

   cd INTO_VASP_FOLDER_YOU_WANT_TO_RESUME
   vfin.pl

vfin.pl is a script included in the ``VTST`` toolset. See https://theory.cm.utexas.edu/vtsttools/ for more information about the ``VTST`` toolset for VASP and how to download it. 

However, if you have lots of jobs you want to resume with VASP, you can run a script to resume your jobs that have not converged. To do this, first cd into the ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder and run a script called ``Run_Adsorber_prepare_unconverged_VASP_jobs.py``. This will perform the ``vfin.pl`` script on all your jobs that have not converged.

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP
   Run_Adsorber_prepare_unconverged_VASP_jobs.py

``Run_Adsorber_prepare_unconverged_VASP_jobs.py`` will tell you which jobs have converged and which have not converged, and will prepare the unconverged jobs for resubmission using the ``vfin.pl`` script. If you do not want the ``Run_Adsorber_prepare_unconverged_VASP_jobs.py`` script to prepare any folders but only tell you which jobs have converged and which jobs have not converged, add ``False`` after the script when you submit it to the terminal, as shown below:

.. code-block:: bash

   Run_Adsorber_prepare_unconverged_VASP_jobs.py False

You can then resume your unconverged jobs by running a script called ``Run_Adsorber_submit_unconverged_VASP_jobs.py`` in the same directory as you ran the ``Run_Adsorber_prepare_unconverged_VASP_jobs.py`` script, which will submit all VASP jobs that have not converged. 

.. code-block:: bash

   Run_Adsorber_submit_unconverged_VASP_jobs.py

If you do not want to submit all the jobs that have been prepared for resuming by the ``Run_Adsorber_submit_unconverged_VASP_jobs.py`` script, you will need to go though by hand and submit the jobs you do want to resume manually. 