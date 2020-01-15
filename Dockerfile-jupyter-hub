ARG BASE_CONTAINER=docker.io/jupyterhub/k8s-hub:0.8.2
FROM $BASE_CONTAINER

USER root

RUN sed -i -e 's:(groups):(groups 2>/dev/null):' /etc/bash.bashrc

COPY ./jupyter-hub/. /usr/local/share/jupyterhub/

WORKDIR /srv/jupyterhub

USER ${NB_USER}