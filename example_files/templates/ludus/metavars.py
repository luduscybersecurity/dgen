#!/usr/bin/python

"""
Pandoc filter to allow interpolation of metadata fields
into a document.  %{fields} will be replaced by the field's
value, assuming it is of the type MetaInlines or MetaString.
"""

from __future__ import print_function
from pandocfilters import toJSONFilter, attributes, Span, Str
import re
import sys

def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

pattern = re.compile('(.*)%\{(.*)\}(.*)')

def metavars(key, value, format, meta):
    if key == 'Str':
        m = pattern.match(value)
        if m:
            field = m.group(2)
            #eprint(value)
            result = meta.get(field, {})
            if result == {}:
                eprint("WARNING: Could not find match for meta variable %{" + field + "}")
                return
            if 'MetaInlines' in result['t']:
                return [Str(m.group(1))] + result['c'] + [Str(m.group(3))]
            elif 'MetaString' in result['t']:
                return [Str(m.group(1))] + result['c'] + [Str(m.group(3))]

if __name__ == "__main__":
    toJSONFilter(metavars)
