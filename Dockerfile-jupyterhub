ARG BASE_CONTAINER=jupyter/scipy-notebook:7a3e968dd212
FROM $BASE_CONTAINER

USER root
RUN echo "group2004:x:2004:" >> /etc/group && \
    echo "group2005:x:2005:" >> /etc/group

USER $NB_UID

RUN conda install --quiet --yes oauthlib gdal fiona rasterio shapely xarray zarr psycopg2 geopandas && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR

RUN jupyter labextension install @jupyterlab/geojson-extension

RUN pip install requests_oauthlib && \
    pip install python-dotenv && \
    pip install git+https://github.com/dcs4cop/xcube && \
    pip install git+https://github.com/dcs4cop/xcube-sh && \
    fix-permissions /home/$NB_USER

RUN git clone https://github.com/eurodatacube/getting-started-notebooks.git /tmp/getting-started-notebooks 2> /dev/null || git -C /tmp/getting-started-notebooks pull
