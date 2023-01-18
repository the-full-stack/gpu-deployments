# 🟩 `modal`

[Modal](https://modal.com/)
is an end-to-end compute stack for data science and machine learning.

This example shows how we set up the
[FSDL Text Recognizer](https://github.com/full-stack-deep-learning/fsdl-text-recognizer-2022-labs)
to run on Modal as a serverless GPU application.

Check out their
[awesome docs here](https://modal.com/docs/guide)
for more information about all the other cool stuff you can do with Modal.

We at FSDL also wrote a tutorial on using it to
[generate art of your pet with Dreambooth + Stable Diffusion](https://modal.com/docs/guide/ex/dreambooth_app).

## Setup

We provide a `Makefile` to keep things simple.

Check that `Makefile` for details on how each command below works.

Run `make help` to see the list of commands and brief descriptions.

You'll also need the Modal client library installed locally.

You'll need `wandb` installed locally as well,
along with a W&B account,
because we locally fetch the model weights from [W&B](https://wandb.ai).

Call `make environment` to install everything you need.

You'll also need a Modal account.
Modal is, as of writing in January 2023,
in private beta.
You can [request access here](https://modal.com/signup).

Then, once you've followed the instructions for setting up the client,
you should have a Modal username (from your GitHub) and token.
You can also call `make modal_token` to create a new token.

Tokens have two parts: an ID and a secret.
Add both of these to a `.env` file that looks like `.env.example`.
Call `make modal_auth` to confirm authentication with Modal.

## Deploying the model

Deployment is easy: just call `make deploy`.

Head to the URL for the `fastapi_app` in the output of that command
to check out the Gradio app wrapped around our model.

It may take a few minutes to spin up at the start.

The Gradio app also includes an API,
which we can access directly, e.g. via `curl`.
Run `make remote_inference` to make a request from the command line.
Note that some requests take up to two minutes to run.

If you run into issues,
use `make debugger` to launch an interactive IPython REPL
inside an app container running on Modal's cloud,
but with input/output inside your local terminal. Slick!
