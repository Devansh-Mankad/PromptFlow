from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "tinybert_intent"
)

# Intent Classifier
class IntentClassifier:
    def __init__(self):
        """
        Load tokenizer and trained TinyBERT model once.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_DIR
        )

        self.model.to("cpu")
        self.model.eval()
        self.id2label = self.model.config.id2label

    # Disable gradient computation during inference to reduce memory usage and improve prediction speed.
    @torch.no_grad() 
    def predict(self, text: str) -> dict:
        """
        Predict user intent.
        Parameters
        ----------
        text : str
            User input.
        Returns
        -------
        dict
        """

        inputs = self.tokenizer(text,return_tensors="pt",truncation=True,max_length=64,)
        outputs = self.model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        confidence, prediction = torch.max(probabilities, dim=1)

        return {
            "intent": self.id2label[prediction.item()],
            "confidence": float(round(confidence.item(), 4)),
        }


# Singleton Instance : Create a single shared instance to load the TinyBERT model only once.
intent_classifier = IntentClassifier()


def classify_intent(text: str) -> dict:
    """
    Convenience wrapper.
    Example
    -------
    classify_intent("Hello")

    Returns
    -------
    {
        "intent": "GREETING",
        "confidence": 0.9982
    }
    """
    return intent_classifier.predict(text)