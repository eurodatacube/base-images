import requests

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

    load_dotenv()

    requirement_name_mapping = _get_requirement_name_mapping()
    notebook = _get_notebook(notebook_id)

    requirements = [
        requirement_name_mapping.get(req, req)
        for req in notebook.get("requirements", [])
    ]

    display(Markdown(
        "# Euro Data Cube Getting Started"
    ))
    if requirements:
        display(Markdown(
            "## Requirements\n"
            "This noteboot requires an active subscription to:\n" +
            "".join(f"* {req}\n" for req in requirements) +
            "\nAPI credentials will be injected automatically."
        ))

    # enable this to also show the notebook name:
    # display(Markdown(f"# {notebook['name']}"))

