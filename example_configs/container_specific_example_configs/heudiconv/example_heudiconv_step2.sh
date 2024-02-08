basedir=/fileserver/project/proj_gari/DATA
sing_path=/fileserver/project/proj_gari/containers
#sub=$(cat $basedir/subSesList.txt | awk 'NR >1 {print $(1)}' | tr ',\n' ' ')
sub=("VB2024012601TD") 
ses=001

cmd="singularity run \
                    --bind ${basedir}:/base \
                    ${sing_path}/heudiconv_1.0.1.sif \
                                                        -d /base/dicom/sub-{subject}/*/*/* \
                                                        -s ${sub} \
                                                        --ses ${ses} \
                                                        -o /base/BIDS/ \
                                                        --overwrite \
                                                        -f /base/BIDS/.heudiconv/heudiconv_heuristics.py \
                                                        -c dcm2niix \
                                                        -b \
                                                        --grouping all \
    "

echo $cmd
eval $cmd
