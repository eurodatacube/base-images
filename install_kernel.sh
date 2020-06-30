#!/bin/bash

set -eux -o pipefail

DEST_PATH=$1

conda env create --file base-environment.yaml --prefix "$DEST_PATH"

# install edc from base image (TODO: make it into package, installable from git)
cp -r /opt/conda/lib/python3.7/site-packages/edc "${DEST_PATH}/lib/python*/site-packages"

conda clean --all -f -y
