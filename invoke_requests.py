"""Runs a prediction on replicate.com infrastructure using requests."""
import json
import os
import requests
import time
import argparse

REPLICATE_API_URL =  "https://api.replicate.com/v1/predictions"
EXAMPLE_URL = "https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png"

def predict_replicate(args, api_url=REPLICATE_API_URL, image_url=EXAMPLE_URL):

    headers = {
            "Authorization": f"Token {str(args.token)}",
            "Content-Type": "application/json"
        }

    data = {
        "version": str(args.version),
        "input": {"image": image_url}
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(data))
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
    parser.add_argument("--token", type=str, help='pass in REPLICATE_API_TOKEN as a string', required=True)
    parser.add_argument("--version", type=str, help='pass in MODEL_VERSION as a string', required=True)
    args = parser.parse_args()

    print(predict_replicate(args))
