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









# basedir="/bcbl/home/public/Gari/MAGNO2/"
basedir="/export/home/glerma/glerma/00local/PROYECTOS/MAGNO2/"
tool   ="fs_7.1.1-03"
# tool   ="rtppreproc_1.1.2"
# tool   ="rtp-pipeline_4.3.4"
analysis="01" 

# PREVIOUS ANALYSIS
# pretoolfs="fs_7.1.1-03"
# preanalysisfs="01"

# pretoolpp="rtppreproc_1.1.2"
# preanalysispp="01"

mem="60G"

# Get the unique list of subjects and sessions
codedir  = "/bcbl/home/home_g-m/glerma/GIT/paper-MAGNO"
subseslist=os.path.join(codedir,"subSesList.txt")
os.chdir(codedir)

# READ THE FILE
dt = pd.read_csv(subseslist, sep=",", header=0)

for row in dt.itertuples(index=True, name='Pandas'):
    sub  = row.sub
    ses  = row.ses
    RUN  = row.RUN
    dwi  = row.dwi
    func = row.func
    if RUN and dwi:
        cmd = os.path.join(codedir,'qsub_generic.sh')+' '+tool+' '+sub+' '+ses+' '+analysis+' '+mem 
        sp.call(cmd, shell=True)
