# 우아한테크코스 프리코스 채점 프로그램

간단하게 만든 우아한테크코스 프리코스 채점 프로그램입니다.

## 동작 과정
1. 환경변수로 지정된 레포지토리(ex. `woowacourse-precourse/javascript-menu`)의 Pull Request 목록을 받아옵니다.
2. 모든 Pull Request를 clone합니다.
3. 제한된 dependency만 설치되어 있는 Docker Container에서 채점(테스트)을 진행합니다.
4. 채점 결과들을 tsv로 정리하고 README.md 파일에 요약해줍니다.

## 실행 방법

이 프로젝트를 실행하려면 python 3.10 또는 그 이상과 docker, make가 필요합니다.

### .env 환경변수 설정

.env 파일을 생성한 다음 아래와 같은 형식으로 내용을 입력해주세요.
```
GITHUB_TOKEN=YOUR_GITHUB_TOKEN
GITHUB_REPOSITORY=woowacourse-precourse/javascript-menu
PULL_STATE=open
JUDGE_VM_DOCKER_IMAGE=woowacourse-precourse-judge/vm-node:14
JUDGE_LIMIT_CONCURRENCY=5
```

* `GITHUB_TOKEN` 은 GitHub 개발자 설정에서 발급받을 수 있습니다.
* `GITHUB_REPOSITORY` 는 채점할 레포지토리입니다.
* `PULL_STATE` 는 open/close되어있는 Pull Request로 한정합니다.
* `JUDGE_VM_DOCKER_IMAGE` 는 채점에 사용할 Docker 이미지입니다. 아래 두 개의 이미지를 지원합니다.
  * woowacourse-precourse-judge/vm-node:14
  * woowacourse-precourse-judge/vm-java:11
  > woowacourse-precourse에서 제공하는 mission-utils 의존성이 포함되어 있습니다.
* `JUDGE_LIMIT_CONCURRENCY` 는 동시에 채점할 갯수입니다.
  * 컴퓨터 사양에 따라 적당히 조절해주세요.
  * i5-10400 기준으로, javascript는 10, java는 5가 적당합니다.

### 채점용 Docker 이미지 빌드

```sh
$ make build
```
> java만 빌드하려면 `make build-java11`을, javascript만 빌드하려면 `make build-node14` 를 입력해주세요.

## 파이썬 스크립트들을 실행하기 위한 dependency 설치

```sh
$ python -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
```
> 이 프로젝트에서는 GitPython, PyGithub, tqdm과 같은 라이브러리를 사용합니다.

### Pull Request 클론

```sh
$ python scripts/clone_pulls.py
```
모든 Pull Request를 clone합니다. 시간이 다소 소요될 수 있습니다.

### 채점

```sh
$ python scripts/judge.py
```
채점을 진행합니다. 시간이 다소 소요될 수 있습니다.

## 채점 결과

채점 결과물은 모두 judge/{owner}/{repository_name} 에 저장됩니다.

* judge-outputs: 채점 진행 중 출력을 저장합니다.
* pulls: clone한 Pull Request가 여기에 저장됩니다.
* judge-results.tsv: 각 채점 당 테스트 결과가 tsv 형식으로 저장됩니다.
* pulls.tsv: clone한 Pull Request 목록이 tsv 형식으로 저장됩니다.
* README.md: 채점 결과를 요약하여 표시합니다.

## woowacourse-precourse/javascript-menu: Pull Request Test Report

> 테스트 환경에 따라 차이가 발생할 수 있습니다.

Total Pulls: **103**

Total Passed: **38**

Total Failed: **65**

```mermaid
pie showData
    title Test Result
    "Passed": 38
    "Failed": 65
```

## woowacourse-precourse/java-menu: Pull Request Test Report

> 테스트 환경에 따라 차이가 발생할 수 있습니다.

Total Pulls: **202**

Total Passed: **142**

Total Failed: **60**

```mermaid
pie showData
    title Test Result
    "Passed": 142
    "Failed": 60
```
