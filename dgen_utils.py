from __future__ import print_function
import sys
import errno
import shutil
import os
import traceback
import subprocess
import io
import glob

import yaml

DEBUG = False
REFRESH_TEMPLATE = False


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
    sys.exit(1)


def log_dbg(*string, **kwargs):
    '''
    Log warning string to std error.
    '''
    if DEBUG is True:
        eprint('DEBUG:', sys._getframe(
            1).f_code.co_name + ':', *string, **kwargs)


def delete_folder(path):
    '''
    Delete the specified folder/files. Globs are supported
    '''
    expanded_paths = expand_path_with_glob(path)
    for expanded_path in expanded_paths:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)


def copy_files(src, dst):
    '''
    Copy all the files from the path src to dst.
    '''
    src = expand_path(src)
    dst = expand_path(dst)
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
    src = expand_path(src)
    dst = expand_path(dst)
    for folder in os.listdir(src):
        copy_src = os.path.join(src, folder)
        copy_dst = os.path.join(dst, folder)
        if os.path.isdir(copy_src):
            copy_files(copy_src, copy_dst)


def __split_args(args):
    result = []
    for arg in args:
        result = result + str(arg).split(' ')
    return result


def run_cmd_with_io(cmd, args, cwd=None, stdindata=None):
    if not isinstance(cmd, list):
        cmd = [cmd]
    if not isinstance(args, list):
        args = [args]
    log_dbg('cwd:', cwd, '\n\t\tcmd:', ' '.join(cmd + args))
    stdin = None
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    result = ''
    if stdindata is not None:
        stdin = subprocess.PIPE
        try:
            stdindata = stdindata.encode('utf-8')
        except UnicodeEncodeError:
            log_dbg("eeeek! UnicodeEncodeError hope everything is okay :$")
    p = subprocess.Popen(cmd + args, cwd=cwd, stdin=stdin,
                         stdout=stdout, stderr=stdout)
    if not (p.returncode is None):
        log_err('died with exitcode "%s" before execution' % (p.returncode))
    try:
        (stdout, stderr) = p.communicate(stdindata if stdindata else None)
        result = stdout.decode('utf-8')
        error_text = stderr.decode('utf-8')
        if error_text != '':
            log_warn('content from stderr for cmd: %s\n%s' %
                     (' '.join(cmd + args), error_text))
        if p.returncode != 0:
            log_err('terminated with exitcode %s' % (p.returncode))
    except OSError:
        log_err('died with exitcode %s during execution.' % (p.returncode))
    except UnicodeDecodeError:
        log_dbg("eeeek! UnicodeDecodeError hope everything is okay :$")
    return result


def run_cmd(cmd, args, cwd=None):
    if not isinstance(cmd, list):
        cmd = [cmd]
    if not isinstance(args, list):
        args = [args]
    cmd_args = []
    for item in (cmd + args):
        cmd_args = cmd_args + [unicode(item)]
    cmd_args = ' '.join(cmd_args)
    log_dbg('cwd: %s\n\t\tcmd: %s' % (cwd, cmd_args))
    rc = subprocess.call(cmd_args, cwd=cwd, shell=True)
    if rc != 0:
        log_err('process terminated with exitcode %s' % (rc))


def expand_path(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    return path


def expand_path_with_glob(path, file_sorter=None):
    expanded_path = expand_path(path)
    unglobbed_paths = glob.glob(expanded_path)
    if file_sorter is not None:
        return file_sorter.sort_files(unglobbed_paths)
    return unglobbed_paths


def load_config(path):
    '''
    Load the yaml config at path
    '''
    config = None
    try:
        expanded_path = expand_path(path)
        with open(expanded_path, 'r') as fpr:
            config = yaml.safe_load(fpr)
    except:
        log_err('can not load config: %s' % (path))
    if config is None:
        config = {}
    return config
