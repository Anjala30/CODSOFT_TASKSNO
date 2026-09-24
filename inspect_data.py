import pandas as pd

# Load the movie datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Basic information
print("MOVIES DATASET")
print("=" * 50)
print("Rows:", len(movies))
print("Columns:")
print(movies.columns.tolist())

print("\n\nCREDITS DATASET")
print("=" * 50)
print("Rows:", len(credits))
print("Columns:")
print(credits.columns.tolist())

# Show first 3 rows
print("\n\nFIRST 3 MOVIES")
print("=" * 50)
print(movies.head(3).to_string())

print("\n\nFIRST 3 CREDIT RECORDS")
print("=" * 50)
print(credits.head(3).to_string())