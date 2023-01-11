ifneq (,$(wildcard ./.env))
    include .env
	# assume includes MODAL_TOKEN_ID and MODAL_TOKEN_SECRET for modal auth,
	# assume includes MODAL_USER_NAME for inference on modal
    export
endif

.PHONY: help
.DEFAULT_GOAL := help

help: ## get a list of all the targets, and their short descriptions
	@# source for the incantation: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

deploy: model_weights modal_auth ## deploys to modal, see output for URL, latency of a few minutes
	modal deploy app.py

# define API_URL and the base64 encoding of an example input image
API_URL=https://$(MODAL_USER_NAME)--fsdl-text-recognizer.modal.run/run
data=$(shell base64 -w0 -i a01-077.png)
remote_inference: ## runs an example inference on Modal, after deployment finished
	@(echo -n '{ "data": ["data:image/png;base64,'$(data)'"] }') \
		| curl -s -X POST "$(API_URL)/predict" -H 'Content-Type: application/json' -d @-

debugger: modal_auth ## starts a debugger in the terminal running on Modal's infra
	modal run app::stub.debug

model_weights: environment ## downloads model weights from wandb
	wandb login
	python text_recognizer/get_model.py --entity=cfrye59

modal_auth: ## confirms authentication with modal
	@modal token set --token-id $(MODAL_TOKEN_ID) --token-secret $(MODAL_TOKEN_SECRET)

environment: ## checks and installs missing requirements
	pip install -q -r requirements.txt
