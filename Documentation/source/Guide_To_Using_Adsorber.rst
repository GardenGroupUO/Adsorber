
.. _Guide_To_Using_Adsorber:

Guide To Using Adsorber
#######################

There are four parts (Part A, Part B, Part C + Part D) + a prelude step to using the Adsorber program. These parts are described in the sections below: 


Prelude Step
------------

In this step, we will step up the ``general.py`` and ``adsorbate.py`` scripts, which include all the inputs that are required across the whole ``Adsorber`` program. Information about how to set up these two python script are given in :ref:`Prelude_General_and_Adsorbates_scripts`. Extra details about how to set up the adsorbates in your ``adsorbate.py`` script are given in :ref:`Prelude_Info_for_Adsorbate_script`.

Part A
------

This part creates the VASP files to locally optimise your system, as well as lone adsorbates and any other molecules that you need to reference your VASP energies to.  
The guide to perform this set is given in :ref:`Part_A_Optimising_System_Initially`. 
If you already have the system locally optimised with your functional, feel free to move on to Part B. 

Part B
------

In this part, your VASP optimised system will have all adsorbates attached to it in all the various top sites, bridging sites, three fold sites, and four fold sites found across the surface of your system. From these you can select which models your want to include for further optimisation by VASP. The guide to perform this part is given in :ref:`Part_B1_Adsorb_Adsorbates_to_System`, with further information in :ref:`Part_B1_marking_surface_atoms` and :ref:`Part_B2_What_to_do_with_files_from_Part_B`. 

Part C
------

In this part, Adsorber will take the models of adsorbates on various sites on your system and create the files required to locally optimise these models in VASP. The guide to perform this part is given in :ref:`Part_C1_Preparing_Adsorbed_Systems_For_VASP`, with further information in :ref:`Part_C1_Submitting_Jobs_to_Slurm` and :ref:`Part_C2_Unconverged_VASP_Jobs`. 

Part D
------

In this part, a subsidiary program is used to gather information about your VASP local optimisations, including the energy of absorbate+system as well as adsorbates and system alone, as well as if the VASP local optimisation converged or not. The guide to perform this part is given in :ref:`Part_D_gathering_information_from_VASP_calculations`. 

Final Notes about this process
------------------------------

You may want to move backwards and forwards between these parts as you progress in your study. Parts B - D can be performed multiple times if you want to include extra adsorbates in your study. I performed Part C multiple times as I like to focus on obtaining and understanding the energetics of an adsorbates on various top, bridging, three-fold, and four-fold sites and understand which of these site are preferable for binding before moving on to the next adsorbate. 
