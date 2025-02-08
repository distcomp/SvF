IMAGE_NAME=distcomp/svf
EVEREST_TOKEN?=INSERT_HERE
HOSTNAME := $(shell hostname)

build:
	docker build -t $(IMAGE_NAME) -f Dockerfile ..

push:
	docker push $(IMAGE_NAME)

run:
	docker run -d -it --restart always --name agent --hostname $(HOSTNAME)-svf -e EVEREST_TOKEN=$(EVEREST_TOKEN) -e MAX_TASKS=16 $(IMAGE_NAME)

stop:
	docker stop agent
	docker rm agent
