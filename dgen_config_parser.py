import subprocess
import os
import io

import glob

import dgen_utils
import dgen_generator
from dgen_model import dgen_project
from dgen_model import dgen_document
from dgen_model import dgen_section
from dgen_model import dgen_template
from dgen_model import dgen_file_sorter


class dgenConfigParser(object):

    def __init__(self):
        self.__project = None

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
        self.project = dgen_project.dgenProject()
        if not isinstance(project_config, dict):
            dgen_utils.log_err('parse_project: project_config is not dict')
        known = ['document',
                 'template',
                 'template_conf',
                 'templates_root',
                 'revealjs_dir',
                 'filename',
                 'classification',
                 'metadata',
                 'file_sorter']
        self.no_unknown_in_conf(known, project_config)
        mandatory = ['document',
                     'template',
                     'filename']
        self.all_mandatory_in_conf(mandatory, project_config)
        if 'templates_root' in project_config:
            self.project.templates_root = self.parse_templates_root(
                os.getenv('templates_root', project_config['templates_root']))
        if 'template' in project_config:
            self.project.template = self.parse_template(
                os.getenv('template', project_config['template']))
            if self.project.template_refresh_required():
                self.project.refresh_template()
        if 'template_conf' in project_config:
            self.project.template_conf = self.parse_template_conf(
                os.getenv('template_conf', project_config['template_conf']))
        if 'document' in project_config:
            self.project.document = self.parse_document(
                project_config['document'])
        if 'metadata' in project_config:
            self.project.metadata = self.parse_metadata(
                os.getenv('metadata', project_config['metadata']))
        if 'revealjs_dir' in project_config:
            self.project.revealjs_dir = self.parse_revealjs(
                os.getenv('metadata', project_config['revealjs_dir']))
        if 'filename' in project_config:
            self.project.filename = self.parse_filename(
                os.getenv('filename', project_config['filename']))
        if 'classification' in project_config:
            self.project.classification = self.parse_classification(
                os.getenv('classification', project_config['classification']))
        if 'file_sorter' in project_config:
            self.project.file_sorter = self.parse_file_sorter(
                os.getenv('file_sorter', project_config['file_sorter']))
        return self.project

    def parse_template_conf(self, template_config_file_conf):
        if not isinstance(template_config_file_conf, dict) and dgen_utils:
            template_config_file_path = os.path.join(
                self.project.local_template_dir, template_config_file_conf)
            template_config_file_conf = dgen_utils.load_config(
                template_config_file_path)
        known = ['pandoc_options',
                 'wkhtmltopdf_options',
                 'metadata']
        self.no_unknown_in_conf(known, template_config_file_conf)
        template = dgen_template.dgenTemplateConfig()
        if 'pandoc_options' in template_config_file_conf:
            template.pandoc_options = self.parse_pandoc_options(
                template_config_file_conf['pandoc_options'])
        if 'wkhtmltopdf_options' in template_config_file_conf:
            template.wkhtmltopdf_options = self.parse_wkhtmltopdf_options(
                template_config_file_conf['wkhtmltopdf_options'])
        if 'metadata' in template_config_file_conf:
            template.metadata = self.parse_metadata(
                template_config_file_conf['metadata'])
        return template

    def parse_document(self, document_conf):
        '''
        parse document config and return the result
        '''
        if not isinstance(document_conf, list):
            dgen_utils.log_err("document_conf is not a list:", document_conf)
        document = dgen_document.dgenDocument()
        known = ['cover', 'toc', 'page']
        for item in document_conf:
            self.no_unknown_in_conf(known, item)
            # TODO: adding the doc_type after is dogey. may need to refactor.
            if 'cover' in item:
                cover = self.parse_section(item['cover'], 'cover')
                document.add_section(cover)
            if 'toc' in item:
                toc = self.parse_section(item['toc'], 'toc')
                document.add_section(toc)
            if 'page' in item:
                section = self.parse_section(item['page'], 'page')
                document.add_section(section)
        return document

    def parse_section(self, section_conf, section_type):
        '''
        parse section config and return the result
        '''
        if not isinstance(section_conf, dict):
            dgen_utils.log_err("section_conf is not a dict", section_conf)
        known = ['name', 'contents', 'template_conf']
        self.no_unknown_in_conf(known, section_conf)
        section = dgen_section.dgenSection()
        section.section_type = section_type
        if 'name' in section_conf:
            section.name = self.parse_name(section_conf['name'])
        if 'contents' in section_conf:
            section.contents = self.parse_contents(section_conf['contents'])
        if 'template_conf' in section_conf:
            section.template_conf = self.parse_template_conf(
                section_conf['template_conf'])
        return section

    def parse_templates_root(self, templates_root_conf):
        return self.parse_string(templates_root_conf)

    def parse_template(self, template_conf):
        return self.parse_string(template_conf)

    def parse_wkhtmltopdf_options(self, wkhtmltopdf_options_conf):
        return self.parse_list(wkhtmltopdf_options_conf)

    def parse_pandoc_options(self, pandoc_options_conf):
        return self.parse_list(pandoc_options_conf)

    def parse_revealjs(self, revealjs_conf):
        return self.parse_string(revealjs_conf)

    def parse_filename(self, filename_conf):
        return self.parse_string(filename_conf)

    def parse_classification(self, classification_conf):
        return self.parse_string(classification_conf)

    def parse_metadata(self, parse_metadata_conf):
        return self.parse_list(parse_metadata_conf)

    def parse_filters(self, filters_conf):
        return self.parse_list(filters_conf)

    def parse_name(self, name_conf):
        return self.parse_string(name_conf)

    def parse_contents(self, contents_conf):
        return self.parse_list(contents_conf)

    def parse_template_root(self, template_root_conf):
        return self.parse_string(template_root_conf)

    def parse_file_sorter(self, file_sorter_conf):
        sorter_path = self.parse_string(file_sorter_conf)
        sorter = dgen_file_sorter.dgenFileSorter()
        symbol_processor = dgen_generator.dgenSymbolProcessor(self.project)
        sorter.source_code_path = symbol_processor.replace_symbols_in_string(
            sorter_path)
        return sorter

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

