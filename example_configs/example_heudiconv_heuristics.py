import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    # anatomical 
    t1_i1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_T1_inv1')
    t1_i2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_T1_inv2')
    t1_un = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_T1_uni')
    
    # nordic dwi


    dwi_normag_rev= create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-magphase_dir-PA_part-mag')
    dwi_norpha_rev= create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-magphase_dir-PA_part-phase')
    dwi_normag= create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-magphase_dir-AP_part-mag')
    dwi_norpha= create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-magphase_dir-AP_part-phase')
   
    # functional
    # top up 
    topup_AP_noipat= create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-APnoipat_dir-{item:01d}_epi')
    
    # BCBL TR =2
    ES_CB_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-ESCB_run-{item:02d}_sbref')
    ES_CB_P     = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-ESCB_run-{item:02d}_phase')
    ES_CB_M     = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-ESCB_run-{item:02d}_magnitude')

    ES_RW30_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-ESRW30_run-{item:02d}_sbref')
    ES_RW30_P     = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-ESRW30_run-{item:02d}_phase')
    ES_RW30_M     = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-ESRW30_run-{item:02d}_magnitude')

    MINI_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MINI_run-{item:02d}_sbref')
    MINI_P     = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MINI_run-{item:02d}_phase')
    MINI_M     = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MINI_run-{item:02d}_magnitude')  
    
    info = {   
    t1_i1: [], t1_i2: [], t1_un: [], 
    topup_AP_noipat: [],
    ES_CB_sbref: [], ES_CB_P: [], ES_CB_M: [],
    ES_RW30_sbref: [], ES_RW30_P: [], ES_RW30_M: [],
    MINI_sbref:[], MINI_P:[], MINI_M:[],

    dwi_normag_rev:[], dwi_normag:[], 
    dwi_norpha_rev:[], dwi_norpha:[],           }
    
    last_run = len(seqinfo)

    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """
        #T1
        if (s.dim1 == 256) and (s.dim2 == 240) and (s.dim3== 176) and ('mp2rage' in s.protocol_name):
            if ('_INV1' in s.series_description):
                info[t1_i1].append(s.series_id)
            elif ('_INV2' in s.series_description):
                info[t1_i2].append(s.series_id)
            elif ('_UNI' in s.series_description):
                info[t1_un].append(s.series_id)

        # dwi 
        if (('diff_PA' in s.protocol_name)  and 
            (('NORDIC' in s.series_description or 'nordic' in s.series_description)) and 
            (s.dim1 == 140) and (s.dim2 == 140) and (s.dim3== 92) and (s.dim4==7)):
            
            if ('10' in s.dcm_dir_name) or ('18' in s.dcm_dir_name): 
                info[dwi_norpha_rev].append(s.series_id)
            if ('9' in s.dcm_dir_name) or ('17' in s.dcm_dir_name): 
                info[dwi_normag_rev].append(s.series_id)                
        
        if (('diff_cmrr_mbep2d_1.5iso_MB4_50b1000_50b2000_lowflip' in s.protocol_name) and 
            (('NORDIC' in s.series_description or 'nordic' in s.series_description)) and 
            (s.dim1 == 140) and (s.dim2 == 140) and (s.dim3== 92) and (s.dim4==105)):
            
            if ('13' in s.dcm_dir_name) or ('21' in s.dcm_dir_name): 
                info[dwi_norpha].append(s.series_id)
            if ('12' in s.dcm_dir_name) or('20' in s.dcm_dir_name): 
                info[dwi_normag].append(s.series_id)    
        
        #TOPUP
        if ('TOPUP' in s.protocol_name.upper()) and ('M' in s.image_type):
            if (('AP' in s.dcm_dir_name) or ('PA' in s.dcm_dir_name)):
                if (s.TR==14.956) :
                    info[topup_AP_noipat].append(s.series_id)
        
        # TR=2 func scan of pRFs
        if s.TR == 2:
            # functional SBref
            if (s.dim4 == 2):
                if 'CB_' in s.protocol_name :
                    info[ES_CB_sbref].append(s.series_id)               
                if 'RW30_' in s.protocol_name :
                    info[ES_RW30_sbref].append(s.series_id) 

            
            # functional for CB and RW30
            if (s.dim1 == 92) and (s.dim3 == 80) and (s.series_files ==160):
                if ('P' in s.image_type) :
                    if 'CB_' in s.protocol_name :
                        info[ES_CB_P].append(s.series_id)
                    if 'RW30_' in s.protocol_name :
                        info[ES_RW30_P].append(s.series_id)
                elif ('M' in s.image_type) :
                    if 'CB_' in s.protocol_name :
                        info[ES_CB_M].append(s.series_id)
                    if 'RW30_' in s.protocol_name :
                        info[ES_RW30_M].append(s.series_id)   
    return info
