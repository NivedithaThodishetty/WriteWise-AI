from flask import Flask, request, jsonify
from flask_cors import CORS
import language_tool_python
import textstat
from transformers import pipeline

app = Flask(_name_)
CORS(app)

# Load grammar checker
tool = language_tool_python.LanguageTool("en-US")

# Load summarization model (for readability feedback)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def check_grammar(text):
    matches = tool.check(text)
    if not matches:
        return "No grammatical issues detected."
    feedback = [match.ruleIssueType + ": " + match.message for match in matches[:5]]
    return " | ".join(feedback)

def analyze_readability(text):
    score = textstat.flesch_kincaid_grade(text)
    if score <= 6:
        return "Very easy to read (suitable for younger audiences)."
    elif score <= 10:
        return "Moderate readability (good for general writing)."
    else:
        return "Complex text, consider simplifying sentence structures."

def suggest_vocabulary(text):
    return "Consider using synonyms for commonly repeated words."

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    grammar_feedback = check_grammar(text)
    readability_feedback = analyze_readability(text)
    vocab_feedback = suggest_vocabulary(text)

    return jsonify({
        "grammar": grammar_feedback,
        "readability": readability_feedback,
        "vocabulary": vocab_feedback
    })

if _name_ == "_main_":
    app.run(debug=True)