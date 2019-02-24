#!/usr/bin/env python

"""
Pandoc filter to allow interpolation of metadata fields
into a document.  %{fields} will be replaced by the field's
value.
"""

import re, codecs, sys, urllib2
from collections import OrderedDict

# disable annoying warning from click caused by panflute. An upgrade to python 3 might fix
import click
click.disable_unicode_literals_warning = True
import panflute
from panflute import Link, Str


import dgen_utils

#import ptvsd
# 5678 is the default attach port in the VS Code debug configurations
#print("Waiting for debugger attach")
#ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
#ptvsd.wait_for_attach()
#breakpoint()

PATTERN = None
PATTERN_BAD = None

def init_metavars(doc):
    global PATTERN, PATTERN_BAD
    PATTERN = re.compile(r'(.*)%{(.*?)}(.*)')
    PATTERN_BAD = re.compile(r'(\${.*?})')

def check_str(elem, document):
    text = urllib2.unquote(elem.text)

    for match in PATTERN.finditer(text):
        #dgen_utils.log_warn(':'.join([str(elem.parent),elem.text, text, match.group(1), match.group(2), match.group(3)]))
        field = match.group(2)
        result = document.get_metadata(field, None)
        if isinstance(result, unicode):
            return Str(match.group(1) + result + match.group(3))
        dgen_utils.log_warn("metavar not found in document:", field)
    match_bad = PATTERN_BAD.match(text)
    if match_bad:
        dgen_utils.log_warn("found wrong syntax for metavar:", match_bad.group(1))
    return None

def filter(elem, document):
    if type(elem) == Str:
        return check_str(elem, document)
    if type(elem) == Link:
        #dgen_utils.log_warn("Link elemement found:", elem)
        pass
    return None

def finalize(doc):
    pass

def main(doc=None):
    input_stream=codecs.getreader('utf8')(sys.stdin)
    return panflute.run_filter(filter, prepare=init_metavars, finalize=finalize, doc=doc, input_stream=input_stream)

if __name__ == '__main__':
    main()
