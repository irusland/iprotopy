#!/bin/sh

PROJECT_ROOT=$(pwd)
PROTO_INCLUDE_PATH=$PROJECT_ROOT/tinkoff/invest/grpc
GOOGLE_API_PATH=$PROJECT_ROOT/tinkoff/invest/grpc/google/api

python -m grpc_tools.protoc --proto_path=$PROJECT_ROOT \
    --proto_path=$PROTO_INCLUDE_PATH \
    --proto_path=$GOOGLE_API_PATH \
    --python_betterproto_out=$PROJECT_ROOT/models \
    $PROTO_INCLUDE_PATH/instruments.proto 2> error.log
