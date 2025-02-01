import streamlit as st
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK tokenizer
nltk.download('punkt')

# Load models from Hugging Face
@st.cache_resource
def load_models():
    grammar_model = pipeline("fill-mask", model="bert-base-uncased")
    suggestion_model_name = "t5-small"
    suggestion_model = AutoModelForSeq2SeqLM.from_pretrained(suggestion_model_name)
    suggestion_tokenizer = AutoTokenizer.from_pretrained(suggestion_model_name)
    return grammar_model, suggestion_model, suggestion_tokenizer

grammar_model, suggestion_model, suggestion_tokenizer = load_models()

# Streamlit UI
st.title("WriteWise: Essay and Assignment Feedback Tool")
st.markdown("Leverage the power of **BERT** and **T5** to enhance your writing!")

# Text Input
text_input = st.text_area("Paste your essay or assignment here:", height=300)

# Buttons for user actions
if st.button("Analyze Text"):
    if text_input.strip():
        st.subheader("Grammatical Analysis")
        sentences = sent_tokenize(text_input)
        for i, sentence in enumerate(sentences):
            masked_sentence = sentence.replace(".", " [MASK].")  # Add mask for BERT
            result = grammar_model(masked_sentence)
            suggestion = result[0]['sequence']
            st.write(f"**Sentence {i+1}:** {sentence}")
            st.write(f"**Suggestion:** {suggestion}")
        
        st.subheader("Suggestions for Improvement")
        input_ids = suggestion_tokenizer.encode("improve: " + text_input, return_tensors="pt", max_length=512, truncation=True)
        output = suggestion_model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
        improved_text = suggestion_tokenizer.decode(output[0], skip_special_tokens=True)
        st.write(improved_text)
    else:
        st.warning("Please enter some text to analyze.")

# Readability Score
if st.button("Evaluate Readability"):
    if text_input.strip():
        st.subheader("Readability Assessment")
        word_count = len(text_input.split())
        sentence_count = len(sent_tokenize(text_input))
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        st.write(f"**Total Words:** {word_count}")
        st.write(f"**Total Sentences:** {sentence_count}")
        st.write(f"**Average Words per Sentence:** {avg_words_per_sentence:.2f}")
        st.write("**Readability Level:**", "Intermediate" if avg_words_per_sentence <= 20 else "Advanced")
    else:
        st.warning("Please enter some text to evaluate.")