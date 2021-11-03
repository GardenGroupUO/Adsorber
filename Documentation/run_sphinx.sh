echo "Deleting files in Build"
rm -rf build
echo "Running Sphinx"
#pip3 install --user --upgrade sphinx sphinx-pyreverse sphinx-rtd-theme sphinx-tabs sphinxcontrib-plantuml sphinxcontrib-websupport
#pip3 install --user --upgrade sphinx sphinx-pyreverse sphinx-rtd-theme sphinx-tabs sphinxcontrib-plantuml sphinxcontrib-websupport astroid==2.6.6  docutils==0.16.0
sphinx-build -b html source build
#sphinx-build -b latex source build
#sphinx-build -b wikipage source build
#sphinx-build -M latexpdf source build
