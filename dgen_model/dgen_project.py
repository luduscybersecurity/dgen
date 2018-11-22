import os

import dgen_document
import dgen_template
import dgen_utils

class dgenProject(object):


    def __init__(self):
        self.document = dgen_document.dgenDocument()
        self.template = dgen_template.dgenTemplate()
        self.templates_root_dir = ''  # root folder where all templates are stored:  ie. ~/dgen-templates
        self.filename = ''

        
    @property
    def document(self):
        return self.__document_set


    @document.setter
    def document(self, value):
        self.__document = value


    @property
    def template(self):
        return self.__template


    @template.setter
    def template(self, value):
        self.__template = value


    @property
    def templates_root_dir(self):
        return self.__templates_root_dir


    @templates_root_dir.setter
    def templates_root_dir(self, value):
        self.__templates_root_dir = value


    @property
    def bin_dir(self):
        path = os.path.dirname(os.path.realpath(__file__))
        return path

