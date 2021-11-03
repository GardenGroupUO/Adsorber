
.. _Installation:

Installation: Setting Up Adsorber and Pre-Requisites Packages
#############################################################

In this article, we will look at how to install the Adsorber and all requisites required for this program.

Pre-requisites
==============

Python 3 and ``pip3``
---------------------

This program is designed to work with **Python 3**. While this program has been designed to work with Python 3.6, it should work with any version of Python 3 that is the same or later than 3.6.

To find out if you have Python 3 on your computer and what version you have, type into the terminal

.. code-block:: bash

	python3 --version

If you have Python 3 on your computer, you will get the version of python you have on your computer. E.g.

.. code-block:: bash

	geoffreyweal@Geoffreys-Mini Documentation % python3 --version
	Python 3.6.3

If you have Python 3, you may have ``pip3`` installed on your computer as well. ``pip3`` is a python package installation tool that is recommended by Python for installing Python packages. To see if you have ``pip3`` installed, type into the terminal

.. code-block:: bash

	pip3 list

If you get back a list of python packages install on your computer, you have ``pip3`` installed. E.g.

.. code-block:: bash

	geoffreyweal@Geoffreys-Mini Documentation % pip3 list
	Package                       Version
	----------------------------- ---------
	alabaster                     0.7.12
	asap3                         3.11.10
	ase                           3.20.1
	Babel                         2.8.0
	certifi                       2020.6.20
	chardet                       3.0.4
	click                         7.1.2
	cycler                        0.10.0
	docutils                      0.16
	Flask                         1.1.2
	idna                          2.10
	imagesize                     1.2.0
	itsdangerous                  1.1.0
	Jinja2                        2.11.2
	kiwisolver                    1.2.0
	MarkupSafe                    1.1.1
	matplotlib                    3.3.1
	numpy                         1.19.1
	packaging                     20.4
	Pillow                        7.2.0
	pip                           20.2.4
	Pygments                      2.7.1
	pyparsing                     2.4.7
	python-dateutil               2.8.1
	pytz                          2020.1
	requests                      2.24.0
	scipy                         1.5.2
	setuptools                    41.2.0
	six                           1.15.0
	snowballstemmer               2.0.0
	Sphinx                        3.2.1
	sphinx-pyreverse              0.0.13
	sphinx-rtd-theme              0.5.0
	sphinx-tabs                   1.3.0
	sphinxcontrib-applehelp       1.0.2
	sphinxcontrib-devhelp         1.0.2
	sphinxcontrib-htmlhelp        1.0.3
	sphinxcontrib-jsmath          1.0.1
	sphinxcontrib-plantuml        0.18.1
	sphinxcontrib-qthelp          1.0.3
	sphinxcontrib-serializinghtml 1.1.4
	sphinxcontrib-websupport      1.2.4
	urllib3                       1.25.10
	Werkzeug                      1.0.1
	wheel                         0.33.1
	xlrd                          1.2.0

If you do not see this, you probably do not have ``pip3`` installed on your computer. If this is the case, check out `PIP Installation <https://pip.pypa.io/en/stable/installing/>`_

.. _Install_ASE:

Atomic Simulation Environment
-----------------------------

Adsorber uses the atomic simulation environment (ASE) to create models of clusters and surfaces that have atoms and moleucles adsorbed to its surface. Read more about `ASE here <https://wiki.fysik.dtu.dk/ase/>`_. 

The installation of ASE can be found on the `ASE installation page <https://wiki.fysik.dtu.dk/ase/install.html>`_, however from experience if you are using ASE for the first time, it is best to install ASE using pip, the package manager that is an extension of python to keep all your program easily managed and easy to import into your python. 

To install ASE using pip, perform the following in your terminal.

.. code-block:: bash

	pip3 install --upgrade --user ase

Installing using ``pip3`` ensures that ASE is being installed to be used by Python 3, and not Python 2. Installing ASE like this will also install all the requisite program needed for ASE. This installation includes the use of features such as viewing the xyz files of structure and looking at ase databases through a website. These should be already assessible, which you can test by entering into the terminal:

.. code-block:: bash

	ase gui

This should show a gui with nothing in it, as shown below.

.. figure:: Images/ase_gui_blank.png
   :align: center
   :figwidth: 50%
   :alt: ase_gui_blank

   This is a blank ase gui screen that you would see if enter ``ase gui`` into the terminal.

However, in the case that this does not work, we need to manually add a path to your ``~/.bashrc`` so you can use the ASE features externally outside python. First enter the following into the terminal:

.. code-block:: bash

	pip3 show ase

This will give a bunch of information, including the location of ase on your computer. For example, when I do this I get:

.. code-block:: bash

	Geoffreys-Mini:~ geoffreyweal$ pip show ase
	Name: ase
	Version: 3.20.1
	Summary: Atomic Simulation Environment
	Home-page: https://wiki.fysik.dtu.dk/ase
	Author: None
	Author-email: None
	License: LGPLv2.1+
	Location: /Users/geoffreyweal/Library/Python/3.6/lib/python/site-packages
	Requires: matplotlib, scipy, numpy
	Required-by: 

In the 'Location' line, if you remove the 'lib/python/site-packages' bit and replace it with 'bin'. The example below is for Python 3.6. 

.. code-block:: bash

	/Users/geoffreyweal/Library/Python/3.6/bin

This is the location of these useful ASE tools. You want to put this as a path in your ``~/.bashrc`` as below:

.. code-block:: bash

	############################################################
	# For ASE
	export PATH=/Users/geoffreyweal/Library/Python/3.6/bin:$PATH
	############################################################





Networkx
--------

``Networkx`` is a python program that is used in ``Adsorber`` to determine if two systems are structurally identical. The easiest way to install ``Networkx`` is though pip. Type the following into the terminal:

.. code-block:: bash

	pip3 install --upgrade --user networkx

Openpyxl
--------

``Openpyxl`` is a python program that is used in ``Adsorber`` to write excel spreadsheets of information of your clusters and surface models with adsorbates attach once they have been locally optimised with VASP. The easiest way to install ``Openpyxl`` is though pip. Type the following into the terminal:

.. code-block:: bash

	pip3 install --upgrade --user openpyxl

Packaging
---------

The ``packaging`` program is also used in this program to check the versions of ASE that you are using for compatibility issues. The easiest way to install ``packaging`` is though pip. Type the following into the terminal:

.. code-block:: bash

	pip3 install --upgrade --user packaging


.. _Installation_of_Adsorber:

Setting up Adsorber
===================

There are three ways to install Adsorber on your system. These ways are described below:

Install Adsorber through ``pip3``
---------------------------------

To install the Adsorber program using ``pip3``, perform the following in your terminal.

.. code-block:: bash

	pip3 install --upgrade --user Adsorber

The website for Adsorber on ``pip3`` can be found by clicking the button below:

.. image:: https://img.shields.io/pypi/v/Adsorber
   :target: https://pypi.org/project/Adsorber/
   :alt: PyPI

Install Adsorber through ``conda``
----------------------------------

You can also install Adsorber through ``conda``, however I am not as versed on this as using ``pip3``. See `docs.conda.io <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html>`_ to see more information about this. Once you have installed anaconda on your computer, I believe you install Adsorber using ``conda`` by performing the following in your terminal.

.. code-block:: bash

	conda install ase
	conda install adsorber

The website for Adsorber on ``conda`` can be found by clicking the button below:

.. image:: https://img.shields.io/conda/v/gardengroupuo/adsorber
   :target: https://anaconda.org/GardenGroupUO/adsorber
   :alt: Conda

Manual installation
-------------------

First, download Adsorber to your computer. You can do this by cloning a version of this from Github, or obtaining a version of the program from the authors. If you are obtaining this program via Github, you want to ``cd`` to the directory that you want to place this program in on the terminal, and then clone the program from Github through the terminal as well

.. code-block:: bash
	
	cd PATH/TO/WHERE_YOU_WANT_Adsorber_TO_LIVE_ON_YOUR_COMPUTER
	git clone https://github.com/GardenGroupUO/Adsorber


Next, add a python path to it in your  ``.bashrc`` to indicate its location. Do this by entering into the terminal where you cloned the Adsorber program into ``pwd``

.. code-block:: bash

	pwd

This will give you the path to the Adsorber program. You want to enter the result from ``pwd`` into the ``.bashrc`` file. This is done as shown below:

.. code-block:: bash

	export PATH_TO_Adsorber="<Path_to_Adsorber>" 
	export PYTHONPATH="$PATH_TO_Adsorber":$PYTHONPATH

where ``"<Path_to_Adsorber>"`` is the directory path that you place Adsorber (Enter in here the result you got from the ``pwd`` command). Once you have run ``source ~/.bashrc``, the genetic algorithm should be all ready to go!

The folder called ``Examples`` contains all the files that one would want to used to use the genetic algorithm for various metals. This includes examples of the basic run code for Adsorber, the ``Run_Adsorber.py`` file. 

Adsorber contains subsidiary programs that may be useful to use when using the Adsorber program. This is called ``Subsidiary_Programs`` in Adsorber. To execute any of the programs contained within the ``Subsidiary_Programs`` folder, include the following in your ``~/.bashrc``:

.. code-block:: bash

	export PATH="$PATH_TO_Adsorber"/Adsorber/Subsidiary_Programs:$PATH

Visualisation Programs for looking at systems with adsorbed molecules
=====================================================================

As well as installing Adsorber, the Atomic Simulation Environment (ASE) GUI and Jmol programs are also used to visualise your system with adsorbed atoms and molecules upon it. Installation and how to use the ASE GUI and Jmol can be found in :ref:`External_programs_that_will_be_useful_to_install_for_using_Adsorber`.

Other Useful things to know before you start
--------------------------------------------

You may use squeue to figure out what jobs are running in slurm. For monitoring what slurm jobs are running, I have found the following alias useful. Include the following in your ``~/.bashrc``:

.. code-block:: bash
	
	squeue -o "%.20i %.9P %.5Q %.50j %.8u %.8T %.10M %.11l %.6D %.4C %.6b %.20S %.20R %.8q" -u $USER --sort=+i

There are also two aliases that are useful, these are 

* ``no_of_jobs_running_or_queued``: Will indicate the number of jobs that are either running or in the queue in slurm. 
* ``no_of_submitSL_files``: Will give the number of VASP models in subdirectories that are to be run. These should all contain submit.sl files, which is what this alias is doing. 

These two aliases are given below for you to also add to your ``~/.bashrc``:

.. code-block:: bash

	alias no_of_jobs_running_or_queued="echo $((squeue -u $USER | wc -l) | awk '{print $1 - 1}')"
	alias no_of_submitSL_files='find . -name "submit.sl" -type f -not -path "*Submission_Folder_*" | wc -l'

These two aliases are explained further in :ref:`How_to_submit_files_to_slurm`.

Summary of what you want in the ``~/.bashrc`` for the LatticeFinder program if you manually installed LatticeFinder
-------------------------------------------------------------------------------------------------------------------

You want to have the following in your ``~/.bashrc``:

.. code-block:: bash

	#########################################################
	# Paths and Pythonpaths for Adsorber

	export PATH_TO_Adsorber="<Path_to_Adsorber>" 
	export PYTHONPATH="$PATH_TO_Adsorber":$PYTHONPATH
	export PATH="$PATH_TO_Adsorber"/Adsorber/Subsidiary_Programs:$PATH

	squeue -o "%.20i %.9P %.5Q %.50j %.8u %.8T %.10M %.11l %.6D %.4C %.6b %.20S %.20R %.8q" -u $USER --sort=+i

	alias no_of_jobs_running_or_queued="echo $((squeue -u $USER | wc -l) | awk '{print $1 - 1}')"
	alias no_of_submitSL_files='find . -name "submit.sl" -type f -not -path "*Submission_Folder_*" | wc -l'

	#########################################################

