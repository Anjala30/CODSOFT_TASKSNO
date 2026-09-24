import html
import os
import ast
import re
import textwrap

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MovieMind AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# DATA LOADING
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "movies_prepared.csv")


@st.cache_data(show_spinner=False)
def load_movies(path):
    df = pd.read_csv(path)
    if "title" not in df.columns:
        raise ValueError("The dataset must contain a 'title' column.")
    df = df.copy()
    df["title"] = df["title"].fillna("").astype(str).str.strip()
    df = df[df["title"] != ""].drop_duplicates(subset=["title"]).reset_index(drop=True)
    return df


try:
    movies = load_movies(DATA_PATH)
    data_error = None
except Exception as exc:
    movies = pd.DataFrame()
    data_error = str(exc)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None


# =========================================================
# HELPERS
# =========================================================


def safe(value, default="Not available"):
    if value is None:
        return default
    if pd.isna(value):
        return default
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null", "[]", "{}"}:
        return default
    return text


def esc(value, default="Not available"):
    return html.escape(safe(value, default))


def first_existing(row, columns, default="Not available"):
    for col in columns:
        if col in row.index:
            value = safe(row[col], "")
            if value:
                return value
    return default


def pretty_list(value, limit=7):
    text = safe(value, "")
    if not text:
        return []

    # Handle strings that contain Python-style lists/dictionaries.
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            items = []
            for item in parsed:
                if isinstance(item, dict):
                    name = item.get("name") or item.get("title")
                    if name:
                        items.append(str(name))
                elif item:
                    items.append(str(item))
            if items:
                return items[:limit]
    except Exception:
        pass

    parts = re.split(r"\s*[,|;]\s*", text)
    return [p.strip() for p in parts if p.strip()][:limit]


def poster_url(row):
    candidates = [
        "poster_url",
        "poster_path",
        "poster",
        "image_url",
        "image",
        "backdrop_path",
    ]

    for col in candidates:
        if col not in row.index:
            continue
        value = safe(row[col], "")
        if not value:
            continue
        if value.startswith("http://") or value.startswith("https://"):
            return value
        if value.startswith("/"):
            return f"https://image.tmdb.org/t/p/w500{value}"

    return None


def go(page):
    st.session_state.page = page
    st.rerun()


def select_movie(title):
    if title in movies["title"].values:
        st.session_state.selected_movie = title
        st.session_state.page = "preview"
        st.rerun()


def movie_row(title):
    if movies.empty:
        return None
    match = movies[movies["title"] == title]
    return None if match.empty else match.iloc[0]


def movie_year(row):
    return first_existing(row, ["year", "release_year", "release_date"], "Year not available")


def movie_rating(row):
    value = first_existing(row, ["vote_average", "rating", "imdb_rating", "score"], "")
    if value == "":
        return "Rating not available"
    return value


def movie_runtime(row):
    return first_existing(row, ["runtime", "duration"], "Runtime not available")


def movie_director(row):
    crew = safe(row.get("crew", ""), "")
    if crew:
        # If crew is a list of dictionaries, extract directors where possible.
        try:
            parsed = ast.literal_eval(crew)
            if isinstance(parsed, list):
                directors = []
                for item in parsed:
                    if isinstance(item, dict):
                        if str(item.get("job", "")).lower() == "director" and item.get("name"):
                            directors.append(str(item["name"]))
                if directors:
                    return ", ".join(directors[:3])
        except Exception:
            pass

        return crew

    return "Director not available"


def poster_block(row, title, large=False):
    url = poster_url(row)
    title_e = esc(title)
    height = 410 if large else 250

    if url:
        return f"""
        <div class='poster-wrap' style='height:{height}px;'>
            <img src='{html.escape(url, quote=True)}' alt='{title_e}' class='poster-img'>
        </div>
        """

    year = esc(movie_year(row), "")
    genres = pretty_list(row.get("genres", ""), 2) if row is not None else []
    genre_text = " • ".join(genres) if genres else "FEATURE FILM"
    return f"""
    <div class='poster-wrap poster-fallback' style='height:{height}px;'>
        <div class='poster-glow'></div>
        <div class='poster-topline'>MOVIEMIND AI • CINEMA</div>
        <div class='poster-clapper'>🎬</div>
        <div class='fallback-title'>{title_e}</div>
        <div class='poster-genre'>{esc(genre_text)}</div>
        <div class='poster-year'>{year}</div>
    </div>
    """


# =========================================================
# AI MODEL
# =========================================================

TEXT_COLUMNS = ["genres", "keywords", "overview", "cast", "crew"]


@st.cache_resource(show_spinner=False)
def build_model(df):
    work = df.copy()
    available = [c for c in TEXT_COLUMNS if c in work.columns]

    if not available:
        raise ValueError("The dataset needs at least one content column such as genres, keywords or overview.")

    work["combined_features"] = (
        work[available]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
    )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True,
    )

    matrix = vectorizer.fit_transform(work["combined_features"])
    return work, vectorizer, matrix, available


def get_recommendations(selected_title, limit=6):
    work, vectorizer, matrix, available = build_model(movies)

    positions = work.index[work["title"] == selected_title].tolist()
    if not positions:
        return [], available

    position = positions[0]
    selected_vector = matrix[position]
    scores = cosine_similarity(selected_vector, matrix).ravel()

    ranked_positions = scores.argsort()[::-1]
    results = []

    for idx in ranked_positions:
        if idx == position:
            continue
        results.append((work.iloc[idx], float(scores[idx])))
        if len(results) == limit:
            break

    return results, available


# =========================================================
# GLOBAL STYLING
# =========================================================

st.markdown(
    """
<style>
.stApp {
    background:
        radial-gradient(circle at 5% 5%, rgba(123, 54, 219, .34), transparent 28%),
        radial-gradient(circle at 95% 10%, rgba(24, 105, 189, .28), transparent 30%),
        radial-gradient(circle at 50% 75%, rgba(183, 57, 201, .09), transparent 35%),
        linear-gradient(135deg, #070612 0%, #0a0818 48%, #06111c 100%);
    color: #fff;
}
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }
.block-container {
    max-width: 1280px;
    padding-top: 1.05rem;
    padding-bottom: 3.5rem;
}

/* NAV */
.nav-brand { padding: 7px 0 0 3px; }
.brand-title { color:#fff; font-size:20px; font-weight:900; letter-spacing:-.7px; }
.brand-title span { color:#c88bff; }
.brand-subtitle { color:#6d6884; font-size:8px; letter-spacing:2.6px; margin-top:4px; }

div.stButton > button {
    min-height:44px;
    border-radius:14px;
    border:1px solid rgba(210,185,255,.16);
    background:rgba(255,255,255,.035);
    color:#eee9ff;
    font-weight:720;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.025);
    transition:all .18s ease;
}
div.stButton > button:hover {
    border-color:rgba(214,124,255,.58);
    background:linear-gradient(135deg,rgba(116,57,186,.25),rgba(35,104,163,.18));
    color:#fff;
    transform:translateY(-1px);
}
div.stButton > button:focus:not(:active) {
    border-color:rgba(206,117,255,.62);
    box-shadow:0 0 0 2px rgba(183,88,239,.10);
}

/* HERO */
.hero { text-align:center; padding:48px 20px 18px; }
.hero-badge {
    display:inline-block; padding:9px 17px; border-radius:999px;
    background:rgba(255,255,255,.055); border:1px solid rgba(255,255,255,.14);
    color:#d9d1ec; font-size:10px; font-weight:850; letter-spacing:1.6px;
}
.hero-title,.section-title {
    font-weight:950; letter-spacing:-2.6px;
    background:linear-gradient(95deg,#fff 0%,#d7c0ff 48%,#94dcff 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero-title { margin-top:22px; font-size:clamp(52px,7vw,88px); line-height:1; }
.hero-subtitle { color:#f0e9ff; font-size:clamp(18px,2vw,24px); font-weight:600; margin-top:17px; }
.hero-description { max-width:760px; margin:14px auto 0; color:#8d89a2; font-size:14px; line-height:1.8; }
.hero-strip {
    max-width:1120px; height:112px; margin:28px auto 0; border-radius:28px;
    border:1px solid rgba(206,170,255,.17);
    background:
        linear-gradient(90deg,rgba(124,39,173,.34),rgba(28,80,154,.23)),
        radial-gradient(circle at 16% 50%,rgba(255,55,207,.26),transparent 23%),
        radial-gradient(circle at 84% 45%,rgba(59,170,255,.19),transparent 25%);
    overflow:hidden; position:relative; box-shadow:0 30px 80px rgba(0,0,0,.25);
}
.hero-strip:before,.hero-strip:after {
    content:""; position:absolute; top:13px; bottom:13px; width:30%;
    border-radius:20px; opacity:.34;
}
.hero-strip:before {
    left:8%;
    background:linear-gradient(145deg,rgba(255,255,255,.10),transparent),
               radial-gradient(circle at 65% 35%,rgba(215,133,255,.65),transparent 35%),
               linear-gradient(145deg,#24154a,#111a3a);
    transform:perspective(400px) rotateY(9deg);
}
.hero-strip:after {
    right:8%;
    background:linear-gradient(145deg,rgba(255,255,255,.08),transparent),
               radial-gradient(circle at 35% 35%,rgba(91,204,255,.55),transparent 35%),
               linear-gradient(145deg,#151d48,#10172a);
    transform:perspective(400px) rotateY(-9deg);
}
.cinema-symbols {
    position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
    gap:34px; z-index:2; font-size:34px; opacity:.78;
    filter:drop-shadow(0 5px 20px rgba(0,0,0,.4));
}

/* BADGES */
.ai-badges { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; max-width:1010px; margin:25px auto 29px; }
.ai-badge {
    min-height:76px; padding:17px 12px; text-align:center; border-radius:17px;
    background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.022));
    border:1px solid rgba(190,170,255,.13); color:#aaa4c0; font-size:12px;
    box-shadow:0 14px 35px rgba(0,0,0,.13);
}
.ai-badge strong { display:block; color:#f2edff; margin-top:7px; font-size:12px; }

/* PROGRESS / HEADERS */
.progress { max-width:650px; margin:24px auto 19px; display:flex; align-items:center; justify-content:center; }
.progress-node {
    width:35px; height:35px; border-radius:50%; display:flex; align-items:center; justify-content:center;
    background:rgba(255,255,255,.045); border:1px solid rgba(255,255,255,.15);
    color:#8e899f; font-size:11px; font-weight:850;
}
.progress-node.active {
    background:linear-gradient(135deg,#c04fe8,#7165ff); border-color:transparent; color:#fff;
    box-shadow:0 0 28px rgba(183,78,239,.30);
}
.progress-line { width:115px; height:1px; background:linear-gradient(90deg,rgba(188,126,255,.42),rgba(94,154,255,.25)); }
.step-label { text-align:center; color:#c47dff; font-size:9px; font-weight:900; letter-spacing:3.2px; margin-top:21px; }
.section-title { text-align:center; font-size:clamp(40px,5vw,64px); line-height:1.08; margin-top:11px; }
.section-description { max-width:780px; margin:13px auto 30px; text-align:center; color:#858197; font-size:13px; line-height:1.8; }

/* PANELS */
.selection-panel,.movie-card,.how-card,.why-card {
    border-radius:24px; background:linear-gradient(145deg,rgba(39,30,70,.70),rgba(9,12,25,.91));
    border:1px solid rgba(194,171,255,.14); box-shadow:0 28px 75px rgba(0,0,0,.28);
}
.selection-panel { max-width:1080px; margin:0 auto; padding:23px 25px 25px; }
.popular-title { max-width:1080px; margin:29px auto 13px; color:#e5e0f1; font-size:14px; font-weight:800; }

/* POSTERS */
.poster-wrap {
    width:100%; border-radius:18px; overflow:hidden; background:linear-gradient(145deg,#37205f,#101936);
    border:1px solid rgba(205,181,255,.16); box-shadow:0 18px 48px rgba(0,0,0,.32);
    display:flex; align-items:center; justify-content:center; position:relative;
}
.poster-img { width:100%; height:100%; object-fit:cover; display:block; }
.poster-fallback {
    flex-direction:column; text-align:center; padding:22px; isolation:isolate;
    background:
        radial-gradient(circle at 70% 20%,rgba(226,117,255,.38),transparent 30%),
        radial-gradient(circle at 20% 80%,rgba(66,165,255,.26),transparent 35%),
        linear-gradient(150deg,#35205e 0%,#18143a 50%,#0c172d 100%);
}
.poster-glow {
    position:absolute; inset:0;
    background:linear-gradient(125deg,transparent 20%,rgba(255,255,255,.06) 48%,transparent 52%);
    z-index:-1;
}
.poster-topline { position:absolute; top:15px; left:16px; right:16px; color:rgba(235,226,255,.62); font-size:7px; letter-spacing:2px; }
.poster-clapper { font-size:52px; filter:drop-shadow(0 8px 20px rgba(0,0,0,.35)); }
.fallback-title { color:#fff; font-size:22px; font-weight:900; line-height:1.12; margin-top:12px; }
.poster-genre { color:#cfc5ea; font-size:9px; margin-top:9px; text-transform:uppercase; letter-spacing:1.2px; }
.poster-year { color:#8e88a6; font-size:9px; margin-top:7px; }

/* PREVIEW */
.movie-card { max-width:1080px; margin:0 auto; padding:25px; }
.movie-grid { display:grid; grid-template-columns:320px 1fr; gap:34px; align-items:start; }
.movie-label { color:#928ba9; font-size:9px; text-transform:uppercase; letter-spacing:2.2px; }
.movie-title { color:#fff; font-size:clamp(31px,4vw,51px); line-height:1.04; font-weight:950; margin-top:8px; }
.meta-row { display:flex; flex-wrap:wrap; gap:8px; margin:17px 0 19px; }
.meta-pill { padding:7px 11px; border-radius:999px; background:rgba(151,125,255,.105); border:1px solid rgba(162,139,255,.18); color:#d9d0ff; font-size:10px; }
.content-label { color:#ebe6f5; font-size:12px; font-weight:850; margin:17px 0 7px; }
.content-text { color:#9691a7; font-size:12px; line-height:1.75; }
.overview-box { padding:16px; border-radius:15px; background:rgba(0,0,0,.18); border:1px solid rgba(255,255,255,.06); }

/* RECOMMENDATIONS */
.rec-intro { text-align:center; color:#ae99ff; font-size:13px; margin:20px auto 25px; }
.rec-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:18px; max-width:1080px; margin:0 auto; }
.rec-card {
    padding:14px; border-radius:21px; background:linear-gradient(145deg,rgba(42,30,73,.84),rgba(8,12,25,.95));
    border:1px solid rgba(194,171,255,.15); box-shadow:0 20px 48px rgba(0,0,0,.28);
}
.rec-poster { height:260px; border-radius:15px; }
.rec-rank { color:#c27cff; font-size:8px; font-weight:900; letter-spacing:2px; margin-top:14px; }
.rec-title { color:#fff; font-size:18px; font-weight:900; line-height:1.2; margin-top:5px; }
.rec-genre { color:#9691a7; font-size:10px; margin-top:8px; min-height:29px; }
.sim-row { display:flex; justify-content:space-between; color:#a09aae; font-size:9px; text-transform:uppercase; letter-spacing:1.1px; margin-top:15px; }
.sim-value { color:#fff; font-weight:850; }
.sim-track { height:5px; border-radius:999px; background:#191a2a; overflow:hidden; margin-top:8px; }
.sim-fill { height:100%; border-radius:999px; background:linear-gradient(90deg,#8d5cff,#f24ed0); }

/* AI EXPLANATION */
.how-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:15px; max-width:1080px; margin:0 auto; }
.how-card { padding:20px; min-height:154px; }
.how-number { color:#bd7dff; font-size:9px; font-weight:900; letter-spacing:2px; }
.how-title { color:#fff; font-size:16px; font-weight:850; margin-top:9px; }
.how-text { color:#8d899d; font-size:11px; line-height:1.72; margin-top:8px; }
.ai-pipeline {
    max-width:1080px; margin:23px auto 0; padding:20px; border-radius:19px;
    border:1px solid rgba(190,170,255,.13);
    background:linear-gradient(90deg,rgba(122,62,176,.10),rgba(44,100,174,.09)); text-align:center;
}
.pipeline-text { color:#dcd5ef; font-size:13px; line-height:2; }
.pipeline-text span { color:#c184ff; font-weight:850; }
.why-card { max-width:1080px; padding:22px; margin:17px auto 0; }
.why-title { color:#fff; font-size:16px; font-weight:880; }
.why-text { color:#8f8b9f; font-size:12px; line-height:1.78; margin-top:8px; }
.footer-text { text-align:center; color:#555266; font-size:10px; margin-top:48px; }

/* INPUTS */
.stSelectbox label,.stTextInput label { color:#ddd8eb !important; font-weight:700 !important; font-size:12px !important; }
.stSelectbox div[data-baseweb='select'] > div {
    background:rgba(255,255,255,.055) !important; border:1px solid rgba(190,170,255,.17) !important;
    border-radius:13px !important; color:#fff !important;
}
.stSelectbox [data-baseweb="select"] * { color:#fff !important; }
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color:rgba(194,171,255,.14) !important;
    background:linear-gradient(145deg,rgba(42,30,73,.62),rgba(8,12,25,.88)) !important;
    border-radius:21px !important;
}

/* RESPONSIVE */
@media (max-width:900px) {
    .ai-badges { grid-template-columns:repeat(2,1fr); }
    .movie-grid { grid-template-columns:1fr; }
    .rec-grid { grid-template-columns:repeat(2,1fr); }
    .how-grid { grid-template-columns:repeat(2,1fr); }
    .progress-line { width:65px; }
}
@media (max-width:620px) {
    .block-container { padding-left:.9rem; padding-right:.9rem; }
    .hero { padding-top:34px; }
    .hero-title { font-size:47px; }
    .hero-strip { height:78px; }
    .hero-strip .cinema-symbols { font-size:25px; gap:15px; }
    .ai-badges,.rec-grid,.how-grid { grid-template-columns:1fr; }
    .movie-grid { grid-template-columns:1fr; }
    .progress-line { width:31px; }
    .section-title { font-size:39px; }
    .selection-panel,.movie-card { padding:17px; }
    .rec-poster { height:300px; }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# NAVIGATION BAR
# =========================================================

nav1, nav2, nav3, nav4, nav5 = st.columns([1.8, 1, 1, 1.15, 1.15])

with nav1:
    st.markdown(
        """
        <div class='nav-brand'>
            <div class='brand-title'>🎬 Movie<span>Mind AI</span></div>
            <div class='brand-subtitle'>INTELLIGENT MOVIE DISCOVERY</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav2:
    if st.button("⌂ Home", use_container_width=True):
        go("home")
with nav3:
    if st.button("✦ Explore", use_container_width=True):
        go("explore")
with nav4:
    if st.button("◉ Recommendations", use_container_width=True):
        if st.session_state.selected_movie:
            go("recommendations")
        else:
            go("explore")
with nav5:
    if st.button("🧠 How AI Works", use_container_width=True):
        go("ai")


# =========================================================
# DATA ERROR STATE
# =========================================================

if data_error:
    st.error(
        "Movie dataset could not be loaded. Make sure your project contains "
        "data/movies_prepared.csv."
    )
    st.code(data_error)
    st.stop()


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "home":

    st.markdown(
        """
        <div class='hero'>
            <div class='hero-badge'>✨ AI-POWERED MOVIE DISCOVERY</div>
            <div class='hero-title'>🎬 MovieMind AI</div>
            <div class='hero-subtitle'>Discover your next favourite movie</div>
            <div class='hero-description'>
                An intelligent content-based recommendation system that transforms
                movie information into machine-learning features and discovers
                movies with similar characteristics.
            </div>
            <div class='hero-strip'><div class='cinema-symbols'>🎬　🍿　🎞️　✦　🤖　🎬　🍿</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='ai-badges'>
            <div class='ai-badge'>🤖<strong>AI Recommendation</strong></div>
            <div class='ai-badge'>🧠<strong>TF-IDF Vectorization</strong></div>
            <div class='ai-badge'>📊<strong>Cosine Similarity</strong></div>
            <div class='ai-badge'>🎬<strong>Content-Based Filtering</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='text-align:center;color:#77728a;font-size:12px;margin-bottom:12px;'>"
        f"🎞️ {len(movies):,} movies available for discovery"
        "</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 1.35, 1])
    with c2:
        if st.button("✨  Start Exploring  →", use_container_width=True):
            go("explore")

    st.markdown(
        """
        <div class='footer-text'>Built with Python • Streamlit • Scikit-learn • Machine Learning</div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# EXPLORE / MOVIE SELECTION
# =========================================================

elif st.session_state.page == "explore":

    st.markdown(
        """
        <div class='progress'>
            <div class='progress-node active'>1</div>
            <div class='progress-line'></div>
            <div class='progress-node'>2</div>
            <div class='progress-line'></div>
            <div class='progress-node'>3</div>
        </div>
        <div class='step-label'>CHOOSE</div>
        <div class='section-title'>🎯 Choose Your Movie</div>
        <div class='section-description'>
            Select a movie you already love. MovieMind AI will analyze its content
            and discover movies with similar characteristics.
        </div>
        """,
        unsafe_allow_html=True,
    )

    titles = movies["title"].tolist()
    current = st.session_state.selected_movie
    default_index = titles.index(current) if current in titles else 0

    st.markdown("<div class='selection-panel'>", unsafe_allow_html=True)
    selected = st.selectbox(
        "🔎 Search or select a movie",
        titles,
        index=default_index,
        key="movie_picker",
    )
    st.markdown(
        f"<div style='color:#77748a;font-size:11px;margin-top:7px;'>"
        f"Choose from {len(titles):,} movies</div></div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='popular-title'>🔥 Popular Choices</div>", unsafe_allow_html=True)

    preferred = ["Inception", "Interstellar", "The Dark Knight", "The Matrix", "Avatar"]
    popular = []
    for name in preferred:
        matches = movies[movies["title"].str.lower() == name.lower()]
        if not matches.empty:
            popular.append(matches.iloc[0]["title"])
    if len(popular) < 5:
        popular.extend([t for t in titles if t not in popular][: 5 - len(popular)])

    cols = st.columns(5)
    for col, title in zip(cols, popular[:5]):
        row = movie_row(title)
        with col:
            st.markdown(poster_block(row, title, large=False).replace("height:250px", "height:185px"), unsafe_allow_html=True)
            if st.button(title, key=f"popular_{title}", use_container_width=True):
                select_movie(title)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("Continue to Movie Preview  →", use_container_width=True):
            st.session_state.selected_movie = selected
            go("preview")

    st.markdown("<div class='footer-text'>Built with Python • Streamlit • Scikit-learn • Machine Learning</div>", unsafe_allow_html=True)


# =========================================================
# SELECTED MOVIE PREVIEW
# =========================================================

elif st.session_state.page == "preview":

    selected_title = st.session_state.selected_movie
    row = movie_row(selected_title)

    if row is None:
        go("explore")

    genres = pretty_list(row.get("genres", ""), 8)
    overview = safe(row.get("overview", ""), "No overview available for this movie.")
    keywords = pretty_list(row.get("keywords", ""), 12)
    cast = pretty_list(row.get("cast", ""), 8)
    director = movie_director(row)

    st.markdown(
        """
        <div class='progress'>
            <div class='progress-node active'>1</div>
            <div class='progress-line'></div>
            <div class='progress-node active'>2</div>
            <div class='progress-line'></div>
            <div class='progress-node'>3</div>
        </div>
        <div class='step-label'>PREVIEW</div>
        <div class='section-title'>🎬 Your Movie</div>
        <div class='section-description'>
            Review your selection before MovieMind AI finds movies with similar characteristics.
        </div>
        """,
        unsafe_allow_html=True,
    )

    genre_html = "".join([f"<span class='meta-pill'>🎭 {esc(g)}</span>" for g in genres])
    cast_text = ", ".join(cast) if cast else "Cast information not available"

    st.markdown(
        f"""
        <div class='movie-card'>
            <div class='movie-grid'>
                <div>{poster_block(row, selected_title, large=True)}</div>
                <div>
                    <div class='movie-label'>SELECTED MOVIE</div>
                    <div class='movie-title'>{esc(selected_title)}</div>
                    <div class='meta-row'>
                        <span class='meta-pill'>📅 {esc(movie_year(row))}</span>
                        <span class='meta-pill'>⭐ {esc(movie_rating(row))}</span>
                        <span class='meta-pill'>⏱️ {esc(movie_runtime(row))}</span>
                    </div>
                    <div class='meta-row'>{genre_html or "<span class='meta-pill'>Genre not available</span>"}</div>
                    <div class='content-label'>📝 Overview</div>
                    <div class='overview-box'><div class='content-text'>{esc(overview)}</div></div>
                    <div class='content-label'>🎥 Director / Crew</div>
                    <div class='content-text'>{esc(director)}</div>
                    <div class='content-label'>👥 Cast</div>
                    <div class='content-text'>{esc(cast_text)}</div>
                    <div class='content-label'>🔑 Keywords</div>
                    <div class='content-text'>{esc(", ".join(keywords) if keywords else "Keywords not available")}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    back, action = st.columns(2)
    with back:
        if st.button("←  Back to Movie Selection", use_container_width=True):
            go("explore")
    with action:
        if st.button("🤖  Find Similar Movies  →", use_container_width=True):
            go("recommendations")

    st.markdown("<div class='footer-text'>Built with Python • Streamlit • Scikit-learn • Machine Learning</div>", unsafe_allow_html=True)


# =========================================================
# AI RECOMMENDATIONS
# =========================================================

elif st.session_state.page == "recommendations":

    selected_title = st.session_state.selected_movie

    if not selected_title:
        go("explore")

    st.markdown(
        """
        <div class='progress'>
            <div class='progress-node active'>1</div>
            <div class='progress-line'></div>
            <div class='progress-node active'>2</div>
            <div class='progress-line'></div>
            <div class='progress-node active'>3</div>
        </div>
        <div class='step-label'>AI RESULTS</div>
        <div class='section-title'>🤖 AI Recommendations</div>
        <div class='section-description'>
            MovieMind AI converts movie content into TF-IDF vectors, measures cosine
            similarity, and ranks the closest movies as recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='rec-intro'>✨ Recommendations based on <strong style='color:white'>{esc(selected_title)}</strong></div>",
        unsafe_allow_html=True,
    )

    with st.spinner("🧠 MovieMind AI is analyzing movie content..."):
        try:
            recommendations, used_features = get_recommendations(selected_title, 6)
            model_error = None
        except Exception as exc:
            recommendations = []
            used_features = []
            model_error = str(exc)

    if model_error:
        st.error("The AI recommendation engine could not run.")
        st.code(model_error)

    elif recommendations:
        # The recommendation result cards use native Streamlit components.
        # This prevents poster/card HTML from being displayed as raw source code.
        for start in range(0, len(recommendations), 3):
            row_recommendations = recommendations[start:start + 3]
            cols = st.columns(3, gap="medium")

            for offset, (rec, score) in enumerate(row_recommendations):
                number = start + offset + 1
                title = safe(rec.get("title", "Unknown Movie"), "Unknown Movie")
                genre_list = pretty_list(rec.get("genres", ""), 4)
                genre_text = " • ".join(genre_list) if genre_list else "Genre not available"
                percentage = max(0.0, min(score * 100, 100.0))
                url = poster_url(rec)

                with cols[offset]:
                    with st.container(border=True):
                        if url:
                            st.image(url, use_container_width=True)
                        else:
                            st.markdown(
                                """
                                <div style="height:230px;border-radius:15px;display:flex;
                                flex-direction:column;align-items:center;justify-content:center;
                                background:linear-gradient(145deg,#392261,#121d3b);
                                border:1px solid rgba(202,180,255,.18);text-align:center;">
                                    <div style="font-size:52px;">🎬</div>
                                    <div style="color:white;font-size:19px;font-weight:800;">MovieMind AI</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        st.caption(f"RECOMMENDATION #{number}")
                        st.markdown(f"### 🎬 {esc(title)}")
                        st.caption(f"🎭 {esc(genre_text)}")
                        st.write(f"**Similarity — {percentage:.1f}%**")
                        st.progress(
                            int(round(percentage)),
                            text=f"{percentage:.1f}% similar",
                        )

        feature_names = ", ".join(used_features)
        st.markdown(
            f"""
            <div class='why-card'>
                <div class='why-title'>💡 Why these movies?</div>
                <div class='why-text'>
                    MovieMind uses <strong style='color:#d2c6ff'>content-based filtering</strong>.
                    It combines available movie features such as <strong style='color:#d2c6ff'>{esc(feature_names)}</strong>,
                    converts the text into TF-IDF vectors, calculates cosine similarity with the selected movie,
                    and ranks the closest results. A higher similarity percentage means the content representation
                    is more similar to the selected movie.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.warning("No similar movies were found for this selection.")

    back, another = st.columns(2)
    with back:
        if st.button("←  Back to Selected Movie", use_container_width=True):
            go("preview")
    with another:
        if st.button("🔄  Recommend Another Movie", use_container_width=True):
            st.session_state.selected_movie = None
            go("explore")

    st.markdown(
        "<div class='footer-text'>Built with Python • Streamlit • Scikit-learn • Machine Learning</div>",
        unsafe_allow_html=True,
    )


# =========================================================
# HOW AI WORKS
# =========================================================

elif st.session_state.page == "ai":

    st.markdown(
        """
        <div class='step-label'>MOVIEMIND INTELLIGENCE</div>
        <div class='section-title'>🧠 How MovieMind AI Works</div>
        <div class='section-description'>
            A simple visual explanation of the machine-learning pipeline behind the movie recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    steps = [
        ("01", "🎬 Movie Data", "Movie information such as genres, keywords, overview, cast and crew becomes the content used by the model."),
        ("02", "📝 Text Processing", "Relevant text features are combined into one content representation for each movie."),
        ("03", "🧠 TF-IDF Vectorization", "TF-IDF converts movie text into numerical feature vectors while giving more weight to informative terms."),
        ("04", "📊 Feature Vectors", "Every movie becomes a point in a high-dimensional numerical feature space."),
        ("05", "📐 Cosine Similarity", "The model measures how similar the selected movie vector is to every other movie vector."),
        ("06", "⭐ Similarity Ranking", "Movies are ranked by similarity and the highest-scoring results become the recommendations."),
    ]

    cards = []
    for number, title, text_value in steps:
        card = f"""
<div class='how-card'>
    <div class='how-number'>{number}</div>
    <div class='how-title'>{title}</div>
    <div class='how-text'>{text_value}</div>
</div>
"""
        cards.append(textwrap.dedent(card))

    st.markdown(
        "<div class='how-grid'>" + "".join(cards) + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='ai-pipeline'>
            <div class='pipeline-text'>
                <span>Movie Data</span> → <span>Text Processing</span> → <span>TF-IDF</span> →
                <span>Feature Vectors</span> → <span>Cosine Similarity</span> →
                <span>Ranking</span> → <span>Recommendations</span>
            </div>
        </div>

        <div class='why-card'>
            <div class='why-title'>🤖 What makes this an AI / ML recommendation system?</div>
            <div class='why-text'>
                MovieMind does not use a fixed list of recommendations. The system learns a numerical
                representation of the movie content from the dataset using TF-IDF and uses a mathematical
                similarity measure to compare the selected movie against the rest of the catalogue.
                The resulting similarity scores determine which movies are surfaced to the user.
            </div>
        </div>

        <div class='why-card'>
            <div class='why-title'>🎯 Why Content-Based Filtering?</div>
            <div class='why-text'>
                Content-based filtering recommends items using the characteristics of the item the user selected.
                For MovieMind, that means the recommendation is driven by movie content rather than requiring a
                large user-rating history. This makes it practical for a compact internship project while still
                demonstrating a real machine-learning pipeline.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("← Back to MovieMind", use_container_width=True):
        go("home")

    st.markdown("<div class='footer-text'>Built with Python • Streamlit • Scikit-learn • Machine Learning</div>", unsafe_allow_html=True)
