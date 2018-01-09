#!/usr/bin/python

"""
Pandoc filter to allow interpolation of metadata fields
into a document.  %{fields} will be replaced by the field's
value, assuming it is of the type MetaInlines or MetaString.
"""
from __future__ import print_function
from pandocfilters import toJSONFilter, attributes, Span, Str
import re
import yaml
import sys
import os

path = os.path.dirname(__file__)
with open(os.path.join(path, 'formattedmetadata.yaml'), 'r') as f:
        doc = yaml.safe_load(f)
pattern = re.compile('(.*)%\{(.*)\}(.*)')

def eprint(*args, **kwargs):
    sys.stderr.write("metavars: ")
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()

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
        return [Str(prefix)] + formatted_string + [Str(postfix)]
    elif 'MetaString' in result['t']:
        formatted_string = format_string(parts[-1], result['c'])
        return [Str(prefix)] + formatted_string + [Str(postfix)]
    return[]

def format_string(variable, pandoc_string):
    format_variable = doc.get(variable)
    if format_variable is not None:
        format_class = format_variable[pandoc_string[0]['c'].lower()]
        return [Span(attributes({'class': format_class}), pandoc_string)]
    return pandoc_string
    

def metavars(key, value, format, meta):
    if key == 'Str':
        m = pattern.match(value)
        if m:
            field = m.group(2)
            result = match_meta_var(m.group(2), m.group(1), m.group(3), meta)    
            if result == [] and m.group(2) != "template_dir":
                eprint("Could not find match for meta variable %{" + field + "}")
            return result

if __name__ == "__main__":
    toJSONFilter(metavars)
