#!/bin/bash

TEMPLATE_MOUNT=""
if [ $DGEN_TEMPLATES_ROOT ]
then
    TEMPLATE_MOUNT="--mount type=bind,source=$DGEN_TEMPLATES_ROOT,target=$DGEN_TEMPLATES_ROOT"
fi

docker run --mount type=bind,source="$(pwd)",target=/project $TEMPLATE_MOUNT\
    --user $(id -u):$(id -g) -it dgen:latest /app/dgen.py "${@:1}"
    