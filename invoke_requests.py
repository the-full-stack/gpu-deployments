"""Runs a prediction on replicate.com infrastructure using requests."""
import json
import os
import requests
import time


REPLICATE_API_URL = "https://api.replicate.com/v1/predictions"

MODEL_VERSION = "04014ed6998f36e9ed94f9d90bc5ff8bdc379a454b119111ceab3a8d158005fa"
EXAMPLE_URL = "https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png"
REPLICATE_API_TOKEN = os.environ["REPLICATE_API_TOKEN"]

HEADERS = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }


def predict_replicate(image_url=EXAMPLE_URL):

    data = {
        "version": MODEL_VERSION,
        "input": {"image": image_url}
    }

    response = requests.post(REPLICATE_API_URL, headers=HEADERS, data=json.dumps(data))
    response.raise_for_status()

    if response.status_code == 201:
        get_url = response.json()["urls"]["get"]

        prediction = _get_from_replicate(get_url)

        return prediction


def _get_from_replicate(get_url):
    awaiting_prediction = True

    while awaiting_prediction:
        response = requests.get(get_url, headers=HEADERS)
        response.raise_for_status()

        if response.json()["status"] == "succeeded":
            prediction = response.json()["output"]

            awaiting_prediction = False

            return prediction

        if awaiting_prediction:
            time.sleep(0.5)


if __name__ == "__main__":
    print(predict_replicate())
