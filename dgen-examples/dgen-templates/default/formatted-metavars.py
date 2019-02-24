#!/usr/bin/env python

"""
Pandoc filter to allow interpolation of metadata fields
into a document.  %{fields} will be replaced by the field's
value.
"""

import re, codecs, sys, logging
from collections import OrderedDict

# disable annoying warning from click caused by panflute. An upgrade to python 3 might fix
import click
click.disable_unicode_literals_warning = True
import panflute
from panflute import Span, Str


LOG_LEVEL= logging.WARNING
PATTERN = None
PATTERN_BAD = None

def init_metavars(doc):
    global PATTERN, PATTERN_BAD
    PATTERN = re.compile(r'(.*)%{(.*?)}(.*)')
    PATTERN_BAD = re.compile(r'(\${.*?})')

def formatted_metavars(elem, document):
    classes = []
    result = None
    # loop through all element classes and look for a matching metadata attribute
    for field in elem.classes:
        result = document.get_metadata(field)
        # check the match is a dictionary and then loop through the elements content looking for
        # a key in the dictionary (case insensitive)
        if isinstance(result, OrderedDict):
            for string in elem.content:
                if type(string) == Str:
                    for key, value in result.items():
                        if key.lower() == string.text.lower():
                            classes = classes + [value]
    if classes != []:
        # update the original element with any matches
        elem.classes = elem.classes + classes
        return elem
    if result != None:
        logging.warning('match on element classes in metadata found but no matching keys\nelem: %s\nmatch:%s' % (elem, result))
    return None

def filter(elem, document):
    if type(elem) == Span:
        return formatted_metavars(elem, document)
    return None

def finalize(doc):
    pass

def main(doc=None):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=LOG_LEVEL)
    input_stream=codecs.getreader('utf8')(sys.stdin)
    
    return panflute.run_filter(filter, prepare=init_metavars, finalize=finalize, doc=doc, input_stream=input_stream)

if __name__ == '__main__':
    main()
