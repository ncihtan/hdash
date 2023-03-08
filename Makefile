PROJ_SLUG = hdash
CLI_NAME = hdash
PY_VERSION = 3.8
LINTER = flake8
FORMATTER = black

check: format lint test

prepare:
	mkdir -p deploy
	mkdir -p deploy/images

freeze:
	pip freeze > requirements.txt

lint:
	$(LINTER) $(PROJ_SLUG)
	$(LINTER) tests

format:
	$(FORMATTER) $(PROJ_SLUG)
	$(FORMATTER) tests

qtest:  prepare
	py.test -s tests/

test:   prepare
	py.test -s --cov-report term --cov=$(PROJ_SLUG) tests/

coverage:
	py.test --cov-report html --cov=$(PROJ_SLUG) tests/

clean:
	rm -rf deploy
	rm -rf *.egg-info
