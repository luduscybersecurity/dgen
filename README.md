<<<<<<< HEAD
# yarg
yarg (yet another report generator) is a text based report generation tool by pentesters for pentesers (and pirates).
=======
# dgen
dgen (document generation for degenerates) is a text based document generation tool by pentesters for pentesters.

Documents are written in markdown and converted to a format for presentation using pandoc. dgen supports:

* reports in html/pdf using wkhtmltopdf
* presentations using reveal

The design principals for dgen are:

* leverage existing tools as much as possible (git, pandoc and so forth)
* encourage people use their own text editors and work-flows with the platform
* provide for modular reports and encourage re-use of IP

# Setup

Each dgen project is a series of markdown files and a yaml config that says how it stitches together.

## Project config

The project should have its own config.yaml, which will reference one or more documents (in an document_set). The documents will have a name (which is used to name the final filenames and directories) and contents, (which will be stitched together in the order they appear in the config). There are a number of other config items that can be used to drive the pandoc engine. In order to work with pandoc all yaml files must start with --- and end with ...

* template: this specifies secondary config required for the presentation of documents. The template file should include everything needed to build a document in the folder that contains it. Additional HTML content (such as images for headers, footers or the title page) should be stored in a subdirectory called 'html'. Example uses for the template feature are:
    * different templates for different letterheads. useful if you're whitelabling reports
    * different templates for different kinds of documents (e.g. a pdf report vs a slide show)
* pandoc_html_config: this specifies additional config items sent to pandoc when generating content. It can include the following sub items:
    * filters: a list of filters for pandoc. A filter to replace metavars has been included.
    * pandoc_options: a list of options to provide to pandoc. See the pandoc documentation for more info.
* wkhtmltopdf_config: this supplies config items to send to wkhtmltopdf and consists of a single key:
    * wkhtmltopdf_options: arguments to send to wkhtmltopdf. See the documentation for further details.

There is also a global_config.yaml with the dgen executables.

## Variable substitution

dgen can perform variable substitution in both its configs and content. A variable is delimited by %{var}.

dgen is smart enough to replace the following variables when preparing to generate a document:

```python
        symbols = {'bin_dir': project.bin_dir,
                   'template_dir': project.template_dir,
                   'html_dir': document.html_dir,
                   'html_filename': document.html_filename,
                   'pdf_filename': document.pdf_filename}
```

Hopefully their meaning is self explanatory. You can also use standard symbols that reference your home folder or environment variables (e.g. ~, %HOME%, etc.).

During generation dgen will loop through the entire document and substitute any variables found in yaml metadata. This can be included either inside a dedicated yaml file, or inline with markdown content. dgen supports nested variables, e.g.

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

## Look and feel

Formatting is done using html and css and is intended to be mostly configured through templates. Ensure you include the required css inside the html templates you use. You can enforce non-standard styles through use of div tags and css classes.

## Change control

Each project can be put into its own git repository.

### Recommended structure

* a git repository for each project
* a git repository for standard markdown files (e.g. finding libraries, standard documents)
* a git repository for your templates, e.g.
    * dgen templates
    * document templates
* a folder for dgen executables, which should be on your path

## Future work

* Enforce work-flows through git commits
* Operations on a remote repository:
    * copy a remote project
    * list remote projects
    * grep remote projects for text
* Auto order markdown files based on variable values
* Rules to allow operations on variables (e.g. counting instances of a nested variable's value)

# Dependencies

dgen requires:

* python 2.7. It might work with python 3, I haven't tried.
* the following non-core python packages:
    * pyyaml
    * pypandoc
* pandoc
* wkhtmltopdf for pdf reports
* reveal.js for slide shows
>>>>>>> eb63ac59d83e920f4bc9b01406d880e6b31b6c0a
