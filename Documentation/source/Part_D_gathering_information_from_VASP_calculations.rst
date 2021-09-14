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