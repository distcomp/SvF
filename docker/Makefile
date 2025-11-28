IMAGE_NAME?=ghcr.io/distcomp/svf
AGENT_IMAGE_NAME?=ghcr.io/distcomp/svf-agent
EVEREST_TOKEN?=INSERT_HERE
HOSTNAME := $(shell hostname)

build:
	docker build -t $(IMAGE_NAME) -f Dockerfile ..

push:
	docker push $(IMAGE_NAME)

build-agent:
	docker build -t $(AGENT_IMAGE_NAME) -f Dockerfile.agent ..

push-agent:
	docker push $(AGENT_IMAGE_NAME)

run:
	docker run -d -it --restart always --name agent --hostname $(HOSTNAME)-svf -e EVEREST_TOKEN=$(EVEREST_TOKEN) -e MAX_TASKS=16 $(IMAGE_NAME)

stop:
	docker stop agent
	docker rm agent
