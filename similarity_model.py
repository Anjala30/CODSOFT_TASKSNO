import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load prepared movie data
movies = pd.read_csv("data/movies_prepared.csv")

# Create TF-IDF model
tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

# Convert movie tags into numerical vectors
tfidf_matrix = tfidf.fit_transform(movies["tags"])

# Calculate cosine similarity
similarity_matrix = cosine_similarity(tfidf_matrix)

print("MOVIEMIND AI - COSINE SIMILARITY")
print("=" * 50)

print("Number of movies:", similarity_matrix.shape[0])
print("Similarity matrix shape:", similarity_matrix.shape)

print("\nCosine similarity calculated successfully! 🤖🎬")