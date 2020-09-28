import os
import sys
import re
import shutil
import git

import dgen_model.dgen_document as dgen_document
import dgen_model.dgen_template as dgen_template
import dgen_model.dgen_file_sorter as dgen_file_sorter
import dgen_utils


class dgenProject(object):

    def __init__(self):
        self.document = dgen_document.dgenDocument()
        self.template = dgen_template.dgenTemplateConfig()
        # root folder where all templates are stored:  ie. ./dgen-templates
        self.templates_root = ''
        self.template = ''
        self.template_conf = ''
        self.filename = ''
        self.classification = ''
        self.revealjs_dir = ''
        self.file_sorter = None
        self.pathspec = 'master'

    @property
    def file_sorter(self):
        return self.__filesorter

    @file_sorter.setter
    def file_sorter(self, value):
        self.__filesorter = value

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, value):
        self.__filename = value

    @property
    def pdf_filename(self):
        if self.filename == '':
            dgen_utils.log_err('filename not set')
        return '.'.join([self.filename, 'pdf'])

    @property
    def classification(self):
        return self.__classification

    @classification.setter
    def classification(self, value):
        self.__classification = value

    @property
    def document(self):
        return self.__document

    @document.setter
    def document(self, value):
        self.__document = value

    @property
    def template_conf(self):
        return self.__template_conf

    @template_conf.setter
    def template_conf(self, value):
        self.__template_conf = value

    @property
    def pathspec(self):
        # if self.__pathspec is '':
        #     dgen_utils.log_warn("pathspec hasn't been set, project template may change over time. using 'master'")
        #     return 'master'
        return self.__pathspec

    @pathspec.setter
    def pathspec(self, value):
        self.__pathspec = value

    def template_refresh_required(self):
        if dgen_utils.REFRESH_TEMPLATE is True or not os.path.exists(self.local_template_dir):
            return True
        return False

    def refresh_template(self):
        if os.path.exists(self.local_template_dir):
            dgen_utils.delete_folder(self.local_template_dir)
        if dgen_utils.is_git_url(self.template_dir) is True:
            repo = git.Repo.clone_from(
                self.template_dir, self.local_template_dir, progress=dgen_utils.GitProgress())
            for remote in repo.remotes:
                remote.fetch(progress=dgen_utils.GitProgress())
            g = git.Git(repo.working_dir)
            g.checkout(self.pathspec)
            repo.submodule_update(recursive=True)
        elif os.path.isdir(self.template_dir):
            dgen_utils.copy_files(self.template_dir, self.local_template_dir)

    @property
    def template_dir(self):
        result = os.path.join(self.templates_root, self.template)
        if dgen_utils.is_git_url(result) is True:
            return result
        result = dgen_utils.expand_path(result)
        if os.path.isdir(result) is False:
            dgen_utils.log_err('template_dir %s does not exist!' % (result))
        return result

    @property
    def local_template_dir(self):
        if dgen_utils.is_git_url(self.template_dir) is True:
            return os.path.join(dgen_utils.get_user_config_dir(), dgen_utils.get_git_repo_name(self.template_dir))
        return os.path.join(dgen_utils.get_user_config_dir(), os.path.basename(os.path.normpath(self.template_dir)))

    @property
    def templates_root(self):
        return self.__templates_root

    @templates_root.setter
    def templates_root(self, value):
        self.__templates_root = value

    @property
    def template(self):
        return self.__template

    @template.setter
    def template(self, value):
        self.__template = value

    @property
    def html_dir(self):
        return os.path.join(os.getcwd(), self.filename + '-html')

    @property
    def bin_dir(self):
        path = os.path.dirname(os.path.realpath(sys.argv[0]))
        return path

    @property
    def revealjs_dir(self):
        return self.__revealjs_dir

    @revealjs_dir.setter
    def revealjs_dir(self, value):
        self.__revealjs_dir = dgen_utils.expand_path(value)
        if not os.path.isdir(self.__revealjs_dir):
            dgen_utils.log_err('revealjs_dir %s does not exist!' % (value))
