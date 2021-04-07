git_clean := "git clean -xd -e .envrc"

clean-dryrun:
	echo "$(git_clean) -n" | sh

can_clean: clean-dryrun
	echo -n "Proceed? [y/N] " && read ans && [ $${ans:-N} == y ]

clean: can_clean
	echo "$(git_clean) -f" | sh

dist:
	pip install build
	python -m build

test:
	pytest

# https://tox.readthedocs.io/en/latest/
tox:
	tox

install-local:
	pip install --editable .
