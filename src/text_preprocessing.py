import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required resources (only the first time)
nltk.download("stopwords")
nltk.download("wordnet")

# Stopwords
stop_words = set(stopwords.words("english"))

# Keep negation words because they are important for sentiment
negation_words = {
    "not",
    "no",
    "nor",
    "never",
    "don't",
    "dont",
    "didn't",
    "didnt",
    "isn't",
    "isnt",
    "wasn't",
    "wasnt",
    "couldn't",
    "couldnt",
    "wouldn't",
    "wouldnt",
    "shouldn't",
    "shouldnt"
}

stop_words = stop_words - negation_words

# Lemmatizer
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):

    if text is None:
        return ""

    text = str(text).lower()

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Split into words
    words = text.split()

    cleaned_words = []

    for word in words:

        if word not in stop_words:
            cleaned_words.append(
                lemmatizer.lemmatize(word)
            )

    return " ".join(cleaned_words)


if __name__ == "__main__":

    sample = "I absolutely LOVED this Product!!! It was AMAZING 😍"

    print(preprocess_text(sample))