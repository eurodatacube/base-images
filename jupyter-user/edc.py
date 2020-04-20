import requests
from textwrap import dedent

from IPython.display import display, HTML, YouTubeVideo, Markdown
from dotenv.main import find_dotenv, DotEnv


# TODO: configure dev or production!!!!
ENTITY_METADATA_URL = "https://api.dev.hub.eox.at/metadata"
CONTRIBUTIONS_API_URL = "https://contributions-api.dev.hub.eox.at"


def _get_requirement_name_mapping():
    response = requests.get(ENTITY_METADATA_URL)
    response.raise_for_status()
    return {
        data['entity']['id']: data['entity']['name']
        for data in response.json()
    }


def _get_notebook(notebook_id: str):
    response = requests.get(f"{CONTRIBUTIONS_API_URL}/notebooks/{notebook_id}")
    response.raise_for_status()
    return response.json()


def prepare(notebook_id: str):

    # actual setup
    dot_env = DotEnv(find_dotenv())
    dot_env.set_as_environment_variables()

    # the rest displays information
    requirement_name_mapping = _get_requirement_name_mapping()
    notebook = _get_notebook(notebook_id)

    requirements = [
        requirement_name_mapping.get(req, req)
        for req in notebook.get("requirements", [])
    ]

    info = dedent(f"""
        ***Notebook Title***  
        {notebook['name']}
        
        ***Notebook Description***  
        {notebook['description']}
        
        """
    )

    if requirements:
        info += dedent(f"""
            ***Notebook Dependencies***  
            This notebook requires an active subscription to:
            """
        )
        info += "".join(f"* {req}\n" for req in requirements)

    info += dedent(
        """
        ---------
        
        *API credentials have automatically been injected for your active subscriptions.*
        
        The following environment variables are now available:
        """
    )
    info += "".join(f"* `{k}`\n" for k in dot_env.dict().keys())
    info += "\n-------------\n"
    display((info))

    display(Markdown(info))
