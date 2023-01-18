ifneq (,$(wildcard ./.env))
    include .env
	# assume includes REPLICATE_USER_NAME for local push,
	# assume includes REPLICATE_CLI_TOKEN for remote push,
	# assume includes REPLICATE_API_TOKEN for remote inference,
	# assume includes latest REPLICATE_MODEL_VERSION for remote inference with latest model
    export
endif

.PHONY: help
.DEFAULT_GOAL := help

help: ## get a list of all the targets, and their short descriptions
	@echo "🥞: Look for messages like this one in command outputs for additional instructions"
	@# source for the incantation: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

deploy: cog_build cog_push ## deploys to replicate

test: local_inference ## runs a local inference from scratch

remote_inference: ## runs an example inference on replicate, higher latencies in the minute range
	python invoke_requests.py --api_token $(REPLICATE_API_TOKEN) --model_version $(REPLICATE_MODEL_VERSION)

local_inference: wandb model_weights ## runs an example inference locally
	cog predict -i image=https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png

cog_push: cog_auth ## pushes container image to replicate container repository
	@echo
	@echo "###"
	@echo "# 🥞: Before pushing a model for the first time, create a page for it via the replicate UI: replicate.com/create"
	@echo "###"
	@echo
	cog push r8.im/$(REPLICATE_USER_NAME)/text-recognizer-gpu:latest
	@echo
	@echo "Don't forget to update the \$$MODEL_VERSION in .env before running remote inference!"
	@echo "You can find your \$$MODEL_VERSION info at https://replicate.com/$(REPLICATE_USER_NAME)/text-recognizer-gpu"

cog_build: wandb model_weights ## creates the deployable container image
	cog build -t r8.im/$(REPLICATE_USER_NAME)/text-recognizer-gpu:latest

cog_auth:  # authenticates to replicate container repository
	@if [ -z $$(echo $(REPLICATE_CLI_TOKEN)) ]; then\
		cog login;\
		echo "###";\
		echo "# 🥞: Add the token to your .env file to speed up future cog authenication";\
		echo "###";\
	else\
		echo $(REPLICATE_CLI_TOKEN) | cog login --token-stdin;\
	fi

model_weights: wandb ## downloads model weights from wandb
	python text_recognizer/get_model.py --entity=cfrye59

wandb: ## installs wandb and authenticates
	grep "wandb" requirements.txt | xargs pip install
	wandb login

environment: ## installs or checks all requirements: Python libraries, docker, cog, GPUs
	pip install -r requirements.txt
	# docker is required locally
	docker --version
	# install cog if not present
	@if [ -z $$(which cog) ]; then\
		sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m` && \
		sudo chmod +x /usr/local/bin/cog; \
	fi
	cog --version
	# GPUs are required locally
	nvidia-smi

cog_shell:  # open a shell locally inside the container, good for debugging
	cog run bash
