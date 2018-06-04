import subprocess
import os
import io
import mimetypes
import glob
import re

import dgen_utils
import dgen_project

class dgenSymbolProcessor(object):
    def __init__(self, project=None, document=None):
        self.__symbols = {}
        if project is not None and document is not None:
            self.initialise(project, document)

    @property
    def symbols(self):
        return self.__symbols

    def initialise(self, project, document):
        self.__symbols = {'html_filename': document.html_filename,
                          'pdf_filename': document.pdf_filename}
        symbols = {'bin_dir': project.bin_dir,
                   'template_dir': project.template_dir,
                   'html_dir': document.html_dir}
        if project.templates_root != '':
            symbols.update({'templates_root': project.templates_root})
        for key, value in symbols.items():
            symbols[key] = dgen_utils.expand_paths(value)
        self.__symbols.update(symbols)

    def replace_symbols_in_collection(self, collection, symbols=None):
        for i, string in enumerate(collection):
            collection[i] = self.replace_symbols_in_string(string)
        return collection

    def replace_symbols_in_string(self, string, symbols=None):
        if symbols is None:
            symbols = self.symbols
        matches_bad = re.finditer(r'(\${.*?})', string)
        for bad_match in matches_bad:
            dgen_utils.log_warn("found wrong syntax for symbol:", bad_match.group(0))
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

    def __init__(self):
        self.__project = dgen_project.dgenProject()
        self.__symbol_processor = dgenSymbolProcessor()

    @property
    def project(self):
        return self.__project

    @project.setter
    def project(self, value):
        self.__project = value

    @property
    def symbol_processor(self):
        return self.__symbol_processor


class dgenPandocGenerator(dgenGenerator):

    def __init__(self):
        dgenGenerator.__init__(self)

    def prepare_html_dir(self, html_dir):
        '''
        Prepare the html_directory, copying it from the project's template
        '''
        cwd = os.getcwd()
        # Delete the html folder if it exists
        dgen_utils.delete_folder(html_dir)
        # Copy the template html folder
        src = os.path.join(self.project.template_dir, 'html')
        src = dgen_utils.expand_paths(src)
        dgen_utils.copy_files(src, html_dir)
        # Copy other files to the HTML dir for referencing
        for item in [p for p in glob.glob('*') if not (p.endswith('.md') or
                                                       p.endswith('.yaml') or
                                                       p.endswith('.pdf') or
                                                       p.endswith('-html'))]:
            src = os.path.join(cwd, item)
            dst =  os.path.join(html_dir, item)
            dgen_utils.copy_files(src, dst)
        # replace ${html_dir} in all files
        for root, _, files in os.walk(html_dir, topdown=False):
            for name in files:
                # Symbol processor must be initialised previously
                self.symbol_processor.replace_symbols_in_file(os.path.join(root, name))

    def generate_document(self, document, to_format):
        self.symbol_processor.initialise(self.project, document)
        # First prepare the html directory for generation
        self.prepare_html_dir(document.html_dir)
        files = self.symbol_processor.replace_symbols_in_collection(document.contents + self.project.metadata)
        files = dgen_utils.expand_paths(files)
        output_file = os.path.join(document.html_dir, document.html_filename)
        # Build the document contents
        contents = u'\n'
        for path in files:
            if os.path.isfile(path):
                with  io.open(path, 'r', encoding='utf-8') as f:
                    filecontents = f.read()
                    contents = contents + filecontents + u'\n\n'
            else:
                dgen_utils.log_warn('file does not exist:', path)
        # Replace symbols in the content and arguments
        contents = self.symbol_processor.replace_symbols_in_string(contents)
        pandoc_options = self.project.pandoc_html_config.pandoc_options
        pandoc_options = self.symbol_processor.replace_symbols_in_collection(pandoc_options)
        pandoc_options = ['--output=' + dgen_utils.expand_paths(output_file), '--from=markdown', '--to='+to_format] + pandoc_options
        output = dgen_utils.run_cmd_with_io('pandoc', pandoc_options, stdindata=contents)
        assert output == ''


    def generate_documents(self, to_format):
        for doc in self.project.document_set:
            self.generate_document(doc, to_format)

class dgenPDFGenerator(dgenGenerator):

    def __init__(self):
        dgenGenerator.__init__(self)

    def generate_pdfs(self):
        for doc in self.project.document_set:
            self.generate_pdf(doc)

    def generate_pdf(self, document):
        cmd = 'wkhtmltopdf'
        args = self.project.wkhtmltopdf_config.wkhtmltopdf_options
        args = args + [os.path.join(document.html_dir, document.html_filename)]
        args = args + [os.path.join(os.getcwd(), document.pdf_filename)]
        self.symbol_processor.initialise(self.project, document)
        args = self.symbol_processor.replace_symbols_in_collection(args)
        dgen_utils.run_cmd(cmd, args, cwd=document.html_dir)

class dgenRevealGenerator(dgenPandocGenerator):
    def __init__(self):
        dgenPandocGenerator.__init__(self)

    def copy_reveal(self):
        if self.project.revealjs_dir is not '':
            for doc in self.project.document_set:
                dgen_utils.copy_files(doc.html_dir, self.project.revealjs_dir)

    def generate_documents(self, to_format):
        dgenPandocGenerator.generate_documents(self, to_format)
        self.copy_reveal()
