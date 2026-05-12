# ══════════════════════════════════════════════
#  CineMatch — utils.py
#  Data loading, poster fetching, recommender
# ══════════════════════════════════════════════

import os
import re
import pickle
import requests
import pandas as pd
import streamlit as st

from config import TMDB_API_KEY, PLACEHOLDER_POSTER, NUM_RECOMMENDATIONS, SIMILARITY_GDRIVE_ID


# ── Google Drive Downloader ───────────────────────────────────────────────────

def download_from_gdrive(file_id: str, dest_path: str):
    """Download a large file from Google Drive, handling the virus-scan warning."""

    session = requests.Session()
    URL = "https://drive.google.com/uc?export=download"

    response = session.get(URL, params={"id": file_id}, stream=True)

    # Extract confirmation token from cookies (older GDrive behaviour)
    token = None
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break

    # Newer GDrive: confirmation token embedded in HTML body
    if not token:
        for chunk in response.iter_content(chunk_size=32768):
            match = re.search(rb"confirm=([0-9A-Za-z_\-]+)", chunk)
            if match:
                token = match.group(1).decode()
            break

    response = session.get(
        URL,
        params={"id": file_id, "confirm": token or "t"},
        stream=True,
    )

    total = int(response.headers.get("content-length", 0))
    progress = st.progress(0, text="Downloading similarity matrix… (first run only)")
    downloaded = 0

    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = min(int(downloaded / total * 100), 100)
                    progress.progress(pct, text=f"Downloading similarity matrix… {pct}%")

    progress.empty()


# ── Data Loading ──────────────────────────────────────────────────────────────

@st.cache_resource
def load_data():
    """
    Load movies DataFrame and similarity matrix.
    similarity.pkl is downloaded from Google Drive on first run if not present.
    """

    with open("movies.pkl", "rb") as f:
        movies = pickle.load(f)

    sim_path = "similarity.pkl"
    if not os.path.exists(sim_path):
        st.info("⏳ First-time setup: downloading similarity matrix…")
        download_from_gdrive(SIMILARITY_GDRIVE_ID, sim_path)

    with open(sim_path, "rb") as f:
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
    return movies[movies["tags"].str.contains(tag, case=False, na=False)]


# ── Recommendation System ────────────────────────────────────────────────────

def recommend(movie_title, movies, similarity, filtered_df):
    """Recommend similar movies. Returns: names, posters, scores"""

    if movie_title not in movies["title"].values:
        return [], [], []

    idx = movies[movies["title"] == movie_title].index[0]
    distances = sorted(enumerate(similarity[idx]), reverse=True, key=lambda x: x[1])

    results = []
    seen = set()

    for i, score in distances[1:]:
        if filtered_df is not movies and i not in filtered_df.index:
            continue
        row = movies.iloc[i]
        if row["title"] in seen:
            continue
        results.append((row["title"], int(row["movie_id"]), round(score * 100, 1)))
        seen.add(row["title"])
        if len(results) == NUM_RECOMMENDATIONS:
            break

    names, posters, scores = [], [], []
    for title, movie_id, score in results:
        names.append(title)
        posters.append(fetch_poster(movie_id))
        scores.append(score)

    return names, posters, scores