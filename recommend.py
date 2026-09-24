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

tfidf_matrix = tfidf.fit_transform(movies["tags"])


# Calculate cosine similarity
similarity_matrix = cosine_similarity(tfidf_matrix)


# Recommendation function
def recommend_movies(movie_title, number_of_recommendations=5):

    # Find selected movie
    movie_index = movies[
        movies["title"].str.lower() == movie_title.lower()
    ].index

    if len(movie_index) == 0:
        return []

    movie_index = movie_index[0]

    # Get similarity scores
    similarity_scores = list(
        enumerate(similarity_matrix[movie_index])
    )

    # Sort by similarity
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove selected movie
    similarity_scores = similarity_scores[
        1:number_of_recommendations + 1
    ]

    recommendations = []

    for index, score in similarity_scores:

        recommendations.append({
            "title": movies.iloc[index]["title"],
            "similarity": round(score * 100, 2)
        })

    return recommendations


# Test the recommendation system
if __name__ == "__main__":

    results = recommend_movies("Avatar", 5)

    print("\nMOVIEMIND AI - RECOMMENDATIONS")
    print("=" * 50)
    print("Based on: Avatar\n")

    for rank, movie in enumerate(results, start=1):

        print(
            f"{rank}. {movie['title']} "
            f"| Similarity: {movie['similarity']:.2f}%"
        )