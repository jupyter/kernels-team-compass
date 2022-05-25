"""Generate HTML Contributors tables for team pages
"""
import pathlib
import pandas as pd
import os
import os.path as op
from ruamel import yaml

# Variables
N_PER_ROW = 4

# Init
path_data = op.join(op.dirname(op.abspath(__file__)), "..", "team")
yaml = yaml.YAML()

template = '<td align="center" class="member_entry"><a href="{HANDLE_URL}"><img src="{AVATAR_URL}" class="headshot" alt="{NAME}" /><br /><p class="name"><b>{NAME}</b></p></a><p class="member_affiliation">{AFFILIATION}</p>'


def _generate_council(members):
    """Generate an HTML list of council members, given a dataframe of their information."""
    s = ['<table class="docutils council">', '<tr class="row-even">']
    for ix, person in members.iterrows():
        if ix % N_PER_ROW == 0 and ix != 0:
            s += ['</tr><tr class="row-even">']

        # Find user gravatar url
        avatar_url = "https://github.com/{HANDLE}.png?size=200".format(
            HANDLE=person["handle"].lstrip("@")
        )

        # Add user
        format_dict = dict(
            HANDLE=person["handle"],
            HANDLE_URL="https://github.com/{HANDLE}".format(
                HANDLE=person["handle"].lstrip("@")
            ),
            AFFILIATION=person["affiliation"],
            AVATAR_URL=avatar_url,
            NAME=person["name"],
        )

        # Render
        s += [template.format(**format_dict)]
    s += ["</table>"]
    final_text = [".. raw:: html", ""]
    for line in s:
        final_text += ["   " + line]
    final_text = "\n".join(final_text)
    return final_text

# Load council member list
source_dir = pathlib.Path(path_data)
council_file = source_dir / "council.yml"
with open(council_file, "r") as ff:
    data = yaml.load(ff)

people = pd.DataFrame(data)
if not people.empty:
    # Create active member table
    active_people = people[people.team == "active"]
    table = _generate_council(active_people)
    with open(source_dir / "active.txt", "w") as ff:
        ff.write(table)

    # Create inactive member table
    inactive_people = people[people.team == "inactive"]
    table = _generate_council(inactive_people)
    with open(source_dir / "inactive.txt", "w") as ff:
        ff.write(table)
