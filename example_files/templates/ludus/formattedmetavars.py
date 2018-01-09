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

def eprint(*args, **kwargs):
            print(*args, file=sys.stderr, **kwargs)

path = os.path.dirname(__file__)
with open(os.path.join(path, 'formattedmetadata.yaml'), 'r') as f:
        doc = yaml.safe_load(f)
pattern = re.compile('(.*)%\{(.*)\}(.*)')


def metavarformat(key, value, format, meta):
    if key == 'Str':
        m = pattern.match(value)
        if m:
            field = m.group(2)
            result = meta.get(field, {})
            format_variable = doc.get(field, {})
            if result == {} or format_variable == {}:
                return            
            elif 'MetaInlines' in result['t']:
                format_key = result['c'][0]['c']
                format_class = format_variable.get(format_key.lower(), {})
                if format_class == {}:
                    eprint("WARNING: Could not find match in format variable. \n\tKey:", format_key, "\n\tVariable: ", format_variable)
                    return
                return Span(attributes({'class': format_class}), [Str(m.group(1))] + result['c']  + [Str(m.group(3))])
            elif 'MetaString' in result['t']:
                format_key = result['c']
                eprint("WARNING: MetaString encountered. Can not do formatted substitution on:", value, " \n\tKey:", format_key, "\n\tVariable: ", format_variable)
                return [Str(m.group(1))] + Str(result['c']  + [Str(m.group(3))])
if __name__ == "__main__":
    toJSONFilter(metavarformat)
