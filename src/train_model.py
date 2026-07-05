import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from load_data import load_dataset
from text_preprocessing import preprocess_text

print("Loading dataset...")

df = load_dataset()

print("Cleaning reviews...")

df["clean_review"] = df["Review"].apply(preprocess_text)

X = df["clean_review"]
y = df["Sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nConverting reviews into numerical vectors...")

vectorizer = TfidfVectorizer(max_features=5000)

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print("TF-IDF Completed!")
print("Training Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)

print("\nTraining Logistic Regression Model...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced")

model.fit(X_train, y_train)

print("Model Training Completed!")

print("\nMaking Predictions...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:\n")

print(classification_report(y_test, predictions, zero_division=0))
# Save the trained model
joblib.dump(model, "models/model.pkl")

# Save the TF-IDF vectorizer
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\nModel and Vectorizer saved successfully!")