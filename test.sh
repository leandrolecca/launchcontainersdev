#!/bin/bash                                                                                                           
#PBS -q bcbl
#PBS -l nodes=1:ppn=1
#PBS -l cput=100:00:00

#PBS -l mem=1gb

#PBS -N lscratchtest

        
export SINGULARITYENV_TMPDIR="test"
export SINGULARITY_BIND=""
TMPDIR=
echo $SINGULARITYENV_TMPDIR
echo "Starting singularity, using:"
date;
echo "PSD_ID: ${PBS_JOBID}"
