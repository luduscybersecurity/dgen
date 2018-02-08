import subprocess
import os
import io
import mimetypes
import glob
import re

import pypandoc

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
        self.__symbols = {}
        symbols = {'bin_dir': project.bin_dir,
                   'template_dir': project.template_dir,
                   'html_dir': document.html_dir,
                   'html_filename': document.html_filename,
                   'pdf_filename': document.pdf_filename}
        self.__symbols.update(symbols)

    def replace_symbols_in_collection(self, collection, symbols=None):
        for i, string in enumerate(collection):
            collection[i] = self.replace_symbols_in_string(string)
        return collection

    def replace_symbols_in_string(self, string, symbols=None):
        if symbols is None:
            symbols = self.symbols

        pattern_bad = re.compile(r'.*?(\$\{.*?\}).*')
        match_bad = pattern_bad.match(string)
        if match_bad:
            dgen_utils.log_warn("found wrong syntax for symbol:", match_bad.group(1))
        pattern = re.compile(r'(.*?)%\{(.*?)\}(.*)')
        match = pattern.match(string)
        if match:
            if match.group(2) not in symbols:
                dgen_utils.log_warn("could not match symbol:", match.group(2))
            else:
                for key, value in symbols.items():
                    if match.group(2) == key:
                        string = match.group(1) + value + match.group(3)
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

        # Delete the html folder if it exists
        dgen_utils.delete_folder(html_dir)
        # Copy the template html folder
        cwd = os.getcwd()
        src = os.path.join(cwd, self.project.template_dir, 'html')
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
        files = document.contents
        output_file = os.path.join(document.html_dir, document.html_filename)
        # Build the document contents
        contents = '\n'
        for path in files:
            if os.path.isfile(path):
                with  io.open(path, 'r', encoding='utf-8') as f:
                    contents = contents + f.read() + '\n\n'
            else:
                dgen_utils.log_warn('file does not exist:', path)
        # Replace symbols in the content and arguments
        contents = self.symbol_processor.replace_symbols_in_string(contents)
        pandoc_options = self.project.pandoc_html_config.pandoc_options
        pandoc_options = self.symbol_processor.replace_symbols_in_collection(pandoc_options)
        filters = self.project.pandoc_html_config.filters
        filters = self.symbol_processor.replace_symbols_in_collection(filters)
        # Generate the HTML
        output = pypandoc.convert_text(contents, to_format, format='md',
                                       outputfile=output_file, extra_args=pandoc_options,
                                       filters=filters)
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
        cmd = ['wkhtmltopdf']
        cmd = cmd + self.project.wkhtmltopdf_config.wkhtmltopdf_options
        cmd = cmd + [os.path.join(document.html_dir, document.html_filename)]
        cmd = cmd + [os.path.join(os.getcwd(), document.pdf_filename)]
        cmd = ' '.join(cmd)
        self.symbol_processor.initialise(self.project, document)
        cmd = self.symbol_processor.replace_symbols_in_string(cmd)
        dgen_utils.log_dbg('cmd:', cmd)
        subprocess.call(cmd, shell=True, cwd=document.html_dir)

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