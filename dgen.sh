#!/bin/bash
# An example shell script to run dgen inside docker

TEMPLATE_MOUNT=""
if [ $DGEN_TEMPLATES_ROOT ]
then
    TEMPLATE_MOUNT="--mount type=bind,source=${DGEN_TEMPLATES_ROOT},target=${DGEN_TEMPLATES_ROOT}"
fi

SCRIPT="groupadd -g $(id -g) ${USER} && useradd -u $(id -u) -g $(id -g) -M -d ${HOME} -l ${USER} && su -c '/app/dgen.py ${@:1}' ${USER}"

docker run --mount type=bind,source="$(pwd)",target=/project $TEMPLATE_MOUNT \
    --mount type=bind,source=$HOME/.gitconfig,target=$HOME/.gitconfig,readonly \
    --mount type=bind,source=$HOME/.git-credentials,target=$HOME/.git-credentials,readonly \
    --mount type=bind,source=$HOME/.dgen,target=$HOME/.dgen \
    --mount type=bind,source=$HOME/.ssh,target=$HOME/.ssh,readonly \
    --rm -it dgen:latest /bin/bash -c "${SCRIPT}"
