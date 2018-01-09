# dgen
dgen (yet another report generator) is a text based report generation tool by pentesters for pentesers (and pirates).

## TODO

* Pick a new name because this one shits me
* Write a check to ensure that variables haven't been left over after generating html
  * include %{} and ${}
* Add support for a section as keys rather than list, ie.

```
sections:
  cover:
      files: 'cover'
      html_options: 
          - '--template=%{template_dir}/template-title.html'
  toc: 
      pdf_options:
          - '--xsl-style-sheet toc.template.xsl'
  section: 
      files:
          - 'exec.md'
          - 'intro.md'
          - 'finding1.md'
          - 'finding2.md'
          - 'appendix.md'
```

* Add support to include config.yaml as an option for generation
* rename 'sections' config item to 'document'
* Add feature to allow the specification of a filename for each line item in a document.
* Ensure the parser dies if it encounters an unknown element, and says why and where in the file
* Bug when replacing numeric config item e.g.

```
    num_low = 4
vs
    num_low = "4"

    %{num_low}
```

* Bug when regenerating document, doesn't seem to update filename. Look at test plan for ColmanComms