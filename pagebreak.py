#!/usr/bin/env python

import dgen_utils

import re
import codecs
import sys
from collections import OrderedDict

# disable annoying warning from click caused by panflute. An upgrade to python 3 might fix
import click
click.disable_unicode_literals_warning = True

import panflute
from panflute import Para, Str, Div


PATTERN = None


def init_pagebreak(doc):
    global PATTERN
    PATTERN = re.compile(r'%pagebreak')


def check_pagebreak(elem, document):
    if type(elem) == Str and PATTERN.match(elem.text):
        return Div(classes=['pagebreak'])
    return None


def filter(elem, document):
    if type(elem) == Para and len(elem.content.list) == 1:
        return check_pagebreak(elem.content.list[0], document)
    return None


def finalize(doc):
    pass


def main(doc=None):
    input_stream = codecs.getreader('utf8')(sys.stdin)
    return panflute.run_filter(filter, prepare=init_pagebreak, finalize=finalize, doc=doc, input_stream=input_stream)


if __name__ == '__main__':
    main()
