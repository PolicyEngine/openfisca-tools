all: install test build
format:
	autopep8 . -r -i
	black . -l 79
test:
	pytest tests -vv
install:
	pip install -e .
build:
	python setup.py sdist bdist_wheel