# Repo notes/requirements

A dgen repo has several sub-repos, some with special meaning.

* stencils, for storing markdown fragments
* templates, for storing
  * standard markdown structure (*.md, *.yaml in example dir), and a document config (config.yaml)
  * document templates (contents of example/.dgen, and a template config (example/.dgen/template_config.yaml)
* projects, for storing project data
  * projects organised in hierarchy. two types:
    * reports - contains a report. built from
    * folders

Generally the contents of each will be a policy thing (e.g. nothing to enforce particular contents in particular folders), but it will affect other functions (creating a document from a config, searching stencils for example findings)

All repos must support change control (git I guess)

Changes to projects folder must be done in isolation (i.e. you can pull/clone just one folder/report)

When you create a report (implemented by the application):

* create a sub-repo
* copy a template (markdown, html and configs)
  * make a copy so that changes to the original template don't affect this document
* commit?

A repo is implemented as a git repo.

The master branch is the template, a seperate branch is created for each document.

The template consists of:
- Default Markdown content
- A config.yaml
- 