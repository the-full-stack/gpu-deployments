# Prediction interface for Cog ⚙️
from cog import BasePredictor, Input, Path

from text_recognizer.paragraph_text_recognizer import ParagraphTextRecognizer


class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        self.model = ParagraphTextRecognizer()

    def predict(
        self,
        image: Path = Input(description="Input image of handwritten text"),
    ) -> str:
        """Run a single prediction on the model"""
        text = self.model.predict(image)
        return text
