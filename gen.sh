#!/bin/sh

# Set the absolute paths
PROJECT_ROOT=$(pwd)
PROTO_INCLUDE_PATH=$PROJECT_ROOT/tinkoff/invest/grpc
GOOGLE_API_PATH=$PROJECT_ROOT/tinkoff/invest/grpc/google/api

# Ensure the protoc-gen-python_betterproto plugin is available in PATH
#export PATH=$PATH:$(python -m site --user-base)/bin

# Run the protoc command with the correct paths
python -m grpc_tools.protoc --proto_path=$PROJECT_ROOT \
    --proto_path=$PROTO_INCLUDE_PATH \
    --proto_path=$GOOGLE_API_PATH \
    --python_betterproto_out=$PROJECT_ROOT/models \
    $PROTO_INCLUDE_PATH/instruments.proto 2> error.log

# Check if the generation was successful
if [ $? -ne 0 ]; then
    echo "Code generation failed. See error.log for details."
    cat error.log
else
    echo "Code generation succeeded."
fi
