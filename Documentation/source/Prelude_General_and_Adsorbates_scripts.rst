
.. _Prelude_General_and_Adsorbates_scripts: 

Prelude 1: Setting your ``general.py`` and ``adsorbate.py`` scripts
###################################################################

The ``Adsorber`` program reads in five input scripts that tell the program how to make the files required to study the adsorption of adsorbates on surfaces and clusters. Theses are:

* ``general.py``: Contains general settings required for all parts of running this program.
* ``adsorbate.py``: Contains information about the types and configurations of adsorbates.
* ``partA.py``: Contains settings regarding Part A.
* ``partB.py``: Contains settings regarding Part B.
* ``partC.py``: Contains settings regarding Part C.

In this page we will talk about how to set up the ``general.py`` and ``adsorbate.py`` scripts.

Setting your ``general.py`` scripts
------------------------------------

We will explain what inputs need to be given in the ``general.py`` script by using the example shown below:

.. literalinclude:: input_files/general.py
	:language: python
	:caption: general.py
	:name: general.py
	:tab-width: 4
	:linenos:

The following input variables are required in the ``general.py`` script:

* **cluster_or_surface_model** (*str.*): This tells ``Adsorber`` if you are wanting to adsorb atoms and clusters to the surface of a cluster or a surface model. 

	* If you are dealing with a cluster, set ``cluster_or_surface_model = 'cluster'``, 
	* f you are dealing with a surface model, set ``cluster_or_surface_model = 'surface model'`` and make sure that your surface and vacuum point in the positive z direction. Adsorber will only attach adsorbates to surfaces from the positive z direction. 

* **system_filename** (*str.*): The name of the file of the cluster or the surface model that you will like to import into Adsorber. This file should be a ``.xyz`` or ``.traj`` file, but in reality any file type will do that ASE can read (see https://wiki.fysik.dtu.dk/ase/ase/io/io.html for more information on formats that ASE can read). For surfaces, you should have already performed surface convergence studies before proceeding with part A. If you want to constrain any atoms in your model, this should be done in this xyz/traj file.
* **add_vacuum** (optional, *float*): This will add a vacuum around your cluster. This is optional, if you do not give this in your ``general.py`` script, your input will be left untouched. 

.. _Setting_your_adsorbatepy_scripts:

Setting your ``adsorbate.py`` scripts
-------------------------------------

We will explain what inputs need to be given in the ``adsorbate.py`` script by using the example shown below:

.. literalinclude:: input_files/adsorbates.py
	:language: python
	:caption: adsorbates.py
	:name: adsorbates.py
	:tab-width: 4
	:linenos:

The only input that is needed from this script is the **adsorbed_species** list. This list contains all the information about each of the adsorbates you would like to adsorb to your system. 

For each adsorbate given, you need to provide a dictionary that contains the following:

* **name** (*str.*): This is the name of the molecule. Give the distinguishing chemical name at the start of this string. If you want to add any other information to the name, add this after a ``_``. For example, if you have a COOH molecule that you would like to configure with the H atom pointing up or down, given these different configurations as ``'name': 'COOH_up'`` and ``'name': 'COOH_down'``. Both of these configurations will be analysed together as ``'COOH'`` by Adsorber, but allows you to begin with different configurations of the adsorbate upon your system.
* **molecule** (*ase.Atoms*): The is the ``Atoms`` object for the atom or molecule, as obtained from the ``molecule`` or ``read`` method as mentioned above.
* **distance_of_adatom_from_surface** (*float*): This is the binding distance that you would like the atom or molecule to be initially placed from the cluster or surface model before you perform further optimisation with DFT. 
* **sites_to_bind_adsorbate_to** (optional, *list of str.*): This list indicates those types of sites that you would like to bind adsorbates to, be it top, bridge, three-fold, and four-fold binding sites. Default: ['Top_Sites','Bridge_Sites','Three_Fold_Sites','Four_Fold_Sites'']

	* include ``'Top_Sites'`` in this list if you want to attach adsorbate to **top** sites.
	* include ``'Bridge_Sites'`` in this list if you want to attach adsorbate to **bridge** sites.
	* include ``'Three_Fold_Sites'`` in this list if you want to attach adsorbate to **three fold** sites.
	* include ``'Four_Fold_Sites'`` in this list if you want to attach adsorbate to **four fold** sites.

For single atoms, this is all that is needed. If you want to adsorb molecules that have two or more atoms in it, you want to give two or three additional inputs into this dictionary.

* **index** (*int.*): This is the index of the atom in the molecule to adsorb to the surface for the cluster/surface model. See :ref:`bind_molecule_to_surface_of_system` for more information on how to select the index of the atom in the molecule you would like to be adsorbed to the surface. 
* **axis** (*str./list/tuple*): This is the axis in your molecule that you would like to point away from the surface of the cluster/surface model, as well as to rotate your moleule around (if you would like to rotate your molecule around the axis). See :ref:`bind_molecule_to_surface_of_system` for more information for how to specify this axis. 
* **rotations** (*list/tuple*, optional): These are the angles of rotation that you would like to rotate the molecules around the **axis** on the surface of your cluster/surface model. If you have a linear molecule that is alligned to the **axis** or you do not want to rotate your molecule around the **axis**, you do not need to add this as this is an optional input. See :ref:`bind_molecule_to_surface_of_system` for more information about how to specify how to best rotate your molecule about the **axis** on the surface of your cluster/surface model. 

See :ref:`bind_molecule_to_surface_of_system` for more information about how to obtain the **index**, **axis**, and **rotations** inputs for your adsorbates. 