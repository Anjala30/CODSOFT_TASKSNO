import pandas as pd

# Load datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Merge both datasets
movies = movies.merge(
    credits,
    left_on="id",
    right_on="movie_id",
    how="left"
)

# Features we will use for AI recommendations
features = ["genres", "keywords", "overview", "cast", "crew"]

print("\nMOVIEMIND AI - DATA QUALITY CHECK")
print("=" * 50)

for feature in features:
    missing = movies[feature].isna().sum()
    total = len(movies)
    available = total - missing

    print(f"\n{feature.upper()}")
    print(f"Available: {available}/{total}")
    print(f"Missing:   {missing}/{total}")

print("\n" + "=" * 50)
print("SAMPLE MOVIE")
print("=" * 50)

sample = movies.iloc[0]

print("Title:", sample["title_x"])
print("Genres:", sample["genres"])
print("Keywords:", sample["keywords"])
print("Overview:", sample["overview"])
print("Cast:", sample["cast"])
print("Crew:", sample["crew"])