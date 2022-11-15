"""Runs a prediction on banana.dev infrastructure using requests."""
import json
import os
import requests

from dotenv import load_dotenv

BANANA_API_URL = "https://api.banana.dev"
INFER_ROUTE = f"{BANANA_API_URL}/start/v4"
CHECK_ROUTE = f"{BANANA_API_URL}/check/v4"
EXAMPLE_URL = "https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png"


def predict_banana(api_key, model_key, image_url=EXAMPLE_URL):

    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"apiKey": api_key, "modelKey": model_key, "modelInputs": {"image": image_url}})

    done = False
    response = requests.post(INFER_ROUTE, data=payload, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    call_id = response_json["callID"]
    check_payload = json.dumps({"apiKey": api_key, "callID": call_id, "longPoll": True})

    while not done:
        if response_json["modelOutputs"] is not None:  
            done = True
        else:
            response = requests.post(CHECK_ROUTE, data=check_payload, headers=headers)
            response_json = response.json()

    prediction = response_json["modelOutputs"][0]["pred"]

    return prediction


def _setup_secrets():
    load_dotenv()  # get environment variables

    api_key = os.environ["BANANA_API_KEY"]
    assert api_key is not None, "define $BANANA_API_KEY to perform remote inference"

    model_key = os.environ["BANANA_MODEL_KEY"]
    assert model_key is not None, "define $BANANA_MODEL_KEY to perform remote inference"

    return api_key, model_key


if __name__ == "__main__":
    print(predict_banana(*_setup_secrets()))
