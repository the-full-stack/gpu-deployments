# 🍌 `banana`

Banana uses GitHub repos containing `Dockerfile`s
as the deployable artifact.

See the deployment guide
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

To deploy on `api.banana.dev`,
just push this to `main` on some GitHub repo
and then use the
[banana UI](https://app.banana.dev/)
to add it to your deployed models.

Note that builds can take tens of minutes,
because Banana attempts model optimizations behind the scenes,
but the model inference service should become available in just a few minutes.
You can watch the build progress in the
[banana UI](https://app.banana.dev).

The `invoke_requests.py` script uses the `requests` Python library
to send a request to a model running on `api.banana.dev`.
You can call it via `make` with `make remote_inference`.

For remote inference to work,
You'll need to add two secrets to the `.env` file:
the banana API key associated with your account
and the key associated with the model you're invoking.
See `.env.example` for the expected format.

You can find both in the
[banana UI](https://app.banana.dev/).
