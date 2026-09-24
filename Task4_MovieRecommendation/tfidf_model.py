import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load prepared movie data
movies = pd.read_csv("data/movies_prepared.csv")

# Create TF-IDF vectorizer
tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

# Convert movie tags into numerical vectors
tfidf_matrix = tfidf.fit_transform(movies["tags"])

print("MOVIEMIND AI - TF-IDF MODEL")
print("=" * 50)

print("Number of movies:", tfidf_matrix.shape[0])
print("Number of features:", tfidf_matrix.shape[1])
print("TF-IDF matrix shape:", tfidf_matrix.shape)

print("\nTF-IDF vectorization completed successfully! 🎬🧠")