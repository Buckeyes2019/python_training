#!/usr/bin/env python3
"""
Requires Python 3.6+
Example usage:
    $ fetch_ghstars.py USERNAME [OPTIONAL_AUTH_TOKEN]
"""

import csv
from functools import reduce
import json
from pathlib import Path
import requests
from sys import argv, exit, stderr

BASE_ENDPOINT = (
    "https://api.github.com/users/{username}/starred?per_page=100&page={pagenum}"
)
BASE_HEADERS = {"Accept": "application/vnd.github.v3.star+json"}
TARGET_DIRNAME = "./ghstars-{username}/"
WRANGLED_BASENAME = "wrangled.csv"
OUTPUT_HEADERS = {
    "repo": "repo.full_name",
    "starred_at": "starred_at",
    "repo_name": "repo.name",
    "owner_name": "repo.owner.login",
    "size": "repo.size",
    "stars": "repo.stargazers_count",
    "watchers": "repo.watchers_count",
    "forks": "repo.forks_count",
    "updated_at": "repo.updated_at",
    "pushed_at": "repo.pushed_at",
    "created_at": "repo.created_at",
    "language": "repo.language",
    "license": "repo.license.key",
    "description": "repo.description",
    "homepage": "repo.homepage",
    "is_private": "repo.private",
    "is_fork": "repo.fork",
    "is_archived": "repo.archived",
    "has_issues": "repo.has_issues",
    "has_downloads": "repo.has_downloads",
    "has_projects": "repo.has_projects",
    "has_wiki": "repo.has_wiki",
    "has_pages": "repo.has_pages",
    "repo_id": "repo.id",
    "repo_url": "repo.html_url",
}


def fetch(user_name: str, target_dir: Path, auth_token: str = None) -> list:
    """fetches each page of GIthub star results, saves the raw json, and returns a compiled list of deserialized objects"""
    target_dir.mkdir(exist_ok=True)
    headers = BASE_HEADERS.copy()
    if auth_token:
        headers["Authorization"] = f"token {auth_token}"

    alldata = []
    i = 0
    while i >= 0:
        i += 1
        url = BASE_ENDPOINT.format(username=user_name, pagenum=i)
        xlog(f"Fetch #{i}")
        xlog(f"-  {url}")

        resp = requests.get(url, headers=headers, stream=True)
        data = resp.json()
        if type(data) is not list:
            exit(f"Unexpected or error response from API:\n{data}")

        if not data:
            xlog("Empty result set, seems we're done fetching!")
            break
        else:
            alldata.extend(data)
            dp = target_dir.joinpath("{}.json".format(str(i).rjust(2, "0")))
            xlog(f"-  Writing {len(data)} results to: {dp}  ({len(alldata)} total)")
            dp.write_text(json.dumps(data, indent=2))

    return alldata


def wrangle(data: list) -> list:
    """returns a compiled list of Github star data, with select header names"""
    wdata = []
    for row in data:
        w = {}
        for hed, ktxt in OUTPUT_HEADERS.items():
            w[hed] = reduce(
                lambda r, k: r[k] if r and r.get(k) else None, ktxt.split("."), row
            )
        wdata.append(w)
    return wdata


def xlog(thing):
    stderr.write(f"{thing}\n")


def main():
    if len(argv) < 2:
        exit("Error: Need to provide a username as first argument")

    username, *xargs = argv[1:]
    oauth = xargs[0] if xargs else None
    oatxt = "token " + oauth[0:4] + "****" + oauth[-3:] if oauth else "no auth"
    target_dir = Path(TARGET_DIRNAME.format(username=username))
    xlog(f"Collecting  `{username}` data. Using {oatxt}. Saving to: {target_dir}/")

    rawdata = fetch(username, target_dir, auth_token=oauth)

    wdata = wrangle(rawdata)
    wpath = target_dir.joinpath(WRANGLED_BASENAME)
    with open(wpath, "w", encoding='utf-8') as w:
        outs = csv.DictWriter(w, fieldnames=OUTPUT_HEADERS.keys())
        outs.writeheader()
        outs.writerows(wdata)

    xlog(f"Wrote {len(wdata)} flattened records to: {wpath}")


if __name__ == "__main__":
    main()