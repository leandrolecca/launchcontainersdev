#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 17:26:14 2023

@author: leiyongning
"""
#%%
import argparse
import os
import shutil as sh
import glob 
import subprocess as sp
import numpy as np
import pip
package='nibabel'
# !{sys.executable} -m pip install nibabel  # inside jupyter console
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])
import_or_install(package)
import nibabel as nib
import pandas as pd
import yaml
from yaml.loader import SafeLoader

from read_config_yaml import *

#%%
subseslist = os.path.join(basedir, 'nifti', "subSesList.txt")
dt = pd.read_csv(subseslist, sep=",", header=0)
for index in dt.index:
    sub = dt.loc[index, 'sub']
   # if isinstance(sub.item(),int):
   #     sub=str(sub)

    ses = dt.loc[index, 'ses']
    run = dt.loc[index, 'RUN']
    dwi = dt.loc[index, 'dwi']
    func = dt.loc[index, 'func']

def createsymlink_rtppreproc():    
    # Main source dir
    
    srcDir=os.path.join(basedir, 'Nifti', 'sub-'+sub, 'ses-'+ses)
    # FS source dir
    srcDirfs=os.path.join(basedir, 'Nifti', 'derivatives', precontainerfs,
                            'analysis-'+preanalysisfs, 'sub-'+sub, 'ses-'+ses, 'output')
    # File dirs
    srcT1file=os.path.join(srcDirfs, "T1.nii.gz")
    srcMaskFile=os.path.join(srcDirfs, "brainmask.nii.gz")

    srcDwiF_niiFile=os.path.join(
        srcDir, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-AP_dwi.nii.gz")
    srcDwiF_bvalFile=os.path.join(
        srcDir, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-AP_dwi.bval")
    srcDwiF_bvecFile=os.path.join(
        srcDir, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-AP_dwi.bvec")

    if rpe:
        srcDwiR_niiFile=os.path.join(
            srcDir, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-PA_dwi.nii.gz")
        srcDwiR_bvalFile=os.path.join(
            srcDir, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-PA_dwi.bval")
        srcDwiR_bvecFile=os.path.join(
            srcDir, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-PA_dwi.bvec")

        # If bval and bvec do not exist because it is only b0-s, create them
        # (it would be better if dcm2niix would output them but...)
        img=nib.load(srcDwiR_niiFile)
        volumes=img.shape[3]
        if (not os.path.isfile(srcDwiR_bvalFile)) or (not os.path.isfile(srcDwiR_bvecFile)):
            # Write bval file
            f=open(srcDwiR_bvalFile, "x")
            f.write(volumes * "0 ")
            f.close()

            # Write bvec file
            f=open(srcDwiR_bvecFile, "x")
            f.write(volumes * "0 ")
            f.write("\n")
            f.write(volumes * "0 ")
            f.write("\n")
            f.write(volumes * "0 ")
            f.write("\n")
            f.close()

    # Main destination  dir
    dstDir=os.path.join(basedir, 'Nifti', 'derivatives', container,
                          'analysis-'+analysis, 'sub-'+sub, 'ses-'+ses, 'input')
    dstDirOp=os.path.join(basedir, 'Nifti', 'derivatives', container,
                            'analysis-'+analysis, 'sub-'+sub, 'ses-'+ses, 'output')
    # Create folders if they do not exist
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    if not os.path.exists(dstDirOp):
        os.makedirs(dstDirOp)

    if not os.path.exists(os.path.join(dstDir, "ANAT")):
        os.makedirs(os.path.join(dstDir, "ANAT"))
    if not os.path.exists(os.path.join(dstDir, "FSMASK")):
        os.makedirs(os.path.join(dstDir, "FSMASK"))
    if not os.path.exists(os.path.join(dstDir, "DIFF")):
        os.makedirs(os.path.join(dstDir, "DIFF"))
    if not os.path.exists(os.path.join(dstDir, "BVAL")):
        os.makedirs(os.path.join(dstDir, "BVAL"))
    if not os.path.exists(os.path.join(dstDir, "BVEC")):
        os.makedirs(os.path.join(dstDir, "BVEC"))
    if rpe:
        if not os.path.exists(os.path.join(dstDir, "RDIF")):
            os.makedirs(os.path.join(dstDir, "RDIF"))
        if not os.path.exists(os.path.join(dstDir, "RBVL")):
            os.makedirs(os.path.join(dstDir, "RBVL"))
        if not os.path.exists(os.path.join(dstDir, "RBVC")):
            os.makedirs(os.path.join(dstDir, "RBVC"))
    # Create the destination paths
    dstT1file=os.path.join(dstDir, 'ANAT', "T1.nii.gz")
    dstMaskFile=os.path.join(dstDir, 'FSMASK', "brainmask.nii.gz")
    dstDwiF_niiFile=os.path.join(dstDir, "DIFF", "dwiF.nii.gz")
    dstDwiF_bvalFile=os.path.join(dstDir, "BVAL", "dwiF.bval")
    dstDwiF_bvecFile=os.path.join(dstDir, "BVEC", "dwiF.bvec")
    if rpe:
        dstDwiR_niiFile=os.path.join(dstDir, "RDIF", "dwiR.nii.gz")
        dstDwiR_bvalFile=os.path.join(dstDir, "RBVL", "dwiR.bval")
        dstDwiR_bvecFile=os.path.join(dstDir, "RBVC", "dwiR.bvec")

    # Create the symbolic links
    os.symlink(srcT1file, dstT1file)
    os.symlink(srcMaskFile, dstMaskFile)
    os.symlink(srcDwiF_niiFile, dstDwiF_niiFile)
    os.symlink(srcDwiF_bvalFile, dstDwiF_bvalFile)
    os.symlink(srcDwiF_bvecFile, dstDwiF_bvecFile)
    if rpe:
        os.symlink(srcDwiR_niiFile, dstDwiR_niiFile)
        os.symlink(srcDwiR_bvalFile, dstDwiR_bvalFile)
        os.symlink(srcDwiR_bvecFile, dstDwiR_bvecFile)
    
createsymlink_rtppreproc()
