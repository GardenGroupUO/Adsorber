
.. _Guide_To_Using_Adsorber:

Guide To Using Adsorber
#######################

There are four parts (Part A, Part B, Part C + Part D) + a prelude step to using the Adsorber program. These parts are described in the sections below: 


Prelude Step
------------

In this step, we will step up the ``Run_Adsorber.py`` script, which includes selecting which atoms in your system are surface atoms. The information about how to set up the ``Run_Adsorber.py`` script is given in :ref:`Prelude_1_How_To_Run_Adsorber`. 
Instructions of some of the more involved settings that are required in the ``Run_Adsorber.py`` script are given in :ref:`Prelude_2_How_To_Obtain_Settings_for_Run_Adsorber`. These include: 

* indicating which atoms are surface atoms, as Adsorber does not identify surface atoms. This is required for Adsorber to know which atoms to consider when placing adsorbates onto top sites, bridging sites, three-fold sites, and four-fold sites. You can find out how to specify this in :ref:`marking_surface_atoms`. 
* indicating how adsorbates are adsorbed to your system. This is given in :ref:`bind_molecule_to_surface_of_system`. 


Part A
------

This part creates the VASP files to locally optimise your system. This is done first because this locally optimised system is used to adsorb adsorbate onto in Parts B and C. This part will also create the VASP files for locally optimising adsorbates (not bound to your system). 
These files are not used further in the Adsorber program, but you often need to know what the energy of you adsorbates are under the functional you are using, so this allows you to easily obtain the energies of these adsorbates. 
The guide to perform this set is given in :ref:`Part_A_Optimising_System_Initially`. 
If you already have the system locally optimised with your functional, feel free to move on to Part B. 

Part B
------

In this part, your VASP optimised system will have all adsorbates attached to it in all the various top sites, bridging sites, three fold sites, and four fold sites found across the surface of your system. From these you can select which models your want to include for further optimisation by VASP. The guide to perform this part is given in :ref:`Part_B_Adsorb_Adsorbates_to_System`. 

Part C
------

In this part, Adsorber will take the models of adsorbates on various sites on your system and create the files required to locally optimise these models in VASP. The guide to perform this part is given in :ref:`Part_C_Preparing_Adsorbed_Systems_For_VASP`. 

Part D
------

In this part, a subsidiary program is used to gather information about your VASP local optimisations, including the energy of absorbate+system as well as adsorbates and system alone, as well as if the VASP local optimisation converged or not. The guide to perform this part is given in :ref:`Part_D_gathering_information_from_VASP_calculations`. 

Final Notes about this process
------------------------------

You may want to move backwards and forwards between these parts as you progress in your study. Parts B - D can be performed multiple times if you want to include extra adsorbates in your study. I performed Part C multiple times as I like to focus on obtaining and understanding the energetics of an adsorbates on various top, bridging, three-fold, and four-fold sites and understand which of these site are preferable for binding before moving on to the next adsorbate. 
