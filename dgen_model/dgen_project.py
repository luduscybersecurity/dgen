import os
import sys

import dgen_document
import dgen_template
import dgen_utils

class dgenProject(object):


    def __init__(self):
        self.document = dgen_document.dgenDocument()
        self.template = dgen_template.dgenTemplateConfig()
        self.templates_root = ''  # root folder where all templates are stored:  ie. ./dgen-templates
        self.template = ''
        self.template_conf = ''
        self.filename = ''
        self.revealjs_dir = ''


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


    def template_refresh_required(self):
        if dgen_utils.REFRESH_TEMPLATE is False and os.path.exists(self.local_template_dir):
            return False
        return True

    def refresh_template(self):
        if not os.path.exists(self.template_dir):
            dgen_utils.log_err('template_dir does not exist')
        if os.path.exists(self.local_template_dir):
            dgen_utils.delete_folder(self.local_template_dir)
        dgen_utils.copy_files(self.template_dir, self.local_template_dir)


    @property
    def template_dir(self):
        return os.path.join(self.templates_root, self.template)


    @property
    def local_template_dir(self):
        return os.path.join(os.getcwd(), self.template)


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
        self.__revealjs_dir = dgen_utils.expand_paths(value)
        if not os.path.isdir(self.__revealjs_dir):
            dgen_utils.log_err('revealjs_dir does not exist!')

