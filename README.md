# dgen

TODO: this needs an update.

dgen (document generation for degenerates) is a text based document generation tool by pentesters for pentesters.

Documents are written in markdown and converted to a format for presentation using pandoc. dgen supports:

* reports in html/pdf using wkhtmltopdf
* presentations using reveal.js

The design principals for dgen are:

* leverage existing tools as much as possible (git, pandoc and so forth)
* encourage people to use their own text editors and work-flows with the platform
* provide for modular reports and encourage re-use of IP

# Setup

Each dgen project is a series of markdown files and yaml configs that say how the markdown stitches together.

## Global config

A global_config.yaml file is loaded from the same directory as dgen. It can be used to load options that will persist across all projects. Any attribute in the project config can be loaded into the global config, with the project config taking precedence.

## Project config

Each project is self contained within a folder, and may reference templates located in another folder elsewhere on the filesystem. The project should have its own config.yaml in the base of the project directory which can include:

* document: defines the structure of the document (described below)
* filename: the filename of generated documents (an extension is appended automatically)
* template_root: a base folder that contains all dgen templates
* template: the template to use (will be a folder found under the template_root). All material for the template must be contained in this folder.
* template_conf: the project template configuration
* revealjs_dir: the location of a reveal.js installation for serving slideshows over HTTP

The document item is a yaml list (of sections) that can be either a:

* cover page (title page), toc (table of contents), or page (main content): each type is supplied it's corresponding object type to wkhtmltopdf (see the man page).
* each section has a name that determines it's filename when it is converted into html
* each section has a list of contents that contain the markdown that section. In order to work with pandoc all yaml files and inline metadata must start with --- and end with ...

The document item may also define it's own template_conf, which is identical to the structure of the main template_conf and takes precedence.

## Templates

Templates specifies secondary config required for the presentation of documents. Each template is structed as a collection of template configurations HTML and CSS needed to build a document. Additional HTML content (such as images for headers, footers or the title page) must be stored in a subdirectory called 'html' so they can be easily referenced during the HTML generation process. Example uses for the template feature are:
    * different templates for different letterheads. useful if you're whitelabling reports
    * different templates for different kinds of documents (e.g. a pdf report vs a slide show)

Templates can have the following attributes:

* pandoc_options: a list of options to provide to pandoc. See the pandoc man page for more info.
* wkhtmltopdf_options: arguments to send to wkhtmltopdf. See the wkhtmltopdf man page for further details.
* metadata: a list of files to add onto the contents of a page during HTML generation (typically just yaml metadata)

# Generating a document

When generating a document the following activities happen:

* the project is initialised and all configurations loaded.
* dgen stores a copy of the specified template in the project folder if it doesn't already exist, or a refresh is specified on the command line
* dgen uses the local copy of the template to construct a folder in which the HTML documentation is generated. if the local HTML folder exists, it is deleted prior to copy
* all files that aren't known by pandoc (.md, yaml, local template) are copied into the local HTML directory
* for each document section, a separate pandoc command is run, creating a separate html file inside the local HTML directory
* variable substitution inside command options and the local HTML folder occurs at this point
* the default template and example documents includes some pandoc filters to do variable substitution and enforce pagebreaks. they use the panflute python library, which is easy to use. 
* when generating a pdf, dgen prepares the command for wkhtmltopdf. variable substitution inside the command happens at this point
* when generating a slideshow, dgen copies the generated html to the configured revealjs_dir. reveal_js can be run from the destination folder


## Variable substitution

dgen can perform variable substitution in both its configs and content. A variable is delimited by %{var}. Structured variables are supported.

dgen is smart enough to replace the following variables when preparing to generate a document:

```python
                symbols = {'pdf_filename': project.pdf_filename, # the defined filename with a .pdf extension
                          'bin_dir': project.bin_dir, # the directory of the dgen script
                          'template_dir': project.local_template_dir, # the directory of the projects local template
                          'html_dir': project.html_dir} # the directory of the project's local html directory
```

Standard symbols that reference the home folder or environment variables are also supported (e.g. ~, %HOME%, etc.).

During HTML generation dgen will loop through the entire document and substitute any variables found in yaml metadata. This can be included either inside a dedicated yaml file, or inline with markdown content. dgen supports nested variables, e.g.

```markdown
---
v_dflt_pw:
    name: Default passwords
    rating: High
    num_treatments: 2
    status: Untested
...

## %{v_dflt_pw.name}{.finding}
```

## Page breaks

dgen will attempt to force a pagebreak when generating a pdf where-ever it sees the string `%pagebreak` in it's own paragraph:

```

%pagebreak

```


## Look and feel

Formatting is done using html and css and is intended to be mostly configured through templates. Ensure you include the required css inside the html templates you use. You can enforce non-standard styles through use of div tags and css classes in the markdown content, or you can write your own pandoc filters.

## Change control

Each project can be put into its own git repository. This way you'll get full change history and colaboration is easier.

## Dependencies

dgen requires:

* python 2.7. 
* the following non-core python packages:
    * pyyaml
    * panflute
* pandoc on your path
* wkhtmltopdf on your path for pdf reports (it must be the qt version to generate a table of contents)
* a folder with reveal.js for slide shows

## OS Support

It should work on any OS but I've only tested MacOS and Linux (Fedora).

## Recommended folder structure

* a git repository for each project
* a git repository for your templates, e.g.
    * dgen templates
    * document templates
    * finding libraries
* a folder for dgen executables, which should be on your path

# Future work

* python3 support
