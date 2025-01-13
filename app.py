import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

# Initialize PorterStemmer
port_stem = PorterStemmer()

# Load the trained model
filename = 'trained_model.sav'
model = pickle.load(open(filename, 'rb'))

# Load the TfidfVectorizer (ensure it matches the one used during training)
vectorizer_filename = 'vectorizer.pkl'
vectorizer = pickle.load(open(vectorizer_filename, 'rb'))

# Define stemming function
def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

# Streamlit app title and description
st.title("Tweet Sentiment Analysis")
st.write("This application predicts the sentiment of a tweet (e.g., positive or negative) using a pre-trained Logistic Regression model.")

# Input text box for user to enter a tweet
user_input = st.text_area("Enter a tweet:", height=100)

# Prediction logic
if st.button("Predict Sentiment"):
    if user_input.strip():
        # Preprocess and vectorize the input tweet
        processed_tweet = stemming(user_input)
        tweet_vector = vectorizer.transform([processed_tweet])
        
        # Predict sentiment
        prediction = model.predict(tweet_vector)
        sentiment = "Positive" if prediction[0] == 1 else "Negative"
        
        # Display the result
        st.write(f"**Sentiment:** {sentiment}")
    else:
        st.warning("Please enter a valid tweet for prediction.")
