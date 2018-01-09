import subprocess
import os

import glob
import pypandoc

import dgen_utils

class dgenLoader(object):

    def __init__(self):
        self.__doc = None

    @property
    def doc(self):
        return self.__doc

    @doc.setter
    def doc(self, value):
        self.__doc = value

    '''
    Loads a dgenDocument from the supplied config
    '''
    def parse_config(self, config):
        if 'template' in config:
            self.doc.template = self.parse_template(config['template'])
        for key in config:
            if key == 'sections':
                self.doc.sections = self.parse_sections(config[key])
            elif key == 'pdf_filename':
                self.doc.pdf_filename = self.parse_file(config[key])
            elif key == 'html_global':
                self.doc.html_global_options = self.parse_html_global(config[key])
            elif key == 'pdf_global':
                self.doc.pdf_global_options = self.parse_pdf_global(config[key])
            elif key == 'template':
                # TODO: why not move code above in here?
                pass
            else:
                dgen_utils.log_warn("Unrecognised option: " + key)
        return self.doc

    def parse_template(self, template_conf):
        return self.parse_string(template_conf)

    def parse_files(self, files_conf):
        '''
        Parse files_conf and return the result
        '''
        return self.parse_list(files_conf)

    def parse_file(self, file_conf):
        return self.parse_string(file_conf)

    def parse_string(self, string_conf):
        if isinstance(string_conf, str):
            return dgen_utils.replace_symbols_in_str(string_conf, self.doc)
        else:
            dgen_utils.log_warn("parse_string: could not parse as string: ", string_conf)
            return ""

    def parse_list(self, list_conf):
        if isinstance(list_conf, str):
            return [self.parse_string(list_conf)]
        elif isinstance(list_conf, list):
            result = []
            for string in list_conf:
                result = result + [self.parse_string(string)]
            return result
        else:
            dgen_utils.log_warn("parse_list: expected string or list, got: ", list_conf)
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
            dgen_utils.log_warn("Sections must be a list")
        return sections

    def parse_section(self, section_conf):
        section = dgenSection()
        if not isinstance(section_conf, dict):
            dgen_utils.log_warn("Section is not a dict")
            return
        for key in section_conf:
            section.doc_type = key
            conf_item = section_conf[key]
            if isinstance(conf_item, str):
                section.files = self.parse_list(conf_item)
            elif isinstance(conf_item, dict):
                if 'files' in conf_item:
                    section.files = self.parse_files(conf_item['files'])
                if 'html_options' in conf_item:
                    section.html_options = self.parse_html_options(conf_item['html_options'])
                if 'pdf_options' in conf_item:
                    section.pdf_options = self.parse_pdf_options(conf_item['pdf_options'])
        return section

    def parse_html_options(self, html_options_conf):
        return self.parse_list(html_options_conf)

    def parse_pdf_options(self, pdf_options_conf):
        return self.parse_list(pdf_options_conf)

    def parse_pdf_global(self, pdf_global_conf):
        pdf_global_options = dgenPDFConfig()
        pdf_global_options.pdf_options = self.parse_pdf_options(pdf_global_conf['pdf_options'])
        return pdf_global_options

    def parse_html_global(self, html_global_conf):
        html_global_options = dgenHTMLConfig()
        html_global_options.filters = self.parse_filters(html_global_conf['pandoc_filters'])
        html_global_options.files = self.parse_files(html_global_conf['files'])
        html_global_options.html_options = self.parse_html_options(html_global_conf['html_options'])
        return html_global_options

    def parse_filters(self, filters):
        return self.parse_list(filters)

class dgenHTMLConfig(object):
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


class dgenPDFConfig(object):
    def __init__(self):
        self.__pdf_options = []

    @property
    def pdf_options(self):
        return self.__pdf_options

    @pdf_options.setter
    def pdf_options(self, value):
        self.__pdf_options = value

class dgenSection(dgenHTMLConfig, dgenPDFConfig):
    '''
    A dgen section
    '''
    def __init__(self):
        dgenHTMLConfig.__init__(self)
        dgenPDFConfig.__init__(self)
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

class dgenDocument(object):
    '''
    A dgen document
    '''

    @property
    def template(self):
        return self.__template

    @template.setter
    def template(self, value):
        self.__template = value

    @property
    def repo_root(self):
        return dgen_utils.get_repo_root()

    @property
    def template_dir(self):
        return os.path.join(dgen_utils.get_repo_root(), self.__template)

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

    def __init__(self, local_config):
        '''
        Create a new document from the supplied configs
        '''

        self.__sections = []
        self.__pdf_filename = ''
        self.__html_global_options = dgenHTMLConfig()
        self.__pdf_global_options = dgenPDFConfig()
        self.__template = ''
        self.__template_dir = ''

        loader = dgenLoader()
        loader.doc = self

        local_config = dgen_utils.load_config(local_config)
        loader.parse_config(local_config)

        template_config = os.path.join(self.template_dir, 'template_config.yaml')
        template_config = dgen_utils.load_config(template_config)
        loader.parse_config(template_config)

class dgenHTMLGenerator(object):

    def __init__(self):
        '''
        Setup the current folder for HTML generation.
        '''
        self.__doc = None
        self.__html_dir = ''

    @property
    def doc(self):
        return self.__doc

    @doc.setter
    def doc(self, value):
        self.__doc = value

    @property
    def html_dir(self):
        if self.__html_dir == '':
            cwd = os.getcwd()
            self.__html_dir = os.path.join(cwd, 'html')
            # Delete the html folder if it exists
            dgen_utils.delete_folder(self.__html_dir)
            # Copy the template html folder
            src = os.path.join(cwd, self.__doc.template_dir, 'html')
            dgen_utils.copy_files(src, self.__html_dir)
            # Copy other files to the HTML dir for referencing
            for item in [p for p in glob.glob('*') if not (p.endswith('.md') 
                                                        or p.endswith('.yaml')
                                                        or p == 'html')]:
                src = os.path.join(cwd, item)
                dst =  os.path.join(self.html_dir, item)
                dgen_utils.copy_files(src, dst)
            # replace ${html_dir} in all files
            for root, _, files in os.walk('html', topdown=False):
                for name in files:
                    dgen_utils.replace_html_dir_symbol_in_file(os.path.join(root, name))
        return self.__html_dir

    def generate_html_section(self, section, html_global_opts):
        '''
        Generate HTML for the section described by config.
        '''
        if section.doc_type == 'toc':
            return
        files = html_global_opts.files + section.files
        # Build the output filename taking the last name from the list of files
        output_file = os.path.join(self.html_dir, section.html_file)
        # Open each file in turn and concatenate together
        contents = '\n'
        for path in files:
            if os.path.isfile(path):
                with  open(path, 'r', encoding='utf-8') as f:
                    contents = contents + f.read() + '\n\n'
            else:
                dgen_utils.log_warn('File does not exist: ' + path)
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

class dgenPDFGenerator(object):

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
        cmd = cmd + [doc.pdf_filename]
        cmd = ' '.join(cmd)
        print('cmd=' + cmd)
        subprocess.call(cmd, shell=True, cwd=dgen_utils.get_html_dir())
