CODE = tests $(MAIN_CODE)
SOURCES = iprotopy/


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

.PHONY: publish
publish:
	poetry publish --build
