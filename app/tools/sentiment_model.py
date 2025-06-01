# app/tools/sentiment_model.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

MODEL_NAME = "ProsusAI/finbert"

# Load tokenizer and model (do this once per container)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

LABELS = ["negative", "neutral", "positive"]

def get_sentiment_score(text: str) -> dict:
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return dict(zip(LABELS, probs[0].detach().numpy().tolist()))
