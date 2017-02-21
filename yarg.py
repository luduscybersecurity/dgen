#!/usr/bin/env python3

'''
Yet another document Generator
'''
import sys
import argparse

import yarg_utils
import yarg_generator
import yarg_repo

class Yarg(object):
    '''
    Run yarg
    '''

    @property
    def doc(self):
        return self.__doc

    @doc.setter
    def doc(self, value):
        self.__doc = value

    def __init__(self):
        '''
        Run yarg
        '''
        self.parse_options()

    def generate_html(self, args):
        '''
        generate a html doc
        '''
        self.doc = yarg_generator.YargDocument('.yarg/global_config.yaml', 'config.yaml')
        try:
            if args.html_dir is not None:
                # TODO - allow changing of html_dir
                pass
        except AttributeError:
            pass
        html_generator = yarg_generator.YargHTMLGenerator()
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
        pdf_generator = yarg_generator.YargPDFGenerator()
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
        parser_pdf.add_argument('--html-dir', action='store',
                                help='write html output to the supplied directory (default html)')
        parser_pdf.add_argument('--pdf-file', action='store',
                                help='write pdf output to the supplied file (defaults to config)')
        parser_pdf.set_defaults(func=self.generate_pdf)

    def add_repo_options(self, subparser):
        return

    def parse_options(self):
        '''
        Parse yarg options
        '''
        parser = argparse.ArgumentParser(prog='yarg',
                                         description='Yet another report generator for pirates')
        subparser = parser.add_subparsers()
        self.add_gen_options(subparser)
        self.add_repo_options(subparser)

        args = parser.parse_args()
        try:
            args.func(args)
        except AttributeError:
            parser.print_usage()
            parser.print_help()

if __name__ == '__main__':
    Yarg()
