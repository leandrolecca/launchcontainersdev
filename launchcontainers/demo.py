#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:22:29 2023

@author: leiyongning
"""
import os, errno



def force_symlink(file1, file2, force):
    '''
    Parameters
    ----------
    file1 : str 
        the path to the source file, which is the output of previous container
    file2 : str
        the path to the destination file, which is the input of the current container
    force : bool
        set in the config file

    Raises
    ------
    e
        OS error.

    Returns
    -------
    None.

    '''
    # if we don't force to overwrite
    if not force:
        try:
            #try the command, if the file are correct and symlink not exist, it will create one
            os.symlink(file1, file2)
            print ('The symlink are correctly created')
        #if raise [erron 2]: file not exist, print the error and pass
        except OSError as n: 
            if n.errno == 2:
                print ("file and directory are missing, maybe due to wrong defination")
        # if raise [erron 17] the symlink exist, we don't force and print that we keep the original one     
            if n.errno == errno.EEXIST:
                print(f"the destination file {file2} exist, remain it")
            else:
                raise n
    #if we force to overwrite
    if force :
        try:
         # try the command, if the file are correct and symlink not exist, it will create one   
            os.symlink(file1, file2)
            print ('The symlink are correctly created')
        # if the symlink exist, and in this case we force a overwrite
        except OSError as e:
            if e.errno == errno.EEXIST:
                os.remove(file2)
                os.symlink(file1, file2)
                print ('The symlink are correctly created')
            if e.errno == 2:
                print ("file and directory are missing, maybe due to wrong defination")
            else:
                print ("the error is : " f'{e}')
    return

def mklink(config):
    
    force = config[0]
    zips =config[1]
    
    try:
        srcFile = config[1][-1]
    except:
        print ("there are no zip file")

    dstFile = config[2]
    #'/Users/tiger/TESTDATA/codetest/dir2/a_link.zip'
    
    force_symlink(srcFile, dstFile, force)
    
    return



