#!/usr/bin/env python

'''
Yet another document Generator
'''

import subprocess
from copy import deepcopy
import argparse
import os

import glob
import pypandoc
import yaml

import yarg_utils

class YargLoader(object):
    '''
    Loads a YargDocument from the supplied config
    '''
    def parse_config(self, doc, config):
        for key in config:
            if key == 'sections':
                doc.sections = self.parse_sections(config[key])
            elif key == 'pdf_filename':
                doc.pdf_filename = self.parse_files(config[key])
            elif key == 'html_global':
                doc.html_global_options = self.parse_html_global(config[key])
            elif key == 'pdf_global':
                doc.pdf_global_options = self.parse_pdf_global(config[key])
            else:
                yarg_utils.log_warn("Unrecognised option: " + key)
        return doc

    def parse_files(self, files_conf):
        '''
        Parse files_conf and return the result
        '''
        return self.conf_to_list(files_conf, "pdf_filename is not a string")

    def conf_to_list(self, conf, error_msg):
        if isinstance(conf, str):
            return [conf]
        elif isinstance(conf, list):
            result = []
            for string in conf:
                if isinstance(string, str):
                    result = result + [string]
                else:
                    yarg_utils.log_warn(error_msg)
            return result
        else:
            yarg_utils.log_warn(error_msg)
            return []

    def parse_sections(self, sections_conf):
        '''
        parse sections_conf and return the result
        '''
        sections = []
        if isinstance(sections_conf, list):
            for section_conf in sections_conf:
                sections = sections + [self.parse_section(section_conf)]
        else:
            yarg_utils.log_warn("Sections must be a list")
        return sections

    def parse_section(self, section_conf):
        section = YargSection()
        if not isinstance(section_conf, dict):
            yarg_utils.log_warn("Section is not a dict")
            return
        for key in section_conf:
            section.doc_type = key
            conf_item = section_conf[key]
            if isinstance(conf_item, str):
                section.files = [conf_item]
            elif isinstance(conf_item, dict):
                if 'files' in conf_item:
                    section.files = conf_item['files']
                if 'html_options' in conf_item:
                    section.html_options = self.parse_html_options(conf_item['html_options'])
                if 'pdf_options' in conf_item:
                    section.pdf_options = self.parse_pdf_options(conf_item['pdf_options'])
        return section

    def parse_html_options(self, html_options_conf):
        return self.conf_to_list(html_options_conf, "html options must be a string or list")

    def parse_pdf_options(self, pdf_options_conf):
        return self.conf_to_list(pdf_options_conf, "pdf options must be string or list")

    def parse_pdf_global(self, pdf_global_conf):
        pdf_global_options = YargPDFConfig()
        pdf_global_options.pdf_options = self.parse_pdf_options(pdf_global_conf['pdf_options'])
        return pdf_global_options

    def parse_html_global(self, html_global_conf):
        html_global_options = YargHTMLConfig()
        html_global_options.filters = self.parse_filters(html_global_conf['pandoc_filters'])
        html_global_options.files = self.parse_files(html_global_conf['files'])
        html_global_options.html_options = self.parse_html_options(html_global_conf['html_options'])
        return html_global_options

    def parse_filters(self, filters):
        return self.conf_to_list(filters, "filters must be string or list")

    def load_config(self, path):
        '''
        Load the yaml config at path
        '''
        config = {}
        with open(path, 'r') as fpr:
            config = yaml.safe_load(fpr)
        return config


class YargHTMLConfig(object):
    def __init__(self):
        self.__html_options = []
        self.__filters = []
        self.__files = []

    @property
    def html_options(self):
        return self.__html_options

    @html_options.setter
    def html_options(self, value):
        self.__html_options = value

    @property
    def filters(self):
        return self.__filters

    @filters.setter
    def filters(self, value):
        self.__filters = value

    @property
    def files(self):
        return self.__files

    @files.setter
    def files(self, value):
        if isinstance(value, str):
            self.__files = self.__files + [value]
        elif isinstance(value, list):    
            self.__files = self.__files + value


class YargPDFConfig(object):
    def __init__(self):
        self.__pdf_options = []

    @property
    def pdf_options(self):
        return self.__pdf_options

    @pdf_options.setter
    def pdf_options(self, value):
        self.__pdf_options = value

class YargSection(YargHTMLConfig, YargPDFConfig):
    '''
    A yarg section
    '''
    def __init__(self):
        YargHTMLConfig.__init__(self)
        YargPDFConfig.__init__(self)
        self.__doc_type = ""

    @property
    def doc_type(self):
        return self.__doc_type

    @doc_type.setter
    def doc_type(self, value):
        self.__doc_type = value

    @property
    def html_file(self):
        if len(self.files) > 0:
            return self.files[-1] + '.html'
        return ''

class YargDocument(object):
    '''
    A yarg document
    '''

    @property
    def sections(self):
        return self.__sections

    @sections.setter
    def sections(self, value):
        self.__sections = value

    @property
    def pdf_filename(self):
        return self.__pdf_filename

    @pdf_filename.setter
    def pdf_filename(self, value):
        self.__pdf_filename = value

    @property
    def html_global_options(self):
        return self.__html_global_options

    @html_global_options.setter
    def html_global_options(self, value):
        self.__html_global_options = value

    @property
    def pdf_global_options(self):
        return self.__pdf_global_options

    @pdf_global_options.setter
    def pdf_global_options(self, value):
        self.__pdf_global_options = value

    def __init__(self, global_config, local_config):
        '''
        Create a new document from the supplied configs
        '''

        self.__sections = []
        self.__pdf_filename = ""
        self.__html_global_options = YargHTMLConfig()
        self.__pdf_global_options = YargPDFConfig()

        loader = YargLoader()
        global_config = loader.load_config(global_config)
        loader.parse_config(self, global_config)
        local_config = loader.load_config(local_config)
        loader.parse_config(self, local_config)

class YargHTMLGenerator(object):

    def __init__(self):
        '''
        Setup the current folder for HTML generation.
        '''
        # Create the html output folder
        cwd = os.getcwd()
        self.__html_dir = os.path.join(cwd, 'html')
        yarg_utils.delete_folder(self.__html_dir)
        # Copy folders and contents from .yarg into html output folder
        self.__yarg_dir = os.path.join(cwd, '.yarg/html')
        yarg_utils.copy_files(self.__yarg_dir, self.__html_dir)
        # Copy other files to the HTML dir for referencing
        for path in [p for p in glob.glob('*') if not (p.endswith('.md') or p.endswith('.yaml'))]:
            path = os.path.join(cwd, path)
            yarg_utils.copy_files(path, self.__html_dir)
        # replace ${cwd} in all files
        for root, _, files in os.walk('html', topdown=False):
            for name in files:
                yarg_utils.replace_html_dir_symbol_in_file(os.path.join(root, name))

    def generate_html_section(self, section, html_global_opts):
        '''
        Generate HTML for the section described by config.
        '''
        if section.doc_type == 'toc':
            return
        files = html_global_opts.files + section.files
        # Build the output filename taking the last name from the list of files
        output_file = os.path.join(self.__html_dir, section.html_file)
        # Open each file in turn and concatenate together
        contents = '\n'
        for path in files:
            if os.path.isfile(path):
                contents = contents + open(path, 'r').read() + '\n'
        html_options = html_global_opts.html_options + section.html_options
        filters = html_global_opts.filters + section.filters
        # Generate the HTML
        output = pypandoc.convert_text(contents, 'html', format='md',
                                       outputfile=output_file, extra_args=html_options,
                                       filters=filters)
        assert output == ''

    def generate_html_document(self, doc):
        '''
        Generate a html document
        '''
        for section in doc.sections:
            self.generate_html_section(section, doc.html_global_options)

class YargPDFGenerator(object):

    def generate_pdf_document(self, doc):
        '''
        Generate a pdf document given the supplied configs
        '''
        cmd = ['wkhtmltopdf']
        cmd = cmd + doc.pdf_global_options.pdf_options
        for section in doc.sections:
            if section.doc_type == 'cover' or section.doc_type == 'toc':
                cmd = cmd + [section.doc_type]
            cmd = cmd + [section.html_file]
            cmd = cmd + section.pdf_options
        cmd = cmd + doc.pdf_filename
        cmd = ' '.join(cmd)
        cmd = yarg_utils.replace_html_dir_symbol_in_str(cmd)
        subprocess.call(cmd, shell=True, cwd=yarg_utils.get_html_dir())

class Yarg(object):
    '''
    Run yarg
    '''

    def __init__(self):
        '''
        Run yarg
        '''
        self.parse_options()
        doc = YargDocument('.yarg/global_config.yaml', 'config.yaml')
        html_generator = YargHTMLGenerator()
        html_generator.generate_html_document(doc)
        pdf_generator = YargPDFGenerator()
        pdf_generator.generate_pdf_document(doc)

    def parse_options(self):
        '''
        Parse yarg options
        '''
        return

if __name__ == '__main__':
    Yarg()
