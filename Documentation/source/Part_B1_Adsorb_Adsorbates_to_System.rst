.. _Part_B1_Adsorb_Adsorbates_to_System:

Part B1: Adsorbing Adsorbates to your System
############################################

On this page, we will talk about Part B to using the ``Adsorber`` program. In Part B, the ``Adsorber`` program will create ``xyz`` files of your models, where your adsorbate is attached to the surface of your cluster or surface in various top, bridge, three-fold, and four-fold binding sites. 

Setting up the  ``partB.py`` input script
-----------------------------------------

To begin, we want to configure the ``partB.py`` script. The ``partB.py`` script looks as follows:

.. literalinclude:: input_files/partB.py
   :language: python
   :caption: partB.py
   :name: partB.py
   :tab-width: 4
   :linenos:

A input variables that are needed are:

* **path_to_VASP_optimised_non_adsorbate_system** (*str.*): This is the directory to your surface or cluster model without adsorbate after you have optimised it with VASP. 

   * For clusters, this should be set to ``path_to_VASP_optimised_non_adsorbate_system = 'Part_A_Non_Adsorbed_Files_For_VASP/system/OUTCAR'`` 
   * For surfaces, this should be pointed to the file that you want to bind your adsorbate to. This may be ``path_to_VASP_optimised_non_adsorbate_system = 'Part_A_Non_Adsorbed_Files_For_VASP/system/OUTCAR'``, or if you have surface converged your surface model, then to the file that represents the surface converged model. 

* **surface_atoms** (*list of ints*): This is a list of the indices of all the surface atoms in your cluster or surface model. **See** :ref:`Part_B1_marking_surface_atoms` **for how to determine which of your atoms are surface atoms and to get those clusters indices to add to the** ``surface_atoms`` **list**. Note that if there are surface atoms that you do not want molecules to adsorb to, dont include them in this list. 
* **cutoff** (*float* or *dict.*): This is the maximum distance between atoms to be considered ``bonded`` or ``neighbouring``. This is used to determine bridging, three-fold, and four-fold sites. This is given as a float for monoatomic cluster and surface systems, or for a multiatomic system if you are happy for the max bonding distance between any two elements to be the same. If you would like different element pairs to have different maximum bonding distances, this is given as a dictionary. For example, for a CuPd system: ``cutoff = {'Cu': 3.2, 'Pd': 3.6, ('Cu','Pd'): 3.4}``

Run ``Adsorber PartB`` 
----------------------

Once you have written your ``general.py``, ``adsorbate.py``, and ``partB.py`` scripts, you can then run ``Adsorber`` in the terminal with the following input:

.. code-block:: bash

   Adsorber PartB

What will ``Adsorber`` do?
--------------------------

This will create a folder called ``Part_B_All_Systems_with_Adsorbed_Species`` that contains adsorbates that are adsorbed at various sites across your system in ``xyz`` format. ``xyz`` files are found in the path: ``Part_B_All_Systems_with_Adsorbed_Species\ADSORBATE\ADSORPTIONSITE``, where ``ADSORBATE`` is the adsorbate you want to focus on, and ``ADSORPTIONSITE`` is the type of surface site that the adsorbate is bound to, being:

* ``Top_Sites``: These are adsorbates that are bound to top sites above each surface atom.
* ``Bridge_Sites``: These are adsorbates that are bound to bridging sites.
* ``Three_Fold_Sites``: These are adsorbates that are bound to three fold sites. 
* ``Four_Fold_Sites``: These are adsorbates that are bound to four fold sites. 

Adsorber will created many ``xyz`` files, many of which you may not want to run in VASP. This may be because many of the sites are structural degenerate, or to orientate the adsorbate in certain directions. 

What do you need to do?
-----------------------

What you need to do is choose which xyz files you want to locally optimise in VASP. To do this, VASP will also create another folder called ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files``. What you want do is to **choose is to select the adsorbates in the sites and orientations that you want to optimise in VASP from the ** ``Part_B_All_Systems_with_Adsorbed_Species`` **folder and copy them into the** ``Part_C_Selected_Systems_with_Adsorbed_Species_to_Convert_into_VASP_files`` **folder**. **It is HIGHLY recommended you read** :ref:`Part_B2_What_to_do_with_files_from_Part_B` **to read about how to do this in more detail**. 