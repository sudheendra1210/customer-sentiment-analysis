import joblib 
from text_preprocessing import preprocess_text

print("Loading trained model...")

model = joblib.load("models/model.pkl")

vectorizer = joblib.load("models/vectorizer.pkl")

print("Model Loaded Successfully!")

review = input("\nEnter Review: ")

clean_review = preprocess_text(review)

review_vector = vectorizer.transform([clean_review])

prediction = model.predict(review_vector)

print("\nPredicted Sentiment:", prediction[0])