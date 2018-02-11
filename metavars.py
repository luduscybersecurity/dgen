#!/usr/bin/env python

"""
Pandoc filter to allow interpolation of metadata fields
into a document.  %{fields} will be replaced by the field's
value.
"""

import re, codecs, sys

import panflute
from panflute import Span, Str, MetaInlines

import dgen_utils

PATTERN = None
PATTERN_BAD = None

def init_metavars(doc):
    global PATTERN, PATTERN_BAD
    PATTERN = re.compile(r'(.*)%{(.*?)}(.*)')
    PATTERN_BAD = re.compile(r'(\${.*?})')

def metavars(elem, document):
    if type(elem) == Str:
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

def finalize(doc):
    pass

def main(doc=None):
    input_stream=codecs.getreader('utf8')(sys.stdin)
    return panflute.run_filter(metavars, prepare=init_metavars, finalize=finalize, doc=doc, input_stream=input_stream)

if __name__ == '__main__':
    main()