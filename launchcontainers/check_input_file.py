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
def input_file_overwritte(dict_config):
    force = dict_config["config"]["force"]
    
    if force == True:
        #overwritte

#%%
def check_rtppreproc(config, sub, ses):
    """
    take the config file info to search the file name
    
    sub and ses from main() 
    
    Returns
    -------
    None

    """
    
    
    return #something, should be true of false
#%%
def check_input_file_is_there(dict_config, df_subSes):
    """
    the two inputs: config is a dict, 
    
    subSesList is a dataframe,
    """
    container = dict_config["config"]["container"]
    
    for row in df_subSesList.itertuples(index=True, name='Pandas'):
        sub  = row.sub
        ses  = row.ses
        RUN  = row.RUN
        dwi  = row.dwi
        func = row.func
        if RUN and ("rtppreproc" in container):
            check_rtppreproc(dict_config, sub, ses)
        #if RUN and ("anatrois" in container):
            # check_anatrois(dict_config, sub, ses)

    return is_there, container 




def prepare_input_file(dict_config, df_subSes):
    
    if check_input_file_is_there()[0] == True :
        print ("\n the input file is there, if you want to overwrite, change force to ture in config.yaml")
        input_file_overwritte()
    else:
        for row in df_subSesList.itertuples(index=True, name='Pandas'):
            sub  = row.sub
            ses  = row.ses
            RUN  = row.RUN
            dwi  = row.dwi
            func = row.func
            if RUN and ("rtppreproc" in container):
                csl.rtppreproc(config, sub, ses)
        
    return 
