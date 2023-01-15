"""Runs a prediction on replicate.com infrastructure using requests."""
import json
import os
import requests
import time

from dotenv import load_dotenv

# load_dotenv()  # get environment variables

# replicate_api_token = os.environ["REPLICATE_API_TOKEN"]

# print(f"Token {replicate_api_token}")


REPLICATE_API_URL =  "https://api.replicate.com/v1/predictions"
EXAMPLE_URL = "https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png"

def predict_replicate(api_token, model_version, image_url=EXAMPLE_URL):

    print(f"Token {api_token}")
    print(f"Version {model_version}")

    headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        }

    data = {
        "version": model_version,
        "input": {"image": image_url}
    }

    response = requests.post(REPLICATE_API_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()

    if response.status_code == 201:
        get_url = response.json()["urls"]["get"]

        prediction = _get_from_replicate(get_url, headers)

        return prediction


def _get_from_replicate(get_url, headers):
    awaiting_prediction = True

    while awaiting_prediction:
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()

        if response.json()["status"] == "succeeded":
            prediction = response.json()["output"]

            awaiting_prediction = False

            return prediction

        if awaiting_prediction:
            time.sleep(0.5)


def _setup_secrets():
    load_dotenv()  # get environment variables

    replicate_api_token = os.environ["REPLICATE_API_TOKEN"]
    assert replicate_api_token is not None, "define $REPLICATE_API_TOKEN to perform remote inference"

    model_version = os.environ["MODEL_VERSION"]
    assert model_version is not None, "define $MODEL_VERSION to perform remote inference"

    return replicate_api_token, model_version


if __name__ == "__main__":
    print(predict_replicate(*_setup_secrets()))
