'''Formats docstring for output'''

import re
from functools import reduce

def format_as_html(doc):
    """Returns doc formatted as HTML.

    Removes leading indentation based on first non-blank line after initial line.

    Substitutions:
        _name_ ==> <i>name</i>
        *name* ==> <b>name</b>
        **name** ==> <code>name</code>
    """
    if not doc:
        return ''

    leading_indent = _get_leading_indent(doc)
    return '<br>'.join(map(
        lambda line: _format_line_as_html(line, leading_indent), doc.splitlines()))


def _format_line_as_html(line, leading_indent):
    line = _trim_leading_indent(line.rstrip(), leading_indent)
    line = re.sub(r'\t| {4}', 4*r'&nbsp;', line)
    line = re.sub(r'__([^_]+)__', r'<i>\1</i>', line)
    line = re.sub(r'\*\*([^*]+)\*\*', r'<code>\1</code>', line)
    line = re.sub(r'\*([^*]+)\*', r'<b>\1</b>', line)
    return line


def _get_leading_indent(docstring):
    for line in filter(lambda l: re.search(r'\S', l), docstring.splitlines()[1:]):
        return _get_line_leading_indent(line)

    return 0


def _get_line_leading_indent(line):
    matched = re.match(r'[ \t]*', line)
    return reduce(
        lambda val, tup: val + (4 if tup[1] == '\t' else 1), enumerate(matched.group(0)), 0)


def _trim_leading_indent(line, indent):
    indent0 = min(indent, _get_line_leading_indent(line))
    return line.expandtabs(tabsize=4)[indent0:]
