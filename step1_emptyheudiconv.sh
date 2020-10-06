# export basedir=/export/home/glerma/public/Gari/MAGNO2
basedir="/export/home/glerma/glerma/00local/PROYECTOS/MAGNO2/"
export subj=01_MAGNO_7851
export subj=T1_7851


# First run it empty
singularity run --bind /bcbl:/bcbl \
	        --bind ${basedir}:/base \
		~/glerma/software/heudiconv \
		-d /base/Dicoms/{subject}/*/*/*.dcm \
                -o /base/Nifti/ \
                -f convertall \
                -s ${subj} \
                -c none


