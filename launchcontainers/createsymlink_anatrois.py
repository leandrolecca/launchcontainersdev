#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:09:48 2023

@author: leiyongning
"""
# this is the createSymlink_anatrois
# the input of this function should be 
'''
  anatrois:
    container_version: 4.2.7-7.1.1
    # If you have run FS previously, you can say true here and it will use the existing output
    pre_fs: false
    # If pre_fs is true, it will try to find it using the two options below
    # It will find a zip file in the anatrois output, that starts with this string
    prefs_zipname: anatrois
    # There can be more than one analysis, give the number of the analysis here
    preanalysisfs: 01
    # These are optional input files. If there is none, leave it empty string
    # If it is empty, it will ignore it and will not create the input/folder
    annotfile: ""
    mniroizip: ""
'''
container_test=vars['container_options']['anatrois']
def createsymlink_anatrois(dict_of_container_options):
    globals().update(dict_of_container_options)
    
    if pre_fs:#pre_fs is a config boolean parameter
        #needs to ask, what is srcAnatPath? what is the naming strategy? 
        srcAnatPath = os.path.join(basedir,'nifti','derivatives',precontainerfs,'analysis-'+preanalysisfs,
                                   'sub-'+sub, 'ses-'+ses,'output')
        zips = sorted(glob.glob(os.path.join(srcAnatPath,prefs_zipname+'*')),key=os.path.getmtime)
        try:
            src_anatomical = zips[-1]
        except:
            print(f"{sub} doesn't have pre_fs, skipping")
            continue
    else:
        # what is scr_anatomical? 
        src_anatomical = os.path.join(
            basedir, 'nifti', 'sub-'+sub, 'ses-'+ses, 'anat', 'sub-'+sub+'_ses-'+ses+'_T1w.nii.gz')
    
    # Main destination  dir
    dstDirInputput = os.path.join(basedir, 'nifti', 'derivatives', container,
                            'analysis-'+analysis, 'sub-'+sub, 'ses-'+ses, 'input')
    dstDirOutput = os.path.join(basedir, 'nifti', 'derivatives', container,
                            'analysis-'+analysis, 'sub-'+sub, 'ses-'+ses, 'output')
    dstDirAnalysisalysis = os.path.join(basedir, 'nifti', 'derivatives', container,
                            'analysis-'+analysis)


   # Add two new variables to the config_launchcontainer.json file,
   # with the name and the location of the annot and mniroi zip
   # files
   # If it is an empty string, do nothing, otherwise, copy the file
   # to the analysis folder and create a symlink to the input folder
   # of the subject.





    # Create folders if they do not exist
    if not os.path.exists(dstDirInputput):
        os.makedirs(dstDirInputput)
    if not os.path.exists(dstDirOutput):
        os.makedirs(dstDirOutput)
    if pre_fs:
        if not os.path.exists(os.path.join(dstDirInput, "pre_fs")):
            os.makedirs(os.path.join(dstDirInput, "pre_fs"))
    else:
        if not os.path.exists(os.path.join(dstDirInput, "anat")):
            os.makedirs(os.path.join(dstDirInput, "anat"))
    if annotfile:    
        if os.path.isfile(annotfile):
            print('Passed '+annotfile+', copying to '+dstDirAnalysis)
            srcAnnotfile = os.path.join(dstDirAnalysis,'annotfile.zip')
            if os.path.isfile(srcAnnotfile):
                print(srcAnnotfile+' exists, if you want it new, delete it first')
            else:
                shutil.copyfile(annotfile,os.path.join(dstDirAnalysis,'annotfile.zip'))
        else:
            print(annotfile + ' does not exist')
        if not os.path.exists(os.path.join(dstDirInput, "annotfile")):
            os.makedirs(os.path.join(dstDirInput, "annotfile"))
    if mniroizip:    
        if os.path.isfile(mniroizip):
            print('Passed '+mniroizip+', copying to '+dstDirAnalysis)
            srcMniroizip = os.path.join(dstDirAnalysis,'mniroizip.zip')
            if os.path.isfile(srcMniroizip):
                print(srcMniroizip+' exists, if you want it new, delete it first')
            else:
                shutil.copyfile(mniroizip,os.path.join(dstDirAnalysis,'mniroizip.zip'))
        else:
            print(mniroizip + ' does not exist')
        if not os.path.exists(os.path.join(dstDirInput, "mniroizip")):
            os.makedirs(os.path.join(dstDirInput, "mniroizip"))

    # Create the destination paths
    if pre_fs:
        dstAnatomicalFile = os.path.join(dstDirInput, 'pre_fs',"existingFS.zip")
    else:
        dstAnatomicalFile = os.path.join(dstDirInput, 'anat', "T1.nii.gz")
    
    dstAnnotfile      = os.path.join(dstDirInput, 'annotfile',"annots.zip")
    dstMniroizip      = os.path.join(dstDirInput, 'mniroizip',"mniroizip.zip")

    # Create the symbolic links
    if os.path.isfile(dstAnatomicalFile):
        os.unlink(dstAnatomicalFile)
    if os.path.isfile(src_anatomical):
        os.symlink(src_anatomical, dstAnatomicalFile)
    else:
        print(src_anatomical + ' does not exist')

    if annotfile:
        if os.path.isfile(dstAnnotfile):
            os.unlink(dstAnnotfile)
        if os.path.isfile(srcAnnotfile):
            os.symlink(srcAnnotfile, dstAnnotfile)
        else:
            print(srcAnnotfile + ' does not exist')
    
    if mniroizip:
        if os.path.isfile(dstMniroizip):
            os.unlink(dstMniroizip)
        if os.path.isfile(srcMniroizip):
            os.symlink(srcMniroizip, dstMniroizip)
        else:
            print(srcMniroizip + ' does not exist')    
    
    print(locals()) 
    print("the symlink of anatrois container has been successfully create")
     

