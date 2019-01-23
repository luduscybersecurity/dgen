#!/bin/bash


if [ -z "$DGEN_TEMPLATES_ROOT" ];
then
    echo "ERROR: must set environment variable DGEN_TEMPLATES_ROOT, e.g."
    echo "      export DGEN_TEMPLATES_ROOT=/path"
    exit 1
fi


docker run --mount type=bind,source="$(pwd)",target=/project \
    --mount type=bind,source=$DGEN_TEMPLATES_ROOT,target=/templates \
    -it dgen:latest /app/dgen "${@:1}"
