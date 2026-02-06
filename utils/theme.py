"""
Clean white design system - Forces light mode aggressively.
"""
import streamlit as st


COLORS = {
    "bg": "#FFFFFF",
    "text": "#1C1C1E",
    "text_secondary": "#8E8E93",
    "blue": "#007AFF",
    "green": "#34C759",
    "orange": "#FF9500",
    "red": "#FF3B30",
    "border": "#D1D1D6",
    "card_bg": "#F2F2F7",
}

SPACING = {"xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px"}
RADII = {"sm": "8px", "md": "12px", "lg": "16px"}


def get_css() -> str:
    """Ultra-aggressive white theme CSS with color-scheme override."""
    return """
    <meta name="color-scheme" content="light only">
    <meta name="theme-color" content="#FFFFFF">
    <style>
    /* FORCE LIGHT COLOR SCHEME */
    :root {
        color-scheme: light only !important;
        --background-color: #FFFFFF !important;
        --text-color: #1C1C1E !important;
    }

    /* Override prefers-color-scheme dark */
    @media (prefers-color-scheme: dark) {
        :root, html, body, .stApp {
            color-scheme: light only !important;
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            color: #1C1C1E !important;
        }
    }

    /* NUCLEAR OPTION - Force white on literally everything */
    *, *::before, *::after,
    :root, html, body,
    html[data-theme], html[data-theme="dark"], html[data-theme="light"],
    body[data-theme], body[data-theme="dark"],
    [data-theme], [data-theme="dark"],
    .stApp, .stApp > *, .stApp > * > *, .stApp > * > * > *,
    .main, .main > *, .main > * > *, .main > * > * > *,
    [data-testid], [data-testid] > *, [data-testid] > * > *,
    [class*="st"], [class*="css"], [class*="block"],
    section, article, div, span, p, h1, h2, h3, h4, h5, h6,
    header, footer, nav, aside, main,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > *,
    [data-testid="stVerticalBlock"],
    [data-testid="stVerticalBlock"] > *,
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .block-container, .block-container > *,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stBottom"],
    .stDeployButton,
    .stApp iframe,
    iframe[title="streamlit_lottie.streamlit_lottie"] {
        color-scheme: light only !important;
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #1C1C1E !important;
    }

    /* Sidebar - light gray */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div > div,
    [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background: #F2F2F7 !important;
        background-color: #F2F2F7 !important;
    }

    [data-testid="stSidebar"] * {
        color: #1C1C1E !important;
    }

    /* Hide collapse button */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    button[kind="header"] {
        display: none !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #1C1C1E !important;
        font-weight: 700 !important;
    }

    p, span, label, div {
        color: #1C1C1E !important;
    }

    /* Buttons */
    .stButton > button {
        background: #007AFF !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        min-height: 48px !important;
    }

    .stButton > button:hover {
        background: #0056B3 !important;
    }

    .stButton > button[kind="secondary"],
    .stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
        background: #F2F2F7 !important;
        color: #007AFF !important;
        border: 1px solid #D1D1D6 !important;
    }

    /* Inputs */
    input, textarea, select,
    .stTextInput input,
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox > div > div {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #1C1C1E !important;
        border: 1px solid #D1D1D6 !important;
        border-radius: 10px !important;
    }

    input::placeholder, textarea::placeholder {
        color: #8E8E93 !important;
    }

    /* Progress bars */
    .stProgress > div > div {
        background: #E5E5EA !important;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #007AFF, #5AC8FA) !important;
    }

    /* Cards */
    .card, .glass-card, .stat-card, .action-card {
        background: #FFFFFF !important;
        border: 1px solid #E5E5EA !important;
        border-radius: 16px !important;
        padding: 16px !important;
    }

    .card h3, .card h4, .stat-value, .action-card-title {
        color: #1C1C1E !important;
    }

    .card p, .stat-label, .action-card-subtitle {
        color: #8E8E93 !important;
    }

    /* Pills */
    .pill {
        display: inline-block !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }
    .pill-blue, .pill-accent { background: rgba(0,122,255,0.15) !important; color: #007AFF !important; }
    .pill-green, .pill-success { background: rgba(52,199,89,0.15) !important; color: #34C759 !important; }
    .pill-orange, .pill-warning { background: rgba(255,149,0,0.15) !important; color: #FF9500 !important; }
    .pill-red, .pill-error { background: rgba(255,59,48,0.15) !important; color: #FF3B30 !important; }

    /* Feedback boxes */
    .feedback-success { background: rgba(52,199,89,0.15) !important; color: #248A3D !important; border-radius: 12px !important; padding: 16px !important; }
    .feedback-error { background: rgba(255,59,48,0.15) !important; color: #D70015 !important; border-radius: 12px !important; padding: 16px !important; }
    .feedback-warning { background: rgba(255,149,0,0.15) !important; color: #C93400 !important; border-radius: 12px !important; padding: 16px !important; }
    .feedback-info { background: rgba(0,122,255,0.15) !important; color: #0040DD !important; border-radius: 12px !important; padding: 16px !important; }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, rgba(0,122,255,0.1), rgba(90,200,250,0.1)) !important;
        border-radius: 20px !important;
        padding: 24px !important;
    }
    .hero-title { color: #1C1C1E !important; font-size: 28px !important; font-weight: 700 !important; }
    .hero-subtitle { color: #8E8E93 !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #F2F2F7 !important;
        border-radius: 10px !important;
        padding: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #8E8E93 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #1C1C1E !important;
    }

    /* Radio buttons */
    .stRadio label {
        background: #FFFFFF !important;
        border: 1px solid #E5E5EA !important;
        border-radius: 10px !important;
        padding: 12px !important;
        color: #1C1C1E !important;
    }

    /* Alerts */
    .stAlert, [data-testid="stAlert"] {
        background: #F2F2F7 !important;
        border-radius: 12px !important;
        color: #1C1C1E !important;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, [data-testid="stToolbar"], header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #FFFFFF !important;
        color: #1C1C1E !important;
    }
    .streamlit-expanderContent {
        background: #FFFFFF !important;
    }

    /* Dropdown menus */
    [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E5EA !important;
    }
    [data-baseweb="menu"] li, [role="option"] {
        color: #1C1C1E !important;
        background: #FFFFFF !important;
    }
    [data-baseweb="menu"] li:hover, [role="option"]:hover {
        background: #F2F2F7 !important;
    }
    </style>
    """


def apply_theme():
    """Apply theme."""
    st.markdown(get_css(), unsafe_allow_html=True)


# Component functions
def render_hero(title: str, subtitle: str = "", pills: list = None) -> None:
    pills_html = ""
    if pills:
        pills_html = '<div style="margin-bottom: 12px;">' + ' '.join(
            f'<span class="pill pill-blue">{p}</span>' for p in pills
        ) + '</div>'
    st.markdown(f'''
    <div class="hero" style="background: linear-gradient(135deg, rgba(0,122,255,0.1), rgba(90,200,250,0.1)); border-radius: 20px; padding: 24px; margin-bottom: 20px;">
        {pills_html}
        <div class="hero-title" style="font-size: 28px; font-weight: 700; color: #1C1C1E;">{title}</div>
        <div class="hero-subtitle" style="color: #8E8E93; font-size: 17px;">{subtitle}</div>
    </div>
    ''', unsafe_allow_html=True)


def render_section_header(title: str, action_label: str = None, action_key: str = None) -> bool:
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


def render_metric_card(value: str, label: str, icon: str = "", color: str = "#007AFF") -> str:
    icon_html = f'<div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>' if icon else ''
    return f'''
    <div style="background: #FFFFFF; border: 1px solid #E5E5EA; border-radius: 16px; padding: 16px; text-align: center;">
        {icon_html}
        <div style="font-size: 34px; font-weight: 700; color: {color};">{value}</div>
        <div style="font-size: 13px; color: #8E8E93; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">{label}</div>
    </div>
    '''


def render_metric_grid(metrics: list) -> None:
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            st.markdown(render_metric_card(
                str(m.get("value", "0")),
                m.get("label", ""),
                m.get("icon", ""),
                m.get("color", "#007AFF")
            ), unsafe_allow_html=True)


def render_progress_bar(current: int, total: int, label: str = "") -> None:
    if label:
        st.caption(label)
    progress = current / total if total > 0 else 0
    st.progress(min(progress, 1.0))


def render_domain_coverage(domains: dict) -> None:
    for domain, coverage in domains.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(min(coverage / 100, 1.0))
        with col2:
            st.caption(f"{domain}: {coverage:.0f}%")


def render_pill(text: str, variant: str = "blue") -> str:
    colors = {
        "blue": ("#007AFF", "rgba(0,122,255,0.15)"),
        "green": ("#34C759", "rgba(52,199,89,0.15)"),
        "orange": ("#FF9500", "rgba(255,149,0,0.15)"),
        "red": ("#FF3B30", "rgba(255,59,48,0.15)"),
    }
    fg, bg = colors.get(variant, colors["blue"])
    return f'<span style="display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; background: {bg}; color: {fg};">{text}</span>'


def render_feedback(feedback_type: str, message: str, details: str = "") -> None:
    colors = {
        "success": ("#248A3D", "rgba(52,199,89,0.15)"),
        "error": ("#D70015", "rgba(255,59,48,0.15)"),
        "warning": ("#C93400", "rgba(255,149,0,0.15)"),
        "info": ("#0040DD", "rgba(0,122,255,0.15)"),
    }
    fg, bg = colors.get(feedback_type, colors["info"])
    details_html = f'<div style="margin-top: 8px;">{details}</div>' if details else ''
    st.markdown(f'''
    <div style="background: {bg}; color: {fg}; padding: 16px; border-radius: 12px; margin: 12px 0;">
        <strong>{message}</strong>
        {details_html}
    </div>
    ''', unsafe_allow_html=True)


def render_card(content: str, title: str = "") -> None:
    title_html = f'<h4 style="margin-bottom: 10px; color: #1C1C1E;">{title}</h4>' if title else ''
    st.markdown(f'''
    <div style="background: #FFFFFF; border: 1px solid #E5E5EA; border-radius: 16px; padding: 16px; margin-bottom: 12px;">
        {title_html}
        <div style="color: #8E8E93;">{content}</div>
    </div>
    ''', unsafe_allow_html=True)


def render_quick_actions(actions: list) -> None:
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


def render_stat_card(value: str, label: str, icon: str = "", color: str = "#007AFF") -> None:
    st.markdown(render_metric_card(value, label, icon, color), unsafe_allow_html=True)


def render_action_card(title: str, subtitle: str, meta: str = "", primary: bool = False, icon: str = "") -> None:
    bg = "rgba(0,122,255,0.1)" if primary else "#FFFFFF"
    border = "#007AFF" if primary else "#E5E5EA"
    icon_html = f'<span style="font-size: 32px; margin-right: 16px;">{icon}</span>' if icon else ''
    meta_html = f'<div style="font-size: 13px; color: #8E8E93; margin-top: 4px;">{meta}</div>' if meta else ''
    st.markdown(f'''
    <div style="background: {bg}; border: 1px solid {border}; border-radius: 16px; padding: 16px; margin-bottom: 12px;">
        <div style="display: flex; align-items: center;">
            {icon_html}
            <div>
                <div style="font-weight: 600; color: #1C1C1E; font-size: 17px;">{title}</div>
                <div style="color: #8E8E93; font-size: 15px;">{subtitle}</div>
                {meta_html}
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_streak_badge(streak: int) -> None:
    if streak > 0:
        st.markdown(f'''
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255,149,0,0.15); padding: 10px 16px; border-radius: 12px;">
            <span style="font-size: 24px;">🔥</span>
            <span style="font-size: 22px; font-weight: 700; color: #FF9500;">{streak}</span>
            <span style="color: #8E8E93; font-size: 15px;">day{"s" if streak != 1 else ""}</span>
        </div>
        ''', unsafe_allow_html=True)


def render_empty_state(message: str, icon: str = "📭") -> None:
    st.markdown(f'''
    <div style="text-align: center; padding: 40px 20px; background: #FFFFFF;">
        <div style="font-size: 48px; margin-bottom: 12px;">{icon}</div>
        <p style="color: #8E8E93; font-size: 17px;">{message}</p>
    </div>
    ''', unsafe_allow_html=True)


def render_loading_skeleton(height: str = "100px") -> None:
    st.markdown(f'''
    <div style="background: linear-gradient(90deg, #F2F2F7 25%, #E5E5EA 50%, #F2F2F7 75%);
                background-size: 200% 100%; height: {height}; border-radius: 12px;
                animation: shimmer 1.5s infinite;">
    </div>
    <style>@keyframes shimmer {{ 0% {{ background-position: 200% 0; }} 100% {{ background-position: -200% 0; }} }}</style>
    ''', unsafe_allow_html=True)


def render_error_state(message: str, retry_label: str = "Try again") -> bool:
    st.markdown(f'''
    <div style="text-align: center; padding: 24px; background: rgba(255,59,48,0.15); border-radius: 16px;">
        <p style="color: #FF3B30; font-size: 17px;"><strong>Something went wrong</strong></p>
        <p style="color: #8E8E93;">{message}</p>
    </div>
    ''', unsafe_allow_html=True)
    return st.button(retry_label, type="primary")


def render_profile_card(name: str, level: str, vocab_count: int, streak: int, is_active: bool = False) -> str:
    border = "#007AFF" if is_active else "#E5E5EA"
    badge = '<span style="background: rgba(52,199,89,0.15); color: #34C759; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600;">Active</span>' if is_active else ''
    return f'''
    <div style="background: #FFFFFF; border: 1px solid {border}; border-radius: 16px; padding: 16px; margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
            <div>
                <div style="font-weight: 600; color: #1C1C1E; font-size: 17px;">{name}</div>
                <div style="font-size: 15px; color: #8E8E93;">Level: {level}</div>
            </div>
            {badge}
        </div>
        <div style="display: flex; gap: 24px;">
            <div>
                <div style="font-weight: 700; color: #007AFF; font-size: 20px;">{vocab_count}</div>
                <div style="font-size: 13px; color: #8E8E93;">Words</div>
            </div>
            <div>
                <div style="font-weight: 700; color: #FF9500; font-size: 20px;">{streak}🔥</div>
                <div style="font-size: 13px; color: #8E8E93;">Streak</div>
            </div>
        </div>
    </div>
    '''


def render_cloze_sentence(before: str, after: str, answer: str = "", show_answer: bool = False) -> None:
    if show_answer:
        blank = f'<span style="border-bottom: 2px solid #34C759; color: #34C759; padding: 0 8px;">{answer}</span>'
    else:
        blank = '<span style="border-bottom: 2px solid #007AFF; color: #007AFF; padding: 0 8px; min-width: 80px; display: inline-block;">_____</span>'
    st.markdown(f'''
    <div style="font-size: 20px; color: #1C1C1E; line-height: 1.5; background: #FFFFFF; padding: 16px; border-radius: 12px;">
        {before}{blank}{after}
    </div>
    ''', unsafe_allow_html=True)


def render_exercise_feedback(correct: bool, correct_answer: str, explanation: str = "", common_mistake: str = "") -> None:
    if correct:
        st.markdown(f'''
        <div style="background: rgba(52,199,89,0.15); color: #248A3D; padding: 16px; border-radius: 12px;">
            <strong>✓ Correct!</strong>
            {f'<div style="margin-top: 8px;">{explanation}</div>' if explanation else ''}
        </div>
        ''', unsafe_allow_html=True)
    else:
        mistake_html = f'<div style="margin-top: 8px;"><em>Tip: {common_mistake}</em></div>' if common_mistake else ''
        st.markdown(f'''
        <div style="background: rgba(255,59,48,0.15); color: #D70015; padding: 16px; border-radius: 12px;">
            <strong>✗ Not quite</strong>
            <div style="margin-top: 8px;">Correct answer: <strong>{correct_answer}</strong></div>
            {f'<div style="margin-top: 8px;">{explanation}</div>' if explanation else ''}
            {mistake_html}
        </div>
        ''', unsafe_allow_html=True)


def get_design_system():
    return {"colors": COLORS, "spacing": SPACING, "radii": RADII}


# Exercise helpers
def validate_exercise(exercise: dict) -> dict:
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
    return {
        "cloze": "Fill in the blank with the correct word",
        "mcq": "Choose the correct answer",
        "translate": "Translate into Spanish",
        "free_recall": "Type the missing word",
    }.get(ex_type, "Complete the exercise")


def normalize_spanish_answer(text: str, strict_accents: bool = False) -> str:
    import re
    text = text.strip().lower()
    text = ' '.join(text.split())
    text = re.sub(r'[^\w\sáéíóúüñ]', '', text)
    if not strict_accents:
        text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i')
        text = text.replace('ó', 'o').replace('ú', 'u').replace('ü', 'u')
    return text


def check_answer(user_answer: str, correct_answers: list, strict_accents: bool = False) -> dict:
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
