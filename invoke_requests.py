"""Runs a prediction on replicate.com infrastructure using requests."""
import json
import os
import requests
import time
import argparse


REPLICATE_API_URL = "https://api.replicate.com/v1/predictions"
EXAMPLE_URL = "https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png"

def predict_replicate(api_token, model_version, image_url=EXAMPLE_URL):

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_token", type=str, help="A token for api.replicate.com", required=True)
    parser.add_argument("--model_version", type=str, help="The version identifier for your model", required=True)
    args = vars(parser.parse_args())

    print(predict_replicate(**args))
