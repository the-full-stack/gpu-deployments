# 🍌: This file is used to verify your http server acts as expected
# 🍌: Run it with `python3 test.py``

import requests

model_inputs = {"image": "https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png"}

res = requests.post("http://localhost:8000/", json=model_inputs)

print(res.json())
