import importlib
import os.path
import sys

import dgen_utils


class dgenFileSorter(object):

    def __init__(self):
        self.__imported_module = None

    @property
    def source_code_path(self):
        return self.__source_code_path

    @source_code_path.setter
    def source_code_path(self, value):
        self.__source_code_path = value
        self.import_source_code()

    def import_source_code(self):
        try:
            source_code_folder = os.path.dirname(self.source_code_path)
            if source_code_folder not in sys.path:
                sys.path.append(source_code_folder)
            module_name = os.path.basename(self.source_code_path).split('.')[0]
            self.__imported_module = importlib.import_module(module_name)
        except ImportError, e:
            dgen_utils.log_err('cannot import %s: %s' %
                               (self.source_code_path, e))

    @property
    def imported_module(self):
        return self.__imported_module

    def sort_files(self, unsorted):
        sorted_files = unsorted
        try:
            sorted_files = self.imported_module.sort_files(unsorted)
        except NotImplementedError, e:
            dgen_utils.log_err('error running %s.sort_files: %s' %
                               (self.imported_module, e))
        return sorted_files
