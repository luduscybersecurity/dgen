import subprocess
import os
import io

import glob
import pypandoc

import dgen_utils
import dgen_project

class dgenLoader(object):

    def __init__(self):
        self.__project = dgen_project.dgenProject()

    @property
    def project(self):
        return self.__project

    @project.setter
    def project(self, value):
        self.__project = value

    '''
    Loads a dgenProject from the supplied project_config
    '''
    def parse_project(self, project_config):
        if not isinstance(project_config, dict):
            dgen_utils.log_err('parse_project: project_config is not dict')
        known = ['document_set',
                 'document',
                 'pandoc_html_config',
                 'wkhtmltopdf_config',
                 'template',
                 'revealjs_dir']
        self.no_unknown_in_conf(known, project_config)
        if 'document_set' in project_config:
            self.project.document_set = self.parse_document_set(project_config['document_set'])
        if 'document' in project_config:
            self.project.document_set = [self.parse_document(project_config['document'])]
        if 'pandoc_html_config' in project_config:
            self.project.pandoc_html_config = self.parse_pandoc_config(project_config[ 'pandoc_html_config'])
        if 'wkhtmltopdf_config' in project_config:
            self.project.wkhtmltopdf_config = self.parse_wkhtmltopdf_config(project_config['wkhtmltopdf_config'])
        if 'template' in project_config:
            self.project.template = self.parse_template(project_config['template'])
        if 'revealjs_dir' in project_config:
            self.project.revealjs_dir = self.parse_revealjs(project_config['revealjs_dir'])
        return self.project

    def parse_document_set(self, document_set_conf):
        if not isinstance(document_set_conf, (list, dict)):
            dgen_utils.log_err('document_set must be list or dict:', document_set_conf)
        document_set = []
        known = ['document']
        mandatory = known
        if isinstance(document_set_conf, dict):
            document_set_conf = [document_set_conf]
        # Load documents
        for doc_conf in document_set_conf:
            self.all_mandatory_in_conf(mandatory, doc_conf)
            document_set = document_set + [self.parse_document(doc_conf['document'])]
        return document_set

    def parse_document(self, doc_conf):
        '''
        parse document config and return the result
        '''
        if not isinstance(doc_conf, dict):
            dgen_utils.log_err("doc_conf is not a dict:", doc_conf)
        known = ['name', 'contents']
        mandatory = known
        self.all_mandatory_in_conf(mandatory, doc_conf)
        self.no_unknown_in_conf(known, doc_conf)
        document = dgen_project.dgenDocument()
        document.name = doc_conf['name']
        document.contents = self.parse_contents(doc_conf['contents'])
        return document

    def parse_wkhtmltopdf_config(self, pdf_conf):
        if not isinstance(pdf_conf, dict):
            dgen_utils.log_err('pdf_conf is not dict:', pdf_conf)
        known = ['wkhtmltopdf_options']
        self.no_unknown_in_conf(known, pdf_conf)
        wkhtmltopdf_config = dgen_project.dgenWkHTMLtoPDFConfig()
        if 'wkhtmltopdf_options' in pdf_conf:
            wkhtmltopdf_config.wkhtmltopdf_options = self.parse_wkhtmltopdf_options(pdf_conf['wkhtmltopdf_options'])
        return wkhtmltopdf_config

    def parse_wkhtmltopdf_options(self, wkhtmltopdf_options_conf):
        return self.parse_list(wkhtmltopdf_options_conf)

    def parse_pandoc_config(self, html_conf):
        if not isinstance(html_conf, dict):
            dgen_utils.log_err('html_conf is not dict:', html_conf)
        known = ['pandoc_filters', 'pandoc_options']
        self.no_unknown_in_conf(known, html_conf)
        pandoc_config = dgen_project.dgenPandocHTMLConfig()
        if 'pandoc_filters' in html_conf:
            pandoc_config.filters = self.parse_filters(html_conf['pandoc_filters'])
        if 'pandoc_options' in html_conf:
            pandoc_config.pandoc_options = self.parse_pandoc_options(html_conf['pandoc_options'])
        return pandoc_config

    def parse_pandoc_options(self, pandoc_options_conf):
        return self.parse_list(pandoc_options_conf)

    def parse_revealjs(self, revealjs_conf):
        return self.parse_string(revealjs_conf)

    def parse_metavars(self, metavars_config):
        return self.parse_string(metavars_config)

    def parse_filters(self, filters_conf):
        return self.parse_list(filters_conf)

    def parse_contents(self, contents_conf):
        return self.parse_list(contents_conf)

    def parse_template(self, template_conf):
        return self.parse_string(template_conf)

    def parse_list(self, list_conf):
        if isinstance(list_conf, str):
            return [self.parse_string(list_conf)]
        elif isinstance(list_conf, list):
            result = []
            for string in list_conf:
                result = result + [self.parse_string(string)]
            return result
        else:
            dgen_utils.log_err("expected string or list, got:", list_conf)

    def parse_string(self, string):
        if not isinstance(string, (str, int, float)):
            dgen_utils.log_err("could not parse as string or number:", string)
        return str(string)

    def all_mandatory_in_conf(self, mandatory, conf):
        dgen_utils.log_dbg('mandatory fields:', mandatory)
        for key in mandatory:
            if not key in conf:
                dgen_utils.log_err('attribute missing:', conf)

    def no_unknown_in_conf(self, known, conf):
        dgen_utils.log_dbg('known fields:', known)
        for key in conf:
            if not key in known:
                dgen_utils.log_err('unknown attribute:', key)
