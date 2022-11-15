# 🍌 `banana`

Banana deploys off of the `main` branch of a GitHub repository.
So to deploy, just push this to `main` on some GitHub repo
and then use the
[banana UI](https://app.banana.dev/)
to add it to your deployed models.

See the documentation
[here](https://docs.banana.dev/banana-docs/quickstart)
for more details,
including information about the template this repo was built off of.

## Building locally with `make`

Local builds allow for much faster iteration
when developing.

The model backend can be built locally using `make` commands
that invoke `docker`.

Run `make help` to see the list of commands and brief descriptions.

If you want to test locally without deploying to Banana,
you can run `make test`,
which builds the Docker image, runs the container,
and sends a request after a short startup delay.
Run `make docker_stop` to clean up afterwards.

You'll need `wandb` installed in the environment where you run `make test`,
along with a W&B account,
because we call `wandb login` as part of stashing the API key secret during the Docker build.
Call `make wandb` to install it
or call `make environment` to get everything needed to run the model backend baremetal.

## Invoking the model on banana via the HTTP API

The code snippet below is not directly executable.

You'll need two secrets:
the banana API key associated with your account
and the key associated with the model you're invoking.

You can find both in the
[banana UI](https://app.banana.dev/).

```bash
BANANA_API_URL=https://api.banana.dev
INFER_ROUTE=$BANANA_API_URL/start/v4

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"apiKey": "your-banana-api-key-here", "modelKey": "your-model-key-here",
          "modelInputs": {"image": "https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png"}}' \
  $INFER_ROUTE
```
