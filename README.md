# 🎬 CineMatch — AI-Powered Movie Recommender

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/TMDB-API-01B4E4?style=for-the-badge&logo=themoviedatabase&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
</p>

> **Tell us one film you love — we'll find five more you'll adore.**

CineMatch is a content-based movie recommendation system built with Python and Streamlit. It analyzes a dataset of 4,800+ movies and uses cosine similarity to surface the most relevant recommendations, complete with live posters fetched from the TMDB API.

---

## ✨ Features

- 🔍 **Smart Recommendations** — Content-based filtering using cosine similarity on NLP-processed tags
- 🎭 **Genre Filters** — Filter recommendations by Action, Thriller, Drama, Horror, Sci-Fi, Romance, Adventure, or Comedy
- 🖼️ **Live Posters** — Movie posters fetched in real-time from the TMDB API
- 📊 **Match Scores** — Each recommendation shows a percentage similarity score
- 🌙 **Cinematic Dark UI** — Custom CSS with a dark, film-noir aesthetic
- ⚡ **Cached Performance** — Data and poster fetches are cached for fast repeat queries

---

---

## 🗂️ Project Structure

```
cinematch/
│
├── app.py              # Streamlit UI entry point
├── utils.py            # Data loading, poster fetching, recommender logic
├── config.py           # Constants, API key, genre definitions
├── style.css           # Custom dark-mode CSS
│
├── movies.pkl          # Preprocessed movies DataFrame (4,806 movies)
├── movie_dict.pkl      # Movie dictionary (title, id, tags)
├── similarity.pkl      # Precomputed cosine similarity matrix (4806×4806)
│
├── requirements.txt    # Python dependencies
└── README.md
```

---

## ⚙️ How It Works

1. **Data Preprocessing** — Movie metadata (genres, cast, crew, keywords, overview) is combined into a single `tags` column and stemmed using NLTK.
2. **Vectorization** — Tags are converted into vectors using `CountVectorizer` (bag-of-words).
3. **Similarity Matrix** — Cosine similarity is computed between all 4,806 movie vectors and saved as `similarity.pkl`.
4. **Recommendation** — When a user selects a movie, the app fetches the top-N most similar movies from the precomputed matrix.
5. **Poster Fetching** — Movie IDs are used to hit the TMDB API and retrieve poster images live.

```
User picks a movie
       │
       ▼
Find movie index in DataFrame
       │
       ▼
Rank all movies by cosine similarity score
       │
       ▼
Return top 5 matches (filtered by genre if selected)
       │
       ▼
Fetch posters from TMDB API → Render cards
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cinematch.git
cd cinematch
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your TMDB API key

Get a free API key from [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api) and add it to `config.py`:

```python
TMDB_API_KEY = "your_api_key_here"
```

> ⚠️ **Never commit your real API key to GitHub.** Use environment variables or a `.env` file in production.

### 4. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📦 Requirements

Create a `requirements.txt` with:

```
streamlit
requests
pandas
numpy
scikit-learn
nltk
```

---

## 📊 Dataset

Based on the **TMDB 5000 Movie Dataset** available on [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).

| Field | Detail |
|---|---|
| Total movies | 4,806 |
| Features used | genres, keywords, cast, crew, overview |
| Similarity matrix | 4,806 × 4,806 cosine similarity |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| Web Framework | Streamlit |
| ML / NLP | scikit-learn, NLTK |
| Data | pandas, NumPy |
| Poster API | TMDB API |
| Styling | Custom CSS |

---

## 🔮 Future Improvements

- [ ] Add collaborative filtering (user-based recommendations)
- [ ] Deploy to Streamlit Cloud / Hugging Face Spaces
- [ ] Add movie ratings and release year to cards
- [ ] Search-as-you-type movie selector
- [ ] Watchlist feature with local storage
- [ ] Trailer preview on hover

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [TMDB](https://www.themoviedb.org/) for the movie data and poster API
- [Kaggle — TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- [Streamlit](https://streamlit.io/) for making ML apps incredibly easy to build

---

<p align="center">Made with ❤️ and Python</p>
