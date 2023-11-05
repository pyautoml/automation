#!/usr/bin/python3.11
# -*- coding: utf-8 -*-

__created__ = "30.10.2023"
__last_udate__ = "01.11.2023"
__author__ = "https://github.com/pyautoml"


import os 
import gc 
import sys
import json
import inspect
import subprocess
from functools import wraps
from typing import Type, Any
#from logger import logger


def required_parameter(validation_type: Type) -> None:
    """
    Indicate what type the first variable of the function should be.
    
    Parameters
    -----------
    validation_type: (Type) Specified file type. Example: for string type enter "", for dict type enter {}. 
    """
    def decorator(original_method):
        @wraps(original_method)
        def wrapper(folder_name, *args, **kwargs):
            if folder_name.strip() == "":
                #logger.critical("Folder name cannot be empty.")
                sys.exit(1)
            
            if not isinstance(folder_name, type(validation_type)):
                #logger.critical(f"Invalid type for {folder_name}. Expected {type(validation_type)}, got {type(folder_name)}.")
                sys.exit(1)
            return original_method(folder_name, *args, **kwargs)
        return wrapper
    return decorator
    
@required_parameter("")
def load_json_data(file_path: str) -> json:
    """
    Read and load data from json if file exists.
    Parameters
    -----------
    path (str): Path to a json file with settings. Example: /home/user/project/config/project_settings.json
    """
    if not os.path.exists(file_path):
        new_path = absolute_path(file_path)
        if not os.path.exists(file_path):
            #logger.error(f"Path {path} does not exist.")
            return None
        else:
            return new_path
    try:
        with open(file_path, 'r') as settings:
            data = json.load(settings)
    except Exception as e:
        #logger.exception(f"e")
        return None
    return data
    
def absolute_path(path: str = None) -> [str|None]:
    """
    Convert path to an absolute path. This can be useful if you are working on server.
    Parameters
    -----------
    path (str):  Partial or complete path to a file or a folder. Example: './new/cat.png'
    """
    if not path:
        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__)
            )
        )
    else:
        if not isinstance(path, str):
            #logger.exception(f"Path must be str type, not {type(path)}.")
            return None
        if not path:
            #logger.exception("Path cannot be empty.")
            return None
        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), path
            )
        )
        
def free_up_memory() -> None:
    """ Remove global values. """
    for name in dir():
        del globals()[name]
    gc.collect()
    
def run_makefile(command: str, project_path: str) -> None:
    try:
        subprocess.run(["make", command], check=True, cwd=project_path)
    except subprocess.CalledProcessError as e:
        #logger.error(f"Error while running Makefile command: '{command}': {e}")
        sys.exit(1)
