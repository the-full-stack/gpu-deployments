from text_recognizer.paragraph_text_recognizer import ParagraphTextRecognizer


# 🍌: init is run on server startup
# 🍌: load your model to GPU as a global variable here using the variable name "model"
def init():
    global model

    model = ParagraphTextRecognizer()


# 🍌: inference is run for every server call
# 🍌: reference your preloaded global model variable here.
def inference(model_inputs: dict) -> dict:
    global model

    # 🍌: parse inputs
    image_url = model_inputs["image"]

    # 🍌: run the model
    result = model.predict(image_url)

    # 🍌: return the results as a dictionary
    result = {"pred": result}

    return result
