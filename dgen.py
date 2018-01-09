#!/usr/bin/env python3

'''
Report generation for degenerates
'''
import argparse
import os

import dgen_generator
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
        self.__doc = None
        self.__global_config = os.path.dirname(os.path.realpath(__file__))
        self.__global_config = os.path.join(self.__global_config, 'global_config.yaml')
        self.options = dgen_utils.load_config(self.__global_config) 
        
        self.parse_options()

    @property
    def doc(self):
        return self.__doc

    @doc.setter
    def doc(self, value):
        self.__doc = value

    @property
    def local_config(self):
        return self.__local_config

    @doc.setter
    def local_config(self, value):
        self.__local_config = value

    def new_project(self, args):
        if not dgen_utils.get_repo_root():
            dgen_utils.log_err('dgen repo not found in CWD or parent')
        dgen_repo.new_project(args.args)

    def list_projects(self, args):
        dgen_repo.list_projects()

    def clone_repo(self, args):
        dgen_repo.clone_repo(args.args)

    def run_git(self, args):
        dgen_repo.run_git_cmd(args.args)

    def generate_html(self, args):
        '''
        generate a html doc
        '''
        self.doc = dgen_generator.dgenDocument(args.config)
        try:
            if args.html_dir is not None:
                self.doc.html_dir = args.html_dir
        except AttributeError:
            pass
        html_generator = dgen_generator.dgenHTMLGenerator()
        html_generator.doc = self.doc
        html_generator.generate_html_document(self.doc)

    def generate_pdf(self, args):
        '''
        generate a pdf doc
        '''
        self.generate_html(args)
        try:
            if args.pdf_file is not None:
                self.doc.pdf_filename = args.pdf_file
        except AttributeError:
            pass
        pdf_generator = dgen_generator.dgenPDFGenerator()
        pdf_generator.generate_pdf_document(self.doc)

    def add_gen_options(self, subparser):
        '''
        define options for document generation
        '''
        parser_gen = subparser.add_parser('generate',
                                          aliases=['gen'],
                                          help='Generate a document')
        parser_gen.set_defaults(func=self.generate_pdf)
        subparser_gen = parser_gen.add_subparsers()
        parser_html = subparser_gen.add_parser('html',
                                               help='Generate a html document')
        parser_html.add_argument('--html-output', action='store',
                                 help='write html output to the supplied directory')
        parser_html.set_defaults(func=self.generate_html)
        parser_pdf = subparser_gen.add_parser('pdf', help='Generate a pdf document')
        parser_pdf.add_argument('--html-dir', action='store', default='html',
                                help='write html output to the supplied directory (default html)')
        parser_pdf.add_argument('--pdf-file', action='store',
                                help='write pdf output to the supplied file (defaults to config)')
        parser_pdf.set_defaults(func=self.generate_pdf)

    def add_git_options(self, subparser):
        parser_repo = subparser.add_parser('git',
                                           aliases=['gi'],
                                           help='run git command')
        parser_repo.add_argument('args', nargs=argparse.REMAINDER)
        parser_repo.set_defaults(func=self.run_git)

    def add_clone_options(self, subparser):
        parser_clone = subparser.add_parser('clone',
                                           aliases=['cl'],
                                           help='clone another repo')
        parser_clone.add_argument('args', nargs=argparse.REMAINDER,
                                 help='remainder of arguments will be sent to "git clone"')
        parser_clone.set_defaults(func=self.clone_repo)

    def add_workflow_options(self, subparser):
        parser_workflow = subparser.add_parser('mark',
                                                aliases=['mk', 'mrk'],
                                                help='mark project as matching a workflow state')
        parser_workflow.add_argument('--ignore', action='store_true', default=False,
                                     help='Ignore worflow rules')
        parser_workflow.add_argument('-m', '--message', action='store',
                                     help='Message documenting workflow change.')

    def add_list_options(self, subparser):
        parser_list = subparser.add_parser('list',
                                           aliases=['ls'],
                                           help='list existing projects on remote server')
        parser_list.set_defaults(func=self.list_projects) #self.list_projects)

    def add_switches(self, parser):
        parser.add_argument('-c', '--config', '--conf', action='store',                                                            default='config.yaml',
                            help='set the local config')


    def parse_options(self):
        '''
        Parse dgen options
        '''
        parser = argparse.ArgumentParser(prog='dgen',
                                         description='Report generation for degenerates')
        self.add_switches(parser)
        subparser = parser.add_subparsers()
        self.add_gen_options(subparser)
        self.add_git_options(subparser)
        self.add_clone_options(subparser)
        #self.add_list_options(subparser)

        args = parser.parse_args()

        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_usage()
            parser.print_help()

if __name__ == '__main__':
    dgen()
