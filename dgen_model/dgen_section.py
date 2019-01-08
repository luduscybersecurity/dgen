import os

import dgen_template
import dgen_utils

class dgenSection(object):


    def __init__(self):
        self.name = ''
        self.contents = []
        self.template_conf = dgen_template.dgenTemplateConfig()
        self.section_type = ''


    @property
    def section_type(self):
        return self.__section_type


    @section_type.setter
    def section_type(self, value):
        self.__section_type = value


    @property
    def name(self):
        return self.__name


    @name.setter
    def name(self, value):
        self.__name = value


    @property
    def contents(self):
        return self.__contents


    @contents.setter
    def contents(self, value):
        if isinstance(value, str):
            self.__contents = [value]
        elif isinstance(value, list):
            self.__contents = value
        else:
            dgen_utils.log_err('value is not str or list: ' + value)


    def add_contents_file(self, value):
        if isinstance(value, str):
            self.__contents = self.__contents + [value]
        elif isinstance(value, list):
            self.__contents = self.__contents + value
        else:
            dgen_utils.log_err('value is not str or list: ' + value)


    @property
    def template_conf(self):
        return self.__template_conf


    @template_conf.setter
    def template_conf(self, value):
        self.__template_conf = value


    @property
    def html_filename(self):
        ext = 'html'
        if self.name == '':
            dgen_utils.log_err('name not set')
        return '.'.join([self.name, ext])


