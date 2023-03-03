#%% import libraries
import os, errno
import glob
import sys

#%%
def force_symlink(file1, file2, force):
    """
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

    """
    # if we don't force to overwrite
    if not force:
        try:
            # try the command, if the file are correct and symlink not exist, it will create one
            os.symlink(file1, file2)
            print("The symlink are correctly created")
        # if raise [erron 2]: file not exist, print the error and pass
        except OSError as n:
            if n.errno == 2:
                print("file and directory are missing, maybe due to wrong defination")
            # if raise [erron 17] the symlink exist, we don't force and print that we keep the original one
            if n.errno == errno.EEXIST:
                print(f"the destination file {file2} exist, remain it")
            else:
                raise n
    # if we force to overwrite
    if force:
        try:
            # try the command, if the file are correct and symlink not exist, it will create one
            os.symlink(file1, file2)
        # if the symlink exist, and in this case we force a overwrite
        except OSError as e:
            if e.errno == errno.EEXIST:
                os.remove(file2)
                os.symlink(file1, file2)
                print("The symlink is correctly created")
            elif e.errno == 2:
                print("file and directory are missing, maybe due to wrong defination")
                raise e
            else:
                print("We don't know what happend")
                raise e
    return


#%%
def anatrois(config, sub, ses, path_to_container_config):

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
    basedir = config["config"]["basedir"]
    container = config["config"]["container"]
    force = config["config"]["force"]
    analysis = config["config"]["analysis"]
    # container specific:
    pre_fs = config["container_options"][container]["pre_fs"]
    prefs_zipname = config["container_options"][container]["prefs_zipname"]
    # I added this line, shall we modify config yaml
    precontainerfs = config["container_options"][container]["precontainerfs"]
    preanalysisfs = config["container_options"][container]["preanalysisfs"]
    annotfile = config["container_options"][container]["annotfile"]
    mniroizip = config["container_options"][container]["mniroizip"]
    version = config["container_options"][container]["version"]

    # if we run freesurfer before:
    if pre_fs:
        srcAnatPath = os.path.join(
            basedir,
            "nifti",
            "derivatives",
            precontainerfs,
            "analysis-" + preanalysisfs,
            "sub-" + sub,
            "ses-" + ses,
            "output",
        )
        zips = sorted(
            glob.glob(os.path.join(srcAnatPath, prefs_zipname + "*")), key=os.path.getmtime
        )
        print(len(zips))
        if len(zips) == 0:
            print(
                f"There are no {prefs_zipname} zip file in {srcAnatPath}, we will listed potential zip file for you"
            )
            zips_new = sorted(glob.glob(os.path.join(srcAnatPath, "*")), key=os.path.getmtime)
            if len(zips_new) == 0:
                print(
                    f"The {srcAnatPath} directory is empty, aborting, please check the output file of previous analysis."
                )
                sys.exit()
            else:
                print()
                answer = input(
                    f"Do you want to use the file: \n{zips_new[-1]} \n we get for you? \n input y for yes, n for no"
                )
                if answer in "y":
                    srcFileT1 = zips_new[-1]
                else:
                    print(zips_new)
                    print("we found all the potential zip file, change them in yaml file")
                    sys.exit()
        elif len(zips) > 1:
            print(f"There are more than one zip file in {srcAnatPath}, selecting the last one")
            srcFileT1 = zips[-1]
        else:
            srcFileT1 = zips[0]

    else:
        srcFileT1 = os.path.join(
            basedir,
            "nifti",
            "sub-" + sub,
            "ses-" + ses,
            "anat",
            "sub-" + sub + "_ses-" + ses + "_T1w.nii.gz",
        )

    # define input output folder for this container
    dir_input = os.path.join(
        basedir,
        "nifti",
        "derivatives",
        f"{container}_{version}",
        "analysis-" + analysis,
        "sub-" + sub,
        "ses-" + ses,
        "input",
    )
    dir_output = os.path.join(
        basedir,
        "nifti",
        "derivatives",
        f"{container}_{version}",
        "analysis-" + analysis,
        "sub-" + sub,
        "ses-" + ses,
        "output",
    )
    dir_analysis = os.path.join(
        basedir, "nifti", "derivatives", f"{container}_{version}", "analysis-" + analysis
    )
    # create corresponding folder
    if not os.path.exists(dir_input):
        os.makedirs(dir_input)
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
    if pre_fs:
        if not os.path.exists(os.path.join(dir_input, "pre_fs")):
            os.makedirs(os.path.join(dir_input, "pre_fs"))
    else:
        if not os.path.exists(os.path.join(dir_input, "anat")):
            os.makedirs(os.path.join(dir_input, "anat"))
    if annotfile:
        if os.path.isfile(annotfile):
            print("Passed " + annotfile + ", copying to " + dir_analysis)
            srcFileAnnot = os.path.join(dir_analysis, "annotfile.zip")
            if os.path.isfile(srcFileAnnot):
                print(srcFileAnnot + " exists, if you want it new, delete it first")
            else:
                shutil.copyfile(annotfile, os.path.join(dir_analysis, "annotfile.zip"))
        else:
            print(annotfile + " does not exist")
        if not os.path.exists(os.path.join(dir_input, "annotfile")):
            os.makedirs(os.path.join(dir_input, "annotfile"))
    if mniroizip:
        if os.path.isfile(mniroizip):
            print("Passed " + mniroizip + ", copying to " + dir_analysis)
            srcFileMiniroizip = os.path.join(dir_analysis, "mniroizip.zip")
            if os.path.isfile(srcFileMiniroizip):
                print(srcFileMiniroizip + " exists, if you want it new, delete it first")
            else:
                shutil.copyfile(mniroizip, os.path.join(dir_analysis, "mniroizip.zip"))
        else:
            print(mniroizip + " does not exist")
        if not os.path.exists(os.path.join(dir_input, "mniroizip")):
            os.makedirs(os.path.join(dir_input, "mniroizip"))

    # Create the destination path
    if pre_fs:
        dstFileT1 = os.path.join(dir_input, "pre_fs", "existingFS.zip")
    else:
        dstFileT1 = os.path.join(dir_input, "anat", "T1.nii.gz")

    dstFileAnnot = os.path.join(dir_input, "annotfile", "annots.zip")
    dstFileMniroizip = os.path.join(dir_input, "mniroizip", "mniroizip.zip")

    # Now that the folder structure is created for this subject, now copy the config file to the analysis folder so that
    # when we call the Singularity container, it is at the base of the analysis folder and it can create a link
    # First check that the file is there
    dstFilecontainer_config = os.path.join(dir_analysis, "config.json")
    if not os.path.isfile(path_to_container_config):
        sys.exit(
            f"{path_to_container_config} des not exist, CANNOT paste it to the analysis folder, aborting. "
        )
    # config is there, now copy to the right folder
    else:
        force_symlink(path_to_container_config, dstFilecontainer_config, force)
        print(
            f"{path_to_container_config} has been succesfully copied to {dstFilecontainer_config}. "
            f"\nREMEMBER TO CHECK/EDIT TO HAVE THE CORRECT PARAMETERS IN THE FILE"
        )

    # Create the symbolic links
    force_symlink(srcFileT1, dstFileT1, force)
    if annotfile:
        force_symlink(srcFileAnnot, dstFileAnnot, force)
    if mniroizip:
        force_symlink(srcFileMniroizip, dstFileMniroizip, force)


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
    basedir = config["config"]["basedir"]
    container = config["config"]["container"]
    force = config["config"]["force"]
    analysis = config["config"]["analysis"]
    # container specific:
    precontainerfs = config["container_options"][container]["precontainerfs"]
    preanalysisfs = config["container_options"][container]["preanalysisfs"]
    rpe = config["container_options"][container]["rpe"]
    version = config["container_options"][container]["version"]

    # define base directory for particular subject and session
    basedir_subses = os.path.join(basedir, "nifti", "sub-" + sub, "ses-" + ses)

    # the source directory that stores the output of previous anatorois analysis
    srcDirFs = os.path.join(
        basedir,
        "nifti",
        "derivatives",
        precontainerfs,
        "analysis-" + preanalysisfs,
        "sub-" + sub,
        "ses-" + ses,
        "output",
    )

    # define the source file, this is where symlink will point to
    # T1 file in anatrois output
    srcFileT1 = os.path.join(srcDirFs, "T1.nii.gz")
    # brainmask file in anatrois output
    srcFileMask = os.path.join(srcDirFs, "brainmask.nii.gz")
    # 3 dwi file that needs to be preprocessed, under nifti/sub/ses/dwi
    # the nii.gz
    srcFileDwi_nii = os.path.join(
        basedir_subses, "dwi", "sub-" + sub + "_ses-" + ses + "_acq-AP_dwi.nii.gz"
    )
    # the bval.gz
    srcFileDwi_bval = os.path.join(
        basedir_subses, "dwi", "sub-" + sub + "_ses-" + ses + "_acq-AP_dwi.bval"
    )
    # the bvec.gz
    srcFileDwi_bvec = os.path.join(
        basedir_subses, "dwi", "sub-" + sub + "_ses-" + ses + "_acq-AP_dwi.bvec"
    )
    # check_create_bvec_bval（force) one of the todo here
    if rpe:
        # the reverse direction nii.gz
        srcFileDwi_nii_R = os.path.join(
            basedir_subses, "dwi", "sub-" + sub + "_ses-" + ses + "_acq-PA_dwi.nii.gz"
        )
        # the reverse direction bval
        srcFileDwi_bval_R = os.path.join(
            basedir_subses, "dwi", "sub-" + sub + "_ses-" + ses + "_acq-PA_dwi.bval"
        )
        # the reverse diretion bvec
        srcFileDwi_bvec_R = os.path.join(
            basedir_subses, "dwi", "sub-" + sub + "_ses-" + ses + "_acq-PA_dwi.bvec"
        )

        # If bval and bvec do not exist because it is only b0-s, create them
        # (it would be better if dcm2niix would output them but...)
        # buildthe img matrix according to the shape of nii.gz
        img = nib.load(srcFileDwi_nii_R)
        volumes = img.shape[3]
        # if one of the bvec and bval are not there, re-write them
        if (not os.path.isfile(srcFileDwi_bval_R)) or (not os.path.isfile(srcFileDwi_bvec_R)):
            # Write bval file
            f = open(srcFileDwi_bval_R, "x")
            f.write(volumes * "0 ")
            f.close()

            # Write bvec file
            f = open(srcFileDwi_bvec_R, "x")
            f.write(volumes * "0 ")
            f.write("\n")
            f.write(volumes * "0 ")
            f.write("\n")
            f.write(volumes * "0 ")
            f.write("\n")
            f.close()

    # creat input and output directory for this container, the dir_output should be empty, the dir_input should contains all the symlinks
    dir_input = os.path.join(
        basedir,
        "nifti",
        "derivatives",
        f"{container}_{version}",
        "analysis-" + analysis,
        "sub-" + sub,
        "ses-" + ses,
        "input",
    )
    dir_output = os.path.join(
        basedir,
        "nifti",
        "derivatives",
        f"{container}_{version}",
        "analysis-" + analysis,
        "sub-" + sub,
        "ses-" + ses,
        "output",
    )
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
    dstT1file = os.path.join(dir_input, "ANAT", "T1.nii.gz")
    dstMaskFile = os.path.join(dir_input, "FSMASK", "brainmask.nii.gz")

    dstFileDwi_nii = os.path.join(dir_input, "DIFF", "dwiF.nii.gz")
    dstFileDwi_bval = os.path.join(dir_input, "BVAL", "dwiF.bval")
    dstFileDwi_bvec = os.path.join(dir_input, "BVEC", "dwiF.bvec")

    if rpe:
        dstFileDwi_nii_R = os.path.join(dir_input, "RDIF", "dwiR.nii.gz")
        dstFileDwi_bval_R = os.path.join(dir_input, "RBVL", "dwiR.bval")
        dstFileDwi_bvec_R = os.path.join(dir_input, "RBVC", "dwiR.bvec")

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
    basedir = config["config"]["basedir"]
    container = config["config"]["container"]
    force = config["config"]["force"]
    analysis = config["config"]["analysis"]
    # rtppipeline specefic variables
    version = config["container_options"][container]["version"]
    precontainerfs = config["container_options"][container]["precontainerfs"]
    preanalysisfs = config["container_options"][container]["preanalysisfs"]
    precontainerpp = config["container_options"][container]["precontainerpp"]
    preanalysispp = config["container_options"][container]["preanalysispp"]

    # the source directory
    srcDirfs = os.path.join(
        basedir,
        "nifti",
        "derivatives",
        precontainerfs,
        "analysis-" + preanalysisfs,
        "sub-" + sub,
        "ses-" + "T01",
        "output",
    )
    srcDirpp = os.path.join(
        basedir,
        "nifti",
        "derivatives",
        precontainerpp,
        "analysis-" + preanalysispp,
        "sub-" + sub,
        "ses-" + ses,
        "output",
    )
    # the source file
    srcFileT1 = os.path.join(srcDirpp, "t1.nii.gz")
    srcFileFs = os.path.join(srcDirfs, "fs.zip")
    srcFileDwi_bvals = os.path.join(srcDirpp, "dwi.bvals")
    srcFileDwi_bvec = os.path.join(srcDirpp, "dwi.bvecs")
    srcFileDwi_nii = os.path.join(srcDirpp, "dwi.nii.gz")

    # creat input and output directory for this container, the dir_output should be empty, the dir_input should contains all the symlinks
    dir_input = os.path.join(
        basedir,
        "nifti",
        "derivatives",
        f"{container}_{version}",
        "analysis-" + analysis,
        "sub-" + sub,
        "ses-" + ses,
        "input",
    )
    dir_output = os.path.join(
        basedir,
        "nifti",
        "derivatives",
        f"{container}_{version}",
        "analysis-" + analysis,
        "sub-" + sub,
        "ses-" + ses,
        "output",
    )
    # under dir_input there are a lot of dir also needs to be there to have symlinks
    if not os.path.exists(dir_input):
        os.makedirs(dir_input)
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
    if not os.path.exists(os.path.join(dir_input, "anatomical")):
        os.makedirs(os.path.join(dir_input, "anatomical"))
    if not os.path.exists(os.path.join(dir_input, "fs")):
        os.makedirs(os.path.join(dir_input, "fs"))
    if not os.path.exists(os.path.join(dir_input, "dwi")):
        os.makedirs(os.path.join(dir_input, "dwi"))
    if not os.path.exists(os.path.join(dir_input, "bval")):
        os.makedirs(os.path.join(dir_input, "bval"))
    if not os.path.exists(os.path.join(dir_input, "bvec")):
        os.makedirs(os.path.join(dir_input, "bvec"))
    if not os.path.exists(os.path.join(dir_input, "tractparams")):
        os.makedirs(os.path.join(dir_input, "tractparams"))

    # Create the destination file
    dstAnatomicalFile = os.path.join(dir_input, "anatomical", "T1.nii.gz")
    dstFsfile = os.path.join(dir_input, "fs", "fs.zip")
    dstDwi_niiFile = os.path.join(dir_input, "dwi", "dwi.nii.gz")
    dstDwi_bvalFile = os.path.join(dir_input, "bval", "dwi.bval")
    dstDwi_bvecFile = os.path.join(dir_input, "bvec", "dwi.bvec")
    dst_tractparams = os.path.join(dir_input, "tractparams", "tractparams.csv")
    src_tractparams = os.path.join(
        basedir, "nifti", "derivatives", container, "analysis-" + analysis, "tractparams.csv"
    )

    # Create the symbolic links
    force_symlink(srcFileT1, dstAnatomicalFile, force)
    force_symlink(srcFileFs, dstFsfile, force)
    force_symlink(srcFileDwi_nii, dstDwi_niiFile, force)
    force_symlink(srcFileDwi_bvec, dstDwi_bvecFile, force)
    force_symlink(srcFileDwi_bvals, dstDwi_bvalFile, force)
    force_symlink(src_tractparams, dst_tractparams, force)

    return
