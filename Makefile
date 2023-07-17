PYTHONFILES = $(shell find -name "*.py" -not -path "./.git/*")

.PHONY: pylint format check check-format check-pylint check-mypy

check-pylint:
	pylint -j 0 $(PYTHONFILES) || ./tools/check-pylint $$?

format:
	yapf -i $(PYTHONFILES)

check-format:
	yapf -d $(PYTHONFILES)

check-mypy:
	mypy --ignore-missing-imports $(PYTHONFILES)

check: check-pylint check-format check-mypy
