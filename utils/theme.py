"""
Robust design system for Streamlit - uses explicit colors with fallbacks.
"""
import streamlit as st


# ============================================
# DESIGN TOKENS
# ============================================
COLORS = {
    "bg_page": "#09090b",
    "bg_surface": "#18181b",
    "bg_elevated": "#27272a",
    "bg_hover": "#3f3f46",
    "text_primary": "#fafafa",
    "text_secondary": "#a1a1aa",
    "text_muted": "#71717a",
    "accent": "#6366f1",
    "accent_hover": "#818cf8",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
}

SPACING = {"xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px"}
RADII = {"sm": "6px", "md": "8px", "lg": "12px", "xl": "16px"}


def get_css() -> str:
    """Return CSS with explicit colors (no variables that might fail)."""
    return """
    <style>
    /* ============================================
       FORCE DARK THEME - Explicit colors everywhere
       ============================================ */

    /* Root variables as fallback */
    :root {
        --bg-page: #09090b;
        --bg-surface: #18181b;
        --bg-elevated: #27272a;
        --bg-hover: #3f3f46;
        --text-primary: #fafafa;
        --text-secondary: #a1a1aa;
        --text-muted: #71717a;
        --border: #27272a;
        --accent: #6366f1;
    }

    /* Force dark background on everything */
    .stApp,
    .stApp > div,
    .main,
    .main > div,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > div {
        background-color: #09090b !important;
        color: #fafafa !important;
    }

    /* Main content area */
    .main .block-container {
        background-color: #09090b !important;
        padding: 24px 32px !important;
        max-width: 1200px !important;
    }

    /* Hide Streamlit branding */
    header[data-testid="stHeader"],
    footer,
    #MainMenu,
    .stDeployButton {
        display: none !important;
    }

    /* ============================================
       TYPOGRAPHY - Explicit colors
       ============================================ */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #fafafa !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
    }

    h1, .stMarkdown h1 { font-size: 2rem !important; }
    h2, .stMarkdown h2 { font-size: 1.5rem !important; }
    h3, .stMarkdown h3 { font-size: 1.25rem !important; }
    h4, .stMarkdown h4 { font-size: 1.125rem !important; }

    p, .stMarkdown p, .stMarkdown {
        color: #a1a1aa !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }

    span, div {
        color: inherit;
    }

    strong, b {
        color: #fafafa !important;
        font-weight: 600 !important;
    }

    a {
        color: #6366f1 !important;
    }

    /* Labels */
    label, .stTextInput label, .stSelectbox label, .stRadio label {
        color: #a1a1aa !important;
        font-size: 0.875rem !important;
    }

    /* ============================================
       SIDEBAR
       ============================================ */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div > div,
    section[data-testid="stSidebar"] {
        background-color: #18181b !important;
        border-right: 1px solid #27272a !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 16px !important;
        background-color: #18181b !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #71717a !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #a1a1aa !important;
    }

    /* ============================================
       BUTTONS
       ============================================ */
    .stButton > button {
        background-color: #18181b !important;
        color: #fafafa !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 12px 20px !important;
        min-height: 44px !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button:hover {
        background-color: #27272a !important;
        border-color: #3f3f46 !important;
    }

    /* Primary button */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #6366f1 !important;
        color: white !important;
        border: none !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #818cf8 !important;
    }

    /* ============================================
       FORM INPUTS
       ============================================ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background-color: #18181b !important;
        color: #fafafa !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #52525b !important;
    }

    /* ============================================
       SELECT / DROPDOWN
       ============================================ */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
    }

    .stSelectbox > div > div > div,
    .stSelectbox [data-baseweb="select"] span {
        color: #fafafa !important;
    }

    /* Dropdown menu */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    div[role="listbox"],
    ul[role="listbox"] {
        background-color: #27272a !important;
        border: 1px solid #3f3f46 !important;
        border-radius: 8px !important;
    }

    [data-baseweb="menu"] li,
    div[role="option"],
    li[role="option"] {
        color: #fafafa !important;
        background-color: transparent !important;
    }

    [data-baseweb="menu"] li:hover,
    div[role="option"]:hover,
    li[role="option"]:hover {
        background-color: #3f3f46 !important;
    }

    /* ============================================
       RADIO BUTTONS
       ============================================ */
    .stRadio > div {
        gap: 8px !important;
    }

    .stRadio > div > label {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        color: #fafafa !important;
        cursor: pointer !important;
    }

    .stRadio > div > label:hover {
        background-color: #27272a !important;
    }

    .stRadio > div > label[data-checked="true"],
    .stRadio > div > label:has(input:checked) {
        border-color: #6366f1 !important;
        background-color: rgba(99, 102, 241, 0.15) !important;
    }

    /* ============================================
       PROGRESS BAR
       ============================================ */
    .stProgress > div > div {
        background-color: #27272a !important;
        border-radius: 4px !important;
    }

    .stProgress > div > div > div {
        background-color: #6366f1 !important;
    }

    /* ============================================
       EXPANDER
       ============================================ */
    .streamlit-expanderHeader {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
        color: #fafafa !important;
    }

    .streamlit-expanderContent {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-top: none !important;
    }

    /* ============================================
       TABS
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #27272a !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #71717a !important;
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #fafafa !important;
    }

    .stTabs [aria-selected="true"] {
        color: #6366f1 !important;
        border-bottom: 2px solid #6366f1 !important;
    }

    /* ============================================
       ALERTS
       ============================================ */
    .stAlert, div[data-testid="stAlert"] {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
        color: #fafafa !important;
    }

    /* ============================================
       DIVIDER
       ============================================ */
    hr {
        border-color: #27272a !important;
    }

    /* ============================================
       METRICS
       ============================================ */
    [data-testid="stMetric"],
    [data-testid="stMetricValue"],
    [data-testid="metric-container"] {
        background-color: #18181b !important;
        color: #fafafa !important;
    }

    [data-testid="stMetricLabel"] {
        color: #71717a !important;
    }

    /* ============================================
       CUSTOM COMPONENT CLASSES
       ============================================ */
    .card {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 16px !important;
    }

    .stat-card {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }

    .stat-value {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #fafafa !important;
    }

    .stat-label {
        font-size: 0.875rem !important;
        color: #71717a !important;
    }

    .action-card {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 12px !important;
        padding: 20px !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }

    .action-card:hover {
        border-color: #6366f1 !important;
    }

    .action-card-primary {
        border-color: #6366f1 !important;
        background-color: rgba(99, 102, 241, 0.1) !important;
    }

    .action-card-title {
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        color: #fafafa !important;
        margin-bottom: 4px !important;
    }

    .action-card-subtitle {
        font-size: 0.875rem !important;
        color: #a1a1aa !important;
    }

    .pill {
        display: inline-block !important;
        padding: 4px 10px !important;
        border-radius: 9999px !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
    }

    .pill-accent {
        background-color: rgba(99, 102, 241, 0.15) !important;
        color: #818cf8 !important;
    }

    .pill-success {
        background-color: rgba(34, 197, 94, 0.15) !important;
        color: #22c55e !important;
    }

    .pill-warning {
        background-color: rgba(245, 158, 11, 0.15) !important;
        color: #f59e0b !important;
    }

    .pill-error {
        background-color: rgba(239, 68, 68, 0.15) !important;
        color: #ef4444 !important;
    }

    .feedback-box {
        padding: 16px !important;
        border-radius: 8px !important;
        margin: 16px 0 !important;
    }

    .feedback-success {
        background-color: rgba(34, 197, 94, 0.15) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        color: #22c55e !important;
    }

    .feedback-error {
        background-color: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #ef4444 !important;
    }

    .feedback-warning {
        background-color: rgba(245, 158, 11, 0.15) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        color: #f59e0b !important;
    }

    .feedback-info {
        background-color: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #3b82f6 !important;
    }

    /* Exercise components */
    .exercise-prompt {
        font-size: 1.25rem !important;
        color: #fafafa !important;
        line-height: 1.5 !important;
        margin-bottom: 16px !important;
    }

    .cloze-blank {
        display: inline-block !important;
        min-width: 100px !important;
        border-bottom: 2px solid #6366f1 !important;
        color: #6366f1 !important;
        text-align: center !important;
        margin: 0 4px !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #18181b;
    }

    ::-webkit-scrollbar-thumb {
        background: #3f3f46;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #52525b;
    }
    </style>
    """


def apply_theme():
    """Apply theme - call this AFTER set_page_config."""
    st.markdown(get_css(), unsafe_allow_html=True)


# ============================================
# COMPONENT FUNCTIONS
# ============================================

def render_hero(title: str, subtitle: str = "", pills: list = None) -> None:
    """Render page header."""
    if pills:
        pills_html = ' '.join(f'<span class="pill pill-accent">{p}</span>' for p in pills)
        st.markdown(f'<div style="margin-bottom: 12px;">{pills_html}</div>', unsafe_allow_html=True)

    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(subtitle)


def render_section_header(title: str, action_label: str = None, action_key: str = None) -> bool:
    """Render section header. Returns True if action clicked."""
    clicked = False
    if action_label and action_key:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {title}")
        with col2:
            clicked = st.button(action_label, key=action_key)
    else:
        st.markdown(f"### {title}")
    return clicked


def render_stat_card(value: str, label: str, icon: str = "") -> None:
    """Render a stat card."""
    icon_html = f'<div style="font-size: 20px; margin-bottom: 4px;">{icon}</div>' if icon else ''
    st.markdown(f"""
    <div class="stat-card">
        {icon_html}
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_action_card(title: str, subtitle: str, meta: str = "", primary: bool = False, icon: str = "") -> None:
    """Render an action card."""
    primary_class = "action-card-primary" if primary else ""
    icon_html = f'<span style="font-size: 24px; margin-right: 12px;">{icon}</span>' if icon else ''
    meta_html = f'<div style="font-size: 0.75rem; color: #71717a; margin-top: 8px;">{meta}</div>' if meta else ''

    st.markdown(f"""
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
    """, unsafe_allow_html=True)


def render_feedback(feedback_type: str, message: str, details: str = "") -> None:
    """Render feedback box."""
    details_html = f'<div style="margin-top: 8px; opacity: 0.9;">{details}</div>' if details else ''
    st.markdown(f"""
    <div class="feedback-box feedback-{feedback_type}">
        <strong>{message}</strong>
        {details_html}
    </div>
    """, unsafe_allow_html=True)


def render_streak_badge(streak: int) -> None:
    """Render streak badge."""
    if streak > 0:
        st.markdown(f"""
        <div style="display: inline-flex; align-items: center; gap: 8px;
                    background: rgba(245, 158, 11, 0.15); padding: 8px 16px;
                    border-radius: 8px; border: 1px solid rgba(245, 158, 11, 0.3);">
            <span style="font-size: 1.25rem;">🔥</span>
            <span style="font-size: 1.125rem; font-weight: 700; color: #f59e0b;">{streak}</span>
            <span style="color: #a1a1aa; font-size: 0.875rem;">day{'s' if streak != 1 else ''}</span>
        </div>
        """, unsafe_allow_html=True)


def render_empty_state(message: str, icon: str = "📭") -> None:
    """Render empty state."""
    st.markdown(f"""
    <div style="text-align: center; padding: 48px 16px; color: #71717a;">
        <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.5;">{icon}</div>
        <p style="color: #71717a;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def render_loading_skeleton(height: str = "100px") -> None:
    """Render loading skeleton."""
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #27272a 25%, #3f3f46 50%, #27272a 75%);
                background-size: 200% 100%; height: {height}; border-radius: 8px;
                animation: shimmer 1.5s infinite;">
    </div>
    <style>
    @keyframes shimmer {{ 0% {{ background-position: 200% 0; }} 100% {{ background-position: -200% 0; }} }}
    </style>
    """, unsafe_allow_html=True)


def render_error_state(message: str, retry_label: str = "Try again") -> bool:
    """Render error state. Returns True if retry clicked."""
    st.markdown(f"""
    <div style="text-align: center; padding: 24px; background: rgba(239, 68, 68, 0.15);
                border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.3);">
        <p style="color: #ef4444;"><strong>Something went wrong</strong></p>
        <p style="color: #ef4444; opacity: 0.9;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    return st.button(retry_label, type="primary")


def render_pill(text: str, variant: str = "accent") -> str:
    """Return HTML for a pill."""
    return f'<span class="pill pill-{variant}">{text}</span>'


def render_cloze_sentence(before: str, after: str, answer: str = "", show_answer: bool = False) -> None:
    """Render cloze sentence with visible blank."""
    if show_answer:
        blank = f'<span class="cloze-blank" style="color: #22c55e;">{answer}</span>'
    else:
        blank = '<span class="cloze-blank">_____</span>'

    st.markdown(f"""
    <div class="exercise-prompt">
        {before}{blank}{after}
    </div>
    """, unsafe_allow_html=True)


def render_exercise_feedback(correct: bool, correct_answer: str, explanation: str = "", common_mistake: str = "") -> None:
    """Render exercise feedback."""
    if correct:
        st.markdown(f"""
        <div class="feedback-box feedback-success">
            <strong>✓ Correct!</strong>
            {f'<div style="margin-top: 8px;">{explanation}</div>' if explanation else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        mistake_html = f'<div style="margin-top: 8px; opacity: 0.85;"><em>Common mistake: {common_mistake}</em></div>' if common_mistake else ''
        st.markdown(f"""
        <div class="feedback-box feedback-error">
            <strong>✗ Not quite</strong>
            <div style="margin-top: 8px;">The correct answer is: <strong>{correct_answer}</strong></div>
            {f'<div style="margin-top: 8px;">{explanation}</div>' if explanation else ''}
            {mistake_html}
        </div>
        """, unsafe_allow_html=True)


# ============================================
# BACKWARD COMPATIBILITY
# ============================================

def render_metric_card(value: str, label: str, icon: str = "") -> str:
    """Return HTML for metric card."""
    icon_html = f'<div style="font-size: 20px; margin-bottom: 4px;">{icon}</div>' if icon else ''
    return f"""
    <div class="stat-card" style="text-align: center;">
        {icon_html}
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """


def render_metric_grid(metrics: list) -> None:
    """Render grid of metrics."""
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            st.markdown(render_metric_card(
                str(m.get("value", "0")),
                m.get("label", ""),
                m.get("icon", "")
            ), unsafe_allow_html=True)


def render_card(content: str, title: str = "") -> None:
    """Render a card."""
    title_html = f'<h4 style="margin-bottom: 12px; color: #fafafa;">{title}</h4>' if title else ''
    st.markdown(f"""
    <div class="card">
        {title_html}
        <div style="color: #a1a1aa;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_domain_coverage(domains: dict) -> None:
    """Render domain coverage."""
    for domain, coverage in domains.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(min(coverage / 100, 1.0))
        with col2:
            st.caption(f"{domain}: {coverage:.0f}%")


def render_quick_actions(actions: list) -> None:
    """Render quick actions."""
    cols = st.columns(len(actions))
    for col, action in zip(cols, actions):
        with col:
            if st.button(
                f"{action.get('icon', '')} {action.get('label', '')}",
                key=action.get('key', action.get('label')),
                use_container_width=True,
                type=action.get('type', 'secondary')
            ):
                if action.get('callback'):
                    action['callback']()


def render_profile_card(name: str, level: str, vocab_count: int, streak: int, is_active: bool = False) -> str:
    """Render profile card."""
    border = 'border-color: #6366f1;' if is_active else ''
    badge = '<span class="pill pill-success">Active</span>' if is_active else ''

    return f"""
    <div class="card" style="{border}">
        <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
            <div>
                <div style="font-weight: 600; color: #fafafa;">{name}</div>
                <div style="font-size: 0.875rem; color: #71717a;">Level: {level}</div>
            </div>
            {badge}
        </div>
        <div style="display: flex; gap: 24px;">
            <div>
                <div style="font-weight: 700; color: #fafafa;">{vocab_count}</div>
                <div style="font-size: 0.75rem; color: #71717a;">Words</div>
            </div>
            <div>
                <div style="font-weight: 700; color: #f59e0b;">{streak}🔥</div>
                <div style="font-size: 0.75rem; color: #71717a;">Streak</div>
            </div>
        </div>
    </div>
    """


def get_design_system():
    """Return design tokens."""
    return {"colors": COLORS, "spacing": SPACING, "radii": RADII}


# ============================================
# EXERCISE HELPERS
# ============================================

def validate_exercise(exercise: dict) -> dict:
    """Validate exercise. Returns {valid: bool, errors: list}."""
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
    """Get instruction for exercise type."""
    return {
        "cloze": "Fill in the blank with the correct word",
        "mcq": "Choose the correct answer",
        "translate": "Translate into Spanish",
        "free_recall": "Type the missing word",
    }.get(ex_type, "Complete the exercise")


def normalize_spanish_answer(text: str, strict_accents: bool = False) -> str:
    """Normalize Spanish text for comparison."""
    import re
    text = text.strip().lower()
    text = ' '.join(text.split())
    text = re.sub(r'[^\w\sáéíóúüñ]', '', text)

    if not strict_accents:
        text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i')
        text = text.replace('ó', 'o').replace('ú', 'u').replace('ü', 'u')

    return text


def check_answer(user_answer: str, correct_answers: list, strict_accents: bool = False) -> dict:
    """Check answer. Returns {result, matched, feedback}."""
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
