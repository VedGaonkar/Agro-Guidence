"""
login_page.py — Welcome / Name Entry UI for Agro Guidance
Renders a beautiful welcome screen where the user enters their name and starts.
"""

import streamlit as st
from auth import start_session


def _inject_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ── Global reset ── */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* ── Dark page background ── */
        .stApp {
            background: radial-gradient(ellipse at 20% 20%, #0d2b1a 0%, #0a0f0d 60%, #050a07 100%);
            min-height: 100vh;
        }

        /* ── Hide Streamlit chrome ── */
        #MainMenu, footer, header { visibility: hidden; }

        /* ── Auth card wrapper ── */
        .auth-container {
            max-width: 480px;
            margin: 0 auto;
            padding: 0 1rem;
        }

        /* ── Logo / hero section ── */
        .auth-hero {
            text-align: center;
            padding: 3.5rem 0 1.5rem;
        }
        .auth-hero .logo-icon {
            font-size: 4rem;
            display: block;
            margin-bottom: 0.6rem;
            filter: drop-shadow(0 0 22px rgba(74, 222, 128, 0.6));
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50%       { transform: translateY(-8px); }
        }
        .auth-hero h1 {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 50%, #86efac 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        .auth-hero p {
            color: #6b7280;
            font-size: 0.95rem;
            margin-top: 0.4rem;
        }

        /* ── Card ── */
        .auth-card {
            background: rgba(15, 30, 20, 0.85);
            border: 1px solid rgba(74, 222, 128, 0.18);
            border-radius: 20px;
            padding: 2.5rem 2rem 2rem;
            box-shadow:
                0 25px 50px rgba(0, 0, 0, 0.5),
                inset 0 1px 0 rgba(74, 222, 128, 0.08);
            backdrop-filter: blur(16px);
            margin-bottom: 1.5rem;
        }

        /* ── Welcome label ── */
        .welcome-label {
            color: #9ca3af;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 0 0 0.5rem;
            text-align: center;
        }
        .welcome-sub {
            color: #4b5563;
            font-size: 0.85rem;
            text-align: center;
            margin: 0 0 1.5rem;
        }

        /* ── Input fields ── */
        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.4) !important;
            border: 1px solid rgba(74, 222, 128, 0.2) !important;
            border-radius: 10px !important;
            color: #e5e7eb !important;
            font-size: 1rem !important;
            padding: 0.75rem 1rem !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: rgba(74, 222, 128, 0.6) !important;
            box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.12) !important;
            outline: none !important;
        }
        .stTextInput > div > div > input::placeholder { color: #4b5563 !important; }

        /* ── Labels ── */
        .stTextInput > label {
            color: #9ca3af !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.02em !important;
            text-transform: uppercase !important;
        }

        /* ── Primary button ── */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #16a34a 0%, #15803d 50%, #166534 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.8rem 1.5rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.03em !important;
            cursor: pointer !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 15px rgba(22, 163, 74, 0.35) !important;
            margin-top: 0.8rem !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(22, 163, 74, 0.5) !important;
        }
        .stButton > button:active { transform: translateY(0) !important; }

        /* ── Selectbox (language picker) ── */
        .stSelectbox > div > div {
            background-color: rgba(0, 0, 0, 0.4) !important;
            border: 1px solid rgba(74, 222, 128, 0.2) !important;
            border-radius: 10px !important;
            color: #e5e7eb !important;
            font-size: 0.95rem !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        .stSelectbox > div > div:focus-within {
            border-color: rgba(74, 222, 128, 0.6) !important;
            box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.12) !important;
        }
        .stSelectbox > label {
            color: #9ca3af !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.02em !important;
            text-transform: uppercase !important;
        }
        [data-baseweb="select"] { background-color: transparent !important; }
        [data-baseweb="popover"] {
            background-color: #0f1e14 !important;
            border: 1px solid rgba(74, 222, 128, 0.2) !important;
            border-radius: 10px !important;
        }

        /* ── Alerts ── */
        .stSuccess, .stError, .stWarning {
            border-radius: 10px !important;
            font-size: 0.875rem !important;
        }

        /* ── Footer note ── */
        .auth-footer {
            text-align: center;
            color: #374151;
            font-size: 0.75rem;
            padding-bottom: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_login_page():
    """Render the welcome / name-entry page."""
    _inject_styles()

    # ── Hero ──────────────────────────────────────────────
    st.markdown(
        """
        <div class="auth-hero">
            <span class="logo-icon">🌱</span>
            <h1>Agro Guidance</h1>
            <p>Your intelligent farming companion</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Card start ────────────────────────────────────────
    st.markdown('<div class="auth-container"><div class="auth-card">', unsafe_allow_html=True)

    from translations import t

    # ── Indian language options ───────────────────────────
    LANGUAGES = {
        "🇮🇳 हिन्दी (Hindi)":       "Hindi",
        "🇮🇳 मराठी (Marathi)":      "Marathi",
        "🇮🇳 தமிழ் (Tamil)":        "Tamil",
        "🇮🇳 తెలుగు (Telugu)":      "Telugu",
        "🇮🇳 ಕನ್ನಡ (Kannada)":      "Kannada",
        "🇮🇳 മലയാളം (Malayalam)":  "Malayalam",
        "🇮🇳 বাংলা (Bengali)":      "Bengali",
        "🇮🇳 ગુજરાતી (Gujarati)":  "Gujarati",
        "🇮🇳 ਪੰਜਾਬੀ (Punjabi)":    "Punjabi",
        "🇮🇳 ଓଡ଼ିଆ (Odia)":         "Odia",
        "🇮🇳 অসমীয়া (Assamese)":   "Assamese",
        "🇮🇳 اردو (Urdu)":          "Urdu",
        "🇮🇳 कोंकणी (Konkani)":     "Konkani",
        "🇮🇳 মণিপুরি (Manipuri)":   "Manipuri",
        "🇬🇧 English":              "English",
    }

    # Put language selector outside the form so it triggers a rerun immediately!
    selected_display = st.selectbox(
        t("Preferred Language"),
        options=list(LANGUAGES.keys()),
        index=0,
        key="entry_language",
    )
    
    st.session_state.language = LANGUAGES[selected_display]

    st.markdown(f'<p class="welcome-label">👋 {t("Welcome")}!</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="welcome-sub">{t("Choose your language & enter your name to get started")}</p>', unsafe_allow_html=True)

    with st.form("name_form", clear_on_submit=False):
        name = st.text_input(t("Your Name"), placeholder=t("e.g. Ravi Sharma"), key="entry_name")
        submitted = st.form_submit_button(f"🌾  {t('Start Exploring')} →")

    if submitted:
        result = start_session(name)
        if result["success"]:
            st.session_state.logged_in = True
            st.session_state.current_user = result["user"]
            st.success(f"{t('Welcome')}, {result['user']['name']}! {t('Let us grow together')} 🌿")
            st.rerun()
        else:
            st.error(t(result["message"]))

    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="auth-footer">🌿 Agro Guidance · {t("Empowering Farmers with Technology")}</div>',
        unsafe_allow_html=True,
    )

