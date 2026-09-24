import pandas as pd
import ast

# Load datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Rename credits movie ID column
credits = credits.rename(columns={
    "movie_id": "id",
    "title": "credit_title"
})

# Merge movies and credits
movies = movies.merge(credits, on="id")

# Keep only required columns
movies = movies[
    ["id", "title", "genres", "keywords", "overview", "cast", "crew"]
]

# Convert JSON-like columns into readable names
def extract_names(value):
    try:
        data = ast.literal_eval(value)
        return " ".join(item["name"] for item in data)
    except:
        return ""


movies["genres"] = movies["genres"].apply(extract_names)
movies["keywords"] = movies["keywords"].apply(extract_names)
movies["cast"] = movies["cast"].apply(extract_names)

# Extract director from crew
def extract_director(value):
    try:
        data = ast.literal_eval(value)
        for item in data:
            if item["job"] == "Director":
                return item["name"]
        return ""
    except:
        return ""


movies["crew"] = movies["crew"].apply(extract_director)

# Handle missing overview
movies["overview"] = movies["overview"].fillna("")

# Create combined AI feature
movies["tags"] = (
    movies["genres"] + " " +
    movies["keywords"] + " " +
    movies["overview"] + " " +
    movies["cast"] + " " +
    movies["crew"]
)

# Convert to lowercase
movies["tags"] = movies["tags"].str.lower()

print("MOVIEMIND AI - DATA PREPARATION")
print("=" * 50)
print("Total movies:", len(movies))
print("Columns:", movies.columns.tolist())
print("\nSample movie:")
print("Title:", movies.iloc[0]["title"])
print("Tags:", movies.iloc[0]["tags"][:500])

# Save prepared dataset
movies.to_csv("data/movies_prepared.csv", index=False)

print("\nPrepared dataset saved successfully!")