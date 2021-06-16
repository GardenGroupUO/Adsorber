
.. _How_To_Use_Adsorber:

Overview of How to Use the Adsorber Program
###########################################

The Adsorber program is designed to assist you in adsorbing atoms and molecules to the surface of clusters and surface models. Adsorber is designed to locate many various binding sites above individual atoms, bridging sites, three-fold sites, and four-fold sites. 

Adosrber is designed to create many variations of atom and molecules bound to the various binding sites in various orientation so that the user does not have to painstakingly make them all by hand.  

This program is only designed to assist in binding atoms and molcules to the various binding sites across a cluster/surface model. Not all of the models need to be included in your tests as this would be a bit overkill, only the most likely orientations of molecules on the surface of the cluster/surface model should be considered and the rest deleted. 

1. To begin, :ref:`Installation` shows how to install Adsorber on your computer.
2. There are two programs that are helpful to use with the Adsorber program. These are the ASE GUI and Jmol. :ref:`External_programs_that_will_be_useful_to_install_for_using_Adsorber` explains how to install these and use them for viewing chemical systems. 
3. :ref:`How_To_Run_Adsorber` shows how to write the ``Run_Adsorber.py`` script that is used to set up and run Adsorber for your cluster/surface model and for all the atoms and molecules you want to adsorb to your cluster/surface model.
4. Some of the settings that are needed for creating the ``Run_Adsorber.py`` script are not obvious, such as how to give the information required for adosrbing molecules to binding sites. Instruction on how to do this are given in :ref:`How_To_Obtain_Settings_for_Run_Adsorber`.
5. Once you run the Adsorber program the first time, a bunch of ``xyz`` and other files and folders will be created. All of these files and folders are described in :ref:`Outputs_from_Adsorber`.
6. Not all of the models that Adsorber created will be sensible and running all the various orientations in VASP will be a bit overkill. You can delete many of the ``xyz`` files placed in the ``System_with_Adsorbed_Species`` folder. This process is described in more detail in :ref:`What_to_do_with_the_Outputs_from_Adsorber`. 
7. Once all the ``xyz`` files that need to be deleted have been, the other adsorbed models can be converted so that they can be run in VASP. This is described in :ref:`How_to_use_output_data_to_obtain_VASP_data_of_systems_with_adsorbed_species`. 
8. Once VASP files have been created, they can be submitted to Slurm by using the ``Run_Adsorber_submitSL_slurm.py`` subsidary program , as described in :ref:`How_to_submit_files_to_slurm`.

More scripts will be being created to process the VASP data. What this space. 