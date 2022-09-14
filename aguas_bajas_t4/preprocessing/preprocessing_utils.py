#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitary files to preprocess large sampling data assiciated with passive acoustic 
monitoring


"""

import os
from os import listdir

def search_files(directory=".", extension=""):
    extension = extension.lower()
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            if extension and name.lower().endswith(extension):
                return os.path.join(dirpath, name)
            elif not extension:
                return os.path.join(dirpath, name)


def listdir_pattern(path_dir, ends_with=None):
    """
    Wraper function from os.listdir to include a filter to search for patterns
    
    Parameters
    ----------
        path_dir: str
            path to directory
        ends_with: str
            pattern to search for at the end of the filename
    Returns
    -------
    """
    flist = listdir(path_dir)

    new_list = []
    for names in flist:
        if names.endswith(ends_with):
            new_list.append(names)
    return new_list
