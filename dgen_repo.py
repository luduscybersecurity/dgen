import subprocess

import dgen_utils

def run_git_cmd(args):
    cmd = ['git'] + args
    # TODO: subprocess.call doesn't print to std_out/err, use pcall instead
    subprocess.call(cmd)

def remote_clone(args):
    pass

def remote_list():
    pass

