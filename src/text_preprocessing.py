import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required resources (only the first time)
nltk.download("stopwords")
nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Split into words
    words = text.split()

    # Remove stopwords and lemmatize
    cleaned_words = []

    for word in words:

        if word not in stop_words:

            cleaned_words.append(lemmatizer.lemmatize(word))

    return " ".join(cleaned_words)
if __name__ == "__main__":
    sample = "I absolutely LOVED this Product!!! It was AMAZING 😍"
    print(preprocess_text(sample))