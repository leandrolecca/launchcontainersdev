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
check_input(configFile, subSesList)


def check_rtppreproc(config, sub, ses):
    """
    take the config file info to search the file name
    
    sub and ses from main() 
    
    Returns
    -------
    Nono

    """
    return 



def check_input_file_is_there (dict_config, df_subSes):
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
        if RUN and dwi:
    
    
        if container in anatrois():
            _check_anatrois()

    return



def main():
    
        
    
    
    return 

if __name__ == "__main__":
    j vcmain()