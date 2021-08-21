#!/usr/bin/env python3
'''
Geoffrey Weal, Run_Adsorber_submitSL_slurm.py, 16/06/2021

This program is designed to submit all sl files called submit.sl to slurm

'''
print('###########################################################################')
print('###########################################################################')
print('Run_submitSl_slurm.py')
print('###########################################################################')
print('This program is designed to submit all your submit.sl scripts appropriately to slurm.')
print('###########################################################################')
print('###########################################################################')

import os, time, sys
import subprocess

# ------------------------------------------------------
# These variables can be changed by the user.
Max_jobs_in_queue_at_any_one_time = 10000
time_to_wait_before_next_submission = 20.0
time_to_wait_max_queue = 60.0

time_to_wait_before_next_submission_due_to_temp_submission_issue = 10.0
number_of_consecutive_error_before_exitting = 20

time_to_wait_before_next_submission_due_to_not_waiting_between_submissions = 60.0
# ------------------------------------------------------

if len(sys.argv) > 1:
    wait_between_submissions = str(sys.argv[1]).lower()
    if wait_between_submissions in ['t','true']:
        wait_between_submissions = True
    elif wait_between_submissions in ['f','false']:
        wait_between_submissions = False
    else:
        print('If you pass this program an argument, it must be either: ')
        print('    t, true, True: will wait 1 minute between submitting jobs')
        print('    f, false. False: will not wait between submitting jobs')
        print('If no argument is entered, the default is given as True')
        exit('This program will exit without running')
else:
    wait_between_submissions = False

if wait_between_submissions == True:
    print('This program will wait one minute between submitting jobs.')
else:
    print('This program will not wait between submitting jobs.')
path = os.getcwd()

def countdown(t):
    print('Will wait for ' + str(float(t)/60.0) + ' minutes, then will resume Slurm submissions.\n')
    while t:
        mins, secs = divmod(t, 60)
        timeformat = str(mins) + ':' + str(secs)
        #timeformat = '{:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write("\r                                                                                   ")
        sys.stdout.flush()
        sys.stdout.write("\rCountdown: " + str(timeformat))
        sys.stdout.flush()
        time.sleep(1)
        t -= 1
    print('Resuming Pan Submissions.\n')

def myrun(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_lines = list(iter(proc.stdout.readline,b''))
    stdout_lines = [line.decode() for line in stdout_lines]
    #stdout_lines = [print(line) for line in iter(proc.stdout.readline,'')]
    #import pdb; pdb.set_trace()
    #proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout_lines = [line for line in io.TextIOWrapper(proc.stdout, encoding="utf-8")]
    """from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html"""
    '''
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        if line == '' and p.poll() != None:
            break
    '''
    return ''.join(stdout_lines)

###########################################################################################
###########################################################################################
###########################################################################################

def get_number_to_trials_that_will_be_submitted_by_submitSL(dirpath):
    return 1

command = "squeue -r -u $USER"
def check_max_jobs_in_queue_after_next_submission(dirpath):
    while True:
        text = myrun(command)
        nlines = len(text.splitlines())-1
        if not (nlines == -1):
            break
        else:
            print('Could not get the number of jobs in the slurm queue. Retrying to get this value.')
    number_of_trials_to_be_submitted = get_number_to_trials_that_will_be_submitted_by_submitSL(dirpath)
    if nlines > Max_jobs_in_queue_at_any_one_time - number_of_trials_to_be_submitted:
        return True, nlines
    else:
        return False, nlines

###########################################################################################
###########################################################################################
###########################################################################################

# Time to submit all the GA scripts! Lets get this stuff going!
if not wait_between_submissions:
    max_consec_counter = 250
    consec_counter = 0
submitting_command = "sbatch submit.sl"
for (dirpath, dirnames, filenames) in os.walk(path):
    dirnames.sort()
    if 'submit.sl' in filenames:
        if 'OUTCAR' in filenames:
            dirnames[:] = []
            filenames[:] = []
            continue
        # determine if it is the right time to submit jobs
        print('*****************************************************************************')
        while True:
            reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath)
            if reached_max_jobs:
                print('-----------------------------------------------------------------------------')
                print('You can not have any more jobs in the queue before submitting the mass_sub. Will wait a bit of time for some of them to complete')
                print('Number of Jobs in the queue = '+str(number_in_queue))
                countdown(time_to_wait_before_next_submission)
                print('-----------------------------------------------------------------------------')
            else:
                print('The number of jobs in the queue currently is: '+str(number_in_queue))
                break
        # submit the jobs
        os.chdir(dirpath)
        name = dirpath.replace(path, '').split('/', -1)[1:]
        name = "_".join(str(x) for x in name)
        print("Submitting " + str(name) + " to slurm.")
        print('Submission .sl file found in: '+str(os.getcwd()))
        error_counter = 0
        while True:
            if error_counter == number_of_consecutive_error_before_exitting:
                break
            else:
                proc = subprocess.Popen(submitting_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if not proc.wait() == 0:
                    error_counter += 1
                    if error_counter == number_of_consecutive_error_before_exitting:
                        print('----------------------------------------------')
                        print('Error in submitting submit script to slurm.')
                        print('I got '+str(number_of_consecutive_error_before_exitting)+" consecutive errors. Something must not be working right somewhere. I'm going to stop here just in case something is not working.")
                        print('')
                        print('The following submit.sl scripts WERE NOT SUBMITTED TO SLURM')
                        print('')
                    else:
                        stdout, stderr = proc.communicate()
                        print('----------------------------------------------')
                        print('Error in submitting submit script to slurm. This error was:')
                        print(stderr)
                        print('Number of consecutive errors: '+str(error_counter))
                        print('Run_submitSL_slurm.py will retry submitting this job to slurm after '+str(time_to_wait_before_next_submission_due_to_temp_submission_issue)+' seconds of wait time')
                        print('----------------------------------------------')
                        countdown(time_to_wait_before_next_submission_due_to_temp_submission_issue)
                else:
                    break
        if error_counter == number_of_consecutive_error_before_exitting:
            print(dirpath)
        else:
            if wait_between_submissions:
                reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath)
                print('The number of jobs in the queue after submitting job is currently is: '+str(number_in_queue))
                #print('Will wait for '+str(time_to_wait_max_queue)+' to give time between consecutive submissions')
                countdown(time_to_wait_max_queue)
                print('*****************************************************************************')
        dirnames[:] = []
        filenames[:] = []
        if not wait_between_submissions:
            if consec_counter >= max_consec_counter:
                print('----------------------------------------------')
                print('As you are not waiting between consecutive submissions, it is good practise to wait for a minute at some stage')
                print(str(max_consec_counter) +' have been submitted consecutively. Will not wait for '+str(time_to_wait_before_next_submission_due_to_not_waiting_between_submissions)+' s before continuing')
                print('----------------------------------------------')
                countdown(time_to_wait_before_next_submission_due_to_not_waiting_between_submissions)
                consec_counter = 0
            else:
                consec_counter += 1


if error_counter == number_of_consecutive_error_before_exitting:
    print('----------------------------------------------')
    print()
    print('"Run_submitSL_slurm.py" will finish WITHOUT HAVING SUBMITTED ALL JOBS.')
    print()
    print('*****************************************************************************')
    print('NOT ALL submit.sl SCRIPTS WERE SUBMITTED SUCCESSFULLY.')
    print('*****************************************************************************') 
else:
    print('*****************************************************************************')
    print('*****************************************************************************')
    print('*****************************************************************************')
    print('All submit.sl scripts have been submitted to slurm successfully.')
    print('*****************************************************************************')
    print('*****************************************************************************')
    print('*****************************************************************************')