import os.path
import subprocess

import dgen_utils

def run_git_cmd(args):
    cmd = ['git'] + args
    # TODO: subprocess.call doesn't print to std_out/err, use pcall instead
    subprocess.call(cmd)

def init_repo(path, bare, args):
    # TODO: when bare == true, setup ssh access
    repo_path = path
    if repo_path is None:
        repo_path = os.getcwd()
    git_args = ['init', repo_path]
    if bare is not None and bare:
        repo_path = os.path.join(path, '.git')
        git_args = ['init', '--bare', repo_path]
    if dgen_utils.get_repo_root(repo_path) != None:
        dgen_utils.log_err('create_repo: repo found in parent folder')
        return
    run_git_cmd(git_args + args)
    for folder in ['', 'templates']:
        folder_path = os.path.join(repo_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    git_args = ['commit', '-m "Repository creation"', repo_path]
    run_git_cmd(git_args)
    return

def new_project(args):
    run_git_cmd(['checkout', '-b'] + args)

def list_projects():
    run_git_cmd(['branch'])

def rename_project(args):
    run_git_cmd(['branch', '-m'] + args.args)

def delete_project(args):
    pass

def clone_repo(args):
    run_git_cmd(['clone'] + args)

