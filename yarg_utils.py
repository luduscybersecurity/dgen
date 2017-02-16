from __future__ import print_function
import sys
import errno
import shutil
import os
import re

def delete_folder(path):
    '''
    Delete the specified folder/file
    '''
    if os.path.exists(path):
        if os.path.isfile(path):
            log_warn('HTML file found and not a path')
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def eprint(*args, **kwargs):
    '''
    Print to std error.
    '''
    print(*args, file=sys.stderr, **kwargs)

def log_warn(string):
    '''
    Log warning string to std error.
    '''
    eprint('WARNING: ' + string)

def copy_files(src, dst):
    '''
    Copy all the files from the path src to dst.
    '''
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)

def copy_folders(src, dst):
    '''
    Copy all the folders (only) in path src to dst.
    '''
    for folder in os.listdir(src):
        copy_src = os.path.join(src, folder)
        copy_dst = os.path.join(dst, folder)
        if os.path.isdir(copy_src):
            copy_files(copy_src, copy_dst)

def get_html_dir():
    return os.path.join(os.getcwd(), 'html')

def replace_html_dir_symbol_in_str(string):
    '''
    Replace all instances of %{html_dir} with the 
    '''
    pattern = re.compile(r'\%\{html_dir\}')
    string = pattern.sub(get_html_dir(), string)
    return string

def replace_html_dir_symbol_in_file(path):
    '''
    Parse the file name in folder root to replace
    %{html_dir} with the supplied value
    '''
    with open(path, 'r') as fpr:
        contents = fpr.read()
        fpr.close()
        contents = replace_html_dir_symbol_in_str(contents)
        with open(path, 'w') as fpw:
            fpw.write(contents)
            fpw.close()
