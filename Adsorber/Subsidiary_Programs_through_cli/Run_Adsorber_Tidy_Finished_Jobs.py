class CLICommand:
    """This command is designed to remove all the unnecessary files from VASP optimisations once you have finished. This is meant to decease the space of your data as well as the filecount. To be used once you are done and dusted.  
    """

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('delete_all_unnecessary_files', nargs='*', help='delete all unnecessary files.')

    @staticmethod
    def run(args):
        Run_method(args)

def Run_method(args_tidy):
    '''
    Geoffrey Weal, LatticeFinder_Tidy_Finished_Jobs.py, 30/04/2021

    This program is designed to remove the files of jobs that have finished. 

    '''
    import os
    from ase.io import read

    VASP_Files_folder_name = 'VASP_Files'
    files_to_remove = ['CHG','CHGCAR','DOSCAR','EIGENVAL','fe.dat','IBZKPT','OSZICAR','PCDAT','POTCAR','REPORT','vasprun.xml','vaspout.eps','WAVECAR','XDATCAR','vdw_kernel.bindat'] # 'CONTCAR', 'INCAR','KPOINTS','POSCAR','submit.sl'

    args_tidy_delete_all_unnecessary_files = args_tidy.delete_all_unnecessary_files

    if (args_tidy_delete_all_unnecessary_files[0].lower() == 'full'):
        files_to_remove += ['INCAR','KPOINTS','submit.sl']

    # always keep POSCAR, OUTCAR, and CONTCAR

    print('================================================================')
    print('Cleaning the following files from completed VASP runs:')
    print(files_to_remove)

    for root, dirs, files in os.walk("."):
        if VASP_Files_folder_name in root:
            dirs[:] = []
            files[:] = []
            continue
        for index in range(len(dirs)-1,-1,-1):
            dirname = dirs[index]
            if dirname.startswith(VASP_Files_folder_name):
                del dirs[index]
        dirs.sort()
        files.sort()
        if 'OUTCAR' in files:
            try:
                system = read(root+'/'+'OUTCAR')
                system.get_potential_energy()
                system.get_volume()
            except Exception:
                dirs[:] = []
                files[:] = []
                continue
            print(root)
            for file_to_remove in files_to_remove:
                if file_to_remove in files:
                    os.remove(root+'/'+file_to_remove)
                if file_to_remove.startswith('core.'):
                    os.remove(root+'/'+file_to_remove)
            '''
            for file in files:
                if file.startswith('slurm-') and file.endswith('.out'):
                    os.remove(root+'/'+file)
                elif file.startswith('slurm-') and file.endswith('.err'):
                    os.remove(root+'/'+file)
            '''
            dirs[:] = []
            files[:] = []

    print('================================================================')