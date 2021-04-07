# Flask API Auto-documentation

A Python module to generate a page documenting the API of a Flask application.

## Installation

pip install flask-audo-doc

## Usage

```
import flask
from flask_api_autodoc.view import render_page

app = flask.Flask('demo')
app.route('/info')(render_something)
app.route('/api/this')(render_something)
app.route('/api/that')(render_something)

@app.route('/doc')
def _():
  return render_page(path_prefixes=['/api'])
```

## Support

Please [open an issue](https://github.com/lsiden/flask-api-autodoc/issues/new) for support.

## Contributing

Clone, edit, and submit pull requests.

## Dev Automation

- `make clean`
- `make test`
- `make tox`
- `make install-local`
- `make build`

## Author

Lawrence Siden
<br>Westside Consulting LLC
<br>Ann Arbor, MI  USA
<br>lsiden@gmail.com

## License

MIT
