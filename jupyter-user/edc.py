import collections
import difflib
import itertools
import os
import os.path
import re
import requests
from textwrap import dedent
from typing import List, Tuple

from IPython.display import display, Markdown
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
    return {data["entity"]["id"]: data["entity"]["name"] for data in response.json()}


def _get_notebook(notebook_id: str, dev: bool):
    response = requests.get(
        f"{CONTRIBUTIONS_API_URL['dev' if dev else 'prod']}/notebooks/{notebook_id}"
    )
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

    info = dedent(
        f"""
        ***Notebook Title***  
        {notebook['name']}
        
        ***Notebook Description***  
        {notebook['description']}
        
        """
    )

    if requirements:
        info += dedent(
            """
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

    info = dedent(
        f"""
        ***Notebook Title***  
        {notebook['name']}
        
        ***Notebook Description***  
        {notebook['description']}
        
        """
    )

    if requirements:
        info += dedent(
            """
            ***Notebook Dependencies***  
            This notebook requires an active subscription to:
            """
        )
        info += "".join(f"* {req}\n" for req in requirements)

    display(Markdown(info))


def _format_env_list(variables):
    groups = itertools.groupby(
        sorted(variables),
        # group by first part, e.g. "SH" or "GEODB"
        key=lambda var: var.split("_", 1)[0],
    )
    formatted_groups = [", ".join(f"`{v}`" for v in group) for _, group in groups]
    return "".join(f"* {line}\n" for line in formatted_groups)


def setup_environment_variables():
    """Called in every notebook to inject credentials to environment"""
    dot_env = DotEnv(find_dotenv())
    dot_env.set_as_environment_variables()
    info = (
        "API credentials have automatically been injected for your active subscriptions.  \n"
        + "The following environment variables are now available:\n"
        + _format_env_list(dot_env.dict().keys())
        + "\n"
    )

    user_dot_env_path = "~/custom.env"
    user_dot_env = DotEnv(os.path.expanduser(user_dot_env_path))
    user_dot_env.set_as_environment_variables(override=True)
    user_vars = user_dot_env.dict()
    if user_vars:
        info += (
            f"The following additional environment variables have been loaded from `{user_dot_env_path}`:\n"
            + _format_env_list(user_vars.keys())
        )

    info += "------\n"

    display(Markdown(info))


release_url = "https://contributions-api.dev.hub.eox.at/base-image-release-notes/{tag}"

# Example: -ipython                   7.13.0           py37hc8dfbb8_2    conda-forge
conda_list_output_regex = (
    r"^[-+](?P<name>\S+)\s+(?P<major_version>\d+)\.\S+\s+\S+\s+\S+$"
)
# TODO: use semver for anything more complicated


def _get_release_message(tag: str) -> str:
    response = requests.get(release_url.format(tag=tag))
    response.raise_for_status()
    return response.text


def _calculate_diff_lines(old: str, new: str) -> List[str]:
    diff = difflib.unified_diff(old.splitlines(), new.splitlines(), n=0, lineterm="")
    # remove position markers ('@@ -25,2 +25,2 @@')
    diff = [
        entry for entry in diff if not (entry.startswith("@@") and entry.endswith("@@"))
    ]
    # remove "header" (---, +++)
    diff = diff[2:]
    return diff


def _group_major_minor_added_remove(
    diff_lines: List[str],
) -> Tuple[List[str], List[str], List[str], List[str]]:
    """Takes diff lines and returns them grouped by meaning of change"""
    libraries = collections.defaultdict(list)

    for line in diff_lines:
        match = re.match(conda_list_output_regex, line)
        if match:
            libraries[match.group("name")].append(
                {"major_version": match.group("major_version"), "line": line}
            )

    major, minor, added, removed = [], [], [], []
    for lib, versions in libraries.items():
        if len(versions) == 2:
            if versions[0]["major_version"] != versions[1]["major_version"]:
                major.extend((versions[0]["line"], versions[1]["line"]))
            else:
                minor.extend((versions[0]["line"], versions[1]["line"]))

        elif len(versions) == 1:
            sign = versions[0]["line"][0]
            if sign == "-":
                removed.append(versions[0]["line"])
            elif sign == "+":
                added.append(versions[0]["line"])

    return major, minor, added, removed


def _append_nl(seq: List[str]) -> List[str]:
    return [f"{i}\n" for i in seq]


def check_compatibility(tag: str) -> None:
    current_image_tag = "v" + os.environ["JUPYTER_IMAGE"].split(":", 2)[1]
    if current_image_tag == tag:
        print("Notebook is compatible")
    else:
        msg = dedent(
            f"""
            ## Base image difference detected
            This notebook has been verified using the [base image **{tag}**](https://github.com/eurodatacube/base-images/releases/tag/{tag}),
            whereas you are currently running [base image **{current_image_tag}**](https://github.com/eurodatacube/base-images/releases/tag/{current_image_tag}).

            If you experience any problems, please consult the [marketplace](https://eurodatacube.com/marketplace) for a more recent version of this notebook.

            The following changes occurred in base image in between these versions:

            """
        )
        notebook_image_release_msg = _get_release_message(tag)
        current_image_release_msg = _get_release_message(current_image_tag)

        diff_lines = _calculate_diff_lines(
            old=notebook_image_release_msg, new=current_image_release_msg,
        )

        major, minor, added, removed = _group_major_minor_added_remove(diff_lines)

        if added:
            msg += f"### New libraries:\n```\n{''.join(_append_nl(added))}```\n"

        if removed:
            msg += f"### Removed libraries:\n```\n{''.join(_append_nl(removed))}```\n"

        if major:
            msg += f"### Libraries with major version differences:\n```\n{''.join(_append_nl(major))}```\n"

        if minor:
            msg += f"### Libraries with minor version differences:\n```\n{''.join(_append_nl(minor))}```\n"

        display(Markdown(msg))
