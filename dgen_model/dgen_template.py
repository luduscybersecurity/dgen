import os
import dgen_utils

class dgenTemplateConfig(object):


    def __init__(self):
        self.pandoc_options = []
        self.wkhtmltopdf_options = []
        self.metadata = []

        
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



