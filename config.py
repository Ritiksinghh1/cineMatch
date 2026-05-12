# ══════════════════════════════════════════════
#  CineMatch — config.py
#  All constants and genre definitions live here
# ══════════════════════════════════════════════

# TMDB API key
TMDB_API_KEY = "2af6a3968a0e2530ef9b05b78d116b69"

# Placeholder poster shown when TMDB has no image
PLACEHOLDER_POSTER = "https://placehold.co/500x750/13131c/8a8799?text=No+Poster"

# How many recommendations to show
NUM_RECOMMENDATIONS = 5

# ── Genre map ──────────────────────────────────────────────────────────────────
# key        → display name shown in the UI
# "tag"      → stemmed substring to look for inside the 'tags' column
# "emoji"    → pill icon
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

# Rank labels for the recommendation cards
RANK_LABELS = ["1st", "2nd", "3rd", "4th", "5th"]