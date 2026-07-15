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

df["combined"] = (
    df["Review"].fillna("").astype(str) + " " +
    df["Summary"].fillna("").astype(str)
)

df["clean_review"] = df["combined"].apply(preprocess_text)

X = df["clean_review"]
y = df["Sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nConverting reviews into numerical vectors...")

vectorizer = TfidfVectorizer(
    max_features=7000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print("TF-IDF Completed!")
print("Training Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)

print("\nTraining Logistic Regression Model...")

model = LogisticRegression(
    solver="lbfgs",
    max_iter=2000,
    class_weight="balanced",
    random_state=42
)

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