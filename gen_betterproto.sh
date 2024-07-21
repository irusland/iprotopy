#!/bin/sh

PROJECT_ROOT=$(pwd)
PROTO_INCLUDE_PATH=$PROJECT_ROOT/tinkoff/invest/grpc
GOOGLE_API_PATH=$PROJECT_ROOT/tinkoff/invest/grpc/google/api
MODELS_PATH=$PROJECT_ROOT/betterproto_models

mkdir $MODELS_PATH

python -m grpc_tools.protoc --proto_path=$PROJECT_ROOT \
    --python_betterproto_out=$MODELS_PATH \
    $PROTO_INCLUDE_PATH/*.proto
