# ══════════════════════════════════════════════
#  CineMatch — app.py  (Streamlit UI entry point)
# ══════════════════════════════════════════════

import streamlit as st
from utils import load_data, load_css, recommend, get_filtered_movies
from config import GENRES, RANK_LABELS, NUM_RECOMMENDATIONS

# ── Page config ────────────────────────────────
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css("style.css")

# ── Load data ──────────────────────────────────
movies, similarity = load_data()

# ── Session state defaults ─────────────────────
if "active_genre" not in st.session_state:
    st.session_state.active_genre = "All"
if "results" not in st.session_state:
    st.session_state.results = None

# ══════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">✦ AI-Powered Discovery</div>
  <h1 class="hero-title">CineMatch</h1>
  <p class="hero-sub">Tell us one film you love — we'll find five more you'll adore.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  GENRE FILTER
# ══════════════════════════════════════════════
st.markdown('<div class="section-label">Filter by Genre</div>', unsafe_allow_html=True)

genre_cols = st.columns(len(GENRES))
for col, (genre, meta) in zip(genre_cols, GENRES.items()):
    with col:
        label = f"{meta['emoji']} {genre}"
        if st.button(label, key=f"genre_{genre}"):
            st.session_state.active_genre = genre
            st.session_state.results = None

active_genre = st.session_state.active_genre
active_meta  = GENRES[active_genre]

if active_genre != "All":
    st.markdown(
        f'<div class="genre-badge-wrap">Showing: '
        f'<span class="genre-badge">{active_meta["emoji"]} {active_genre}</span></div>',
        unsafe_allow_html=True,
    )

# ── Filtered movie list ────────────────────────
filtered_df = get_filtered_movies(movies, active_meta["tag"])
movie_list  = sorted(filtered_df["title"].tolist())

# ══════════════════════════════════════════════
#  SEARCH + RECOMMEND
# ══════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem;">Pick a Movie</div>', unsafe_allow_html=True)

col_select, col_btn = st.columns([4, 1])

with col_select:
    selected_movie = st.selectbox(
        "Movie",
        movie_list,
        index=0,
        label_visibility="collapsed",
    )

with col_btn:
    st.markdown('<div class="recommend-btn">', unsafe_allow_html=True)
    go = st.button("✦ Recommend", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Run recommendation ─────────────────────────
if go:
    with st.spinner("Finding your perfect matches…"):
        names, posters, scores = recommend(
            selected_movie, movies, similarity, filtered_df
        )
    st.session_state.results = (selected_movie, names, posters, scores)

# ══════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════
if st.session_state.results:
    title_movie, names, posters, scores = st.session_state.results

    if names:
        st.markdown(f"""
        <div class="results-header">
          <div class="results-header-line"></div>
          <div class="results-header-text">Because you liked &nbsp;<strong style="color:var(--accent)">{title_movie}</strong></div>
          <div class="results-header-line"></div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(NUM_RECOMMENDATIONS)
        for col, name, poster, score, rank in zip(cols, names, posters, scores, RANK_LABELS):
            with col:
                st.markdown(f"""
                <div class="movie-card">
                  <img src="{poster}" alt="{name}" loading="lazy"
                       onerror="this.src='https://placehold.co/500x750/13131c/8a8799?text=No+Poster'"/>
                  <div class="movie-card-body">
                    <div class="movie-rank">{rank} match · {score}%</div>
                    <div class="movie-title">{name}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="no-results">
          😕 No matches found in this genre. Try a different filter.
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════
st.markdown("""
<div class="footer">
  Made with ❤️ · Powered by <strong>TMDB</strong> &amp; content-based filtering
</div>
""", unsafe_allow_html=True)
