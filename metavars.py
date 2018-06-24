#!/usr/bin/env python

"""
Pandoc filter to allow interpolation of metadata fields
into a document.  %{fields} will be replaced by the field's
value.
"""

import re, codecs, sys
from collections import OrderedDict

import panflute
from panflute import Span, Str, MetaInlines

import dgen_utils

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
        dgen_utils.log_warn('match on element classes in metadata found but no matching keys\nelem: %s\nmatch:%s' % (elem, result))
    return None

def metavars(elem, document):
    for match in PATTERN.finditer(elem.text):
        field = match.group(2)
        result = document.get_metadata(field, None)
        if type(result) == MetaInlines:
            result = Span(*result.content, classes=['interpolated'], attributes={'field': field})
            return Span(Str(match.group(1)), result, Str(match.group(3)), classes=['interpolated'])
        elif isinstance(result, unicode):
            return Str(match.group(1) + result + match.group(3))
        dgen_utils.log_warn("metavar not found in document:", field)
    match_bad = PATTERN_BAD.match(elem.text)
    if match_bad:
        dgen_utils.log_warn("found wrong syntax for metavar:", match_bad.group(1))
    return None

def filter(elem, document):
    if type(elem) == Str:
        return metavars(elem, document)
    elif type(elem) == Span:
        return formatted_metavars(elem, document)
    return None

def finalize(doc):
    pass

def main(doc=None):
    input_stream=codecs.getreader('utf8')(sys.stdin)
    return panflute.run_filter(filter, prepare=init_metavars, finalize=finalize, doc=doc, input_stream=input_stream)

if __name__ == '__main__':
    main()
