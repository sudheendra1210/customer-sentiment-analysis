from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
import joblib

from src.text_preprocessing import preprocess_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


def read_csv_safely(filepath):
    encodings = [
        "utf-8",
        "utf-8-sig",
        "latin1",
        "cp1252",
        "ISO-8859-1",
    ]

    last_error = None

    for encoding in encodings:
        try:
            print(f"Trying encoding: {encoding}")
            return pd.read_csv(filepath, encoding=encoding)

        except UnicodeDecodeError as e:
            last_error = e
            continue

    raise ValueError(
        "Unable to read the CSV. Please save it as UTF-8 CSV and try again."
    ) from last_error


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

    review = data.get("review", "")

    clean_review = preprocess_text(review)

    review_vector = vectorizer.transform([clean_review])

    prediction = model.predict(review_vector)[0]

    probabilities = model.predict_proba(review_vector)[0]

    confidence = round(max(probabilities) * 100, 2)

    return jsonify({
        "prediction": prediction,
        "confidence": confidence
    })


@app.route("/upload_csv", methods=["POST"])
def upload_csv():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)

    try:
        df = read_csv_safely(filepath)

    except ValueError as e:

        return jsonify({"error": str(e)}), 400

    # -----------------------------
    # Detect Review Column
    # -----------------------------

    df.columns = df.columns.str.strip()

    print("\nDetected Columns:")

    for column in df.columns:
        print(f"• {column}")

    preferred_columns = [
        "Review",
        "reviewText",
        "reviews.text",
        "review"
    ]

    review_column = None

    for col in preferred_columns:

        if col in df.columns:

            review_column = col

            break

    if review_column is None:

        for col in df.columns:

            lower = col.lower()

            if "reviewer" in lower:
                continue

            if "review" in lower:

                review_column = col

                break

    if review_column is None:

        return jsonify({
            "error": "No review column found in the uploaded CSV."
        }), 400

    print(f"\nUsing review column: {review_column}")

    # -----------------------------
    # Clean Reviews
    # -----------------------------

    df[review_column] = (
        df[review_column]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df = df[df[review_column] != ""].copy()

    if df.empty:

        return jsonify({
            "error": "No valid reviews found."
        }), 400

    clean_reviews = df[review_column].apply(preprocess_text)

    # -----------------------------
    # Predict
    # -----------------------------

    vectors = vectorizer.transform(clean_reviews)

    predictions = model.predict(vectors).tolist()

    df["Prediction"] = predictions

    # -----------------------------
    # Counts
    # -----------------------------

    positive = predictions.count("positive")
    neutral = predictions.count("neutral")
    negative = predictions.count("negative")

    total = len(predictions)

    positive_percent = round((positive / total) * 100, 1)
    neutral_percent = round((neutral / total) * 100, 1)
    negative_percent = round((negative / total) * 100, 1)

    # -----------------------------
    # Save CSV
    # -----------------------------

    output_filename = "analyzed_" + file.filename

    output_path = os.path.join(
        UPLOAD_FOLDER,
        output_filename
    )

    df.to_csv(output_path, index=False)

    return jsonify({

        "message": "CSV analyzed successfully!",

        "positive": positive,
        "neutral": neutral,
        "negative": negative,

        "positive_percent": positive_percent,
        "neutral_percent": neutral_percent,
        "negative_percent": negative_percent,

        "download": f"/download/{output_filename}"

    })


@app.route("/download/<filename>")
def download(filename):

    return send_file(

        os.path.join(
            UPLOAD_FOLDER,
            filename
        ),

        as_attachment=True

    )


if __name__ == "__main__":
    app.run(debug=True)