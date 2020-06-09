#FROM eurodatacube/jupyter-hub:0.18.4
FROM myhub:1
RUN apt update && apt install npm node-gyp nodejs-dev libssl1.0-dev -y && npm install -g configurable-http-proxy
RUN python3 -m pip install notebook
