#!/usr/bin/env python

'''
Report generation for degenerates
'''
import argparse
import os

import dgen_generator
import dgen_config_parser
import dgen_repo
import dgen_utils


class dgen(object):
    '''
    Run dgen
    '''

    def __init__(self):
        '''
        Run dgen
        '''
        self.project = None
        global_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'global_config.yaml')
        global_config_file = dgen_utils.expand_path(global_config_file)
        self.global_config = dgen_utils.load_config(global_config_file)
        self.parse_options()


    @property
    def project(self):
        return self.__project


    @project.setter
    def project(self, value):
        self.__project = value


    @property
    def global_config(self):
        return self.__global_config


    @global_config.setter
    def global_config(self, value):
        self.__global_config = value


    def load_project(self, project_config_file):
        parser = dgen_config_parser.dgenConfigParser()
        project_config = dgen_utils.load_config(project_config_file)
        config = {}
        config.update(self.global_config)
        config.update(project_config)
        project = parser.parse_project(config)
        return project


    def generate_html(self, args):
        self.project = self.load_project(args.config)
        html_generator = dgen_generator.dgenPandocGenerator(self.project)
        html_generator.generate_pages('html')


    def generate_pdf(self, args):
        self.generate_html(args)
        print("Generating PDF")
        pdf_generator = dgen_generator.dgenPDFGenerator(self.project)
        pdf_generator.generate_pdf()


    def generate_revealjs(self, args):
        self.project = self.load_project(args.config)
        reveal_generator = dgen_generator.dgenRevealGenerator(self.project)
        reveal_generator.generate_pages('revealjs')

    
    def add_switches(self, parser):
        parser.add_argument('-c', '--config', '--conf', 
                            action='store', default='config.yaml',
                            help='set the local config')
        parser.add_argument('-d', '--debug',
                            action='store_true', default=False,
                            help='enable debugging output')
        parser.add_argument('-r', '--refresh', '--refresh-template',
                            action='store_true', default=False,
                            help='force a refresh of the local document template')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--pdf', action='store_true', default=True,
                            help='Generate a pdf document')
        group.add_argument('--html', action='store_true', default=False,
                            help='Generate a html document')
        group.add_argument('--revealjs', action='store_true', default=False,
                            help='Generate a reveal.js presentation')
        

    def parse_options(self):
        '''
        Parse dgen options
        '''
        parser = argparse.ArgumentParser(prog='dgen',
                                         description='Report generation for degenerates')
        self.add_switches(parser)
        args = parser.parse_args()
        
        dgen_utils.DEBUG=args.debug
        dgen_utils.REFRESH_TEMPLATE=args.refresh
        if args.html is True:
            self.generate_html(args)
        elif args.revealjs is True:
            self.generate_revealjs(args)
        else:
            self.generate_pdf(args)


if __name__ == '__main__':
    dgen()
