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
    
export SINGULARITYENV_TMPDIR=$tmpdir
export SINGULARITY_BIND=""
TMPDIR=
module load $sin_ver

echo $sub
echo "Starting singularity, using:"
echo "Tool: ${tool}"
echo "Path: ${path2subderivatives}"
echo "Config: ${path2config}"
date;
singularity run -e --no-home \
    --bind /scratch:/scratch \
	--bind ${path2subderivatives}/input:/flywheel/v0/input:ro \
	--bind ${path2subderivatives}/output:/flywheel/v0/output \
	--bind ${path2config}:/flywheel/v0/config.json \
	$container

echo "ended singularity"

date;

