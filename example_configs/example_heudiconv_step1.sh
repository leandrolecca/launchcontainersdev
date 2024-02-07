basedir=/fileserver/project/proj_gari/DATA
sing_path=/fileserver/project/proj_gari/containers
#sub=$(cat $basedir/subSesList.txt | awk 'NR >1 {print $(1)}' | tr ',\n' ' ')
# define an array of subjects
sub=("VB2024012601TD") 
#cmd="ls ${basedir}/dicom/${subj}"
#echo $cmd
#eval $cmd

for sub in "${sub[@]}";do 
	echo "Working with  sub: $sub "
	cmd="singularity run \
                        --bind ${basedir}:/base \
                        ${sing_path}/heudiconv_1.0.1.sif \
                                                        -d /base/dicom/sub-{subject}/*/*/* \
                                                        --subjects ${sub} \
                                                        -o /base/BIDS/ \
                                                        -f convertall \
                                                        -c none \
                                                        -g all \
                                                        --overwrite \
        "

    
	echo $cmd
	eval $cmd	
done
