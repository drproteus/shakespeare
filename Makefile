build:
	python main.py

.PHONY: clean
clean:
	rm -rf build/

.PHONY: setup
setup:
	pip install Jinja2

serve: build
	python -m http.server -d build/
