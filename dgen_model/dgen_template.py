import os
import dgen_utils

class dgenTemplate(object):


    def __init__(self):
        self.template_file = ''
        self.pandoc_options = []
        self.wkhtmltopdf_options = []
        self.metadata = []
        self.revealjs_dir = ''
        

    @property
    def template_file(self):
        return self.__template_file


    @template_file.setter
    def template_file(self, value):
        self.__template_file = value


    @property
    def template_dir(self):
        self.__template_dir = os.path.join(self.template, '..')
        return self.__template_dir


    @property
    def pandoc_options(self):
        return self.__pandoc_options


    @pandoc_options.setter
    def pandoc_options(self, value):
        self.__pandoc_options = value


    @property
    def wkhtmltopdf_options(self):
        return self.__wkhtmltopdf_options


    @wkhtmltopdf_options.setter
    def wkhtmltopdf_options(self, value):
        self.__wkhtmltopdf_options = value


    @property
    def metadata(self):
        return self.__metadata


    @metadata.setter
    def metadata(self, value):
        self.__metadata = value


    @property
    def revealjs_dir(self):
        return self.__revealjs_dir


    @revealjs_dir.setter
    def revealjs_dir(self, value):
        self.__revealjs_dir = value

