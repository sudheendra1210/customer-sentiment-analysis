from flask import Flask, render_template, request, jsonify
from nltk import data
from flask import send_file
import pandas as pd
import os
import joblib

from src.text_preprocessing import preprocess_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


@app.route("/")
def home():
    return render_template(
        "index.html",
        prediction=None,
        review=""
    )


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    review = data["review"]

    clean_review = preprocess_text(review)

    print("Original:", review)
    print("Processed:", clean_review)

    review_vector = vectorizer.transform([clean_review])

    prediction = model.predict(review_vector)[0]

    return jsonify({
        "prediction": prediction
    })


@app.route("/upload_csv", methods=["POST"])
def upload_csv():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"})

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)

    # ============================
    # Read CSV
    # ============================

    df = pd.read_csv(filepath)

    # Make sure Review column exists
    if "Review" not in df.columns:
        return jsonify({
            "error": "CSV must contain a 'Review' column."
        })

    # ============================
    # Predict Every Review
    # ============================

    predictions = []

    for review in df["Review"]:

        clean = preprocess_text(str(review))

        vector = vectorizer.transform([clean])

        prediction = model.predict(vector)[0]

        predictions.append(prediction)

    # Add new column
    df["Prediction"] = predictions

    # ============================
    # Count Predictions
    # ============================

    positive = predictions.count("positive")
    neutral = predictions.count("neutral")
    negative = predictions.count("negative")

    # ============================
    # Save Result CSV
    # ============================

    output_path = os.path.join(
        UPLOAD_FOLDER,
        "analyzed_" + file.filename
    )

    df.to_csv(output_path, index=False)

    return jsonify({

        "message": "CSV analyzed successfully!",

        "positive": positive,

        "neutral": neutral,

        "negative": negative,

        "download": output_path

    })
@app.route("/download")
def download():

    return send_file(
        os.path.join(
            UPLOAD_FOLDER,
            "analyzed_flipkart.csv"
        ),
        as_attachment=True
    )
if __name__ == "__main__":
    app.run(debug=True)