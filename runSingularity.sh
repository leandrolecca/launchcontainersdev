#!/bin/bash
#PBS -l cput=1000:00:00

# be alart
# variables that are passing to this script from outside layer
# ...
# $sin_ver                  singualrity version to load
# $container                container you want to run
# $tmpdir                   TMP dir for ENV variable pass to singularity
# $tool                     which tool we are running (only for printing aim)
# $path2subderivatives      input and output dir location
# $path2config              config file location
    
module load $sin_ver
# we need following lines for running fixAllSegmentations.m
# (from thalamus segmentation) successfully in DIPC


# SELECT THE TMP DIR 
export SINGULARITYENV_TMPDIR=$tmpdir
# Neuropythy (maybe others) fail when using lscratch as TMPDIR
# export SINGULARITYENV_TMPDIR=/lscratch/$USER/tmp/jobs/$PBS_JOBID





export SINGULARITY_BIND=""
TMPDIR=
echo $SINGULARITYENV_TMPDIR
echo $sub
echo "Starting singularity, using:"
echo "Tool: ${tool}"
echo "Path: ${path2subderivatives}"
echo "Config: ${path2config}"
echo "Container: ${container}"
date;
echo "Running: ${sin_ver}"

echo "PSD_ID: ${PBS_JOBID}"
if [ "$host" == "BCBL" ];then 
    cmd="singularity run -e --no-home \
        --bind /bcbl:/bcbl \
        --bind /tmp:/tmp \
        --bind /scratch:/scratch \
        --bind ${path2subderivatives}/input:/flywheel/v0/input:ro \
        --bind ${path2subderivatives}/output:/flywheel/v0/output \
        --bind ${path2config}:/flywheel/v0/config.json \
        $container"
    echo $cmd
    eval $cmd
    echo "ended singularity"

elif [ "$host" == "DIPC" ];then
    # use LSCRATCH_DIR as temporary dir to do the computation
    # once finished, move the content back to /scratch
    export LSCRATCH_DIR=/lscratch/$USER/jobs/$PBS_JOBID
    mkdir -p $LSCRATCH_DIR
    # CReate a tmpdir in local scratch as well, no need to move it back
    # later on, it is emptied automatically (but delete it nonetheless,
    # the folder will remain although empty
    mkdir -p $SINGULARITYENV_TMPDIR 


    cmd="singularity run -e --no-home \
        --bind /scratch:/scratch \
        --bind ${path2subderivatives}/input:/flywheel/v0/input:ro \
        --bind ${LSCRATCH_DIR}:/flywheel/v0/output \
        --bind ${path2config}:/flywheel/v0/config.json \
        $container"
    echo $cmd
    eval $cmd
    echo "ended singularity"
    export RESULTS_DIR=${path2subderivatives}/output
    echo "### copying from $LSCRATCH_DIR to $RESULTS_DIR/ ###"
    cp -r $LSCRATCH_DIR/* $RESULTS_DIR/
    rm -rf  $LSCRATCH_DIR
    rm -rf  $SINGULARITYENV_TMPDIR
fi
date;

