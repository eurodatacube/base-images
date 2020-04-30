import os.path
import requests
from textwrap import dedent

from IPython.display import display, HTML, YouTubeVideo, Markdown
from dotenv.main import find_dotenv, DotEnv


ENTITY_METADATA_URL = {
    "dev": "https://api.dev.hub.eox.at/metadata",
    "prod": "https://api.hub.eox.at/metadata",
}
CONTRIBUTIONS_API_URL = {
    "dev": "https://contributions-api.dev.hub.eox.at",
    "prod": "https://contributions-api.hub.eox.at",
}


def _get_requirement_name_mapping(dev: bool):
    response = requests.get(ENTITY_METADATA_URL["dev" if dev else "prod"])
    response.raise_for_status()
    return {
        data['entity']['id']: data['entity']['name']
        for data in response.json()
    }


def _get_notebook(notebook_id: str, dev: bool):
    response = requests.get(f"{CONTRIBUTIONS_API_URL['dev' if dev else 'prod']}/notebooks/{notebook_id}")
    response.raise_for_status()
    return response.json()


def prepare(notebook_id: str, dev: bool = False):
    # Legacy. This will be removed in an upcoming release.

    # actual setup
    dot_env = DotEnv(find_dotenv())
    dot_env.set_as_environment_variables()

    # the rest displays information
    requirement_name_mapping = _get_requirement_name_mapping(dev=dev)
    notebook = _get_notebook(notebook_id, dev=dev)

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

    display(Markdown(info))


def print_info(notebook_id: str, dev: bool = False):
    """Shows nice info for shared notebooks."""
    requirement_name_mapping = _get_requirement_name_mapping(dev=dev)
    notebook = _get_notebook(notebook_id, dev=dev)

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

    display(Markdown(info))


def setup_environment_variables():
    """Called in every notebook to inject credentials to environment"""
    dot_env = DotEnv(find_dotenv())
    dot_env.set_as_environment_variables()
    info =  (
        "API credentials have automatically been injected for your active subscriptions.  \n" +
        "The following environment variables are now available:\n" +
        "".join(f"* `{k}`\n" for k in dot_env.dict().keys()) +
        "\n"
    )

    user_dot_env_path = "~/custom.env"
    user_dot_env = DotEnv(os.path.expanduser(user_dot_env_path))
    user_dot_env.set_as_environment_variables(override=True)
    user_vars = user_dot_env.dict()
    if user_vars:
        info += (
            f"The following additional environment variables have been loaded from `{user_dot_env_path}`:\n" +
            "".join(f"* `{k}`\n" for k in user_vars)
        )

    info += "------\n"

    display(Markdown(info))