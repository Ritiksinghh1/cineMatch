# ══════════════════════════════════════════════
#  CineMatch — config.py
#  All constants and genre definitions live here
# ══════════════════════════════════════════════

import os

# TMDB API key — set via Streamlit secrets or environment variable
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "2af6a3968a0e2530ef9b05b78d116b69")

# ── Google Drive file ID for similarity.pkl ────────────────────────────────────
# Get this from your Google Drive share link:
# https://drive.google.com/file/d/YOUR_FILE_ID_HERE/view
# Paste just the ID below:
SIMILARITY_GDRIVE_ID = "1VlBwBIyWFqng3w_VaPkATwXVv3ZzqJZG"

# Placeholder poster shown when TMDB has no image
PLACEHOLDER_POSTER = "https://placehold.co/500x750/13131c/8a8799?text=No+Poster"

# How many recommendations to show
NUM_RECOMMENDATIONS = 5

# ── Genre map ──────────────────────────────────────────────────────────────────
GENRES: dict[str, dict] = {
    "All":         {"tag": None,           "emoji": "🎬"},
    "Action":      {"tag": "action",       "emoji": "💥"},
    "Thriller":    {"tag": "thriller",     "emoji": "😰"},
    "Drama":       {"tag": "drama",        "emoji": "🎭"},
    "Horror":      {"tag": "horror",       "emoji": "👻"},
    "Sci-Fi":      {"tag": "sciencefict",  "emoji": "🚀"},
    "Romance":     {"tag": "romanc",       "emoji": "❤️"},
    "Adventure":   {"tag": "adventur",     "emoji": "🗺️"},
    "Comedy":      {"tag": "comedi",       "emoji": "😂"},
}

# Rank labels for recommendation cards
RANK_LABELS = ["1st", "2nd", "3rd", "4th", "5th"]