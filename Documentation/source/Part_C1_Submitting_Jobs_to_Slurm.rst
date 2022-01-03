.. _Part_C1_Submitting_Jobs_to_Slurm:

Part C1: How to submit VASP jobs to Slurm: ``Adsorber submit``
##############################################################

Once you have run the ``Adsorber partC`` command, you can submit your jobs. If you use a computer cluster that run the Slurm Workload Manager, you can submit all your jobs at the same time by changing directory into the ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` folder and running a command called ``Adsorber submit``.

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP
   Adsorber submit

Running the ``Adsorber submit`` command in the terminal will look through all subdirectories that this program is executed from and looks for folders that contain a ``'submit.sl'`` file. 

* **This program will not submit VASP jobs that are currently running or have been run**. **This program will only submit VASP jobs that do not contain a ``OUTCAR`` file**. Any job that is running or has already run will contain an ``OUTCAR`` file, which tells the ``Adsorber`` program that that VASP job is currently running or has already been run.
* ``Run_Adsorber_submitSL_slurm.py`` will execute all folders that contain a ``'submit.sl'`` file. However, ``Adsorber submit`` will not run any ``'submit.sl'`` files from previously run calculations, which are found in the ``Submission_Folder`` folders. 

If you dont want to run all the jobs in ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP`` but just a select few, you want to move into that folder and then type ``Adsorber submit`` into the terminal. For example, lets say that I only want to run the jobs that are in the directory ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/COOH_symmetric/Bridge_Sites/Other_5_fold_Sites_Blue``, then we want to move into this directory and then type ``Adsorber submit`` into the terminal:

.. code-block:: bash

   cd Part_C_Selected_Systems_with_Adsorbed_Species_to_Run_in_VASP/COOH_symmetric/Bridge_Sites/Other_5_fold_Sites_Blue
   Adsorber submit

``Adsorber submit`` settings that can be changed
------------------------------------------------

Write this once I am happy with how the program works here.


``Adsorber check_submit``: Other useful commands to see how many jobs are running and the number of jobs that you will submit
-----------------------------------------------------------------------------------------------------------------------------

Before you run ``Adsorber submit`` you can see how many jobs you are submitting to the queue by running typing ``Adsorber check_submit`` into the terminal in the directory you are in. 

.. code-block:: bash

   Adsorber check_submit

This will show all the VASP jobs that would be submitted if you were to run the ``Adsorber submit`` command. 

A command to determine the number of jobs you have already running in slurm
---------------------------------------------------------------------------

To find out the number of jobs that are running or are waiting in the queue in slurm, you can type ``no_of_jobs_running_or_queued`` into the terminal. To use this command, you need to enter this alias into your ``~/.bashrc``:

.. code-block:: bash

   alias no_of_jobs_running_or_queued='squeue -u $USER | wc -l'

Note: This will give you the number of jobs you have in your slurm queue, plus 1. So whatever number you get from ``no_of_jobs_running_or_queued``, minus 1 from it to get the actual number of jobs in your queue. Not suer how to fix this yet. 

NOTE: You **CAN** enter more than 1000 jobs into the slurm queue with ``Run_Adsorber_submitSL_slurm.py``. If you reach 1000 jobs queued in slurm, ``Run_Adsorber_submitSL_slurm.py`` will patiently wait for current running jobs to complete and add more of your jobs into the slurm queue as current jobs are completed. 

What to do if some jobs need to be resubmit for some reason
-----------------------------------------------------------

If you would like to resubmit one or many jobs for some particualy reason, see :ref:`Part_C2_Unconverged_VASP_Jobs` for information about the programs for doing this. 