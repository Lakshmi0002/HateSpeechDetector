# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KU3PMuRnZwn8e5Ikt_4j6SvlVQUQlArG
"""

from flask import Flask, request, render_template
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the fine-tuned HateBERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_hatebert")
model = AutoModelForSequenceClassification.from_pretrained("./fine_tuned_hatebert")

app = Flask(__name__)

# Function to classify input text
def classify_text(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # Get predictions
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    # Map prediction to label
    label = "Non-Bullying" if predicted_class == 0 else "Bullying"
    return label

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        text_input = request.form['text_input']
        result = classify_text(text_input)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)