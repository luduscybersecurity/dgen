from __future__ import print_function
import sys
import errno
import shutil
import shlex
import os
import traceback
import subprocess
import io
import glob
import re

import git
import yaml

DEBUG = False
REFRESH_TEMPLATE = False
WORK_OFFLINE = False


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
        if os.path.exists(expanded_path):
            if os.path.isfile(expanded_path):
                os.unlink(expanded_path)
            elif os.path.isdir(expanded_path):
                shutil.rmtree(expanded_path)


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
    cmd_str = ''

    # this is gross, but wkhtmltopdf doesn't support being run from a list
    for arg in shlex.split(' '.join(cmd + args)):
        cmd_str += shlex.quote(arg) + ' '
    log_dbg('cwd: %s\n\t\tcmd: %s' % (cwd, cmd_str))
    rc = subprocess.call(cmd_str, cwd=cwd, shell=True)
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
        log_dbg('can not load config: %s' % (path))
        config = {}
    return config


def get_user_config_dir():
    config_dir = os.path.join(os.path.expanduser("~"), ".dgen")
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    return config_dir


def is_git_url(url):
    PATTERN = re.compile(r'.*(\:|\/)(.*?)\.git\/?')
    if PATTERN.match(url):
        return True
    return False


def get_git_repo_name(url):
    PATTERN = re.compile(r'.*(\:|\/)(.*?)\.git\/?')
    if PATTERN.match(url):
        return PATTERN.match(url).group(2)
    return ''


class GitProgress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        log_dbg(self._cur_line)
