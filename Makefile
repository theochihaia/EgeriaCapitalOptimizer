setup:
	python3 -m venv venv

install:
	./venv/bin/pip install -r requirements.txt

test:
	./venv/bin/python -m unittest discover

clean:
	rm -rf venv
	find . -type f -name "*.pyc" -delete

.PHONY: setup install test clean
