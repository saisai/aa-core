.PHONY: build test benchmark typecheck typecheck-strict clean

build:
	poetry install

test:
	python -m pytest tests -v --cov=aa_core --cov=aa_datastore --cov=aa_transform --cov=aa_query

.coverage:
	make test

coverage_html: .coverage
	python -m coverage html -d coverage_html

benchmark:
	python -m aa_datastore.benchmark

typecheck:
	export MYPYPATH=./stubs; python -m mypy aa_core aa_datastore aa_transform aa_query --show-traceback --ignore-missing-imports --follow-imports=skip

typecheck-strict:
	export MYPYPATH=./stubs; python -m mypy aa_core aa_datastore aa_transform aa_query --strict-optional --check-untyped-defs; echo "Not a failing step"

lint:
	ruff check .

lint-fix:
	ruff check --fix .

format:
	ruff format .

clean:
	rm -rf build dist
	rm -rf aa_core/__pycache__ aa_datastore/__pycache__
