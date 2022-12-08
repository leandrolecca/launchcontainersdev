.PHONY: all lint

all_tests: lint unittest integrationtest

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  lint			to run flake8 on all Python files"
	@echo "  unittest		to run unit tests on rtp"
	@echo "  integrationtest		to run integration tests"

lint:
	@flake8 rtp

unittest:
	@py.test -m "not integration" --cov-append --cov-report xml --cov-report term-missing --cov=rtp rtp

performancetest:
	@py.test -m "integration" --cov-append --cov-report xml --cov-report term-missing --cov=rtp rtp
