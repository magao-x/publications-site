all: pyenv
	pyenv/bin/python -m pip install -r ./requirements.txt
	pyenv/bin/python generate_from_ads.py

pyenv:
	python -m venv pyenv

.PHONY: all