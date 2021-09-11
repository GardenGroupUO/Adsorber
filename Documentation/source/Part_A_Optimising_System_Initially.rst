
.. _Part_A_Optimising_System_Initially:

Part A: How to optimise your system initially
#############################################

To begin, we need to obtain the locally optimise version of the system you want to adsorb adsorbates onto. To do this, you will want to **set the** ``Step_to_Perform`` **variable in the** ``Run_Adsorber.py`` **script to** ``'Part A'``:

.. code-block:: python

	Step_to_Perform = 'Part A'

You also need to create a folder called ``VASP_Files`` that contains the following files and folders:

* ``INCAR``: This is a VASP file that contains all the information required to run the VASP job (https://www.vasp.at/wiki/index.php/INCAR and https://cms.mpi.univie.ac.at/vasp/vasp/INCAR_File.html).
* ``KPOINTS``: The KPOINTS file is used to specify the Bloch vectors (k-points) that will be used to sample the Brillouin zone in your calculation (https://www.vasp.at/wiki/index.php/KPOINTS).
* ``POTCARs``: This is a folder that contains all of the ``POTCAR`` files for all of the different elements in your models. Each of the ``POTCAR`` files in this folder need to be labelled as ``POTCAR_XX``, where ``XX`` is the symbol for the particular element. For example, for the POTCAR to describe Cu, you want to name the POTCAR as ``POTCAR_Cu``, the POTCAR for C should be called ``POTCAR_C``, the POTCAR for H should be called ``POTCAR_H``, .... 

You want to also include any other files that will be needed. For example, if you are running VASP with the BEEF functional, you need to include the ``vdw_kernel.bindat`` file in the ``VASP_Files`` folder. 

An example of ``VASP_Files`` folders can be found in `Adsorber Examples on Github <https://github.com/GardenGroupUO/Adsorber/tree/main/Example>`_. 

You can then run the ``Run_Adsorber.py`` script in the terminal:

.. code-block:: bash

	python Run_Adsorber.py

This will create a folder called ``Part_A_Non_Adsorbed_Files_For_VASP``. In this folder is another folder called ``system`` that contains all the VASP files required to locally optimise your system in VASP. 

This ``Part_A_Non_Adsorbed_Files_For_VASP`` folder also contains all the VASP files of your adsorbates that you can also locally optimise in VASP. This is often required to determine in the adsorption energy of your adsorbate onto your system

.. math::

	E_{abs} = E(system+adsorbate) - (E(system) + E(adsorbate))

or if you are defining your adsorption energy with reference species, such as C from graphene, H from H :sub:`2` , and O from H :sub:`2` O: 

.. math::

	E_{abs} = E(system+adsorbate) - (E(system) + E(each\;element\;in\;the\;adsorbate\;in\;stiochiometic\;amounts))

Once you have run VASP on your system and all your adsorbates, proceed to Part B (:ref:`Part_B_Adsorb_Adsorbates_to_System`). 