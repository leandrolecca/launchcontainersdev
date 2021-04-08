#!/bin/bash
#PBS -q bcbl
#PBS -l nodes=1:ppn=1
#PBS -l cput=1:00:00
#PBS -l mem=1gb
#PBS -N lscratshtest

export LSCRATCH_DIR=/lscratch/$USER/jobs/$PBS_JOBID

mkdir -p $LSCRATCH_DIR

echo $PBS_JOBID > $LSCRATCH_DIR/lstracttest.txt

export RESULTS_DIR=/scratch/$USER/jobs/RESULSTS_test

mkdir -p $RESULTS_DIR

cp -r $LSCRATCH_DIR/lstracttest.txt $RESULTS_DIR

rm -rf $LSCRATCH_DIR

