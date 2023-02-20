#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:20:19 2023

@author: leiyongning
"""
#%%
import createsymlinks as csl
import pandas as pd
#%%
"""
Some documentation here

"""
#%%


def prepare_input_file(config_dict, df_subSes):
    for row in df_subSes.itertuples(index= True, name = "Pandas"):
        sub = row.sub
        ses = row.ses
        RUN = row.RUN
        dwi = row.dwi
        func = row.func
        container = config_dict['config']['container']
        cont_version = config_dict['container_options'][container]['container_version']
        print(f"{sub}_{ses}_RUN-{RUN}_{container}_{cont_version}")
        
        if not RUN: 
            continue
        
        if "rtppreproc" in container:
            csl.rtppreproc(config_dict, sub, ses)
        elif "rtp-pipeline" in container:
            print('rtppipeline')
        elif "rtp-pipeline" in container:
            print('rtppipeline')
        elif "rtp-pipeline" in container:
            print('rtppipeline')
        elif "rtp-pipeline" in container:
            print('rtppipeline')
        else:
            print(f"{container} is not created, check for typos or if it is a new container create it in prepareinput.py")
   
    return 
"""
looping thing should be outside of this file

"""