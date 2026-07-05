from flask import Flask, render_template, request
import joblib

from src.text_preprocessing import preprocess_text

app = Flask(__name__)

# Load trained model and vectorizer
model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    review = request.form["review"]

    clean_review = preprocess_text(review)

    review_vector = vectorizer.transform([clean_review])

    prediction = model.predict(review_vector)[0]

    return render_template(
        "index.html",
        prediction=prediction,
        review=review
    )


if __name__ == "__main__":
    app.run(debug=True)