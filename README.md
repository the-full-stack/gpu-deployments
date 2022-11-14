## REST API:
```bash
BANANA_API_URL=https://api.banana.dev
INFER_ROUTE=$BANANA_API_URL/start/v4

curl -X POST \
	-H "Content-Type: application/json" \
	-d '{"apiKey": "your-banana-api-key-here", "modelKey": "your-model-key-here", "modelInputs": {"image": "https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png"}}' \
  $INFER_ROUTE
```
