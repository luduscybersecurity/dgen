import dgen_model
import dgen_utils

class dgenDocument(object):


    def __init__(self):
        self.sections = []


    @property
    def sections(self):
        return self.__sections


    @sections.setter
    def sections(self, value):
        if isinstance(value, str):
            self.__sections = [value]
        elif isinstance(value, list):
            self.__sections = value


    def add_section(self, value):
        if isinstance(value, list):
            self.__sections = self.__sections + value
        else:
            self.__sections = self.__sections + [value]

