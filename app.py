# Install required packages first
# pip install flask pandas numpy scikit-learn nltk flask-cors

from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from flask_cors import CORS

# Download stopwords
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)  # Enable CORS

# Initialize vectorizer and stopwords
stop_words = set(stopwords.words('english'))
vectorizer = TfidfVectorizer(stop_words=list(stop_words), max_features=5000)

# Sample training data (REPLACE with actual dataset in production)
training_questions = [
    "What is the capital of France?",
    "Where is Paris located?",
    "How to learn programming?",
    "Best way to learn coding?",
    "What is machine learning?",
    "How does AI work?",
    "How to cook pasta?",
    "What are healthy foods?",
    "How to train for a marathon?",
    "What is the weather today?"
    "How to learn Python?",
    "Best way to study Python?",
    "What is Python?",
    "How to install Python?",
    "Python programming tutorial",
    "What is machine learning?",
    "How does machine learning work?",
    "AI vs machine learning",
    "How to cook pasta?",
    "What's the best pasta recipe?"

]

# Preprocess and fit vectorizer
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)  # Keep only words and spaces
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

# Preprocess training data
processed_training = [preprocess(q) for q in training_questions]
vectorizer.fit(processed_training)  # CRITICAL: Fit the vectorizer


#@app.route('/predict', methods=['POST'])
@app.route('/')
def predict():
    data = request.get_json()
    print("Received data:", data)  # Debug line
    q1 = preprocess(data['question1'])
    q2 = preprocess(data['question2'])
    
    # Vectorize questions
    q1_vec = vectorizer.transform([q1])
    q2_vec = vectorizer.transform([q2])
    
    # Calculate similarity
    similarity = cosine_similarity(q1_vec, q2_vec)[0][0]
    
    # Determine result (adjust threshold as needed)
    result = "Duplicate" if similarity > 0.6 else "Not Duplicate"
    
    return jsonify({
        'result': result,
        'similarity_score': float(similarity)  # For debugging
    })

if __name__ == '__main__':
    app.run(debug=True)