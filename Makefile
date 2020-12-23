PROJ_SLUG = hdash
CLI_NAME = hdash
PY_VERSION = 3.8
LINTER = flake8
FORMATTER = black

check: format lint test

freeze:
	pip freeze > requirements.txt

lint:
	$(LINTER) $(PROJ_SLUG)
	$(LINTER) tests

format:
	$(FORMATTER) $(PROJ_SLUG)
	$(FORMATTER) tests

qtest:
	py.test -s tests/

test:
	py.test -s --cov-report term --cov=$(PROJ_SLUG) tests/

coverage:
	py.test --cov-report html --cov=$(PROJ_SLUG) tests/

clean:
	rm -rf dist \
	rm -rf docs/build \
	rm -rf *.egg-info
	coverage erase
