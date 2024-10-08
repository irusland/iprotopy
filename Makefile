CODE = tests $(MAIN_CODE)
SOURCES = protopy/


.PHONY: install
install:
	pre-commit install


.PHONY: format
format:
	ruff format $(SOURCES)
	ruff check --fix $(SOURCES)
	ruff check --select I --fix $(SOURCES)
	ruff format $(SOURCES)
	pyprojectsort

.PHONY: lint
lint:
	ruff $(SOURCES)
