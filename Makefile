git_clean := "git clean -xd -e .envrc"

.PHONY: dist

_clean-dryrun:
	echo "$(git_clean) -n" | sh

_can_clean: _clean-dryrun
	@echo -n "Proceed? [y/N] " && read ans && [ $${ans:-N} == y ]

clean: _can_clean
	echo "$(git_clean) -f" | sh

lint:
	pylint src/

test:
	pytest

coverage:
	# https://pytest-cov.readthedocs.io/en/latest/reporting.html
	pytest --cov-report term-missing --cov=flask_api_autodoc tests/

# https://tox.readthedocs.io/en/latest/
tox:
	tox

install:
	poetry install

install-local:
	pip install --editable .

dist: clean
	poetry build

publish-test:
	# poetry config repositories.test https://test.pypi.org/legacy
	poetry publish -r test

publish:
	poetry publish
