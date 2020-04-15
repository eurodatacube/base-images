import requests
from textwrap import dedent

from IPython.display import display, HTML, YouTubeVideo, Markdown
from dotenv import load_dotenv


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
    load_dotenv()

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
        nl = "\n"  # newline not allowed in f-string
        info += dedent(f"""
            ***Notebook Dependencies***  
            This notebook requires an active subscription to:
            {"".join(f"* {req}" + nl for req in requirements)}
            """
        )

    info += dedent(
        """
        ---------
        
        *API credentials have automatically been injected for your active subscriptions.*
        
        -------------
        """
    )

    display(Markdown(info))
