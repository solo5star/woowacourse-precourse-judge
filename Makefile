freeze:
	pip freeze > requirements.txt

build: build-node14 build-java11

build-node14:
	docker build --tag woowacourse-precourse-judge/vm-node:14 ./vm/node14

build-java11:
	docker build --tag woowacourse-precourse-judge/vm-java:11 ./vm/java11
