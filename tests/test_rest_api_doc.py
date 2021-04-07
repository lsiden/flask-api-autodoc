"""Tests index HTML view."""

import logging
import re
import flask

from flask_api_autodoc.view import render_page

LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)


def render_something():
    return 'Lorem ipsum dolor sit amet.'


def test_rest_api_doc_1():
    app = flask.Flask('test')
    app.route('/')(render_page)
    app.route('/something')(render_something)

    with app.test_client() as client:
        res = client.get('/')

    assert res.status_code == 200
    assert re.match(r'text/html', res.headers['Content-type'])

    content = res.data.decode('utf-8')
    assert re.match('<!DOCTYPE html>', content)
    assert re.search(r'<div class="url">/something</div>', content)


def test_rest_api_doc_with_filter_2():
    app = flask.Flask('test')
    app.route('/info')(render_something)
    app.route('/api/this')(render_something)
    app.route('/api/that')(render_something)

    @app.route('/doc')
    def _():
        return render_page(path_prefixes=['/api'])

    with app.test_client() as client:
        res = client.get('/doc')

        assert res.status_code == 200
        assert re.match(r'text/html', res.headers['Content-type'])

        content = res.data.decode('utf-8')
        # LOGGER.debug(content)
        assert re.search(r'<div class="url">/api/this</div>', content)
        assert re.search(r'<div class="url">/api/that</div>', content)
        assert not re.search(r'<div class="url">/doc</div>', content)
        assert not re.search(r'<div class="url">/info</div>', content)


def test_rest_api_doc_with_template_3():
    template = 'It works'
    app = flask.Flask('test')

    @app.route('/')
    def _():
        return render_page(template)

    with app.test_client() as client:
        res = client.get('/')

    assert res.status_code == 200
    assert res.data == template.encode('utf-8')
