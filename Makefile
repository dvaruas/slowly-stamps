.PHONY: setup
setup:
	python3 -m venv venv

.PHONY: install
install:
	./venv/bin/pip3 install -r myapp/requirements.txt

.PHONY: run
run:
	./venv/bin/python3 myapp/wsgi.py
