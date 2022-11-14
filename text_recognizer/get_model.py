"""Pulls down the Text Recognizer model from W&B."""
import argparse
from pathlib import Path

import wandb


# these names are all set by the pl.loggers.WandbLogger
LOG_DIR = Path("training") / "logs"

STAGED_MODEL_TYPE = "prod-ready"  # we can choose the name of this type, and ideally it's different from checkpoints
STAGED_MODEL_FILENAME = "model.pt"  # standard nomenclature; pytorch_model.bin is also used

PROJECT_ROOT = Path(__file__).resolve().parents[1]

api = wandb.Api()

DEFAULT_ENTITY = api.default_entity
DEFAULT_FROM_PROJECT = "fsdl-text-recognizer-2021-training"
DEFAULT_STAGED_MODEL_NAME = "paragraph-text-recognizer"

PROD_STAGING_ROOT = PROJECT_ROOT / "text_recognizer" / "artifacts"


def main(args):
    prod_staging_directory = PROD_STAGING_ROOT / args.staged_model_name
    prod_staging_directory.mkdir(exist_ok=True, parents=True)
    entity = _get_entity_from(args)

    # find it and download it
    staged_model = f"{entity}/{args.from_project}/{args.staged_model_name}:latest"
    artifact = download_artifact(staged_model, prod_staging_directory)
    print_info(artifact)
    return


def get_logging_run(artifact):
    api_run = artifact.logged_by()
    return api_run


def print_info(artifact, run=None):
    if run is None:
        run = get_logging_run(artifact)

    full_artifact_name = f"{artifact.entity}/{artifact.project}/{artifact.name}"
    print(f"Using artifact {full_artifact_name}")
    artifact_url_prefix = f"https://wandb.ai/{artifact.entity}/{artifact.project}/artifacts/{artifact.type}"
    artifact_url_suffix = f"{artifact.name.replace(':', '/')}"
    print(f"View at URL: {artifact_url_prefix}/{artifact_url_suffix}")

    print(f"Logged by {run.name} -- {run.project}/{run.entity}/{run.id}")
    print(f"View at URL: {run.url}")


def get_checkpoint_metadata(run, checkpoint):
    config = run.config
    out = {"config": config}
    try:
        ckpt_filename = checkpoint.metadata["original_filename"]
        out["original_filename"] = ckpt_filename
        metric_key = checkpoint.metadata["ModelCheckpoint"]["monitor"]
        metric_score = checkpoint.metadata["score"]
        out[metric_key] = metric_score
    except KeyError:
        pass
    return out


def download_artifact(artifact_path, target_directory):
    """Downloads the artifact at artifact_path to the target directory."""
    if wandb.run is not None:  # if we are inside a W&B run, track that we used this artifact
        artifact = wandb.use_artifact(artifact_path)
    else:  # otherwise, just download the artifact via the API
        artifact = api.artifact(artifact_path)
    artifact.download(root=target_directory)

    return artifact


def _get_entity_from(args):
    entity = args.entity
    if entity is None:
        raise RuntimeError(f"No entity argument provided. Use --entity=DEFAULT to use {DEFAULT_ENTITY}.")
    elif entity == "DEFAULT":
        entity = DEFAULT_ENTITY

    return entity


def _setup_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--entity",
        type=str,
        default=None,
        help=f"Entity from which to download the checkpoint. Note that checkpoints are always uploaded to the logged-in wandb entity. Pass the value 'DEFAULT' to also download from default entity, which is currently {DEFAULT_ENTITY}.",
    )
    parser.add_argument(
        "--from_project",
        type=str,
        default=DEFAULT_FROM_PROJECT,
        help=f"Project from which to download the staged model artifact. Default is {DEFAULT_FROM_PROJECT}",
    )
    parser.add_argument(
        "--staged_model_name",
        type=str,
        default=DEFAULT_STAGED_MODEL_NAME,
        help=f"Name of the staged model artifact. Default is '{DEFAULT_STAGED_MODEL_NAME}'.",
    )
    return parser


if __name__ == "__main__":
    parser = _setup_parser()
    args = parser.parse_args()
    main(args)
