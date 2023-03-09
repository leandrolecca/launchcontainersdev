import nibabel as nib
import argparse
from logging import DEBUG
import os
import shutil as sh
import glob
import subprocess as sp
import shutil
# from xxlimited import Str
# import numpy as np
import pandas as pd
import json
import sys

# from launchcontainers import __version__
import yaml
from yaml.loader import SafeLoader
import pip
import numpy as np

# Dask imports
from dask import compute
from dask import delayed as delayed_dask
from dask import config
from dask.distributed import Client
from dask_jobqueue import PBSCluster, SGECluster, SLURMCluster
from dask.distributed import progress
# My packages
import dask_schedule_queue as dsq
import createsymlinks as csl

"""s
TODO: 
    4./ Add the check in launchcontainers.py, that only in some cases we wiill 
        need to use createSymLinks, and for the anatrois, rtppreproc and 
        rtp-pipeline, we will need to do it
    5./ Edit createSymLinks again and make one function per every container
        createSymLinks_anatrois.py
        createSymLinks_rtppreproc.py
        createSymLinks_rtp-pipeline.py
"""
# %% parser
def _get_parser():
    """
    Input:
    Parse command line inputs

    Returns:
    a dict stores information about the cmd input

    """
    parser = argparse.ArgumentParser(
        description=""" This is lanchcontianer.py, you need to input path to the following files after the keywords \n       
                        '-lcc path to config_lc.yaml \n 
                        -ssl path to subSesList.txt  \n
                        -cc path to container_config.json \n
                        And you also need to decide if you are sure you want to launch the container by typying
                        --run_lc  \n
                        if you type --run_lc, this code will actually launch containers, \n
                        otherwise just prints all the config information for you checking and  prepare all the input files"""
    )
    parser.add_argument(
        "-lcc",
        "--lc_config",
        type=str,
        default="/Users/tiger/TESTDATA/PROJ01/nifti/config_launchcontainer_copy.yaml",
        # default="/export/home/tlei/tlei/TESTDATA/PROJ01/nifti/config_lc.yaml",
        help="path to the config file",
    )
    parser.add_argument(
        "-ssl",
        "--sub_ses_list",
        type=str,
        default="/Users/tiger/TESTDATA/PROJ01/nifti/subSesList.txt",
        #default="/export/home/tlei/tlei/TESTDATA/PROJ01/nifti/subSesList.txt",
        help="path to the subSesList",
    )
    parser.add_argument(
        "-cc",
        "--container_config",
        type=str,
        default="/Users/tiger/Documents/GitHub/launchcontainers/example_configs/container_especific_example_configs/anatrois/4.2.7_7.1.1/example_config.json",
        #default="/export/home/tlei/tlei/github/launchcontainers/example_configs/container_especific_example_configs/anatrois/4.2.7_7.1.1/example_config.json",
        help="path to the container specific config file",
    )
    parser.add_argument('--run_lc', action='store_true',
                        help= "if you type --run_lc, the entire program will be launched, jobs will be send to \
                        cluster and launch the corresponding container you suggest in config_lc.yaml. \
                        We suggest that the first time you run launchcontainer.py, leave this arguement empty. \
                        then the launchcontainer.py will preapre \
                        all the input files for you and print the command you want to send to container, after you \
                        check all the configurations are correct and ready, you type --run_lc to make it run"
                        )
    parser.add_argument('--not_run_lc', dest='run_lc', action='store_false')
    parser.set_defaults(run_lc=False)



    parse_result = vars(parser.parse_args())
    print("1111111111111111111111111111111111111111111111111111111111111111111111\n")
    
    print ("This is the result from _get_parser()\n")
    print(parse_result,"\n")
    
    print("1111111111111111111111111111111111111111111111111111111111111111111111\n")
    return parse_result


# %% function to read config file, yaml
def _read_config(path_to_config_file):
    """
    Input:
    the path to the config file

    Returns
    a dictionary that contains all the config info

    """
    print("2222222222222222222222222222222222222222222222222222222222222222222222222 \n")
    print(f"Read the config file {path_to_config_file} \n ")

    with open(path_to_config_file, "r") as v:
        config = yaml.load(v, Loader=SafeLoader)

    container = config["config"]["container"]

    print(f"Successfully read config_lc.yaml")
    print(f'\nBasedir is: {config["config"]["basedir"]}')
    print(f'\nContainer is: {container}_{config["container_options"][container]["version"]}')
    print(f'\nAnalysis is: analysis-{config["config"]["analysis"]}\n')
    print(f"22222222222222222222222222222222222222222222222222222222222222222222222\n")

    return config


# %% function to read subSesList. txt
def _read_subSesList(path_to_subSesList_file):
    """
    Input:
    path to the subject and session list txt file

    Returns
    a dataframe

    """
    subSesList = pd.read_csv(path_to_subSesList_file, sep=",", header=0)
    num_rows = len(subSesList)

    # Print the result
    print(f"#333333333333333333333333333333333333333333333333333333333333333333333\n")
    print(f'The subseslist is successfully read. \n')
    print(f'The DataFrame has {num_rows} rows. \n')
    print(f"33333333333333333333333333333333333333333333333333333333333333333333333\n")
    

    return subSesList


# %% prepare_input_files
def prepare_input_files(lc_config, df_subSes, container_config):
    """

    Parameters
    ----------
    lc_config : TYPE
        DESCRIPTION.
    df_subSes : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    print ("44444444444444444444444444444started to parepare the input file for all sub and ses 444444444444444444444\n")
    
    for row in df_subSes.itertuples(index=True, name="Pandas"):
        sub = row.sub
        ses = row.ses
        RUN = row.RUN
        dwi = row.dwi
        func = row.func
        container = lc_config["config"]["container"]
        version = lc_config["container_options"][container]["version"]
        print("The current run is:\n")
        print(f"{sub}_{ses}_RUN-{RUN}_{container}_{version}\n")

        if not RUN:
            continue

        if "rtppreproc" in container:
            csl.rtppreproc(lc_config, sub, ses, container_config)
        elif "rtp-pipeline" in container:
            csl.rtppipeline(lc_config, sub, ses, container_config)
        elif "anatrois" in container:
            csl.anatrois(lc_config, sub, ses, container_config)
        # future container
        else:
            print(f"******************* ERROR ********************\n")
            print(
                f"{container} is not created, check for typos or contact for singularity images\n"
            )
    print ("44444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444\n")
    return

# %% launchcontainers

def launchcontainers(sub_ses_list, lc_config, run_it):
    """
    This function launches containers generically in different Docker/Singularity HPCs
    This function is going to assume that all files are where they need to be.

    Parameters
    ----------
    sub_ses_list: Pandas data frame
        Data frame with subject information and if run or not run
    lc_config : dict
        Dictionary with all the values in the configuracion yaml file
    """
    print("5555555555555555555555555555---------the real launchconatiner-----------55555555555555555555555555555555\n")
    tmp_path = lc_config["config"]["tmpdir"]
    log_path = lc_config["config"]["logdir"]
    
    # If tmpdir and logdir do not exist, create them
    if not os.path.isdir(tmp_path):
        os.mkdir(tmp_path)
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
   
    host = lc_config["config"]["host"]
    jobqueue_config= lc_config["host_options"][host]
    
    # Count how many jobs we need to launch from  sub_ses_list
    # n_jobs = np.sum(sub_ses_list.RUN == True)
    n_jobs = 1

    basedir = lc_config["config"]["basedir"]
    container = lc_config["config"]["container"] 
    version = lc_config["container_options"][container]["version"]
    analysis = lc_config["config"]["analysis"] 
    containerdir = lc_config["config"]["containerdir"] 
    container_path = os.path.join(containerdir, f"{container}_{version}.sif")
    
    # Iterate between temporal and spatial regularizations
    if run_it: client, cluster = dsq.dask_scheduler(jobqueue_config, n_jobs)
    
    futures = []
    for row in sub_ses_list.itertuples(index=True, name='Pandas'):
        sub  = row.sub
        ses  = row.ses
        RUN  = row.RUN
        dwi  = row.dwi
        func = row.func
        if RUN and dwi:
            # command for launch singularity
            path_to_sub_derivatives=os.path.join(basedir,"nifti","derivatives",
                                                 f"{container}_{version}",
                                                 f"analysis-{analysis}",
                                                 f"sub-{sub}",
                                                 f"ses-{ses}")
            path_to_config=os.path.join(basedir,"nifti","derivatives",
                                                 f"{container}_{version}",
                                                 f"analysis-{analysis}",
                                                 "config.json")
            cmd=f"module load singularity/3.5.2 " 
                f"&& singularity run -e --no-home "\
                f"--bind /bcbl:/bcbl "\
                f"--bind /tmp:/tmp "\
                f"--bind /scratch:/scratch "\
                f"--bind {path_to_sub_derivatives}/input:/flywheel/v0/input:ro "\
                f"--bind {path_to_sub_derivatives}/output:/flywheel/v0/output:ro "\
                f"--bind {path_to_config}:/flywheel/v0/config.json "\
                f"{container_path} "
            if run_it: 
                print(f"-------run_lc is True, we will launch this command: \n" \
                      f"-------{cmd}")
                future = client.submit(sp.run, cmd, shell=True)
            else:
                print(f"--------run_lc is false, if True, we would launch this command: \n" \
                      f"--------{cmd}")

           
    print("5555555555555555555555555555---------the real launchconatiner-----------55555555555555555555555555555555555555\n")

    




def backup_config_info():
    """
    One of the TODO:
        make a function, when this file was run, create a copy of the original yaml file
        then rename it , add the date and time in the end
        stored the new yaml file under the output folder
        At the end, thiknk if we want it per subject, right now it is in the analysis folder
    """
    return None

# %% main()


def main():
    """launch_container entry point"""
    inputs = _get_parser()
    lc_config = _read_config(inputs["lc_config"])
    sub_ses_list = _read_subSesList(inputs["sub_ses_list"])
    container_config = inputs["container_config"]
    run_lc = inputs["run_lc"]
    basedir = lc_config['config']["basedir"]
    container = lc_config["config"]["container"]
    version = lc_config["container_options"][container]
    prepare_input_files(lc_config, sub_ses_list, container_config)

    # launchcontainers('kk', command_str=command_str)
    if run_lc:
        launchcontainers(sub_ses_list, lc_config, True)
    else:
        launchcontainers(sub_ses_list, lc_config, False)

  #  cmd_copy= f"scp {basedir}/nifti/config_lc.yaml {basedir}/nifti/derivatives/{container}_{version}/analysis_{analysis}"
  #  sp.run(cmd_copy, Shell=True)
   

# #%%
if __name__ == "__main__":
    main()
