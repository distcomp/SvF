IMAGE_NAME=distcomp/svf
EVEREST_TOKEN?=INSERT_HERE

build:
	docker build -t $(IMAGE_NAME) -f Dockerfile ..

push:
	docker push $(IMAGE_NAME)

run:
	docker run -d -it --rm --name agent -e EVEREST_TOKEN=$(EVEREST_TOKEN) -e MAX_TASKS=16 $(IMAGE_NAME)

stop:
	docker stop agent
