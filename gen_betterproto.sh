#!/bin/sh

PROJECT_ROOT=$(pwd)
PROTO_INCLUDE_PATH=$PROJECT_ROOT/tinkoff/invest/grpc
GOOGLE_API_PATH=$PROJECT_ROOT/tinkoff/invest/grpc/google/api

mkdir models

python -m grpc_tools.protoc --proto_path=$PROJECT_ROOT \
    --python_betterproto_out=$PROJECT_ROOT/models \
    $PROTO_INCLUDE_PATH/instruments.proto
