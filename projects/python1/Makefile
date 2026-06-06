
.PHONY: venv install build wheel test lint docker-build

venv:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip

install:
	. .venv/bin/activate && pip install -e .[dev]

build:
	. .venv/bin/activate && python -m build

wheel:
	. .venv/bin/activate && python -m pip wheel --no-deps -w dist .

test:
	. .venv/bin/activate && pytest -q

lint:
	. .venv/bin/activate && ruff check src

docker-build:
	docker build -t kcsv:latest .
