#!/bin/sh

PROTO_INCLUDE_PATH=$1
MODELS_PATH=$2

if [ -z "$PROTO_INCLUDE_PATH" ] || [ -z "$MODELS_PATH" ]; then
    echo "Usage: gen_mypy.sh <proto_include_path> <models_output_path>"
    exit 1
fi

PROJECT_ROOT=$(pwd)

mkdir -p $MODELS_PATH

PROTO_FILES=$(find $PROTO_INCLUDE_PATH -name "*.proto")

python -m grpc_tools.protoc \
    --proto_path=$PROJECT_ROOT \
    --mypy_out=$MODELS_PATH \
    --python_out=$MODELS_PATH \
    --grpc_python_out=$MODELS_PATH \
    $PROTO_FILES
