#!/usr/bin/env bash
set -o pipefail -eux

JUPYTER_USER_IMAGE=$1

docker run --rm --name edc -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "${HOME}"/tmp:/home/jovyan -it $JUPYTER_USER_IMAGE start-notebook.sh --NotebookApp.token=''
