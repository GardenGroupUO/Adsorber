#!/bin/bash -e
#SBATCH -J Adsorber_Run_COOH_symmetric_top_sites_29_106_rotation_119.2
#SBATCH -A uoo02568         # Project Account
#SBATCH --partition large

#SBATCH --time=48:00:00     # Walltime
#SBATCH --nodes=1
#On VASP, Ben Roberts recommends using the same number
#of tasks on all nodes, even if this makes scheduling
#a little more difficult
#SBATCH --ntasks-per-node=12
#SBATCH --mem-per-cpu=1200MB

#SBATCH --output=slurm-%j.out      # %x and %j are replaced by job name and ID
#SBATCH --error=slurm-%j.err
#SBATCH --mail-user=geoffreywealslurmnotifications@gmail.com
#SBATCH --mail-type=ALL
#SBATCH --hint nomultithread

module load VASP/5.3.5-intel-2017a-VTST-BEEF

#Run VASP job.
srun -K vasp_cd
