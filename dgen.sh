#!/bin/bash

TEMPLATE_MOUNT=""
if [ $DGEN_TEMPLATES_ROOT ]
then
    TEMPLATE_MOUNT="--mount type=bind,source=$DGEN_TEMPLATES_ROOT,target=$DGEN_TEMPLATES_ROOT"
fi

docker run --mount type=bind,source="$(pwd)",target=/project $TEMPLATE_MOUNT\
    --mount type=bind,source=$HOME/.ssh,target=$HOME/.ssh,readonly\
    --mount type=bind,source=/etc/passwd,target=/etc/passwd,readonly\
    --user $(id -u):$(id -g) --rm -it dgen:latest /app/dgen.py "${@:1}"
