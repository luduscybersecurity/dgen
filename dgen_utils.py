from __future__ import print_function
import sys
import errno
import shutil
import os
import traceback

import yaml

DEBUG=False

def eprint(*args, **kwargs):
    '''
    Print to std error.
    '''
    print(*args, file=sys.stderr, **kwargs)

def log_warn(*string, **kwargs):
    '''
    Log warning string to std error.
    '''
    eprint('WARNING:', sys._getframe(1).f_code.co_name + ':', *string, **kwargs)

def log_err(*string, **kwargs):
    '''
    Log warning string to std error.
    '''
    eprint('ERROR:', sys._getframe(1).f_code.co_name + ':', *string, **kwargs)
    if DEBUG is True:
        traceback.print_stack()
    sys.exit('exiting dgen')

def log_dbg(*string, **kwargs):
    '''
    Log warning string to std error.
    '''
    if DEBUG is True:
        eprint('DEBUG:', sys._getframe(1).f_code.co_name + ':', *string, **kwargs)

def delete_folder(path):
    '''
    Delete the specified folder/file
    '''
    path = safe_path(path)
    if os.path.exists(path):
        if os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def copy_files(src, dst):
    '''
    Copy all the files from the path src to dst.
    '''
    src = safe_path(src)
    dst = safe_path(dst)
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            for item in os.listdir(src):
                src_rec = os.path.join(src, item)
                dst_rec = os.path.join(dst, item)
                copy_files(src_rec, dst_rec)
        elif exc.errno == errno.ENOTDIR:
            shutil.copy2(src, dst)
    if not os.path.exists(dst):
        os.makedirs(dst)

def copy_folders(src, dst):
    '''
    Copy all the folders (only) in path src to dst.
    '''
    src = safe_path(src)
    dst = safe_path(dst)
    for folder in os.listdir(src):
        copy_src = os.path.join(src, folder)
        copy_dst = os.path.join(dst, folder)
        if os.path.isdir(copy_src):
            copy_files(copy_src, copy_dst)

def safe_path(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    return path

def load_config(path):
    '''
    Load the yaml config at path
    '''
    path = safe_path(path)
    config = {}
    with open(path, 'r') as fpr:
        config = yaml.safe_load(fpr)
    return config