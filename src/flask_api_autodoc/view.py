'''spam-api web app'''

from pprint import pformat
import pkgutil
from functools import partial
import logging

from flask import render_template_string, current_app as app
from flask_api_autodoc import docstring

LOGGER = logging.getLogger(__name__)

#################
## Routes

def render_page(template=None, path_prefixes=None):
    """Returns HTML list of URLS and endpoints.

    Parameters:
        template - string; see template.html in this package
        path_prefixes - list; e.g. ['/foo', '/bar']
    """
    LOGGER.debug("template=%s", template)
    LOGGER.debug("path_prefixes=%s", path_prefixes)
    template = template or pkgutil.get_data(__package__, 'template.html').decode('utf-8')
    rules = app.url_map.iter_rules()

    if path_prefixes:
        rules = filter(partial(_matches_prefix, path_prefixes), rules)
        
    if path_exclusions:
        rules = filter(partial(_matches_exclusion, path_exclusions), rules)

    rules = sorted(rules, key=str)
    LOGGER.debug(pformat(rules))
    urls = [_make_url_templ_item(rule) for rule in rules]
    # LOGGER.debug(pformat(urls))
    return render_template_string(template, urls=urls)


############
## internals

def _matches_prefix(path_prefixes, rule):
    return any(map(lambda prefix: str(rule).startswith(prefix), path_prefixes))

def _matches_exclusion(path_exclusions, rule):
    return any(map(lambda prefix: str(rule).startswith(prefix) is False, path_exclusions))

def _make_url_templ_item(rule):
    """Returns dict for one item in index.html template.
    """
    return dict(
        path=str(rule).replace('<', '&lt;').replace('>', '&gt;'),
        py_method_signature=_render_py_method_signature(rule),
        http_methods=rule.methods,
        doc=docstring.format_as_html(app.view_functions[rule.endpoint].__doc__)
    )

def _render_py_method_signature(rule):
    """Returns route endpoint method name for rendering as HTML.
    """
    return ''.join([
        app.view_functions[rule.endpoint].__module__,
        '.',
        app.view_functions[rule.endpoint].__name__,
        '(',
        ', '.join(list(rule.arguments)),
        ')',
    ])
