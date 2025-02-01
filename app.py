from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
app = Flask(_name_)
CORS(app)  # Allow frontend requests

# Load NLP models (Replace with BERT/T5-based models if needed)
grammar_checker = pipeline("text-classification", model="textattack/bert-base-uncased-imdb")
summarizer = pipeline("summarization")

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Simulated grammar feedback (replace with actual NLP model)
    grammar_result = grammar_checker(text[:512])  # Limiting text length
    grammar_feedback = "Good grammar" if grammar_result[0]["label"] == "POSITIVE" else "Needs improvement."

    # Summarization (simulating readability feedback)
    summary = summarizer(text[:1024], max_length=100, min_length=30, do_sample=False)
    readability_feedback = summary[0]["summary_text"]

    # Vocabulary suggestion (Placeholder)
    vocab_feedback = "Consider using more varied synonyms."

    return jsonify({
        "grammar": grammar_feedback,
        "readability": readability_feedback,
        "vocabulary": vocab_feedback
    })

if _name_ == "_main_":
    app.run(debug=True)