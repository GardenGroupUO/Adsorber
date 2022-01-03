from shutil import rmtree

from Adsorber import __version__

def get_version_number():
	version = __version__
	return version

def version_no():
	"""
	Will provide the version of the Adsorber program
	"""
	version = get_version_number() 
	return version

def introductory_remarks():
	print('=================================')
	print()
	print('            Adsorber             ')
	print()
	print('         Version: '+str(version_no()))
	print()
	print('=================================')

def finish_up():
	try:
		rmtree('__pycache__')
	except Exception as ee:
		print('Could not remove __pycache__')