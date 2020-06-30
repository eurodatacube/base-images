#!/bin/bash

set -eux -o pipefail

DEST_PATH=$1

conda env create --file base-environment.yaml --prefix $DEST_PATH

conda clean --all -f -y
