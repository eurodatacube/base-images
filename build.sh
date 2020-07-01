#!/bin/bash

set -eux -o pipefail

BASE_IMAGE_VERSION=0.18.4
CORE_KERNEL_VERSION=0.0.1

BASE_IMAGE=eurodatacube/jupyter-user-base
GPU_BASE_IMAGE=eurodatacube/jupyter-user-base-g

docker build . \
    --file Dockerfile-jupyter-user-base \
    --cache-from ${BASE_IMAGE} \
    --cache-from ${BASE_IMAGE}:${BASE_IMAGE_VERSION} \
    -t ${BASE_IMAGE}:${BASE_IMAGE_VERSION}


# TODO: GPU BUILD

CORE_TAG=${BASE_IMAGE_VERSION}_core-${CORE_KERNEL_VERSION}
docker build . \
    --file Dockerfile-jupyter-user-modular-semidumb \
    --cache-from eurodatacube/jupyter-user \
    --cache-from eurodatacube/jupyter-user:${CORE_TAG} \
    --build-arg BASE_IMAGE_VERSION=${BASE_IMAGE_VERSION} \
    --build-arg KERNEL_VERSION=${CORE_KERNEL_VERSION} \
    -t eurodatacube/jupyter-user:${CORE_TAG}


