#!/usr/bin/python

"""
Pandoc filter to allow interpolation of metadata fields
into a document.  %{fields} will be replaced by the field's
value, assuming it is of the type MetaInlines or MetaString.
"""
from __future__ import print_function
import re
import sys
import os
import traceback

import yaml
from pandocfilters import toJSONFilter, attributes, Span, Str

import dgen_utils

DOC = {}
PATTERN = None
PATTERN_BAD = None

def init_metavars():
    path = os.getcwd()

    path = os.path.dirname(__file__)
    path = os.path.join(path, 'formattedmetadata.yaml')
    global DOC, PATTERN, PATTERN_BAD
    if os.path.isfile(path):
        with open(path, 'r') as f:
            DOC = yaml.safe_load(f)
    PATTERN = re.compile(r'(.*?)%\{(.*?)\}(.*)')
    PATTERN_BAD = re.compile(r'.*?(\$\{.*?\}).*')

def format_string(variable, pandoc_string):
    format_variable = DOC.get(variable)
    if format_variable is not None:
        format_class = format_variable[pandoc_string[0]['c'].lower()]
        return Span(attributes({'class': format_class}), pandoc_string)
    return Str(pandoc_string)

def match_meta_var(string, prefix, postfix, meta):
    parts = string.split('.', 1)
    key = parts[0]
    subkey = ''
    if len(parts) > 1:
        subkey = parts[1]
    result = meta.get(key, {})
    
    if result == {}:
        return []
    elif 'MetaMap' in result['t']:
        return match_meta_var(subkey, prefix, postfix, result['c'])
    elif 'MetaInlines' in result['t']:
        formatted_string = format_string(parts[-1], result['c'])
        return [Str(prefix)] + [formatted_string] + [Str(postfix)]
    elif 'MetaString' in result['t']:
        formatted_string = format_string(parts[-1], result['c'])
        return [Str(prefix)] + [formatted_string] + [Str(postfix)]
    return[]    

def metavars(key, value, format, meta):
    if key == 'Str':
        match = PATTERN.match(value)
        if match:
            field = match.group(2)
            result = match_meta_var(match.group(2), match.group(1), match.group(3), meta)    
            if result == []:
                dgen_utils.log_warn("could not find match for metavar: %{" + field + "}")
            return result
        match_bad = PATTERN_BAD.match(value)
        if match_bad:
            dgen_utils.log_warn("found wrong syntax for metavar:", match_bad.group(1))


if __name__ == "__main__":
    init_metavars()
    toJSONFilter(metavars)
