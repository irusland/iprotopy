POETRY_RUN = poetry run

PROTO_DIR = protos/tinkoff/invest/grpc
PACKAGE_PROTO_DIR = tinkoff/invest/grpc
OUT = .
PROTOS = protos

TEST = $(POETRY_RUN) pytest $(args)
MAIN_CODE = tinkoff examples scripts
CODE = tests $(MAIN_CODE)

.PHONY: install
install:
	pre-commit install


.PHONY: grpc
grpc:
	#rm -r ${PACKAGE_PROTO_DIR}
	python -m grpc_tools.protoc -I${PROTOS} --python_out=${OUT} --pyi_out=${OUT} --grpc_python_out=${OUT} ${PROTO_DIR}/google/api/*.proto
	python -m grpc_tools.protoc -I${PROTOS} --python_out=${OUT} --pyi_out=${OUT} --grpc_python_out=${OUT} ${PROTO_DIR}/*.proto
	touch ${PACKAGE_PROTO_DIR}/__init__.py

.PHONY: format
format:
	ruff check --select I --fix src/
	ruff format src/

.PHONY: lint
lint:
	ruff src/
