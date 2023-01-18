---
tags:
- image-to-text
widget:
- src: https://fsdl-public-assets.s3.us-west-2.amazonaws.com/paragraphs/a01-077.png
  example_title: paragraph a01-077
---

# 🚀 `replicate` and `cog`

To deploy a model on [replicate.com](https://replicate.com),
we need to build a special kind of Docker container image
and push it to the replicate Docker container registry at `r8.im`.

These containers are built using a tool called `cog`,
which is designed to make working with GPU accelerated containers easier.

The `cog` building process is configured by the `cog.yaml` file.

See Replicate's deployment guide [here](https://replicate.com/docs/guides/push-a-model)
for a more detailed walkthrough.

## Building with `make` and local testing

The provided `Makefile` is intended to make it easier
to develop and deploy locally.

Run `make help` to see the list of commands and brief descriptions.
These commands wrap setup shell commands
and `cog` commands.

Run `make environment` to install most requirements
(Python packages, `cog`)
and check for others
(Docker, NVIDIA GPUs).

To test locally without deploying to `replicate`,
run `make test` or `make local_inference`,
which build and run the container locally.
Use `make cog_shell` to spin up a shell inside
of the inference container.

## Deployment to Replicate

To deploy a model and run inference on `replicate`,
you'll also need a [Replicate account](https://replicate.com/join).

After you've set one up,
create a `.env` file
and add your user name and API token,
which you can find on Replicate's website
[here](https://replicate.com/account).

Then, we have one manual step:
go to [https://replicate.com/create](https://replicate.com/create)
and make a new model page called `fsdl-text-recognizer-gpu`.

Next, call `make cog_auth`
to authenticate to Replicate's container image registry.
In the process, you'll generate a `cog` CLI token --
that's separate from your Replicate API token!

Once you have it, add it to the `.env` file
as the `REPLICATE_CLI_TOKEN`.

Once you've authenticated to the registry, run `make cog_push`
and copy the model version number that gets returned into the `.env` file as well.

Finally, run `make remote_inference` to test
that the model runs.
