class CLICommand:
    """This command is designed to remove all the unnecessary files from VASP optimisations once you have finished. This is meant to decease the space of your data as well as the filecount. To be used once you are done and dusted.  
    """

    @staticmethod
    def add_arguments(parser):
        pass

    @staticmethod
    def run(args):
        Run_method()

import os
from Adsorber.Subsidiary_Programs_through_cli.Run_Adsorber_single_prep_for_resubmission import Run_method as prep_method
from Adsorber.Subsidiary_Programs_through_cli.Run_Adsorber_repeat_current_job           import Run_method as repeat_method

def Run_method():
    folder_name = os.path.basename(os.getcwd())
    print('===========================')
    print('PREPPING: '+str(folder_name))
    if prep_method():
        print('===========================')
        print('CREATING REPEAT JOB FOR: '+str(folder_name))
        repeat_method()
    else:
        print('The prep method did not finish successfully. Will not create repeat job folder.')
    print('===========================')