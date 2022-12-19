import asyncio
import csv
import json
import os
from dataclasses import asdict, dataclass
from functools import partial, reduce

import aiodocker
from aiodocker.containers import DockerContainer
from dotenv import load_dotenv
from tqdm.asyncio import tqdm

load_dotenv()

GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
WORKING_DIRECTORY = f"judge/{GITHUB_REPOSITORY}"
JUDGE_VM_DOCKER_IMAGE = os.environ["JUDGE_VM_DOCKER_IMAGE"]
JUDGE_LIMIT_CONCURRENCY = int(os.environ.get("JUDGE_LIMIT_CONCURRENCY", 10))

os.chdir(WORKING_DIRECTORY)

tqdm.gather = partial(tqdm.gather, colour="blue")


@dataclass(frozen=True)
class JudgeResult:
    username: str
    success: bool
    exit_code: int
    num_total_tests: int
    num_failed_tests: int
    num_ignored_tests: int
    num_passed_tests: int
    output: str


async def judge(username: str, timeout: int | None = 60):
    async with aiodocker.Docker() as docker:
        pull_dir = os.path.join(os.getcwd(), f"pulls/{username}")
        container: DockerContainer = await docker.containers.run(
            config={
                "Image": JUDGE_VM_DOCKER_IMAGE,
                "AttachStdout": True,
                "AttachStderr": True,
                "HostConfig": {
                    "Binds": [f"{pull_dir}:/code:ro"],
                    "NetworkMode": "none",
                },
            },
        )
        try:
            result = await container.wait(timeout=timeout)
        except asyncio.TimeoutError as error:
            return JudgeResult(
                username=username,
                success=False,
                exit_code=124,
                num_total_tests=0,
                num_failed_tests=0,
                num_ignored_tests=0,
                num_passed_tests=0,
                output=repr(error),
            )

        exit_code = result["StatusCode"]

        stdout = await container.log(stdout=True)
        stderr = "".join(await container.log(stderr=True))
        await container.delete(force=True)

        test_result_parsed = False
        test_result = {
            "numTotalTests": 0,
            "numFailedTests": 0,
        }
        for line in stdout:
            try:
                test_result.update(json.loads(line))
                test_result_parsed = True
                break
            except json.decoder.JSONDecodeError:
                pass

        test_result.setdefault("success", test_result_parsed and test_result["numFailedTests"] == 0)
        test_result.setdefault("numIgnoredTests", 0)
        test_result.setdefault(
            "numPassedTests",
            test_result["numTotalTests"] - test_result["numFailedTests"] - test_result["numIgnoredTests"],
        )

        return JudgeResult(
            username=username,
            success=test_result["success"],
            exit_code=exit_code,
            num_total_tests=test_result["numTotalTests"],
            num_failed_tests=test_result["numFailedTests"],
            num_ignored_tests=test_result["numIgnoredTests"],
            num_passed_tests=test_result["numPassedTests"],
            output=stderr,
        )


def load_pulls():
    with open("pulls.tsv", mode="r", encoding="utf-8") as file:
        tr = csv.DictReader(file, delimiter="\t")
        pulls = list(tr)

    return pulls


def write_results(judge_results: list[JudgeResult]):
    print("Writing judge results to judge-results.tsv ...")
    os.makedirs("judge-outputs", exist_ok=True)
    with open("judge-results.tsv", mode="w", encoding="utf-8") as file:
        headers = ["username", "success", "exit_code", "num_total_tests", "num_failed_tests", "num_passed_tests"]
        tw = csv.DictWriter(file, delimiter="\t", fieldnames=headers)
        tw.writeheader()

        for judge_result in judge_results:
            tw.writerow({key: value for key, value in asdict(judge_result).items() if key in headers})

            with open(f"judge-outputs/{judge_result.username}.txt", mode="w", encoding="utf-8") as judge_output:
                judge_output.write(judge_result.output)


def write_report(judge_results: list[JudgeResult]):
    num_passed = reduce(lambda count, judge_result: count + int(judge_result.success), judge_results, 0)
    num_failed = reduce(lambda count, judge_result: count + int(not judge_result.success), judge_results, 0)

    content = f"""
# {GITHUB_REPOSITORY}: Pull Request Test Report

Total Pulls: **{len(judge_results)}**

Total Passed: **{num_passed}**

Total Failed: **{num_failed}**

```mermaid
pie showData
    title Test Result
    "Passed": {num_passed}
    "Failed": {num_failed}
```
    """.strip()

    with open("README.md", mode="w", encoding="utf-8") as file:
        file.write(content)


async def main():
    pulls = load_pulls()
    semaphore = asyncio.Semaphore(JUDGE_LIMIT_CONCURRENCY)

    async def concurrency_limited_judge(username: str):
        async with semaphore:
            return await judge(username)

    usernames = [row["username"] for row in pulls]
    judge_tasks = [concurrency_limited_judge(username) for username in usernames]

    print("Judge processing ...")
    judge_results: list[JudgeResult] = await tqdm.gather(*judge_tasks)

    write_results(judge_results)
    write_report(judge_results)


if __name__ == "__main__":
    asyncio.run(judge("thdwoqor"))
