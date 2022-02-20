install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=lib test_api.py

format:
	black *.py

lint:
	pylint --disable=R,C,E1120 dcli.py lib/Joke_api.py

all: install lint test