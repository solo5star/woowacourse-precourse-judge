import csv
import os
from functools import partial

from dotenv import load_dotenv
from git import Repo
from github import Github
from tqdm import tqdm

load_dotenv()

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
PULL_STATE = os.environ.get("PULL_STATE", "open")
WORKING_DIRECTORY = f"judge/{GITHUB_REPOSITORY}"

tqdm = partial(tqdm, colour="green")

g = Github(GITHUB_TOKEN)
r = g.get_repo(GITHUB_REPOSITORY)

os.makedirs(WORKING_DIRECTORY, exist_ok=True)
os.chdir(WORKING_DIRECTORY)

print(f"Get all pull requests from {r.full_name}")
_pulls = r.get_pulls(PULL_STATE)
pulls = list(tqdm(_pulls, unit="pulls", total=_pulls.totalCount))

print("Writing pulls data to pulls.tsv ...")
with open("pulls.tsv", mode="w", encoding="utf-8", newline="") as file:
    tw = csv.DictWriter(
        file, delimiter="\t", fieldnames=["username", "url", "branch", "created_at", "updated_at", "pushed_at"]
    )
    tw.writeheader()

    for pull in pulls:
        tw.writerow(
            {
                "username": pull.user.login,
                "url": pull.head.repo.clone_url,
                "branch": pull.head.ref,
                "created_at": pull.head.repo.created_at,
                "updated_at": pull.head.repo.updated_at,
                "pushed_at": pull.head.repo.pushed_at,
            }
        )

print(f"Clone pull requests from {r.full_name}")
pull_log = tqdm(total=0, position=2, bar_format="{desc}")
for pull in tqdm(pulls, position=1, unit="pulls"):
    pull_log.set_description(f"Clone {pull.head.label}")
    pulls_dir = f"pulls/{pull.user.login}"
    Repo.clone_from(pull.head.repo.clone_url, pulls_dir, branch=pull.head.ref)
