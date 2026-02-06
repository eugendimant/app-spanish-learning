"""
VivaLingo Design System
Clean, modern, Duolingo-inspired interface for Spanish learning.
"""
import streamlit as st

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
    """Return the main CSS stylesheet."""
    return '''<style>
/* ============================================ */
/* BASE STYLES                                  */
/* ============================================ */

/* Force light mode */
:root {
    color-scheme: light;
}

/* Reset and base */
.stApp {
    background-color: #FFFFFF !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
}

.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}

/* ============================================ */
/* SIDEBAR                                       */
/* ============================================ */

[data-testid="stSidebar"] {
    background-color: #F7F7F7 !important;
    border-right: 1px solid #E5E5E5 !important;
}

[data-testid="stSidebar"] > div:first-child {
    background-color: #F7F7F7 !important;
    padding-top: 1rem !important;
}

[data-testid="stSidebarContent"] {
    background-color: #F7F7F7 !important;
}

/* Hide default collapse button */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Sidebar text */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #3C3C3C !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #3C3C3C !important;
}

/* ============================================ */
/* TYPOGRAPHY                                   */
/* ============================================ */

h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #3C3C3C !important;
    font-weight: 700 !important;
}

p, span, label, div {
    color: #3C3C3C;
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

.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #1CB0F6 !important;
    box-shadow: 0 0 0 3px rgba(28, 176, 246, 0.2) !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea textarea::placeholder {
    color: #AFAFAF !important;
}

/* ============================================ */
/* PROGRESS BARS                                */
/* ============================================ */

.stProgress > div > div {
    background-color: #E5E5E5 !important;
    border-radius: 8px !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #58CC02, #89E219) !important;
    border-radius: 8px !important;
}

/* ============================================ */
/* TABS                                         */
/* ============================================ */

.stTabs [data-baseweb="tab-list"] {
    background-color: #F7F7F7 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #777777 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: #3C3C3C !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}

/* ============================================ */
/* ALERTS                                       */
/* ============================================ */

.stAlert {
    border-radius: 12px !important;
    border: none !important;
}

/* ============================================ */
/* EXPANDER                                     */
/* ============================================ */

.streamlit-expanderHeader {
    background-color: #F7F7F7 !important;
    border-radius: 12px !important;
    color: #3C3C3C !important;
}

.streamlit-expanderContent {
    background-color: #FFFFFF !important;
    border: 1px solid #E5E5E5 !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
}

/* ============================================ */
/* HIDE STREAMLIT ELEMENTS                      */
/* ============================================ */

#MainMenu,
footer,
[data-testid="stToolbar"] {
    display: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ============================================ */
/* CUSTOM COMPONENT CLASSES                     */
/* ============================================ */

/* Legacy class support - backward compatible */
.card, .glass-card, .vl-card {
    background: #FFFFFF !important;
    border: 2px solid #E5E5E5 !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin-bottom: 16px !important;
    color: #3C3C3C !important;
}

.card h3, .card h4, .glass-card h3, .glass-card h4 {
    color: #3C3C3C !important;
    font-weight: 700 !important;
    margin-bottom: 8px !important;
}

.card p, .glass-card p {
    color: #777777 !important;
}

/* Stat cards - legacy support */
.stat-card, .vl-stat {
    background: #FFFFFF !important;
    border: 2px solid #E5E5E5 !important;
    border-radius: 16px !important;
    padding: 20px !important;
    text-align: center !important;
    margin-bottom: 12px !important;
}

.stat-value, .vl-stat-value {
    font-size: 32px !important;
    font-weight: 800 !important;
    color: #58CC02 !important;
    line-height: 1.2 !important;
}

.stat-label, .vl-stat-label {
    font-size: 12px !important;
    color: #777777 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-top: 6px !important;
}

/* Action cards - legacy support */
.action-card {
    background: #FFFFFF !important;
    border: 2px solid #E5E5E5 !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin-bottom: 12px !important;
}

.action-card-primary {
    background: linear-gradient(135deg, #58CC02, #89E219) !important;
    border: none !important;
    color: #FFFFFF !important;
}

.action-card-title {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #3C3C3C !important;
}

.action-card-primary .action-card-title {
    color: #FFFFFF !important;
}

.action-card-subtitle {
    font-size: 14px !important;
    color: #777777 !important;
}

.action-card-primary .action-card-subtitle {
    color: rgba(255, 255, 255, 0.9) !important;
}

/* Pills/Badges - legacy support */
.pill {
    display: inline-block !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}

.pill-accent, .pill-blue {
    background: rgba(28, 176, 246, 0.15) !important;
    color: #1CB0F6 !important;
}

.pill-success, .pill-green {
    background: rgba(88, 204, 2, 0.15) !important;
    color: #58CC02 !important;
}

.pill-warning, .pill-orange {
    background: rgba(255, 150, 0, 0.15) !important;
    color: #FF9600 !important;
}

.pill-error, .pill-red {
    background: rgba(255, 75, 75, 0.15) !important;
    color: #FF4B4B !important;
}

/* Progress ring */
.vl-progress-ring {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: conic-gradient(#58CC02 var(--progress, 0%), #E5E5E5 0%);
    position: relative;
}

.vl-progress-ring::before {
    content: "";
    position: absolute;
    width: 100px;
    height: 100px;
    background: #FFFFFF;
    border-radius: 50%;
}

/* Badge/Pill */
.vl-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
}

.vl-badge-green {
    background: rgba(88, 204, 2, 0.15);
    color: #58CC02;
}

.vl-badge-blue {
    background: rgba(28, 176, 246, 0.15);
    color: #1CB0F6;
}

.vl-badge-orange {
    background: rgba(255, 150, 0, 0.15);
    color: #FF9600;
}

.vl-badge-red {
    background: rgba(255, 75, 75, 0.15);
    color: #FF4B4B;
}

.vl-badge-purple {
    background: rgba(206, 130, 255, 0.15);
    color: #CE82FF;
}

/* Streak badge */
.vl-streak {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #FF9600 0%, #FF4B4B 100%);
    color: #FFFFFF;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 700;
}

/* XP badge */
.vl-xp {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #FFC800;
    color: #3C3C3C;
    padding: 6px 12px;
    border-radius: 16px;
    font-weight: 700;
    font-size: 14px;
}

/* Action card */
.vl-action-card {
    background: #FFFFFF;
    border: 2px solid #E5E5E5;
    border-radius: 16px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.vl-action-card:hover {
    border-color: #1CB0F6;
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

/* Success feedback */
.vl-success {
    background: rgba(88, 204, 2, 0.1);
    border: 2px solid #58CC02;
    border-radius: 16px;
    padding: 20px;
    color: #3C3C3C;
}

/* Error feedback */
.vl-error {
    background: rgba(255, 75, 75, 0.1);
    border: 2px solid #FF4B4B;
    border-radius: 16px;
    padding: 20px;
    color: #3C3C3C;
}

/* Lesson card */
.vl-lesson {
    background: #FFFFFF;
    border: 2px solid #E5E5E5;
    border-radius: 20px;
    overflow: hidden;
}

.vl-lesson-header {
    background: linear-gradient(135deg, #58CC02, #89E219);
    padding: 24px;
    color: #FFFFFF;
}

.vl-lesson-content {
    padding: 24px;
}
</style>'''


def apply_theme():
    """Apply the theme CSS to the page."""
    st.markdown(get_css(), unsafe_allow_html=True)


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_hero(title: str, subtitle: str = "", icon: str = "") -> None:
    """Render a hero section with gradient background."""
    icon_html = f'<div style="font-size: 48px; margin-bottom: 16px;">{icon}</div>' if icon else ''
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, #58CC02 0%, #89E219 100%);
                border-radius: 20px; padding: 32px; margin-bottom: 24px; color: #FFFFFF;">
        {icon_html}
        <h1 style="color: #FFFFFF !important; margin: 0 0 8px 0; font-size: 32px;">{title}</h1>
        <p style="color: rgba(255,255,255,0.9) !important; margin: 0; font-size: 18px;">{subtitle}</p>
    </div>
    ''', unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = "") -> None:
    """Render a section header."""
    subtitle_html = f'<p style="color: #777777; margin: 4px 0 0 0; font-size: 15px;">{subtitle}</p>' if subtitle else ''
    st.markdown(f'''
    <div style="margin-bottom: 16px;">
        <h2 style="color: #3C3C3C !important; margin: 0; font-size: 24px; font-weight: 700;">{title}</h2>
        {subtitle_html}
    </div>
    ''', unsafe_allow_html=True)


def render_stat_card(value: str, label: str, icon: str = "", color: str = "#58CC02") -> None:
    """Render a statistic card."""
    icon_html = f'<div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>' if icon else ''
    st.markdown(f'''
    <div style="background: #FFFFFF; border: 2px solid #E5E5E5; border-radius: 16px;
                padding: 24px; text-align: center;">
        {icon_html}
        <div style="font-size: 36px; font-weight: 800; color: {color}; line-height: 1;">{value}</div>
        <div style="font-size: 13px; color: #777777; text-transform: uppercase;
                    letter-spacing: 1px; margin-top: 8px;">{label}</div>
    </div>
    ''', unsafe_allow_html=True)


def render_metric_card(value: str, label: str, icon: str = "", color: str = "#58CC02") -> str:
    """Return HTML for a metric card (for use in columns)."""
    icon_html = f'<div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>' if icon else ''
    return f'''
    <div style="background: #FFFFFF; border: 2px solid #E5E5E5; border-radius: 16px;
                padding: 20px; text-align: center;">
        {icon_html}
        <div style="font-size: 32px; font-weight: 800; color: {color}; line-height: 1;">{value}</div>
        <div style="font-size: 12px; color: #777777; text-transform: uppercase;
                    letter-spacing: 1px; margin-top: 6px;">{label}</div>
    </div>
    '''


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


def render_xp_badge(xp: int) -> None:
    """Render an XP badge."""
    st.markdown(f'''
    <div style="display: inline-flex; align-items: center; gap: 6px;
                background: #FFC800; color: #3C3C3C; padding: 8px 16px;
                border-radius: 16px; font-weight: 700;">
        <span style="font-size: 16px;">⭐</span>
        <span>{xp} XP</span>
    </div>
    ''', unsafe_allow_html=True)


def render_progress_bar(current: int, total: int, label: str = "", color: str = "#58CC02") -> None:
    """Render a custom progress bar."""
    progress = min(current / total * 100, 100) if total > 0 else 0
    label_html = f'<div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span style="color: #3C3C3C; font-weight: 600;">{label}</span><span style="color: #777777;">{current}/{total}</span></div>' if label else ''

    st.markdown(f'''
    <div style="margin-bottom: 16px;">
        {label_html}
        <div style="background: #E5E5E5; border-radius: 8px; height: 12px; overflow: hidden;">
            <div style="background: {color}; height: 100%; width: {progress}%;
                        border-radius: 8px; transition: width 0.3s ease;"></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


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

    st.markdown(f'''
    <div style="background: {bg}; border: 2px solid {color}; border-radius: 16px;
                padding: 20px; margin: 12px 0;">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 24px; color: {color};">{icon}</span>
            <div>
                <div style="font-weight: 700; color: #3C3C3C; font-size: 16px;">{message}</div>
                {details_html}
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_card(content: str, title: str = "", padding: str = "20px") -> None:
    """Render a simple card container."""
    title_html = f'<div style="font-weight: 700; color: #3C3C3C; font-size: 18px; margin-bottom: 12px;">{title}</div>' if title else ''
    st.markdown(f'''
    <div style="background: #FFFFFF; border: 2px solid #E5E5E5; border-radius: 16px;
                padding: {padding}; margin-bottom: 16px;">
        {title_html}
        <div style="color: #3C3C3C;">{content}</div>
    </div>
    ''', unsafe_allow_html=True)


def render_empty_state(message: str, icon: str = "📭", action: str = "") -> None:
    """Render an empty state placeholder."""
    action_html = f'<div style="margin-top: 16px;">{action}</div>' if action else ''
    st.markdown(f'''
    <div style="text-align: center; padding: 48px 24px; background: #F7F7F7;
                border-radius: 16px; margin: 16px 0;">
        <div style="font-size: 56px; margin-bottom: 16px;">{icon}</div>
        <p style="color: #777777; font-size: 17px; margin: 0;">{message}</p>
        {action_html}
    </div>
    ''', unsafe_allow_html=True)


def render_loading_skeleton(height: str = "100px") -> None:
    """Render a loading skeleton placeholder."""
    st.markdown(f'''
    <div style="background: linear-gradient(90deg, #F7F7F7 25%, #EFEFEF 50%, #F7F7F7 75%);
                background-size: 200% 100%; height: {height}; border-radius: 16px;
                animation: shimmer 1.5s infinite;">
    </div>
    <style>@keyframes shimmer {{ 0% {{ background-position: 200% 0; }} 100% {{ background-position: -200% 0; }} }}</style>
    ''', unsafe_allow_html=True)


def render_error_state(message: str, retry_label: str = "Try again") -> bool:
    """Render an error state with retry button."""
    st.markdown(f'''
    <div style="text-align: center; padding: 32px; background: rgba(255, 75, 75, 0.1);
                border: 2px solid #FF4B4B; border-radius: 16px;">
        <div style="font-size: 48px; margin-bottom: 16px;">😕</div>
        <p style="color: #FF4B4B; font-size: 18px; font-weight: 700;">Something went wrong</p>
        <p style="color: #777777;">{message}</p>
    </div>
    ''', unsafe_allow_html=True)
    return st.button(retry_label, type="primary")


def render_profile_card(name: str, level: str, vocab_count: int, streak: int, is_active: bool = False) -> str:
    """Return HTML for a profile card."""
    border_color = "#58CC02" if is_active else "#E5E5E5"
    badge = f'''<span style="background: rgba(88, 204, 2, 0.15); color: #58CC02;
                padding: 4px 12px; border-radius: 12px; font-size: 13px;
                font-weight: 700;">Active</span>''' if is_active else ''

    return f'''
    <div style="background: #FFFFFF; border: 2px solid {border_color}; border-radius: 16px;
                padding: 20px; margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 16px;">
            <div>
                <div style="font-weight: 700; color: #3C3C3C; font-size: 18px;">{name}</div>
                <div style="font-size: 14px; color: #777777;">Level: {level}</div>
            </div>
            {badge}
        </div>
        <div style="display: flex; gap: 32px;">
            <div>
                <div style="font-weight: 800; color: #58CC02; font-size: 24px;">{vocab_count}</div>
                <div style="font-size: 12px; color: #777777; text-transform: uppercase;">Words</div>
            </div>
            <div>
                <div style="font-weight: 800; color: #FF9600; font-size: 24px;">{streak} 🔥</div>
                <div style="font-size: 12px; color: #777777; text-transform: uppercase;">Streak</div>
            </div>
        </div>
    </div>
    '''


def render_cloze_sentence(before: str, after: str, answer: str = "", show_answer: bool = False) -> None:
    """Render a cloze deletion sentence."""
    if show_answer:
        blank = f'''<span style="background: rgba(88, 204, 2, 0.2); color: #58CC02;
                    padding: 4px 16px; border-radius: 8px; font-weight: 700;">{answer}</span>'''
    else:
        blank = '''<span style="display: inline-block; min-width: 100px; border-bottom: 3px solid #1CB0F6;
                   padding: 4px 8px; margin: 0 4px;"></span>'''

    st.markdown(f'''
    <div style="font-size: 22px; color: #3C3C3C; line-height: 2; background: #FFFFFF;
                padding: 24px; border-radius: 16px; border: 2px solid #E5E5E5;">
        {before}{blank}{after}
    </div>
    ''', unsafe_allow_html=True)


def render_exercise_feedback(correct: bool, correct_answer: str, explanation: str = "",
                            common_mistake: str = "") -> None:
    """Render exercise feedback."""
    if correct:
        st.markdown(f'''
        <div style="background: rgba(88, 204, 2, 0.1); border: 2px solid #58CC02;
                    border-radius: 16px; padding: 24px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <span style="font-size: 32px;">🎉</span>
                <span style="font-size: 24px; font-weight: 800; color: #58CC02;">Correct!</span>
            </div>
            {f'<p style="color: #3C3C3C; margin: 12px 0 0 0;">{explanation}</p>' if explanation else ''}
        </div>
        ''', unsafe_allow_html=True)
    else:
        mistake_html = f'''<div style="background: #F7F7F7; padding: 12px; border-radius: 8px;
                          margin-top: 12px;"><strong>💡 Tip:</strong> {common_mistake}</div>''' if common_mistake else ''
        st.markdown(f'''
        <div style="background: rgba(255, 75, 75, 0.1); border: 2px solid #FF4B4B;
                    border-radius: 16px; padding: 24px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="font-size: 32px;">😅</span>
                <span style="font-size: 24px; font-weight: 800; color: #FF4B4B;">Not quite</span>
            </div>
            <p style="color: #3C3C3C; margin: 0;">
                Correct answer: <strong style="color: #58CC02;">{correct_answer}</strong>
            </p>
            {f'<p style="color: #777777; margin: 8px 0 0 0;">{explanation}</p>' if explanation else ''}
            {mistake_html}
        </div>
        ''', unsafe_allow_html=True)


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
