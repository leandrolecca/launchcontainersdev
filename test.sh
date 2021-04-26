#!/bin/bash

#PBS -q bcbl
#PBS -l nodes=1:ppn=1
#PBS -l mem=1gb
#PBS -N cleanlscrath
#PBS

export LSCRATCH_DIR=/lscratch/lmx/
rm -rf /lscratch/$USER/*

echo "cleaned" > /scratch/lmx/logs/clean.o
 
