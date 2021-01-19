import argparse
import os
import shutil as sh
import glob
import subprocess as sp
import numpy as np
import nibabel as nib
import pandas as pd


# Hardcoded variables
# singularityVersion > runSingularity.sh








# CHOOSE TOOL
# tool   ="fs_7.1.1-03d"
# tool   ="rtppreproc_1.1.3"
tool   ="rtp-pipeline_4.3.7"

# CHOOSE ANALYSI SNUMBER
analysis="01" 

# CHOOSE PROJECT
pj = "BERTSOLARI" # possible values: BERTSOLARI, MAGNO, ThaTract

# CHOOSE HOST
host ='bcbl' # possible values: dipc, bcbl




# IT SHOOULD WORK BELOW
# find the correct code dir
if pj == "MAGNO":
    gitdir = "paper-MAGNO"
elif pj == "BERTSOLARI":
    gitdir = "paper-MAGNO"
elif pj == "ThaTract":
    gitdir = "ThaTract"


if host == "dipc":
    
    basedir = f"/scratch/lmx/{pj}"
    codedir = f"/dipc/lmx/GIT/{gitdir}"
    mem = "100G"  # memory to use for each qsub task
    que = "bcbl"  # in dipc cluster, we can only submit tasks to bcbl queue
    core = 6      # use 6 cores to compute one single task
    tmpdir = "/scratch/lmx" # this will pass to SINGULARITYENV_TMPDIR for matlab use.
    sin_ver = "Singularity/3.5.3-GCC-8.3.0" 
    container = f"/scratch/lmx/containers/{tool}.sif"

elif host == "bcbl":
    
    basedir = f"/bcbl/home/public/Gari/{pj}"
    codedir = f"/bcbl/home/home_g-m/glerma/GIT/{gitdir}"
    mem = "31G"     
    que = "long.q"
    core = "6"
    tmpdir = "/scratch" # in bcbl, /scratch is writable, it's ok to use /scratch as tmp dir
    sin_ver = "singularity/3.5.2"
    container = f"/bcbl/home/home_g-m/glerma/containers/{tool}.sif"

qsub="True"   # use qsub to run singualrity or not, possible values: 'True' or 'False'


# Get the unique list of subjects and sessions
subseslist=os.path.join(codedir,f"subSesList_{pj}.txt")
os.chdir(codedir)

# all arguments we need to submit the task
"""
-t tool       # which container we are running
-s sub        # subject
-e ses        # session
-a analysis   # analysis
-b basedir    # the base dir of project
-o codedir    # the git dir of project
-m mem        # how much memory to request for qsub
-q que        # queue to submit the tasks
-c core       # core numbers to request for qsub
-p tmpdir     # tmp dir for singularity containers
-i sin_ver    # singularity version
-n container  # the location of the container to run
-u noqsub     # use qsub or not
"""

# READ THE FILE
dt = pd.read_csv(subseslist, sep=",", header=0)

for row in dt.itertuples(index=True, name='Pandas'):
    sub  = row.sub
    ses  = row.ses
    RUN  = row.RUN
    dwi  = row.dwi
    func = row.func
    if RUN and dwi:
        cmdstr = (f"{codedir}/qsub_generic.sh " + 
                  f"-t {tool} -s {sub} -e {ses} " + 
                  f"-a {analysis} "              +
                  f"-b {basedir} -o {codedir} " + 
                  f"-m {mem} -q {que} -c {core} " + 
                  f"-p {tmpdir} -i {sin_ver} " + 
                  f"-n {container} -u {qsub} ")
        print(cmdstr)
        sp.call(cmdstr, shell=True)
