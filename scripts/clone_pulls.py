import csv
import os
import shutil
from functools import partial

from dotenv import load_dotenv
from git import Repo
from github import Github
from github.PullRequest import PullRequest
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


def is_pull_valid(pull: PullRequest):
    return pull.head.repo is not None and pull.user.login != "ghost"


_pulls = r.get_pulls(PULL_STATE)
pulls: list[PullRequest] = []

print(f"Clone pull requests from {r.full_name}")
pull_log = tqdm(total=0, position=2, bar_format="{desc}")
for pull in tqdm(_pulls, total=_pulls.totalCount, position=1, unit="PR"):
    pull_log.set_description(f"Clone {pull.head.label}")
    if not is_pull_valid(pull):
        continue

    pull_dir = f"pulls/{pull.user.login}"
    if os.path.exists(pull_dir):
        pull_log.set_description(f"{pull_dir} exists. clean directory ...")
        shutil.rmtree(pull_dir)

    try:
        pull_log.set_description(f"Clone {pull.head.label} PR to {pull_dir} ...")
        Repo.clone_from(pull.head.repo.clone_url, pull_dir, branch=pull.head.ref)
        pulls.append(pull)
    except:
        pass


print("Writing pulls data to pulls.tsv ...")
with open("pulls.tsv", mode="w", encoding="utf-8", newline="") as file:
    tw = csv.DictWriter(
        file,
        delimiter="\t",
        fieldnames=["number", "username", "url", "branch", "created_at", "updated_at", "pushed_at"],
    )
    tw.writeheader()

    for pull in pulls:
        tw.writerow(
            {
                "number": pull.number,
                "username": pull.user.login,
                "url": pull.head.repo.clone_url,
                "branch": pull.head.ref,
                "created_at": pull.head.repo.created_at,
                "updated_at": pull.head.repo.updated_at,
                "pushed_at": pull.head.repo.pushed_at,
            }
        )
