#!/bin/bash

# get the arguments from the command line
while getopts "t:s:e:a:b:o:m:q:c:p:i:n:u:" opt; do
    case $opt in
        t) tool="$OPTARG";;
        s) sub="$OPTARG";;
        e) ses="$OPTARG";;
        a) analysis="$OPTARG";;
        b) basedir="$OPTARG";;
        o) codedir="$OPTARG";;
        m) mem="$OPTARG";;
        q) que="$OPTARG";;
        c) core="$OPTARG";;
        p) tmpdir="$OPTARG";;
        i) sin_ver="$OPTARG";;
        n) container="$OPTARG";;
        u) qsub="$OPTARG";;
    esac
done

printf "Calling the tool $tool, with sub $sub, ses $ses, running analysis $analysis "

export subjbids="$sub"
export path2subderivatives="${basedir}/Nifti/derivatives/${tool}/analysis-${analysis}/sub-${subjbids}/ses-${ses}"
export path2config="${basedir}/Nifti/derivatives/${tool}/analysis-${analysis}/config.json"
	
printf "\n\n It will use basedir:$basedir and tool:$tool \n\n"

	if [ "$qsub" = "False" ]; then
		printf "\n\nNO-QSUB MODE DETECTED\n\n"
		module load $sin_ver
		printf "Starting singularity, using:\n"
		printf "Tool: ~/containers/${tool}.sif\n"
		printf "Path: ${path2subderivatives}\n"
		printf "Config: ${path2config}\n"
		set -x
		singularity run -e --no-home \
		        --bind /scratch:/scratch \
		        --bind ${path2subderivatives}/input:/flywheel/v0/input:ro \
                --bind ${path2subderivatives}/output:/flywheel/v0/output \
		        --bind ${path2config}:/flywheel/v0/config.json \
		        ${container}

	fi
	if [ "${qsub}" = "True" ]; then
		printf "#########################################\n"
 		printf "############## $sub_$ses ################\n"
   		printf "#########################################\n"
   		qsub \
            -q $que -l mem=$mem,nodes=1:ppn=$core \
            -N t-${tool}_a-${analysis}_s-${sub}_s-${ses} \
            -o "$HOME"/logs/t-${tool}_a-${analysis}_s-${sub}_s-${ses}.o \
            -e "$HOME"/logs/t-${tool}_a-${analysis}_s-${sub}_s-${ses}.e \
            -v tool=${tool},path2subderivatives=${path2subderivatives},path2config=${path2config},sin_ver=${sin_ver},container=${container},tmpdir=${tmpdir} ${codedir}/runSingularity.sh 
	fi

