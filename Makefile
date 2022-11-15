.PHONY: help
.DEFAULT_GOAL := help

CONTAINER_NAME = text-recognizer-banana

help: ## get a list of all the targets, and their short descriptions
	@# source for the incantation: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

remote_inference: ## runs inference on banana
	python invoke_requests.py

test: docker_stop docker_run pause local_inference  ## runs a local inference from scratch

local_inference: ## runs an example inference locally
	curl -X POST \
	  -H "Content-Type: application/json" \
	  -d '{"image": "https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png"}' \
	  localhost:8000

environment: ## installs Python requirements for local baremetal
	pip install -r requirements.txt

docker_image: docker_base_image ## creates the image that is used by banana
	docker build -t $(CONTAINER_NAME) . -f Dockerfile

docker_run: ## runs the model backend container on port 8000
	docker run --gpus all --detach -p 8000:8000 $(CONTAINER_NAME):latest

docker_stop: ## stops a running model backend container, if it exusts
	-docker stop $$(docker ps --filter ancestor=$(CONTAINER_NAME) --format="{{.ID}}")

docker_base_image: ## creates the base image with model weights pulled from wandb.ai
	wandb login
	DOCKER_BUILDKIT=1 docker build --secret id=netrc,src=$(HOME)/.netrc -t $(CONTAINER_NAME)-base -f Dockerfile.base .

pause: ## sleeps for 30 seconds, to wait for the server to start
	@sleep 30s

wandb:  ## installs just the wandb dependency, required to get model weights
	grep "wandb" requirements.txt | xargs pip install

dotenv: ## install just the dotenv dependency, required for running remote inference
	grep "dotenv" requirements.txt | xargs pip install
