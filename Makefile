.PHONY: style

check_dirs := arrow CParser

style:
	ruff check --fix $(check_dirs) setup.py
	ruff format $(check_dirs) setup.py
