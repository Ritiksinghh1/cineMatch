# ══════════════════════════════════════════════
#  CineMatch — utils.py
#  Data loading, poster fetching, recommender
# ══════════════════════════════════════════════

import pickle
import requests
import pandas as pd
import streamlit as st

from config import TMDB_API_KEY, PLACEHOLDER_POSTER, NUM_RECOMMENDATIONS

# ── Data Loading ──────────────────────────────────────────────────────────────

@st.cache_resource
def load_data():
    """Load movies DataFrame and similarity matrix."""

    # Load movies dataframe directly
    with open("movies.pkl", "rb") as f:
        movies = pickle.load(f)

    # Load similarity matrix
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)

    return movies, similarity


# ── CSS ───────────────────────────────────────────────────────────────────────

def load_css(path="style.css"):
    """Load external CSS file."""

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            css = f.read()

        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"CSS file not loaded: {e}")


# ── TMDB Poster Fetching ─────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def fetch_poster(movie_id):
    """Fetch movie poster from TMDB."""

    try:
        url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}"
            f"?api_key={TMDB_API_KEY}&language=en-US"
        )

        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

    except Exception:
        pass

    return PLACEHOLDER_POSTER


# ── Genre Filtering ───────────────────────────────────────────────────────────

def get_filtered_movies(movies, tag=None):
    """Filter movies based on genre tag."""

    if tag is None or tag == "All":
        return movies

    return movies[
        movies["tags"].str.contains(tag, case=False, na=False)
    ]


# ── Recommendation System ────────────────────────────────────────────────────

def recommend(movie_title, movies, similarity, filtered_df):
    """
    Recommend similar movies.
    Returns:
        names, posters, scores
    """

    if movie_title not in movies["title"].values:
        return [], [], []

    idx = movies[movies["title"] == movie_title].index[0]

    distances = sorted(
        enumerate(similarity[idx]),
        reverse=True,
        key=lambda x: x[1]
    )

    results = []
    seen = set()

    for i, score in distances[1:]:

        # Skip filtered movies
        if filtered_df is not movies and i not in filtered_df.index:
            continue

        row = movies.iloc[i]

        if row["title"] in seen:
            continue

        results.append(
            (
                row["title"],
                int(row["movie_id"]),
                round(score * 100, 1)
            )
        )

        seen.add(row["title"])

        if len(results) == NUM_RECOMMENDATIONS:
            break

    names = []
    posters = []
    scores = []

    for title, movie_id, score in results:
        names.append(title)
        posters.append(fetch_poster(movie_id))
        scores.append(score)

    return names, posters, scores