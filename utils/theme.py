"""
VivaLingo Design System
Clean, modern, Duolingo-inspired interface for Spanish learning.
"""
import streamlit as st
from textwrap import dedent

# =============================================================================
# DESIGN TOKENS
# =============================================================================

COLORS = {
    # Primary palette
    "primary": "#58CC02",        # Duolingo green - main actions
    "primary_dark": "#46A302",   # Darker green for hover
    "primary_light": "#89E219",  # Lighter green for backgrounds

    # Secondary palette
    "blue": "#1CB0F6",           # Info, links
    "purple": "#CE82FF",         # Achievements, streaks
    "orange": "#FF9600",         # Warnings, fire/streak
    "red": "#FF4B4B",            # Errors, hearts
    "gold": "#FFC800",           # XP, rewards

    # Neutrals
    "white": "#FFFFFF",
    "bg": "#FFFFFF",             # Main background
    "bg_secondary": "#F7F7F7",   # Cards, sidebar
    "bg_tertiary": "#EFEFEF",    # Hover states
    "border": "#E5E5E5",         # Borders
    "border_light": "#F0F0F0",   # Subtle borders

    # Text
    "text": "#3C3C3C",           # Primary text
    "text_secondary": "#777777", # Secondary text
    "text_muted": "#AFAFAF",     # Muted text
}

FONTS = {
    "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif",
    "size_xs": "12px",
    "size_sm": "14px",
    "size_base": "16px",
    "size_lg": "18px",
    "size_xl": "24px",
    "size_2xl": "32px",
    "size_3xl": "40px",
}

SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "2xl": "48px",
}

RADII = {
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "20px",
    "full": "9999px",
}

# =============================================================================
# MAIN CSS
# =============================================================================

def get_css() -> str:
    """Ultra-aggressive white theme CSS with color-scheme override."""
    return """
    <meta name="color-scheme" content="light only">
    <meta name="theme-color" content="#FFFFFF">
    <style>
    /* ============================================
       iPHONE-STYLE DESIGN SYSTEM
       Pure White • Colorful Accents • Clean
       ============================================ */
    :root {
        --bg-surface: rgba(255, 255, 255, 0.03);
        --bg-elevated: rgba(255, 255, 255, 0.06);
        --surface: rgba(255, 255, 255, 0.03);
        --border: rgba(255, 255, 255, 0.08);
        --primary: #6366f1;
        --accent: #6366f1;
        --accent-muted: rgba(99, 102, 241, 0.15);
        --text-primary: #ffffff;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
    }
    .stApp,
    .stApp > div,
    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > *,
    [data-testid="stVerticalBlock"],
    .main .block-container {
        background: linear-gradient(180deg, #0c0c0f 0%, #111118 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif, 'Apple Color Emoji',
            'Segoe UI Emoji', 'Noto Color Emoji' !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Hide Streamlit branding */
    footer,
    #MainMenu,
    .stDeployButton,
    [data-testid="stToolbar"] {
        display: none !important;
    }

    /* Keep header for sidebar toggle, but make it subtle */
    header[data-testid="stHeader"] {
        background: transparent !important;
        border-bottom: none !important;
        height: 2.5rem !important;
    }

    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"] > button,
    [data-testid="collapsedControl"],
    [data-testid="collapsedControl"] > button {
        opacity: 1 !important;
        pointer-events: auto !important;
        color: #ffffff !important;
    }

    /* ============================================
       SIDEBAR - Clean White
       ============================================ */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div > div,
    [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background: #F2F2F7 !important;
        background-color: #F2F2F7 !important;
    }

/* ============================================ */
/* SIDEBAR                                       */
/* ============================================ */

[data-testid="stSidebar"] {
    background-color: #F7F7F7 !important;
    border-right: 1px solid #E5E5E5 !important;
}

    /* Sidebar content */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #8E8E93 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label {
        color: #000000 !important;
    }

    /* Hide default Streamlit pages navigation (use custom nav) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* ============================================
       TYPOGRAPHY - iOS Style
       ============================================ */
    html, body, .stApp, .stMarkdown, p, span, div, label, button, input, textarea {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Inter', 'Helvetica Neue', sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
    }

    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #000000 !important;
        font-weight: 700 !important;
    }

[data-testid="stSidebarContent"] {
    background-color: #F7F7F7 !important;
}

    /* Buttons */
    .stButton > button {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
        font-weight: 600 !important;
        font-size: 17px !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        min-height: 50px !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }

    /* Secondary button - Light gray fill */
    .stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
        background: #F2F2F7 !important;
        color: #007AFF !important;
    }

    .stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover {
        background: #E5E5EA !important;
    }

    /* Primary button - iOS Blue */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #6366f1 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }

    .stButton > button:disabled {
        color: #cbd5f5 !important;
        opacity: 0.6 !important;
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }

    /* ============================================
       FORM INPUTS - iOS Style
       ============================================ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background: rgba(15, 15, 20, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    div[data-baseweb="input"] input:focus,
    div[data-baseweb="textarea"] textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder,
    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {
        color: #64748b !important;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        caret-color: #e2e8f0 !important;
    }

/* ============================================ */
/* TYPOGRAPHY                                   */
/* ============================================ */

    /* Radio buttons - make selection obvious */
    div[role="radiogroup"] input[type="radio"] {
        accent-color: #6366f1 !important;
    }

    div[role="radiogroup"] label[data-baseweb="radio"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
        margin-right: 8px !important;
    }

    div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] {
        background: rgba(99, 102, 241, 0.2) !important;
        border-color: rgba(99, 102, 241, 0.6) !important;
    }

    div[role="radiogroup"] label[data-baseweb="radio"] span {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }

    /* Dropdown popover */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    div[role="listbox"],
    ul[role="listbox"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
    }

    [data-baseweb="menu"] li,
    div[role="option"],
    li[role="option"] {
        color: #0f172a !important;
    }

.stMarkdown p {
    color: #3C3C3C !important;
    line-height: 1.6 !important;
}

/* ============================================ */
/* BUTTONS                                      */
/* ============================================ */

/* Primary button - Green */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background-color: #58CC02 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 24px !important;
    min-height: 48px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 0 #46A302 !important;
    transition: all 0.1s ease !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    background-color: #46A302 !important;
    transform: translateY(2px) !important;
    box-shadow: 0 2px 0 #3A8A02 !important;
}

.stButton > button[kind="primary"]:active,
.stButton > button[data-testid="baseButton-primary"]:active {
    transform: translateY(4px) !important;
    box-shadow: none !important;
}

/* Secondary button - Gray outline */
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
    background-color: #FFFFFF !important;
    color: #777777 !important;
    border: 2px solid #E5E5E5 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 10px 22px !important;
    min-height: 48px !important;
    box-shadow: 0 4px 0 #E5E5E5 !important;
    transition: all 0.1s ease !important;
}

.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover {
    background-color: #F7F7F7 !important;
    border-color: #D5D5D5 !important;
    transform: translateY(2px) !important;
    box-shadow: 0 2px 0 #D5D5D5 !important;
}

/* Disabled button */
.stButton > button:disabled {
    opacity: 0.5 !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ============================================ */
/* FORM INPUTS                                  */
/* ============================================ */

.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    background-color: #FFFFFF !important;
    border: 2px solid #E5E5E5 !important;
    border-radius: 12px !important;
    color: #3C3C3C !important;
    font-size: 16px !important;
    padding: 12px 16px !important;
}

    /* Dropdown menus */
    [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E5EA !important;
        border-radius: 16px !important;
        padding: 16px !important;
        text-align: center !important;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        text-align: center !important;
    }

    .stat-value {
        font-size: 34px !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }

    .metric-value {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        line-height: 1 !important;
        margin-bottom: 0.25rem !important;
    }

    .stat-label {
        font-size: 13px !important;
        color: #8E8E93 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-weight: 600 !important;
    }

    .metric-label {
        font-size: 0.8rem !important;
        color: #64748b !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Action Card */
    .action-card {
        background: #FFFFFF !important;
    }

    .feedback-success {
        background: rgba(52, 199, 89, 0.12) !important;
        color: #248A3D !important;
    }

    .feedback-error {
        background: rgba(255, 59, 48, 0.12) !important;
        color: #D70015 !important;
    }

    .feedback-warning {
        background: rgba(255, 149, 0, 0.12) !important;
        color: #C93400 !important;
    }

    .feedback-info {
        background: rgba(0, 122, 255, 0.12) !important;
        color: #0040DD !important;
    }

    /* Hero section */
    .hero {
        background: linear-gradient(135deg, rgba(0, 122, 255, 0.08), rgba(90, 200, 250, 0.08)) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
    }

    .hero-title {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }

    .hero-subtitle {
        color: #8E8E93 !important;
        font-size: 17px !important;
    }

    .emoji-flag {
        width: 52px;
        height: 52px;
        display: inline-block;
        margin-bottom: 16px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.25); }

    /* Focus states for accessibility */
    *:focus-visible {
        outline: 2px solid #6366f1 !important;
        outline-offset: 2px !important;
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }
    </style>
    """


def apply_theme():
    """Apply the theme CSS to the page."""
    st.markdown(get_css(), unsafe_allow_html=True)


def _clean_html(markup: str) -> str:
    """Normalize HTML markup to avoid markdown code blocks."""
    return dedent(markup).strip()


def render_html(markup: str) -> None:
    """Render HTML with consistent formatting."""
    st.markdown(_clean_html(markup), unsafe_allow_html=True)


# ============================================
# COMPONENT FUNCTIONS
# ============================================

def render_hero(title: str, subtitle: str = "", pills: list = None) -> None:
    pills_html = ""
    if pills:
        pills_html = '<div style="margin-bottom: 12px;">' + ' '.join(
            f'<span class="pill pill-blue">{p}</span>' for p in pills
        ) + '</div>'

    render_html(f"""
        <div class="hero">
            {pills_html}
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
    """)


def render_section_header(title: str, subtitle: str = "") -> None:
    """Render a section header."""
    subtitle_html = f'<p style="color: #777777; margin: 4px 0 0 0; font-size: 15px;">{subtitle}</p>' if subtitle else ''
    st.markdown(f'''
    <div style="margin-bottom: 16px;">
        <h2 style="color: #3C3C3C !important; margin: 0; font-size: 24px; font-weight: 700;">{title}</h2>
        {subtitle_html}
    </div>
    ''', unsafe_allow_html=True)


def render_metric_card(value: str, label: str, icon: str = "", color: str = "#007AFF") -> str:
    """Return HTML for a metric card."""
    icon_html = f'<div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>' if icon else ''
    return _clean_html(f"""
        <div class="stat-card">
            {icon_html}
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
    """)


def render_metric_grid(metrics: list) -> None:
    """Render a grid of metric cards."""
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            st.markdown(render_metric_card(
                str(m.get("value", "0")),
                m.get("label", ""),
                m.get("icon", ""),
                m.get("color", "#58CC02")
            ), unsafe_allow_html=True)


def render_action_card(title: str, subtitle: str, icon: str = "",
                       primary: bool = False, badge: str = "") -> None:
    """Render an action card."""
    bg_color = "linear-gradient(135deg, #58CC02, #89E219)" if primary else "#FFFFFF"
    text_color = "#FFFFFF" if primary else "#3C3C3C"
    subtitle_color = "rgba(255,255,255,0.9)" if primary else "#777777"
    border = "none" if primary else "2px solid #E5E5E5"

    icon_html = f'<div style="font-size: 36px; margin-bottom: 12px;">{icon}</div>' if icon else ''
    badge_html = f'''<span style="background: rgba(255,255,255,0.2); color: {text_color};
                     padding: 4px 12px; border-radius: 12px; font-size: 13px; font-weight: 700;">
                     {badge}</span>''' if badge else ''

    st.markdown(f'''
    <div style="background: {bg_color}; border: {border}; border-radius: 16px;
                padding: 24px; margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                {icon_html}
                <div style="font-size: 20px; font-weight: 700; color: {text_color}; margin-bottom: 4px;">
                    {title}
                </div>
                <div style="font-size: 15px; color: {subtitle_color};">{subtitle}</div>
            </div>
            {badge_html}
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_streak_badge(streak: int) -> None:
    """Render a streak badge with fire icon."""
    if streak > 0:
        st.markdown(f'''
        <div style="display: inline-flex; align-items: center; gap: 8px;
                    background: linear-gradient(135deg, #FF9600 0%, #FF4B4B 100%);
                    color: #FFFFFF; padding: 10px 20px; border-radius: 20px; font-weight: 700;">
            <span style="font-size: 24px;">🔥</span>
            <span style="font-size: 24px;">{streak}</span>
            <span style="font-size: 14px; opacity: 0.9;">day{"s" if streak != 1 else ""}</span>
        </div>
        ''', unsafe_allow_html=True)


def render_feedback(feedback_type: str, message: str, details: str = "") -> None:
    """Render a feedback box."""
    details_html = f'<div style="margin-top: 8px; opacity: 0.9;">{details}</div>' if details else ''
    render_html(f"""
        <div class="feedback-box feedback-{feedback_type}">
            <strong>{message}</strong>
            {details_html}
        </div>
    """)


def render_card(content: str, title: str = "") -> None:
    """Render a glass card."""
    title_html = f'<h4 style="margin-bottom: 12px; color: #ffffff;">{title}</h4>' if title else ''
    render_html(f"""
        <div class="glass-card">
            {title_html}
            <div style="color: #94a3b8;">{content}</div>
        </div>
    """)


def render_pill(text: str, variant: str = "green") -> str:
    """Return HTML for a pill/badge."""
    colors = {
        "green": ("#58CC02", "rgba(88, 204, 2, 0.15)"),
        "blue": ("#1CB0F6", "rgba(28, 176, 246, 0.15)"),
        "orange": ("#FF9600", "rgba(255, 150, 0, 0.15)"),
        "red": ("#FF4B4B", "rgba(255, 75, 75, 0.15)"),
        "purple": ("#CE82FF", "rgba(206, 130, 255, 0.15)"),
        "gold": ("#FFC800", "rgba(255, 200, 0, 0.15)"),
    }
    fg, bg = colors.get(variant, colors["green"])
    return f'''<span style="display: inline-block; padding: 6px 14px; border-radius: 20px;
               font-size: 13px; font-weight: 700; background: {bg}; color: {fg};">{text}</span>'''


def render_feedback(feedback_type: str, message: str, details: str = "") -> None:
    """Render feedback message (success, error, warning, info)."""
    styles = {
        "success": ("#58CC02", "rgba(88, 204, 2, 0.1)", "✓"),
        "error": ("#FF4B4B", "rgba(255, 75, 75, 0.1)", "✗"),
        "warning": ("#FF9600", "rgba(255, 150, 0, 0.1)", "⚠"),
        "info": ("#1CB0F6", "rgba(28, 176, 246, 0.1)", "ℹ"),
    }
    color, bg, icon = styles.get(feedback_type, styles["info"])
    details_html = f'<div style="margin-top: 12px; font-size: 15px;">{details}</div>' if details else ''

def render_action_card(title: str, subtitle: str, meta: str = "", primary: bool = False, icon: str = "") -> None:
    bg = "rgba(0,122,255,0.1)" if primary else "#FFFFFF"
    border = "#007AFF" if primary else "#E5E5EA"
    icon_html = f'<span style="font-size: 32px; margin-right: 16px;">{icon}</span>' if icon else ''
    meta_html = f'<div style="font-size: 13px; color: #8E8E93; margin-top: 4px;">{meta}</div>' if meta else ''

    render_html(f"""
        <div class="action-card {primary_class}">
            <div style="display: flex; align-items: flex-start;">
                {icon_html}
                <div>
                    <div class="action-card-title">{title}</div>
                    <div class="action-card-subtitle">{subtitle}</div>
                    {meta_html}
                </div>
            </div>
        </div>
    """)


def render_streak_badge(streak: int) -> None:
    if streak > 0:
        render_html(f"""
            <div style="display: inline-flex; align-items: center; gap: 10px;
                        background: rgba(245, 158, 11, 0.15); padding: 10px 18px;
                        border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.3);">
                <span style="font-size: 1.5rem;">🔥</span>
                <span style="font-size: 1.25rem; font-weight: 700; color: #fbbf24;">{streak}</span>
                <span style="color: #94a3b8; font-size: 0.9rem;">day{'s' if streak != 1 else ''}</span>
            </div>
        """)


def render_empty_state(message: str, icon: str = "📭") -> None:
    """Render an empty state."""
    render_html(f"""
        <div style="text-align: center; padding: 3rem 1rem; color: #64748b;">
            <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">{icon}</div>
            <p style="color: #64748b;">{message}</p>
        </div>
    """)


def render_loading_skeleton(height: str = "100px") -> None:
    """Render a loading skeleton."""
    render_html(f"""
        <div style="background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.03) 75%);
                    background-size: 200% 100%; height: {height}; border-radius: 12px;
                    animation: shimmer 1.5s infinite;">
        </div>
        <style>
        @keyframes shimmer {{ 0% {{ background-position: 200% 0; }} 100% {{ background-position: -200% 0; }} }}
        </style>
    """)


def render_error_state(message: str, retry_label: str = "Try again") -> bool:
    """Render error state. Returns True if retry clicked."""
    render_html(f"""
        <div style="text-align: center; padding: 2rem; background: rgba(239, 68, 68, 0.1);
                    border-radius: 16px; border: 1px solid rgba(239, 68, 68, 0.3);">
            <p style="color: #f87171; font-size: 1.1rem;"><strong>Something went wrong</strong></p>
            <p style="color: #f87171; opacity: 0.9;">{message}</p>
        </div>
    """)
    return st.button(retry_label, type="primary")


def render_profile_card(name: str, level: str, vocab_count: int, streak: int, is_active: bool = False) -> str:
    """Render a profile card."""
    border_color = "#007AFF" if is_active else "#E5E5EA"
    badge = '<span class="pill pill-green">Active</span>' if is_active else ''

    return _clean_html(f"""
        <div class="glass-card" style="{border}">
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                <div>
                    <div style="font-weight: 600; font-size: 1.1rem; color: #ffffff;">{name}</div>
                    <div style="font-size: 0.875rem; color: #64748b;">Level: {level}</div>
                </div>
                {badge}
            </div>
            <div style="display: flex; gap: 24px;">
                <div>
                    <div style="font-weight: 700; font-size: 1.25rem; color: #ffffff;">{vocab_count}</div>
                    <div style="font-size: 0.75rem; color: #64748b;">Words</div>
                </div>
                <div>
                    <div style="font-weight: 700; font-size: 1.25rem; color: #fbbf24;">{streak}🔥</div>
                    <div style="font-size: 0.75rem; color: #64748b;">Streak</div>
                </div>
            </div>
        </div>
    """)


def render_cloze_sentence(before: str, after: str, answer: str = "", show_answer: bool = False) -> None:
    """Render a cloze deletion sentence."""
    if show_answer:
        blank = f'''<span style="background: rgba(88, 204, 2, 0.2); color: #58CC02;
                    padding: 4px 16px; border-radius: 8px; font-weight: 700;">{answer}</span>'''
    else:
        blank = '<span class="cloze-blank">_____</span>'

    render_html(f"""
        <div class="exercise-prompt">
            {before}{blank}{after}
        </div>
    """)


def render_exercise_feedback(correct: bool, correct_answer: str, explanation: str = "",
                            common_mistake: str = "") -> None:
    """Render exercise feedback."""
    if correct:
        render_html(f"""
            <div class="feedback-box feedback-success">
                <strong>✓ Correct!</strong>
                {f'<div style="margin-top: 8px;">{explanation}</div>' if explanation else ''}
            </div>
        """)
    else:
        mistake_html = f'<div style="margin-top: 8px; opacity: 0.85;"><em>Tip: {common_mistake}</em></div>' if common_mistake else ''
        render_html(f"""
            <div class="feedback-box feedback-error">
                <strong>✗ Not quite</strong>
                <div style="margin-top: 8px;">Correct answer: <strong>{correct_answer}</strong></div>
                {f'<div style="margin-top: 8px;">{explanation}</div>' if explanation else ''}
                {mistake_html}
            </div>
        """)


def render_lesson_card(title: str, subtitle: str, progress: int = 0, icon: str = "📚",
                      locked: bool = False) -> None:
    """Render a lesson card."""
    opacity = "0.5" if locked else "1"
    lock_icon = "🔒 " if locked else ""
    progress_bar = f'''
    <div style="background: rgba(255,255,255,0.3); border-radius: 4px; height: 8px; margin-top: 12px;">
        <div style="background: #FFFFFF; height: 100%; width: {progress}%; border-radius: 4px;"></div>
    </div>
    ''' if progress > 0 and not locked else ''

    st.markdown(f'''
    <div style="background: linear-gradient(135deg, #58CC02, #89E219); border-radius: 16px;
                padding: 20px; margin-bottom: 12px; opacity: {opacity};">
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="font-size: 36px;">{icon}</div>
            <div style="flex: 1;">
                <div style="font-size: 18px; font-weight: 700; color: #FFFFFF;">{lock_icon}{title}</div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.9);">{subtitle}</div>
                {progress_bar}
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_quick_actions(actions: list) -> None:
    """Render quick action buttons in a grid."""
    cols = st.columns(len(actions))
    for col, action in zip(cols, actions):
        with col:
            if st.button(
                f"{action.get('icon', '')} {action.get('label', '')}",
                key=action.get('key', action.get('label', 'action')),
                use_container_width=True,
                type=action.get('type', 'secondary')
            ):
                if action.get('callback'):
                    action['callback']()


def render_domain_coverage(domains: dict) -> None:
    """Render domain coverage bars."""
    for domain, coverage in domains.items():
        render_progress_bar(int(coverage), 100, domain)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_design_system() -> dict:
    """Return the design system tokens."""
    return {
        "colors": COLORS,
        "fonts": FONTS,
        "spacing": SPACING,
        "radii": RADII,
    }


def validate_exercise(exercise: dict) -> dict:
    """Validate exercise structure."""
    errors = []
    ex_type = exercise.get("type", "")

    if ex_type == "cloze":
        if "before" not in exercise or "after" not in exercise:
            errors.append("Cloze must have 'before' and 'after'")
        if not exercise.get("answer"):
            errors.append("Cloze must have an answer")
    elif ex_type == "mcq":
        if not exercise.get("choices") or len(exercise.get("choices", [])) < 2:
            errors.append("MCQ must have at least 2 choices")

    if not exercise.get("type"):
        errors.append("Exercise must have a type")

    return {"valid": len(errors) == 0, "errors": errors}


def get_instruction_for_type(ex_type: str) -> str:
    """Get instruction text for exercise type."""
    return {
        "cloze": "Fill in the blank with the correct word",
        "mcq": "Choose the correct answer",
        "translate": "Translate into Spanish",
        "free_recall": "Type the missing word",
    }.get(ex_type, "Complete the exercise")


def normalize_spanish_answer(text: str, strict_accents: bool = False) -> str:
    """Normalize Spanish text for answer comparison."""
    import re
    text = text.strip().lower()
    text = ' '.join(text.split())
    text = re.sub(r'[^\w\sáéíóúüñ]', '', text)

    if not strict_accents:
        text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i')
        text = text.replace('ó', 'o').replace('ú', 'u').replace('ü', 'u')

    return text


def check_answer(user_answer: str, correct_answers: list, strict_accents: bool = False) -> dict:
    """Check user answer against correct answers."""
    user_norm = normalize_spanish_answer(user_answer, strict_accents=True)
    user_fold = normalize_spanish_answer(user_answer, strict_accents=False)

    for answer in correct_answers:
        ans_norm = normalize_spanish_answer(answer, strict_accents=True)
        ans_fold = normalize_spanish_answer(answer, strict_accents=False)

        if user_norm == ans_norm:
            return {"result": "correct", "matched": answer, "feedback": ""}
        if user_fold == ans_fold:
            return {"result": "almost", "matched": answer, "feedback": f"Watch the accents: {answer}"}

    return {"result": "incorrect", "matched": None, "feedback": f"Correct answer: {correct_answers[0]}"}
