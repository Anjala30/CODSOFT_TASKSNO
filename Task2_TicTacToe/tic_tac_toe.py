import streamlit as st
from math import inf


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tic-Tac-Toe AI | CodSoft Task 2",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="auto",
)


# ============================================================
# CUSTOM CSS — COLORFUL UI
# ============================================================

st.markdown(
    """
<style>
/* ---------- APP BACKGROUND ---------- */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 8% 8%, rgba(168, 85, 247, 0.22), transparent 28%),
        radial-gradient(circle at 92% 15%, rgba(59, 130, 246, 0.22), transparent 28%),
        radial-gradient(circle at 70% 88%, rgba(236, 72, 153, 0.18), transparent 26%),
        linear-gradient(135deg, #0f1024 0%, #171a3d 48%, #24134f 100%);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1050px;
    padding-top: 2.2rem;
    padding-bottom: 2rem;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 80% 10%, rgba(139, 92, 246, 0.25), transparent 25%),
        linear-gradient(180deg, #11152f 0%, #19164a 55%, #25134f 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] * {
    color: #f8f7ff !important;
}

.sidebar-brand {
    padding: 18px 16px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.34), rgba(236, 72, 153, 0.24));
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
    margin-bottom: 18px;
}

.sidebar-brand-title {
    font-size: 1.22rem;
    font-weight: 800;
    margin-bottom: 4px;
}

.sidebar-brand-subtitle {
    font-size: 0.82rem;
    color: #d9d7f3 !important;
}

.setting-card {
    padding: 14px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.065);
    border: 1px solid rgba(255, 255, 255, 0.09);
    margin: 12px 0;
}

.method-card {
    padding: 16px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.17), rgba(168, 85, 247, 0.19));
    border: 1px solid rgba(129, 140, 248, 0.25);
    margin-top: 16px;
}

.method-title {
    font-weight: 800;
    font-size: 1rem;
    margin-bottom: 8px;
}

.method-highlight {
    color: #c4b5fd !important;
    font-weight: 700;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
    color: white !important;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 52%, #ec4899 100%) !important;
    border: none !important;
    border-radius: 14px !important;
    min-height: 48px;
    font-weight: 800 !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.28);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(139, 92, 246, 0.38);
}

/* ---------- HERO HEADER ---------- */
.hero {
    text-align: center;
    padding: 28px 24px 24px;
    border-radius: 28px;
    background:
        linear-gradient(135deg, rgba(79, 70, 229, 0.96), rgba(124, 58, 237, 0.92) 50%, rgba(219, 39, 119, 0.90));
    border: 1px solid rgba(255, 255, 255, 0.16);
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.26);
    margin-bottom: 20px;
}

.hero h1 {
    margin: 0;
    color: white !important;
    font-size: 2.65rem;
    font-weight: 900;
    letter-spacing: -0.03em;
}

.hero p {
    margin: 8px 0 0;
    color: #f4f1ff !important;
    font-size: 1rem;
}

/* ---------- TOP INFO PILLS ---------- */
.pill-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 6px 0 20px;
}

.pill {
    padding: 8px 13px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.09);
    color: #f4f3ff !important;
    border: 1px solid rgba(255, 255, 255, 0.11);
    font-size: 0.82rem;
    font-weight: 700;
}

/* ---------- SCORE CARDS ---------- */
.score-card {
    text-align: center;
    padding: 14px 10px;
    border-radius: 18px;
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.97), rgba(242, 242, 255, 0.94));
    border: 1px solid rgba(255, 255, 255, 0.65);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.16);
    color: #242447 !important;
}

.score-label {
    font-size: 0.83rem;
    font-weight: 800;
    color: #55557c !important;
}

.score-value {
    font-size: 1.65rem;
    font-weight: 900;
    margin-top: 3px;
    color: #312e81 !important;
}

/* ---------- STATUS ---------- */
.status-card {
    text-align: center;
    padding: 14px 18px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.13), rgba(255, 255, 255, 0.07));
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.14);
    color: #ffffff !important;
    font-size: 1.02rem;
    font-weight: 800;
    margin: 18px 0 16px;
}

/* ---------- BOARD ---------- */
.board-frame {
    padding: 18px;
    border-radius: 26px;
    background: linear-gradient(145deg, rgba(255,255,255,0.11), rgba(255,255,255,0.055));
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 18px 38px rgba(0,0,0,0.20);
}

/* Main board buttons */
div[data-testid="stButton"] > button {
    color: #26204b !important;
    background: linear-gradient(145deg, #ffffff 0%, #f3f1ff 100%) !important;
    border: 2px solid rgba(129, 140, 248, 0.30) !important;
    border-radius: 20px !important;
    min-height: 108px !important;
    font-size: 2.7rem !important;
    font-weight: 900 !important;
    box-shadow:
        0 8px 18px rgba(15, 23, 42, 0.18),
        inset 0 1px 0 rgba(255, 255, 255, 0.85);
    transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    border-color: #a78bfa !important;
    box-shadow:
        0 12px 24px rgba(124, 58, 237, 0.22),
        inset 0 1px 0 rgba(255, 255, 255, 0.85);
}

/* ---------- INFORMATION CARDS ---------- */
.info-card {
    padding: 20px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(236, 72, 153, 0.11));
    border: 1px solid rgba(129, 140, 248, 0.20);
    color: #f6f5ff !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.14);
    margin-top: 20px;
}

.info-card h3 {
    margin: 0 0 10px;
    color: white !important;
}

.info-card p,
.info-card li {
    color: #ebe9fb !important;
    line-height: 1.6;
}

/* ---------- EXPANDERS ---------- */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    color: white;
}

div[data-testid="stExpander"] * {
    color: #f5f4ff;
}

/* ---------- FOOTER ---------- */
.footer {
    text-align: center;
    color: #b8b6d9 !important;
    margin-top: 26px;
    padding: 12px;
    font-size: 0.82rem;
}

/* ---------- MOBILE ---------- */
@media (max-width: 700px) {
    .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
        padding-top: 1rem !important;
    }

    .hero h1 {
        font-size: 2.1rem;
    }

    /* ---------- MOBILE RESPONSIVE LAYOUT ---------- */
    /*
       Streamlit can apply a large minimum width to columns on small screens.
       The rules below explicitly keep the scoreboard and game board inside
       the phone viewport. No game logic is changed.
    */

    /* Keep the main content inside the phone viewport */
    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        padding-top: 0.9rem !important;
        padding-bottom: 1.5rem !important;
        overflow-x: hidden !important;
    }

    /* Compact but readable hero */
    .hero {
        padding: 22px 15px 20px !important;
        border-radius: 22px !important;
        margin-bottom: 14px !important;
    }

    .hero h1 {
        font-size: 1.85rem !important;
        line-height: 1.15 !important;
    }

    .hero p {
        font-size: 0.9rem !important;
        line-height: 1.45 !important;
    }

    /* Compact feature pills */
    .pill-row {
        gap: 7px !important;
        margin: 4px 0 14px !important;
    }

    .pill {
        padding: 7px 9px !important;
        font-size: 0.70rem !important;
    }

    /*
       IMPORTANT:
       Keep every 3-column Streamlit block on one row.
       This prevents Streamlit's mobile stacking behaviour.
    */
    div[data-testid="stHorizontalBlock"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
        box-sizing: border-box !important;
        overflow: visible !important;
    }

    /* Force each column to share the available width equally */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        flex: 1 1 0 !important;
        width: 0 !important;
        max-width: none !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }

    /* Score cards: compact 3-across layout */
    .score-card {
        padding: 10px 4px !important;
        border-radius: 15px !important;
        min-height: 76px !important;
        box-sizing: border-box !important;
    }

    .score-label {
        font-size: 0.67rem !important;
        line-height: 1.2 !important;
    }

    .score-value {
        font-size: 1.35rem !important;
        margin-top: 3px !important;
    }

    /* Status message */
    .status-card {
        padding: 12px 10px !important;
        margin: 12px 0 12px !important;
        border-radius: 15px !important;
        font-size: 0.88rem !important;
        line-height: 1.35 !important;
    }

    /* ---------- MOBILE GAME BOARD ---------- */
    .board-frame {
        padding: 8px !important;
        border-radius: 20px !important;
        box-sizing: border-box !important;
        width: 100% !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    /* Each of the 3 board rows stays exactly 3 columns wide */
    .board-frame ~ div[data-testid="stHorizontalBlock"] {
        width: 100% !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 7px !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) > div[data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) > div[data-testid="column"] {
        flex: 1 1 0 !important;
        width: 0 !important;
        max-width: none !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) div[data-testid="stButton"] {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) div[data-testid="stButton"] > button {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        min-height: 0 !important;
        height: auto !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0 !important;
        font-size: clamp(1.7rem, 9vw, 2.35rem) !important;
        line-height: 1 !important;
        border-radius: 14px !important;
        box-sizing: border-box !important;
    }

    /* Prevent text/content from creating horizontal overflow */
    .info-card {
        padding: 16px !important;
        border-radius: 18px !important;
        margin-top: 14px !important;
        overflow-wrap: anywhere !important;
    }

    .info-card h3 {
        font-size: 1.35rem !important;
        line-height: 1.25 !important;
    }

    .info-card p,
    .info-card li {
        font-size: 0.88rem !important;
        line-height: 1.5 !important;
    }

    .footer {
        font-size: 0.70rem !important;
        padding: 10px 4px !important;
    }

    /* ---------- FINAL MOBILE SIDEBAR ---------- */
    /* Keep the sidebar compact. Streamlit's mobile sidebar remains an overlay when opened. */
    section[data-testid="stSidebar"] {
        width: min(300px, 78vw) !important;
        min-width: min(300px, 78vw) !important;
        max-width: min(300px, 78vw) !important;
    }

    section[data-testid="stSidebar"] > div {
        width: min(300px, 78vw) !important;
        min-width: min(300px, 78vw) !important;
        max-width: min(300px, 78vw) !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        min-height: 50px !important;
        height: 50px !important;
        padding: 8px 10px !important;
        font-size: 0.92rem !important;
        border-radius: 13px !important;
    }

    section[data-testid="stSidebar"] .sidebar-brand {
        padding: 13px !important;
        margin-bottom: 12px !important;
    }

    section[data-testid="stSidebar"] .method-card {
        padding: 13px !important;
        margin-top: 12px !important;
    }

    /* ---------- FINAL MOBILE BOARD ---------- */
    /* Keep the 3 x 3 board inside the phone viewport with equal square cells. */
    .board-frame {
        width: 100% !important;
        max-width: 100% !important;
        padding: 6px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 7px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) > div[data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) > div[data-testid="column"] {
        flex: 1 1 0 !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: none !important;
        margin: 0 !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) div[data-testid="stButton"],
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) div[data-testid="stButton"] > button {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        min-height: 0 !important;
        height: auto !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) div[data-testid="stButton"] > button {
        font-size: clamp(1.55rem, 8vw, 2.2rem) !important;
        line-height: 1 !important;
        border-radius: 14px !important;
    }



/* ============================================================
   FINAL MOBILE POLISH — PREMIUM GAME LAYOUT
   Desktop layout and game logic remain unchanged.
   ============================================================ */
@media (max-width: 700px) {

    html, body,
    [data-testid="stAppViewContainer"],
    .stApp {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 auto !important;
        padding: 0.75rem 10px 1.25rem !important;
        box-sizing: border-box !important;
        overflow-x: hidden !important;
    }

    /* ---------- FULL-SCREEN MOBILE SIDEBAR ---------- */
    /* When opened, settings become a clean mobile drawer instead of
       leaving a strip of the game visible behind it. */
    section[data-testid="stSidebar"] {
        width: 100vw !important;
        min-width: 100vw !important;
        max-width: 100vw !important;
        box-sizing: border-box !important;
        z-index: 999999 !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 100vw !important;
        min-width: 100vw !important;
        max-width: 100vw !important;
        box-sizing: border-box !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
    }

    section[data-testid="stSidebar"] .sidebar-brand {
        margin-top: 8px !important;
        padding: 18px 16px !important;
        border-radius: 20px !important;
    }

    section[data-testid="stSidebar"] .sidebar-brand-title {
        font-size: 1.25rem !important;
    }

    section[data-testid="stSidebar"] .sidebar-brand-subtitle {
        font-size: 0.88rem !important;
        line-height: 1.45 !important;
    }

    section[data-testid="stSidebar"] .stRadio {
        margin-top: 4px !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        min-height: 52px !important;
        height: 52px !important;
        border-radius: 15px !important;
        font-size: 0.98rem !important;
    }

    section[data-testid="stSidebar"] .method-card {
        padding: 18px !important;
        border-radius: 20px !important;
    }

    /* ---------- HERO ---------- */
    .hero {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 22px 14px 19px !important;
        margin: 0 0 14px !important;
        border-radius: 22px !important;
    }

    .hero h1 {
        font-size: clamp(1.65rem, 7vw, 2rem) !important;
        line-height: 1.15 !important;
    }

    .hero p {
        font-size: 0.88rem !important;
        line-height: 1.45 !important;
        margin-top: 9px !important;
    }

    /* ---------- FEATURE BADGES ---------- */
    .pill-row {
        width: 100% !important;
        box-sizing: border-box !important;
        gap: 7px !important;
        margin: 0 0 14px !important;
    }

    .pill {
        padding: 7px 9px !important;
        font-size: 0.69rem !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
    }

    /* ---------- SCOREBOARD ---------- */
    div[data-testid="stHorizontalBlock"]:has(.score-card) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        max-width: 100% !important;
        gap: 7px !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.score-card) > div[data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"]:has(.score-card) > div[data-testid="column"] {
        flex: 1 1 0 !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: none !important;
        box-sizing: border-box !important;
    }

    .score-card {
        width: 100% !important;
        min-height: 78px !important;
        padding: 10px 3px !important;
        border-radius: 16px !important;
        box-sizing: border-box !important;
    }

    .score-label {
        font-size: 0.64rem !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
    }

    .score-value {
        font-size: 1.4rem !important;
        line-height: 1.1 !important;
    }

    /* ---------- STATUS ---------- */
    .status-card {
        width: 100% !important;
        box-sizing: border-box !important;
        margin: 12px 0 12px !important;
        padding: 12px 9px !important;
        border-radius: 16px !important;
        font-size: 0.88rem !important;
        line-height: 1.35 !important;
    }

    /* ---------- GAME BOARD ---------- */
    .board-frame {
        width: 100% !important;
        max-width: 100% !important;
        padding: 7px !important;
        margin: 0 !important;
        border-radius: 21px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }

    /* Every board row = exactly three equal cells. */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        gap: 7px !important;
        margin: 0 0 7px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) > div[data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) > div[data-testid="column"] {
        flex: 1 1 0 !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) div[data-testid="stButton"],
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) div[data-testid="stButton"] > button {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        min-height: 0 !important;
        height: auto !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0 !important;
        margin: 0 !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) div[data-testid="stButton"] > button {
        border-radius: 15px !important;
        font-size: clamp(1.55rem, 9vw, 2.25rem) !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* ---------- INFORMATION ---------- */
    .info-card {
        width: 100% !important;
        box-sizing: border-box !important;
        margin-top: 15px !important;
        padding: 17px 15px !important;
        border-radius: 20px !important;
        overflow: hidden !important;
    }

    .info-card h3 {
        font-size: 1.25rem !important;
        line-height: 1.25 !important;
        margin-bottom: 9px !important;
    }

    .info-card p,
    .info-card li {
        font-size: 0.87rem !important;
        line-height: 1.52 !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }

    div[data-testid="stExpander"] {
        width: 100% !important;
        box-sizing: border-box !important;
        margin-top: 10px !important;
        border-radius: 17px !important;
        overflow: hidden !important;
    }

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] button {
        font-size: 0.9rem !important;
    }

    /* ---------- FOOTER ---------- */
    .footer {
        width: 100% !important;
        box-sizing: border-box !important;
        margin-top: 18px !important;
        padding: 10px 5px !important;
        font-size: 0.68rem !important;
        line-height: 1.5 !important;
        overflow-wrap: anywhere !important;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# GAME CONSTANTS
# ============================================================

HUMAN = "X"
AI = "O"
EMPTY = ""

WIN_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


# ============================================================
# GAME ENGINE
# ============================================================

def check_winner(board):
    """Return X, O, Draw, or None."""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]

    if EMPTY not in board:
        return "Draw"

    return None


def available_moves(board):
    """Return all currently available board indexes."""
    return [index for index, value in enumerate(board) if value == EMPTY]


def minimax(board, depth, maximizing, alpha, beta):
    """
    Minimax with Alpha-Beta Pruning.

    The AI maximizes its score while the human minimizes it.
    Depth is used so that the AI prefers faster wins and delays losses.
    """
    result = check_winner(board)

    if result == AI:
        return 10 - depth

    if result == HUMAN:
        return depth - 10

    if result == "Draw":
        return 0

    if maximizing:
        best_score = -inf

        for move in available_moves(board):
            board[move] = AI

            score = minimax(
                board,
                depth + 1,
                False,
                alpha,
                beta,
            )

            board[move] = EMPTY

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_score

    best_score = inf

    for move in available_moves(board):
        board[move] = HUMAN

        score = minimax(
            board,
            depth + 1,
            True,
            alpha,
            beta,
        )

        board[move] = EMPTY

        best_score = min(best_score, score)
        beta = min(beta, best_score)

        if beta <= alpha:
            break

    return best_score


def find_best_move(board):
    """Find the optimal move for the AI."""
    best_score = -inf
    best_move = None

    for move in available_moves(board):
        board[move] = AI

        score = minimax(
            board,
            0,
            False,
            -inf,
            inf,
        )

        board[move] = EMPTY

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def reset_board(start_player):
    """Start a new round."""
    st.session_state.board = [EMPTY] * 9
    st.session_state.result = None
    st.session_state.turn = start_player


def update_score(result):
    """Update the scoreboard once a round finishes."""
    if result == HUMAN:
        st.session_state.human_score += 1
    elif result == AI:
        st.session_state.ai_score += 1
    elif result == "Draw":
        st.session_state.draw_score += 1


# ============================================================
# SESSION STATE
# ============================================================

if "board" not in st.session_state:
    st.session_state.human_score = 0
    st.session_state.ai_score = 0
    st.session_state.draw_score = 0
    st.session_state.starter = HUMAN
    reset_board(HUMAN)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">🎮 Tic-Tac-Toe AI</div>
            <div class="sidebar-brand-subtitle">
                CodSoft Artificial Intelligence — Task 2
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ Game Settings")

    starter_label = st.radio(
        "Who should start?",
        ["You (X)", "AI (O)"],
        index=0 if st.session_state.starter == HUMAN else 1,
    )

    selected_starter = HUMAN if starter_label == "You (X)" else AI

    if selected_starter != st.session_state.starter:
        st.session_state.starter = selected_starter
        reset_board(selected_starter)
        st.rerun()

    if st.button("🔄 New Game", use_container_width=True):
        reset_board(st.session_state.starter)
        st.rerun()

    if st.button("🧹 Reset Score", use_container_width=True):
        st.session_state.human_score = 0
        st.session_state.ai_score = 0
        st.session_state.draw_score = 0
        reset_board(st.session_state.starter)
        st.rerun()

    st.markdown(
        """
        <div class="method-card">
            <div class="method-title">🧠 AI Method</div>
            <div class="method-highlight">Minimax + Alpha-Beta Pruning</div>
            <br>
            🎯 The AI evaluates possible future game states and selects
            the optimal move.
            <br><br>
            🛡️ <b>Goal:</b> unbeatable play
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🎮 Tic-Tac-Toe AI</h1>
        <p>Challenge an unbeatable AI powered by Minimax + Alpha-Beta Pruning</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pill-row">
        <div class="pill">👤 Human vs 🤖 AI</div>
        <div class="pill">🧠 Minimax</div>
        <div class="pill">⚡ Alpha-Beta Pruning</div>
        <div class="pill">🏆 Optimal Play</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SCOREBOARD
# ============================================================

col1, col2, col3 = st.columns(3, gap="small")

with col1:
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">❌ YOU</div>
            <div class="score-value">{st.session_state.human_score}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">⭕ AI</div>
            <div class="score-value">{st.session_state.ai_score}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">🤝 DRAWS</div>
            <div class="score-value">{st.session_state.draw_score}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# AI TURN
# ============================================================

if (
    st.session_state.result is None
    and st.session_state.turn == AI
):

    best_move = find_best_move(st.session_state.board)

    if best_move is not None:
        st.session_state.board[best_move] = AI

        result = check_winner(st.session_state.board)

        if result is not None:
            st.session_state.result = result
            update_score(result)
        else:
            st.session_state.turn = HUMAN


# ============================================================
# STATUS
# ============================================================

if st.session_state.result == HUMAN:
    status_text = "🎉 You won this round! Great play."
elif st.session_state.result == AI:
    status_text = "🤖 AI wins this round. Try another strategy!"
elif st.session_state.result == "Draw":
    status_text = "🤝 It's a draw — both sides played perfectly."
elif st.session_state.turn == HUMAN:
    status_text = "👤 Your turn — choose a square."
else:
    status_text = "🤖 AI is thinking..."

st.markdown(
    f'<div class="status-card">{status_text}</div>',
    unsafe_allow_html=True,
)


# ============================================================
# BOARD
# ============================================================

st.markdown('<div class="board-frame">', unsafe_allow_html=True)

for row_start in (0, 3, 6):

    cols = st.columns(3, gap="small")

    for offset, col in enumerate(cols):

        index = row_start + offset
        value = st.session_state.board[index]

        with col:

            if value == HUMAN:
                button_label = "❌"
            elif value == AI:
                button_label = "⭕"
            else:
                button_label = " "

            disabled = (
                value != EMPTY
                or st.session_state.result is not None
                or st.session_state.turn != HUMAN
            )

            if st.button(
                button_label,
                key=f"cell_{index}",
                use_container_width=True,
                disabled=disabled,
            ):

                st.session_state.board[index] = HUMAN

                result = check_winner(st.session_state.board)

                if result is not None:
                    st.session_state.result = result
                    update_score(result)
                else:
                    st.session_state.turn = AI

                st.rerun()

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    """
<div class="info-card">
    <h3>🧠 How the AI Works</h3>
    <p>
        The AI uses the <b>Minimax algorithm</b> together with
        <b>Alpha-Beta Pruning</b> to evaluate possible future moves.
    </p>
    <p>
        Minimax explores the possible outcomes of a move and assigns
        scores to wins, losses, and draws. Alpha-Beta Pruning skips
        branches that cannot improve the final decision, reducing
        unnecessary search.
    </p>
    <p>
        <b>❌ Human:</b> X &nbsp;&nbsp;&nbsp;
        <b>⭕ AI:</b> O
    </p>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# GAME INFORMATION
# ============================================================

with st.expander("📖 Game Rules"):
    st.markdown(
        """
        1. You play as **X** and the AI plays as **O**.
        2. Players take turns placing their symbol in an empty square.
        3. Three matching symbols in a row, column, or diagonal win the round.
        4. If all nine squares are filled without a winner, the result is a draw.
        """
    )

with st.expander("🔍 Why Alpha-Beta Pruning?"):
    st.markdown(
        """
        Alpha-Beta Pruning improves Minimax by eliminating game-tree
        branches that do not need to be evaluated. This allows the AI
        to search efficiently while still selecting the same optimal move.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🎮 Tic-Tac-Toe AI &nbsp;•&nbsp;
        Minimax + Alpha-Beta Pruning &nbsp;•&nbsp;
        CodSoft Artificial Intelligence Internship — Task 2
    </div>
    """,
    unsafe_allow_html=True,
)
