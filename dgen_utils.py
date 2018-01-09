from __future__ import print_function
import sys
import errno
import shutil
import os
import re
import mimetypes
import yaml

def delete_folder(path):
    '''
    Delete the specified folder/file
    '''
    if os.path.exists(path):
        if os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def eprint(*args, **kwargs):
    '''
    Print to std error.
    '''
    print(*args, file=sys.stderr, **kwargs)

def log_warn(*string, **kwargs):
    '''
    Log warning string to std error.
    '''
    eprint('WARNING: ', *string, **kwargs)

def log_err(*string, **kwargs):
    '''
    Log warning string to std error.
    '''
    eprint('ERROR: ', *string, **kwargs)
    # TODO: change to 2
    sys.exit(0)

def is_dgen_repo(path=None):
    if path is None:
        path = os.getcwd()
    for directory in dgen_TLDS:
        if not os.path.exists(os.path.join(path, directory)):
            return False
    ## BUG: Unsure if this is strictly nessesary. 
    #try:
    #    if Repo(path) is None:
    #        return False
    #except:
    #    return False
    return True

dgen_TLDS = ['templates', '.git']

def get_repo_root(path=None):
    if path is None:
        path = os.getcwd()
    if not is_dgen_repo(path):
        if path != '/':
            return get_repo_root(os.path.abspath(os.path.join(path, '..')))
        else:
            log_err('get_repo_root: repo not  found in parent folder')
            return None
    return path

def copy_files(src, dst):
    '''
    Copy all the files from the path src to dst.
    '''
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

def replace_symbols_in_str(string, doc):
    string = replace_html_dir_symbol_in_str(string)
    string = replace_template_dir_symbol_in_str(string, doc)
    return string

def replace_html_dir_symbol_in_str(string):
    '''
    Replace all instances of %{html_dir} with the html directory
    '''
    pattern = re.compile(r'\%\{html_dir\}')
    string = pattern.sub(get_html_dir(), string)
    return string

def replace_template_dir_symbol_in_str(string, doc):
    '''
    Replace all instances of %{template_dir} with the html directory
    '''
    pattern = re.compile(r'\%\{template_dir\}')
    string = pattern.sub(doc.template_dir, string)
    return string

def replace_html_dir_symbol_in_file(path):
    '''
    Parse the file name in folder root to replace
    %{html_dir} with the supplied value
    '''
    mime_type, _ = mimetypes.guess_type(path)
    pattern = re.compile(r'text|xml|html|css|javascript|plain')
    if (mime_type is not None and
            pattern.search(mime_type) is not None):
        with open(path, 'r') as fpr:
            contents = fpr.read()
            fpr.close()
            contents = replace_html_dir_symbol_in_str(contents)
            with open(path, 'w') as fpw:
                fpw.write(contents)
                fpw.close()

def load_config(path):
    '''
    Load the yaml config at path
    '''
    config = {}
    with open(path, 'r') as fpr:
        config = yaml.safe_load(fpr)
    return config