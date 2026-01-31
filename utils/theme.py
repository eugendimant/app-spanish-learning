"""Clean, high-contrast design system for Spanish Learning App."""
import streamlit as st


def get_css() -> str:
    """Return clean, readable CSS with high contrast and proper typography."""
    return """
    <style>
    /* ============================================
       DESIGN TOKENS
       ============================================ */
    :root {
        /* Colors - High contrast palette */
        --bg-primary: #0f1117;
        --bg-secondary: #1a1d24;
        --bg-card: #1e222a;
        --bg-input: #262a33;

        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --text-hint: #64748b;

        --accent-primary: #6366f1;
        --accent-primary-hover: #818cf8;
        --accent-success: #22c55e;
        --accent-warning: #f59e0b;
        --accent-error: #ef4444;
        --accent-info: #3b82f6;

        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-medium: rgba(255, 255, 255, 0.15);

        /* Typography */
        --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        --font-mono: 'SF Mono', Monaco, 'Courier New', monospace;

        /* Font sizes */
        --text-xs: 0.75rem;
        --text-sm: 0.875rem;
        --text-base: 1rem;
        --text-lg: 1.125rem;
        --text-xl: 1.25rem;
        --text-2xl: 1.5rem;
        --text-3xl: 2rem;

        /* Line heights */
        --leading-tight: 1.25;
        --leading-normal: 1.5;
        --leading-relaxed: 1.75;

        /* Spacing scale */
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 0.75rem;
        --space-4: 1rem;
        --space-5: 1.25rem;
        --space-6: 1.5rem;
        --space-8: 2rem;
        --space-10: 2.5rem;
        --space-12: 3rem;

        /* Radii */
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;

        /* Shadows */
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* ============================================
       BASE STYLES
       ============================================ */
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-sans) !important;
    }

    /* Remove default Streamlit header */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Main content area */
    .main .block-container {
        padding: var(--space-6) var(--space-8) !important;
        max-width: 1200px !important;
    }

    /* ============================================
       TYPOGRAPHY
       ============================================ */

    /* Headings */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        line-height: var(--leading-tight) !important;
        margin-bottom: var(--space-4) !important;
    }

    h1, .stMarkdown h1 { font-size: var(--text-3xl) !important; }
    h2, .stMarkdown h2 { font-size: var(--text-2xl) !important; }
    h3, .stMarkdown h3 { font-size: var(--text-xl) !important; }
    h4, .stMarkdown h4 { font-size: var(--text-lg) !important; }

    /* Body text */
    p, .stMarkdown p, .stText {
        color: var(--text-secondary) !important;
        font-size: var(--text-base) !important;
        line-height: var(--leading-relaxed) !important;
        max-width: 65ch;
    }

    /* Strong/bold text */
    strong, b {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    /* Captions and hints */
    .stCaption, small, .caption {
        color: var(--text-muted) !important;
        font-size: var(--text-sm) !important;
    }

    /* ============================================
       SIDEBAR
       ============================================ */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding: var(--space-4) !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: var(--text-primary) !important;
        font-size: var(--text-sm) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin: var(--space-4) 0 var(--space-2) 0 !important;
    }

    /* ============================================
       BUTTONS
       ============================================ */

    /* Primary button */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: var(--accent-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-weight: 500 !important;
        font-size: var(--text-base) !important;
        padding: var(--space-3) var(--space-6) !important;
        min-height: 44px !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: var(--accent-primary-hover) !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button[kind="primary"]:active,
    .stButton > button[data-testid="baseButton-primary"]:active {
        transform: translateY(0) !important;
    }

    /* Secondary button */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"],
    .stButton > button {
        background: transparent !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: var(--radius-md) !important;
        font-weight: 500 !important;
        font-size: var(--text-base) !important;
        padding: var(--space-3) var(--space-6) !important;
        min-height: 44px !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover,
    .stButton > button:hover {
        background: var(--bg-card) !important;
        border-color: var(--accent-primary) !important;
    }

    /* ============================================
       FORM INPUTS
       ============================================ */

    /* Text inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-size: var(--text-base) !important;
        padding: var(--space-3) var(--space-4) !important;
        min-height: 44px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-hint) !important;
    }

    /* Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stRadio > label,
    .stCheckbox > label {
        color: var(--text-secondary) !important;
        font-size: var(--text-sm) !important;
        font-weight: 500 !important;
        margin-bottom: var(--space-2) !important;
    }

    /* ============================================
       RADIO BUTTONS
       ============================================ */
    .stRadio > div {
        gap: var(--space-3) !important;
    }

    .stRadio > div > label {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-3) var(--space-4) !important;
        color: var(--text-primary) !important;
        font-size: var(--text-base) !important;
        min-height: 44px !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }

    .stRadio > div > label:hover {
        border-color: var(--accent-primary) !important;
        background: var(--bg-input) !important;
    }

    .stRadio > div > label[data-checked="true"],
    .stRadio > div > label:has(input:checked) {
        border-color: var(--accent-primary) !important;
        background: rgba(99, 102, 241, 0.15) !important;
    }

    /* ============================================
       SELECT / DROPDOWN
       ============================================ */
    .stSelectbox > div > div {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: var(--radius-md) !important;
    }

    .stSelectbox > div > div > div {
        color: var(--text-primary) !important;
    }

    /* Dropdown menu */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    div[role="listbox"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: var(--radius-md) !important;
    }

    [data-baseweb="menu"] li,
    div[role="option"] {
        color: var(--text-primary) !important;
        background: transparent !important;
        padding: var(--space-3) var(--space-4) !important;
    }

    [data-baseweb="menu"] li:hover,
    div[role="option"]:hover {
        background: var(--bg-input) !important;
    }

    [data-baseweb="menu"] li[aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background: rgba(99, 102, 241, 0.2) !important;
    }

    /* ============================================
       MULTISELECT
       ============================================ */
    .stMultiSelect > div > div {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: var(--radius-md) !important;
    }

    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(99, 102, 241, 0.2) !important;
        border: 1px solid var(--accent-primary) !important;
        color: var(--text-primary) !important;
    }

    /* ============================================
       SLIDER
       ============================================ */
    .stSlider > div > div > div {
        background: var(--border-medium) !important;
    }

    .stSlider > div > div > div > div {
        background: var(--accent-primary) !important;
    }

    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--accent-primary) !important;
        border: 2px solid white !important;
    }

    /* ============================================
       PROGRESS BAR
       ============================================ */
    .stProgress > div > div {
        background: var(--bg-input) !important;
        border-radius: var(--radius-sm) !important;
        height: 8px !important;
    }

    .stProgress > div > div > div {
        background: var(--accent-primary) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ============================================
       CARDS & CONTAINERS
       ============================================ */

    /* Base card */
    .card {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-6) !important;
        margin-bottom: var(--space-4) !important;
    }

    /* Muted card for secondary content */
    .card-muted {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-4) !important;
        margin-bottom: var(--space-4) !important;
    }

    /* ============================================
       HERO SECTION
       ============================================ */
    .hero {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-xl) !important;
        padding: var(--space-8) !important;
        margin-bottom: var(--space-6) !important;
    }

    .hero-title {
        color: var(--text-primary) !important;
        font-size: var(--text-2xl) !important;
        font-weight: 700 !important;
        margin-bottom: var(--space-2) !important;
        line-height: var(--leading-tight) !important;
    }

    .hero-subtitle {
        color: var(--text-secondary) !important;
        font-size: var(--text-base) !important;
        line-height: var(--leading-relaxed) !important;
        max-width: 60ch !important;
    }

    .hero-pills {
        display: flex !important;
        gap: var(--space-2) !important;
        flex-wrap: wrap !important;
        margin-bottom: var(--space-4) !important;
    }

    .hero-pill {
        background: rgba(99, 102, 241, 0.15) !important;
        color: var(--accent-primary-hover) !important;
        padding: var(--space-1) var(--space-3) !important;
        border-radius: var(--radius-sm) !important;
        font-size: var(--text-xs) !important;
        font-weight: 500 !important;
    }

    /* ============================================
       EXERCISE COMPONENTS
       ============================================ */

    /* Exercise prompt - the main question/instruction */
    .exercise-prompt {
        color: var(--text-primary) !important;
        font-size: var(--text-lg) !important;
        font-weight: 500 !important;
        line-height: var(--leading-relaxed) !important;
        padding: var(--space-4) !important;
        background: var(--bg-secondary) !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: var(--space-4) !important;
    }

    /* Exercise type badge */
    .exercise-type {
        display: inline-block !important;
        background: var(--accent-primary) !important;
        color: white !important;
        padding: var(--space-1) var(--space-3) !important;
        border-radius: var(--radius-sm) !important;
        font-size: var(--text-xs) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: var(--space-3) !important;
    }

    /* ============================================
       FEEDBACK BOXES
       ============================================ */
    .feedback-box {
        padding: var(--space-4) !important;
        border-radius: var(--radius-md) !important;
        margin: var(--space-4) 0 !important;
        font-size: var(--text-base) !important;
        line-height: var(--leading-normal) !important;
    }

    .feedback-success {
        background: rgba(34, 197, 94, 0.15) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        color: #4ade80 !important;
    }

    .feedback-error {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #f87171 !important;
    }

    .feedback-warning {
        background: rgba(245, 158, 11, 0.15) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        color: #fbbf24 !important;
    }

    .feedback-info {
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #60a5fa !important;
    }

    /* ============================================
       METRICS
       ============================================ */
    .metric-card {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-5) !important;
        text-align: center !important;
    }

    .metric-value {
        color: var(--text-primary) !important;
        font-size: var(--text-2xl) !important;
        font-weight: 700 !important;
        line-height: 1 !important;
        margin-bottom: var(--space-1) !important;
    }

    .metric-label {
        color: var(--text-muted) !important;
        font-size: var(--text-sm) !important;
    }

    /* ============================================
       PILLS / BADGES
       ============================================ */
    .pill {
        display: inline-flex !important;
        align-items: center !important;
        gap: var(--space-1) !important;
        padding: var(--space-1) var(--space-3) !important;
        border-radius: var(--radius-sm) !important;
        font-size: var(--text-xs) !important;
        font-weight: 500 !important;
    }

    .pill-primary {
        background: rgba(99, 102, 241, 0.2) !important;
        color: var(--accent-primary-hover) !important;
    }

    .pill-success {
        background: rgba(34, 197, 94, 0.2) !important;
        color: var(--accent-success) !important;
    }

    .pill-warning {
        background: rgba(245, 158, 11, 0.2) !important;
        color: var(--accent-warning) !important;
    }

    .pill-error {
        background: rgba(239, 68, 68, 0.2) !important;
        color: var(--accent-error) !important;
    }

    .pill-muted {
        background: var(--bg-input) !important;
        color: var(--text-muted) !important;
    }

    /* ============================================
       ALERTS
       ============================================ */
    .stAlert {
        border-radius: var(--radius-md) !important;
    }

    .stAlert > div {
        padding: var(--space-4) !important;
    }

    /* Info alert */
    div[data-baseweb="notification"][kind="info"],
    .element-container div[data-testid="stAlert"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
    }

    /* Success alert */
    div[data-baseweb="notification"][kind="positive"] {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.2) !important;
    }

    /* Warning alert */
    div[data-baseweb="notification"][kind="warning"] {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
    }

    /* Error alert */
    div[data-baseweb="notification"][kind="negative"] {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
    }

    /* ============================================
       DIVIDERS
       ============================================ */
    hr, .stDivider {
        border-color: var(--border-subtle) !important;
        margin: var(--space-6) 0 !important;
    }

    /* ============================================
       EXPANDER
       ============================================ */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }

    .streamlit-expanderContent {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        padding: var(--space-4) !important;
    }

    /* ============================================
       TABS
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: var(--space-2) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
        padding-bottom: 0 !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-muted) !important;
        border: none !important;
        border-radius: var(--radius-md) var(--radius-md) 0 0 !important;
        padding: var(--space-3) var(--space-4) !important;
        font-weight: 500 !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary) !important;
        background: var(--bg-card) !important;
    }

    .stTabs [aria-selected="true"] {
        color: var(--accent-primary) !important;
        background: var(--bg-card) !important;
        border-bottom: 2px solid var(--accent-primary) !important;
    }

    /* ============================================
       COLUMNS
       ============================================ */
    [data-testid="column"] {
        padding: var(--space-2) !important;
    }

    /* ============================================
       SPINNER
       ============================================ */
    .stSpinner > div {
        border-color: var(--accent-primary) transparent transparent transparent !important;
    }

    /* ============================================
       DOWNLOAD BUTTON
       ============================================ */
    .stDownloadButton > button {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-medium) !important;
        color: var(--text-primary) !important;
    }

    /* ============================================
       FILE UPLOADER
       ============================================ */
    .stFileUploader > div {
        background: var(--bg-input) !important;
        border: 2px dashed var(--border-medium) !important;
        border-radius: var(--radius-lg) !important;
    }

    /* ============================================
       TOGGLE
       ============================================ */
    .stCheckbox > label > span {
        color: var(--text-primary) !important;
    }

    /* ============================================
       TOOLTIP
       ============================================ */
    [data-baseweb="tooltip"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-medium) !important;
        color: var(--text-primary) !important;
    }

    /* ============================================
       SECTION HEADER
       ============================================ */
    .section-header {
        display: flex !important;
        align-items: center !important;
        gap: var(--space-2) !important;
        margin-bottom: var(--space-4) !important;
        padding-bottom: var(--space-2) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
    }

    .section-header-title {
        color: var(--text-primary) !important;
        font-size: var(--text-lg) !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }

    /* ============================================
       ACCESSIBILITY
       ============================================ */

    /* Focus states */
    button:focus-visible,
    input:focus-visible,
    textarea:focus-visible,
    select:focus-visible {
        outline: 2px solid var(--accent-primary) !important;
        outline-offset: 2px !important;
    }

    /* Reduced motion */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation: none !important;
            transition: none !important;
        }
    }

    /* ============================================
       UTILITY CLASSES
       ============================================ */
    .text-center { text-align: center !important; }
    .text-left { text-align: left !important; }
    .text-right { text-align: right !important; }

    .mt-4 { margin-top: var(--space-4) !important; }
    .mb-4 { margin-bottom: var(--space-4) !important; }
    .my-4 { margin-top: var(--space-4) !important; margin-bottom: var(--space-4) !important; }

    .p-4 { padding: var(--space-4) !important; }
    .p-6 { padding: var(--space-6) !important; }

    /* Hide elements */
    .hidden { display: none !important; }
    </style>
    """


def apply_theme() -> None:
    """Apply theme settings to the Streamlit app."""
    st.set_page_config(
        page_title="Spanish Learning",
        page_icon="🇪🇸",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(get_css(), unsafe_allow_html=True)


def render_hero(title: str, subtitle: str = "", pills: list = None) -> None:
    """Render a clean hero section."""
    pills_html = ""
    if pills:
        pills_html = '<div class="hero-pills">' + ''.join(
            f'<span class="hero-pill">{pill}</span>' for pill in pills
        ) + '</div>'

    st.markdown(f"""
    <div class="hero">
        {pills_html}
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, icon: str = "") -> None:
    """Render a section header with optional icon."""
    icon_html = f'<span style="font-size: 1.25rem;">{icon}</span>' if icon else ''
    st.markdown(f"""
    <div class="section-header">
        {icon_html}
        <span class="section-header-title">{title}</span>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(value: str, label: str, icon: str = "") -> str:
    """Return HTML for a metric card."""
    icon_html = f'<div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''
    return f"""
    <div class="metric-card">
        {icon_html}
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def render_feedback(feedback_type: str, message: str, details: str = "") -> None:
    """Render a feedback box with consistent styling."""
    details_html = f'<div style="margin-top: 0.5rem; font-size: 0.9rem; opacity: 0.9;">{details}</div>' if details else ''
    st.markdown(f"""
    <div class="feedback-box feedback-{feedback_type}">
        {message}
        {details_html}
    </div>
    """, unsafe_allow_html=True)


def render_exercise_card(exercise_type: str, prompt: str) -> None:
    """Render an exercise card with type badge and prompt."""
    st.markdown(f"""
    <div class="card">
        <span class="exercise-type">{exercise_type}</span>
        <div class="exercise-prompt">{prompt}</div>
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(current: int, total: int, label: str = "") -> None:
    """Render a progress indicator."""
    if label:
        st.caption(label)
    st.progress(current / total if total > 0 else 0)


def render_pill(text: str, variant: str = "primary") -> str:
    """Return HTML for a pill/badge."""
    return f'<span class="pill pill-{variant}">{text}</span>'


def render_profile_card(name: str, level: str, vocab_count: int, streak: int, is_active: bool = False) -> str:
    """Render a profile card."""
    active_badge = '<span class="pill pill-success">Active</span>' if is_active else ''
    return f"""
    <div class="card" style="{'border-color: var(--accent-primary);' if is_active else ''}">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <div>
                <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">{name}</div>
                <div style="color: var(--text-muted); font-size: 0.875rem;">Level: {level}</div>
            </div>
            {active_badge}
        </div>
        <div style="display: flex; gap: 1.5rem;">
            <div>
                <div style="font-weight: 600; color: var(--text-primary);">{vocab_count}</div>
                <div style="font-size: 0.75rem; color: var(--text-muted);">Words</div>
            </div>
            <div>
                <div style="font-weight: 600; color: var(--text-primary);">{streak}🔥</div>
                <div style="font-size: 0.75rem; color: var(--text-muted);">Streak</div>
            </div>
        </div>
    </div>
    """


def render_streak_badge(streak: int) -> None:
    """Render a streak badge."""
    if streak > 0:
        st.markdown(f"""
        <div style="display: inline-flex; align-items: center; gap: 0.5rem;
                    background: rgba(245, 158, 11, 0.15); padding: 0.5rem 1rem;
                    border-radius: 8px; border: 1px solid rgba(245, 158, 11, 0.3);">
            <span style="font-size: 1.5rem;">🔥</span>
            <span style="font-size: 1.25rem; font-weight: 700; color: #fbbf24;">{streak}</span>
            <span style="color: var(--text-secondary);">day{'s' if streak != 1 else ''}</span>
        </div>
        """, unsafe_allow_html=True)


# Backward compatibility aliases
def get_design_system():
    """Return design tokens for programmatic access."""
    return {
        "colors": {
            "bg_primary": "#0f1117",
            "bg_secondary": "#1a1d24",
            "bg_card": "#1e222a",
            "text_primary": "#f8fafc",
            "text_secondary": "#cbd5e1",
            "accent_primary": "#6366f1",
            "success": "#22c55e",
            "warning": "#f59e0b",
            "error": "#ef4444",
        },
        "spacing": {
            "xs": "0.25rem",
            "sm": "0.5rem",
            "md": "1rem",
            "lg": "1.5rem",
            "xl": "2rem",
        },
        "typography": {
            "base_size": "1rem",
            "heading_weight": 600,
            "line_height": 1.5,
        }
    }
