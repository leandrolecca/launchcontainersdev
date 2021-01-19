basedir="/bcbl/home/public/KSHIPRA/dwibygari"
subj="TEEN_CONT_06_TP1"


# First run it empty
singularity run --bind /bcbl:/bcbl \
	        --bind ${basedir}:/base \
		~/glerma/software/heudiconv \
		-d /base/Dicoms/{subject}/*/*.dcm \
                -o /base/Nifti/ \
                -f convertall \
                -s ${subj} \
		--grouping all \
                -c none


