#%% import libraries
import os, errno
#%%
def force_symlink(file1, file2, force):
    '''
    Parameters
    ----------
    file1 : str 
        the path to the source file, which is the output of previous container
    file2 : str
        the path to the destination file, which is the input of the current container
    force : bool
        set in the config file

    Raises
    ------
    e
        OS error.

    Returns
    -------
    None.

    '''
    # if we don't force to overwrite
    if not force:
        try:
            #try the command, if the file are correct and symlink not exist, it will create one
            os.symlink(file1, file2)
            print ('The symlink are correctly created')
        #if raise [erron 2]: file not exist, print the error and pass
        except OSError as n: 
            if n.errno == 2:
                print ("file and directory are missing, maybe due to wrong defination")
        # if raise [erron 17] the symlink exist, we don't force and print that we keep the original one     
            if n.errno == errno.EEXIST:
                print(f"the destination file {file2} exist, remain it")
            else:
                raise n
    # if we force to overwrite
    if force :
        try:
         # try the command, if the file are correct and symlink not exist, it will create one   
            os.symlink(file1, file2)
            print ('The symlink are correctly created')
        # if the symlink exist, and in this case we force a overwrite
        except OSError as e:
            if e.errno == errno.EEXIST:
                os.remove(file2)
                os.symlink(file1, file2)
                print ('The symlink are correctly created')
            if e.errno == 2:
                print ("file and directory are missing, maybe due to wrong defination")
            else:
                raise e
    return
#%%
def rtppreproc_force_rpe(force,rpe,reverse_bvec, reverse_bval):
    '''
    Parameters
    ----------
    force : bool
        determine if we want to overwrite
    rpe : bool
        determine if we do reverse phase encoding
    reverse_bvec : str
        the path to reverse direction .bvec file
    reverse_bval : str
        the path to reverse direction .bval file

    Returns
    -------
    None.

    '''
    
    
    return
#%%
def anatrois(config, sub, ses):
    """
    Parameters
    ----------
    config : dict
        the config dictionary from _read_config
    sub : str
        the subject name looping from df_subSes
    ses : str
        the session name looping from df_subSes.

    Returns
    -------
    none, create symbolic links 

    """
    # define local variables from config dict
    # general level variables:
    basedir           = config["config"]["basedir"]
    container         = config["config"]["container"]
    force             = config['config']['force']
    analysis          = config["config"]["analysis"]
    # container specific: 
    pre_fs    = config["container_options"][container]["pre_fs"]
    prefs_zipname     = config["container_options"][container]["prefs_zipname"]
    # I added this line, shall we modify config yaml
    precontainerfs    = config["container_options"][container]["precontainerfs"]
    prenanlysisfs     = config["container_options"][container]["prenanlysisfs"]
    annotfile         = config["container_options"][container]["annotfile"]
    mniroizip         = config["container_options"][container]["mniroizip"]
    version           = config ["container_options"][container]["version"]
    
    # ????????
     if pre_fs:
         srcAnatPath = os.path.join(basedir,'Nifti','derivatives',pretoolfs,'analysis-'+preanalysisfs,
                                    'sub-'+sub, 'ses-'+ses,'output')
         zips = sorted(glob.glob(os.path.join(srcAnatPath,prefs_zipname+'*')),key=os.path.getmtime)
         try:
             src_anatomical = zips[-1]
         except:
             print(f"{sub} doesn't have pre_fs, skipping")
             continue
     else:
         src_anatomical = os.path.join(
             basedir, 'Nifti', 'sub-'+sub, 'ses-'+ses, 'anat', 'sub-'+sub+'_ses-'+ses+'_T1w.nii.gz')
     
     # Main destination  dir
     dstDirIn = os.path.join(basedir, 'Nifti', 'derivatives', tool,
                             'analysis-'+analysis, 'sub-'+sub, 'ses-'+ses, 'input')
     dstDirOp = os.path.join(basedir, 'Nifti', 'derivatives', tool,
                             'analysis-'+analysis, 'sub-'+sub, 'ses-'+ses, 'output')
     dstDirAn = os.path.join(basedir, 'Nifti', 'derivatives', tool,
                             'analysis-'+analysis)
     
     # Create folders if they do not exist
     if not os.path.exists(dstDirIn):
         os.makedirs(dstDirIn)
     if not os.path.exists(dstDirOp):
         os.makedirs(dstDirOp)
     if pre_fs:
         if not os.path.exists(os.path.join(dstDirIn, "pre_fs")):
             os.makedirs(os.path.join(dstDirIn, "pre_fs"))
     else:
         if not os.path.exists(os.path.join(dstDirIn, "anat")):
             os.makedirs(os.path.join(dstDirIn, "anat"))
     if annotfile:    
         if os.path.isfile(annotfile):
             print('Passed '+annotfile+', copying to '+dstDirAn)
             srcAnnotfile = os.path.join(dstDirAn,'annotfile.zip')
             if os.path.isfile(srcAnnotfile):
                 print(srcAnnotfile+' exists, if you want it new, delete it first')
             else:
                 shutil.copyfile(annotfile,os.path.join(dstDirAn,'annotfile.zip'))
         else:
             print(annotfile + ' does not exist')
         if not os.path.exists(os.path.join(dstDirIn, "annotfile")):
             os.makedirs(os.path.join(dstDirIn, "annotfile"))
     if mniroizip:    
         if os.path.isfile(mniroizip):
             print('Passed '+mniroizip+', copying to '+dstDirAn)
             srcMniroizip = os.path.join(dstDirAn,'mniroizip.zip')
             if os.path.isfile(srcMniroizip):
                 print(srcMniroizip+' exists, if you want it new, delete it first')
             else:
                 shutil.copyfile(mniroizip,os.path.join(dstDirAn,'mniroizip.zip'))
         else:
             print(mniroizip + ' does not exist')
         if not os.path.exists(os.path.join(dstDirIn, "mniroizip")):
             os.makedirs(os.path.join(dstDirIn, "mniroizip"))

     # Create the destination paths
     if pre_fs:
         dstAnatomicalFile = os.path.join(dstDirIn, 'pre_fs',"existingFS.zip")
     else:
         dstAnatomicalFile = os.path.join(dstDirIn, 'anat', "T1.nii.gz")
     dstAnnotfile      = os.path.join(dstDirIn, 'annotfile',"annots.zip")
     dstMniroizip      = os.path.join(dstDirIn, 'mniroizip',"mniroizip.zip")

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
    return
#%%    
def rtppreproc(config, sub, ses):    
    """
    Parameters
    ----------
    config : dict
        the config dictionary from _read_config
    sub : str
        the subject name looping from df_subSes
    ses : str
        the session name looping from df_subSes.

    Returns
    -------
    none, create symbolic links 

    """
    # define local variables from config dict
    # general level variables:
    basedir           = config["config"]["basedir"]
    container         = config["config"]["container"]
    force             = config['config']['force']
    analysis          = config["config"]["analysis"]
    # container specific: 
    precontainerfs    = config["container_options"][container]["precontainerfs"]
    preanalysisfs     = config["container_options"][container]["preanalysisfs"]
    rpe               = config["container_options"][container]["rpe"]
    version           = config ["container_options"][container]["version"]
    
    # define base directory for particular subject and session
    basedir_subses=os.path.join(basedir, 'Nifti', 'sub-'+sub, 'ses-'+ses)
    
    # the source directory that stores the output of previous anatorois analysis
    srcDirFs=os.path.join(basedir, 'Nifti', 'derivatives', precontainerfs,
                            'analysis-'+preanalysisfs, 'sub-'+sub, 'ses-'+ses, 'output')
    
    # define the source file, this is where symlink will point to
    # T1 file in anatrois output
    srcFileT1=os.path.join(srcDirFs, "T1.nii.gz")
    # brainmask file in anatrois output
    srcFileMask=os.path.join(srcDirFs, "brainmask.nii.gz")
    # 3 dwi file that needs to be preprocessed, under nifti/sub/ses/dwi
    # the nii.gz
    srcFileDwi_nii=os.path.join(
        basedir_subses, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-AP_dwi.nii.gz")
    # the bval.gz
    srcFileDwi_bval=os.path.join(
        basedir_subses, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-AP_dwi.bval")
    # the bvec.gz
    srcFileDwi_bvec=os.path.join(
        basedir_subses, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-AP_dwi.bvec")
    # check_create_bvec_bval（force) one of the todo here
    if rpe: 
        # the reverse direction nii.gz
        srcFileDwi_nii_R=os.path.join(
            basedir_subses, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-PA_dwi.nii.gz")
        # the reverse direction bval
        srcFileDwi_bval_R=os.path.join(
            basedir_subses, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-PA_dwi.bval")
        # the reverse diretion bvec
        srcFileDwi_bvec_R=os.path.join(
            basedir_subses, 'dwi', "sub-"+sub+"_ses-"+ses+"_acq-PA_dwi.bvec")

        # If bval and bvec do not exist because it is only b0-s, create them
        # (it would be better if dcm2niix would output them but...)
        # buildthe img matrix according to the shape of nii.gz
        img=nib.load(srcFileDwi_nii_R)
        volumes=img.shape[3]
        # if one of the bvec and bval are not there, re-write them
        if (not os.path.isfile(srcFileDwi_bval_R)) or (not os.path.isfile(srcFileDwi_bvec_R)):
            # Write bval file
            f=open(srcFileDwi_bval_R, "x")
            f.write(volumes * "0 ")
            f.close()

            # Write bvec file
            f=open(srcFileDwi_bvec_R, "x")
            f.write(volumes * "0 ")
            f.write("\n")
            f.write(volumes * "0 ")
            f.write("\n")
            f.write(volumes * "0 ")
            f.write("\n")
            f.close()

    # creat input and output directory for this container, the dir_output should be empty, the dir_input should contains all the symlinks
    dir_input=os.path.join(basedir, 'Nifti', 'derivatives', f'{container}_{version}', 
                          'analysis-'+analysis, 'sub-'+sub, 'ses-'+ses, 'input')
    dir_output=os.path.join(basedir, 'Nifti', 'derivatives', f'{container}_{version}',
                            'analysis-'+analysis, 'sub-'+sub, 'ses-'+ses, 'output')
    if not os.path.exists(dir_input):
        os.makedirs(dir_input)
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
    # destination directory under dir_input
    if not os.path.exists(os.path.join(dir_input, "ANAT")):
        os.makedirs(os.path.join(dir_input, "ANAT"))
    if not os.path.exists(os.path.join(dir_input, "FSMASK")):
        os.makedirs(os.path.join(dir_input, "FSMASK"))
    if not os.path.exists(os.path.join(dir_input, "DIFF")):
        os.makedirs(os.path.join(dir_input, "DIFF"))
    if not os.path.exists(os.path.join(dir_input, "BVAL")):
        os.makedirs(os.path.join(dir_input, "BVAL"))
    if not os.path.exists(os.path.join(dir_input, "BVEC")):
        os.makedirs(os.path.join(dir_input, "BVEC"))
    if rpe:
        if not os.path.exists(os.path.join(dir_input, "RDIF")):
            os.makedirs(os.path.join(dir_input, "RDIF"))
        if not os.path.exists(os.path.join(dir_input, "RBVL")):
            os.makedirs(os.path.join(dir_input, "RBVL"))
        if not os.path.exists(os.path.join(dir_input, "RBVC")):
            os.makedirs(os.path.join(dir_input, "RBVC"))
    
    # Create the destination paths
    dstT1file=os.path.join(dir_input, 'ANAT', "T1.nii.gz")
    dstMaskFile=os.path.join(dir_input, 'FSMASK', "brainmask.nii.gz")
    
    dstFileDwi_nii=os.path.join(dir_input, "DIFF", "dwiF.nii.gz")
    dstFileDwi_bval=os.path.join(dir_input, "BVAL", "dwiF.bval")
    dstFileDwi_bvec=os.path.join(dir_input, "BVEC", "dwiF.bvec")
    
    if rpe:
        dstFileDwi_nii_R=os.path.join(dir_input, "RDIF", "dwiR.nii.gz")
        dstFileDwi_bval_R=os.path.join(dir_input, "RBVL", "dwiR.bval")
        dstFileDwi_bvec_R=os.path.join(dir_input, "RBVC", "dwiR.bvec")

    # Create the symbolic links
    force_symlink(srcFileT1, dstT1file, force)
    force_symlink(srcFileMask, dstMaskFile, force)
    force_symlink(srcFileDwi_nii, dstFileDwi_nii, force)
    force_symlink(srcFileDwi_bval, dstFileDwi_bval, force)
    force_symlink(srcFileDwi_bvec, dstFileDwi_bvec, force)
    if rpe:
        force_symlink(srcFileDwi_nii_R, dstFileDwi_nii_R, force)
        force_symlink(srcFileDwi_bval_R, dstFileDwi_bval_R, force)
        force_symlink(srcFileDwi_bvec_R, dstFileDwi_bvec_R, force)
    return 

#%%
def rtppipeline(config, sub, ses):
    """
    Parameters
    ----------
    config : dict
        the config dictionary from _read_config
    sub : str
        the subject name looping from df_subSes
    ses : str
        the session name looping from df_subSes.

    Returns
    -------
    none, create symbolic links 

    """
    # define local variables from config dict
    # general level variables:
    basedir           = config["config"]["basedir"]
    container         = config["config"]["container"]
    force             = config['config']['force']
    analysis          = config["config"]["analysis"]
    # rtppipeline specefic variables
    version           = config ["container_options"][container]["version"]
    precontainerfs    = config["container_options"][container]["precontainerfs"]
    preanalysisfs     = config["container_options"][container]["preanalysisfs"]
    precontainerpp    = config["container_options"][container]["precontainerpp"]
    preanalysispp     = config["container_options"][container]["preanalysispp"]
    
    # the source directory
    # the source file
    
    # the destination directory
    # the destination file
    
    # create symlink
    
    return 
