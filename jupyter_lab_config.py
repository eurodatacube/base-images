import os
# Configuration file for lab.

## Extra paths to look for federated JupyterLab extensions
if (env := os.environ.get("ENV_NAME")):
    c.LabApp.extra_labextensions_path = [
        f"/opt/conda/envs/{env}/share/jupyter/labextensions"
    ]
