import subprocess
import os
import io
import mimetypes
import glob
import re

import dgen_model
import dgen_utils

from dgen_model import dgen_project


class dgenSymbolProcessor(object):

    def __init__(self, project):
        self.symbols = {}
        self.initialise(project)

    @property
    def symbols(self):
        return self.__symbols

    @symbols.setter
    def symbols(self, val):
        self.__symbols = val

    def initialise(self, project):
        self.symbols = {'pdf_filename': project.pdf_filename,
                        'bin_dir': project.bin_dir,
                        'template_dir': project.local_template_dir,
                        'html_dir': project.html_dir,
                        'classification': project.classification}
        for key, value in self.symbols.items():
            if key is not 'classification':
                self.symbols[key] = dgen_utils.expand_path(value)

    def replace_symbols_in_collection(self, collection, symbols=None):
        for i, string in enumerate(collection):
            collection[i] = self.replace_symbols_in_string(string)
        return collection

    def replace_symbols_in_string(self, string, symbols=None):
        if symbols is None:
            symbols = self.symbols
        matches_bad = re.finditer(r'(\${.*?})', string)
        for bad_match in matches_bad:
            dgen_utils.log_warn(
                "found wrong syntax for symbol:", bad_match.group(0))
        for key, value in symbols.items():
            search_string = '%{' + key + '}'
            string = re.sub(search_string, unicode(value), string)
        return string

    def replace_symbols_in_file(self, path, symbols=None):
        mime_type, _ = mimetypes.guess_type(path)
        pattern = re.compile(r'text|xml|html|css|javascript|plain')
        if (mime_type is not None and
                pattern.search(mime_type) is not None):
            with open(path, 'r') as fpr:
                contents = fpr.read()
                fpr.close()
                contents = self.replace_symbols_in_string(contents, symbols)
                with open(path, 'w') as fpw:
                    fpw.write(contents)
                    fpw.close()


class dgenGenerator(object):

    def __init__(self, project=None):
        self.project = project
        self.symbol_processor = dgenSymbolProcessor(project)

    @property
    def project(self):
        return self.__project

    @project.setter
    def project(self, value):
        self.__project = value

    @property
    def symbol_processor(self):
        return self.__symbol_processor

    @symbol_processor.setter
    def symbol_processor(self, value):
        self.__symbol_processor = value


class dgenPandocGenerator(dgenGenerator):

    def __init__(self, project=None):
        dgenGenerator.__init__(self, project)

    def prepare_html_dir(self, html_dir):
        '''
        Prepare the html_directory, copying it from the project's template
        '''
        cwd = os.getcwd()
        # Delete the html folder if it exists
        dgen_utils.delete_folder(html_dir)
        # Copy the template html folder
        src = os.path.join(self.project.local_template_dir, 'html')
        src = dgen_utils.expand_path(src)
        dgen_utils.copy_files(src, html_dir)
        # Copy other files to the HTML dir for referencing
        for item in [p for p in glob.glob('*') if not (p.endswith('.md') or
                                                       p.endswith('.yaml') or
                                                       p.endswith('.pdf') or
                                                       p.endswith('-html'))]:
            src = os.path.join(cwd, item)
            dst = os.path.join(html_dir, item)
            dgen_utils.copy_files(src, dst)
        # replace ${html_dir} in all files
        for root, _, files in os.walk(html_dir, topdown=False):
            for name in files:
                # Symbol processor must be initialised previously
                self.symbol_processor.replace_symbols_in_file(
                    os.path.join(root, name), self.symbol_processor.symbols)

    def print_markdown_contents(self, contents):
        output = ""
        line_num = 1
        lines = contents.splitlines()
        for line in lines:
            output = output + str(line_num) + ": " + line + "\n"
            line_num = line_num + 1
        dgen_utils.log_dbg(output)

    def generate_page(self, document, to_format):
        files = self.symbol_processor.replace_symbols_in_collection(
            self.project.template_conf.metadata +
            document.template_conf.metadata +
            document.contents)
        # Build the document contents
        contents = u'\n'
        symbols = dict(self.symbol_processor.symbols)
        for path in files:
            for expanded_path in dgen_utils.expand_path_with_glob(
                    path, self.project.file_sorter):
                if os.path.isfile(expanded_path):
                    symbols['file'] = os.path.basename(
                        expanded_path).split('.')[0]
                    with io.open(expanded_path, 'r', encoding='utf-8') as f:
                        filecontents = self.symbol_processor.replace_symbols_in_string(
                            f.read(), symbols)
                        contents = contents + filecontents + u'\n\n'
                else:
                    dgen_utils.log_err('file does not exist:', expanded_path)
        self.print_markdown_contents(contents)
        output_file = os.path.join(
            self.project.html_dir, document.html_filename)
        pandoc_options = self.project.template_conf.pandoc_options
        pandoc_options = document.template_conf.pandoc_options + pandoc_options
        pandoc_options = self.symbol_processor.replace_symbols_in_collection(
            pandoc_options)
        pandoc_options = ['--output=' + dgen_utils.expand_path(
            output_file), '--from=markdown', '--to='+to_format] + pandoc_options
        output = dgen_utils.run_cmd_with_io(
            'pandoc', pandoc_options, stdindata=contents)
        assert output == ''

    def generate_pages(self, to_format):
        self.prepare_html_dir(self.project.html_dir)
        for page in self.project.document.sections:
            if page.section_type is not 'toc':
                self.generate_page(page, to_format)


class dgenPDFGenerator(dgenGenerator):

    def __init__(self, project):
        dgenGenerator.__init__(self, project)

    def generate_pdf(self):
        cmd = 'wkhtmltopdf'
        args = self.project.template_conf.wkhtmltopdf_options
        for section in self.project.document.sections:
            args += [section.section_type]
            if section.section_type is not 'toc':
                args += [os.path.join(self.project.html_dir,
                                      section.html_filename)]
            args += section.template_conf.wkhtmltopdf_options
        args = args + [os.path.join(os.getcwd(), self.project.pdf_filename)]
        args = self.symbol_processor.replace_symbols_in_collection(args)
        dgen_utils.run_cmd(cmd, args, cwd=self.project.html_dir)


class dgenRevealGenerator(dgenPandocGenerator):

    def __init__(self, project=None):
        dgenPandocGenerator.__init__(self, project)

    def copy_reveal(self):
        if self.project.revealjs_dir is '':
            dgen_utils.log_err('config item revealjs_dir not set for project')
        dgen_utils.copy_files(self.project.html_dir, self.project.revealjs_dir)

    def generate_pages(self, to_format):
        dgenPandocGenerator.generate_pages(self, to_format)
        self.copy_reveal()
