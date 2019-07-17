#!/usr/bin/env python

import dgen_utils

# disable annoying warning from click caused by panflute. An upgrade to python 3 might fix
import click
click.disable_unicode_literals_warning = True
from panflute import Link, Str, ListContainer, Code
import panflute

import re
import codecs
import sys
import urllib2

PATTERN = None
PATTERN_BAD = None


def init_metavars(doc):
    global PATTERN, PATTERN_BAD
    PATTERN = re.compile(r'(.*)%{(.*?)}(.*)')
    PATTERN_BAD = re.compile(r'(\${.*?})')


def filter_text(text, document):
    text = urllib2.unquote(text)
    for match in PATTERN.finditer(text):
        field = match.group(2)
        result = document.get_metadata(field, None)
        if isinstance(result, unicode):
            return match.group(1) + result + match.group(3)
        dgen_utils.log_warn("metavar not found in document:", field)
    match_bad = PATTERN_BAD.match(text)
    if match_bad:
        dgen_utils.log_warn(
            "found wrong syntax for metavar:", match_bad.group(1))
    return text


def filter_code(elem, document):
    return elem


def filter_str(elem, document):
    return Str(filter_text(elem.text, document))


def filter_link(elem, document):
    for item in elem.content:
        item = filter(item, document)
    elem.url = filter_text(elem.url, document)
    elem.title = filter_text(elem.title, document)
    return elem


def filter(elem, document):
    if type(elem) == Str:
        return filter_str(elem, document)
    if type(elem) == Link:
        return filter_link(elem, document)
    if type(elem) == Code:
        return filter_code(elem, document)
    return None


def finalize(doc):
    pass


def main(doc=None):
    input_stream = codecs.getreader('utf8')(sys.stdin)
    return panflute.run_filter(filter, prepare=init_metavars, finalize=finalize, doc=doc, input_stream=input_stream)


if __name__ == '__main__':
    main()
