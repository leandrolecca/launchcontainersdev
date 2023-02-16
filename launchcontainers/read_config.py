#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 18:58:54 2023

@author: leiyongning
"""
'''
use this python file to read yaml, and import this to launchcountainer.py
'''
#%% import modules
import argparse
import os
import yaml
from yaml.loader import SafeLoader    
#%% use parse to load 
# parser = argparse.ArgumentParser(
#     description='''createSymLinks.py 'pathTo/config_launchcontainers.yaml' ''')
#
# # Required positional argument
# parser.add_argument('configfile', type=str, help='path to the config file')
# parser.add_argument('wildcard', type=str, help='wildcard to select folders')
# parser.add_argument('fullPathFile', type=str, help='path and file name to write')
# parser.add_argument('separator', type=str, help='separator to use')

# Optional positional argument
# parser.add_argument('opt_pos_arg', type=int, nargs='?',
#                             help='An optional integer positional argument')

# Optional argument
# parser.add_argument('--opt_arg', type=int,
#                             help='An optional integer argument')

# Switch
# parser.add_argument('--switch', action='store_true',
#                             help='A boolean switch')

args = parser.parse_args()
print('Read config file: ')
print(args.configfile)

with open(args.configfile, 'r') as v:
    config = yaml.load(v, Loader=SafeLoader)

#%%
# config setting load
globals().update(config['config'])

print('Basedir: ')
print(basedir)

print('container: ')
print(container)

print('analysis: ')
print(analysis)

#%%
# Container options load: 
# this sections are container independent
globals().update(config['container_options'][container])

print('version: ')
print(container_version)

