freeze:
	pip freeze > requirements.txt

vm: vm-node vm-java

vm-node:
	docker build --tag woowacourse-precourse-judge/vm-node:14-jest ./vm/node/14-jest
	docker build --tag woowacourse-precourse-judge/vm-node:14-cypress ./vm/node/14-cypress

vm-java:
	docker build --tag woowacourse-precourse-judge/vm-java:11 ./vm/java/11

vm-kotlin:
	docker build --tag woowacourse-precourse-judge/vm-kotlin:1.6.20 ./vm/kotlin/1.6.20
