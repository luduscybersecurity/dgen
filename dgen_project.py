import os

import dgen_utils

class dgenProject(object):
    
    def __init__(self):
        self.__document_set = []
        self.__pandoc_html_config = dgenPandocHTMLConfig()
        self.__wkhtmltopdf_config = dgenWkHTMLtoPDFConfig()
        self.__template = ''
        self.__template_dir = ''
        self.__revealjs_dir = ''
        self.__metavars_config = ''

    @property
    def document_set(self):
        return self.__document_set

    @document_set.setter
    def document_set(self, value):
        self.__document_set = value

    @property
    def pandoc_html_config(self):
        return self.__pandoc_html_config

    @pandoc_html_config.setter
    def pandoc_html_config(self, value):
        self.__pandoc_html_config = value

    @property
    def wkhtmltopdf_config(self):
        return self.__wkhtmltopdf_config

    @wkhtmltopdf_config.setter
    def wkhtmltopdf_config(self, value):
        self.__wkhtmltopdf_config = value

    @property
    def template(self):
        return self.__template

    @template.setter
    def template(self, value):
        self.__template = dgen_utils.safe_path(value)

    @property
    def revealjs_dir(self):
        return self.__revealjs_dir

    @revealjs_dir.setter
    def revealjs_dir(self, value):
        self.__revealjs_dir = dgen_utils.safe_path(value)

    '''
    @property
    def metavars_config(self):
        return self.__metavars_config

    @metavars_config.setter
    def metavars_config(self, value):
        self.__metavars_config = dgen_utils.safe_path(value)
    '''

    @property
    def template_dir(self):
        if self.__template_dir != '':
            return self.__template_dir
        self.__template_dir = os.path.join(self.template, '..')
        self.__template_dir = dgen_utils.safe_path(self.__template_dir)
        return self.__template_dir

    @property 
    def bin_dir(self):
        path = os.path.dirname(os.path.realpath(__file__))
        path = dgen_utils.safe_path(path)
        return path

class dgenDocument(object):

    def __init__(self):
        self.__name = ''
        self.__contents = []

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
            self.__contents = self.__contents + [value]
        elif isinstance(value, list):    
            self.__contents = self.__contents + value

    @property 
    def html_dir(self):
        path = os.path.join(os.getcwd(), self.name+'-html')
        return dgen_utils.safe_path(path)

    @property
    def html_filename(self):
        ext = 'html'
        return self.__set_extension(ext)

    @property
    def pdf_filename(self):
        ext = 'pdf'
        return self.__set_extension(ext)

    def __set_extension(self, ext):
        if self.name != '':
            return '.'.join([self.name, ext])
        dgen_utils.log_err('name not set')


class dgenPandocHTMLConfig(object):
    def __init__(self):
        self.__pandoc_options = []
        self.__filters = []
        self.__contents = []

    @property
    def pandoc_options(self):
        return self.__pandoc_options

    @pandoc_options.setter
    def pandoc_options(self, value):
        self.__pandoc_options = value

    @property
    def filters(self):
        return self.__filters

    @filters.setter
    def filters(self, value):
        self.__filters = value

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value


class dgenWkHTMLtoPDFConfig(object):
    def __init__(self):
        self.__wkhtmltopdf_options = []

    @property
    def wkhtmltopdf_options(self):
        return self.__wkhtmltopdf_options

    @wkhtmltopdf_options.setter
    def wkhtmltopdf_options(self, value):
        self.__wkhtmltopdf_options = value
