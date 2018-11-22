import subprocess
import os
import io

import glob

import dgen_utils
from dgen_model import *

class dgenConfigParser(object):

    '''
    Loads a dgenProject from the supplied project_config
    '''
    def parse_project(self, project_config):
        project = dgen_project.dgenProject()
        if not isinstance(project_config, dict):
            dgen_utils.log_err('parse_project: project_config is not dict')
        known = ['document',
                 'template',
                 'template_root_dir',
                 'revealjs_dir',
                 'filename',
                 'metadata']
        self.no_unknown_in_conf(known, project_config)
        if 'document' in project_config:
            project.document_set = [self.parse_document(project_config['document'])]
        if 'template_root_dir' in project_config:
            project.template_dir = self.parse_template_dir(project_config['template_root_dir'])
        if 'template' in project_config:
            project.template = self.parse_template(project_config['template'])
        if 'metadata' in project_config:
            project.metadata = self.parse_metadata(project_config['metadata'])
        if 'revealjs_dir' in project_config:
            project.revealjs_dir = self.parse_revealjs(project_config['revealjs_dir'])
        if 'filename' in project_config:
            project.filename = self.parse_filename(project_config['filename'])
        return project


    def parse_template(self, template_config):
        if not isinstance(template_config, dict):
            dgen_utils.log_err('parse_project: template_config is not dict')
        known = ['pandoc_options',
                 'wkhtmltopdf_options',
                 'metadata',
                 'revealjs_dir']
        template = dgen_template.dgenTemplate()
        self.no_unknown_in_conf(known, template_config)
        if 'pandoc_options' in template_config:
            template.pandoc_options = parse_pandoc_options(template_config['pandoc_options'])
        if 'wkhtmltopdf_options' in template_config:
            template.wkhtmltopdf_options = parse_wkhtmltopdf_options(template_config['wkhtmltopdf_options'])
        if 'metadata' in template_conflig:
            template.metadata = parse_metadata(template_config['metadata'])
        if 'revealjs_dir' in template_config:
            template.revealjs_dir = parse_revealjs(template_config['revealjs_dir'])


    def parse_document(self, document_conf):
        '''
        parse document config and return the result
        '''
        if not isinstance(document_conf, list):
            dgen_utils.log_err("document_conf is not a list:", document_conf)
        document = dgen_document.dgenDocument()
        known = ['cover', 'toc', 'section']
        for item in document_conf:
            self.no_unknown_in_conf(known, item)
            #TODO: adding the doc_type after is dogey. may need to refactor.
            if 'cover' in item:
                cover = self.parse_section(item['cover'], 'cover')
                document.add_section(cover)
            if 'toc' in item:
                toc = self.parse_section(item['toc'], 'toc')
                document.add_section(toc)
            if 'section' in item:
                section = self.parse_section(item['section'], 'section')
                document.add_section(section)
        return document


    def parse_section(self, section_conf, section_type):
        '''
        parse section config and return the result
        '''
        if not isinstance(section_conf, dict):
            dgen_utils.log_err("section_conf is not a dict", section_conf)
        known = ['name', 'contents', 'template']
        self.no_unknown_in_conf(known, section_conf)
        section = dgen_section.dgenSection()
        section.section_type = section_type
        if 'name' in section_conf:
            section.name = self.parse_name(section_conf['name'])
        if 'contents' in section_conf:
            section.contents = self.parse_contents(sections_conf['contents'])
        if 'template' in section_conf:
            section.template = self.parse_template(section_conf['template'])
        # if 'pandoc_options' in section_conf:
        #     template.pandoc_options = self.parse_pandoc_options(section_conf['pandoc_options'])
        # if 'wkhtmltopdf_options' in section_conf:
        #     template.wkhtmltopdf_options = self.parse_wkhtmltopdf_options(section_conf['wkhtmltopdf_options'])


    def parse_wkhtmltopdf_options(self, wkhtmltopdf_options_conf):
        return self.parse_list(wkhtmltopdf_options_conf)


    def parse_pandoc_options(self, pandoc_options_conf):
        return self.parse_list(pandoc_options_conf)


    def parse_revealjs(self, revealjs_conf):
        return self.parse_string(revealjs_conf)


    def parse_metadata(self, parse_metadata_config):
        return self.parse_list(parse_metadata_config)


    def parse_filters(self, filters_conf):
        return self.parse_list(filters_conf)

    def parse_name(self, name_conf):
        return self.parse_string(name_conf)

    def parse_contents(self, contents_conf):
        return self.parse_list(contents_conf)


    # def parse_template(self, template_conf):
    #     return self.parse_string(template_conf)


    def parse_templates_root(self, templates_root_conf):
        return self.parse_string(templates_root_conf)


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

