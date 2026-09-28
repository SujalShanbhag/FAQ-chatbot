from html import escape

import streamlit as st

from chatbot import get_bot_response
from faq_data import FAQ_DATA


SAMPLE_QUESTIONS = [
    "What documents are required for admission?",
    "How can I apply for a scholarship?",
    "When is the application deadline?",
    "Can international students apply?",
    "Do I need English proficiency proof?",
    "How can I check my application status?",
]


def add_custom_styles():
    """Add the black + blue dashboard theme."""
    st.markdown(
        """
        <style>
        :root {
            --page-bg: #030712;
            --card-bg: #07111f;
            --text: #f2f7ff;
            --muted: #9db0c9;
            --border: rgba(57,151,255,.40);
            --blue: #1683ff;
            --blue-hover: #0d5fbd;
        }

        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: var(--page-bg) !important;
            color: var(--text) !important;
            font-family: "Segoe UI", Arial, sans-serif;
        }

        header[data-testid="stHeader"] {
            background: var(--page-bg) !important;
            border-bottom: 1px solid var(--border);
        }

        header[data-testid="stHeader"] button,
        header[data-testid="stHeader"] a,
        [data-testid="stToolbar"] {
            display: none !important;
        }

        .main .block-container {
            max-width: 1180px;
            padding-bottom: 2rem;
            padding-top: 1.5rem;
        }

        .app-header,
        div[data-testid="stForm"],
        .chat-card,
        .sidebar-note {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
        }

         .app-header {
            margin-bottom: 1rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, #050b18, #071a35) !important;
        }

        .app-header h1 {
            color: #ffffff;
            font-size: 2.8rem;
            margin-bottom: 0.25rem;
        }

        .subtitle {
            color: var(--blue);
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .description {
            color: var(--muted);
            font-size: 1rem;
        }

        div[data-testid="stForm"] {
            margin-bottom: 1rem;
            padding: 1rem 1rem 0.35rem 1rem;
        }

        div[data-testid="stForm"] label {
            color: var(--text) !important;
            font-weight: 600;
        }

        .stTextInput input {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text);
        }

        .stTextInput input::placeholder {
            color: #8198b6;
            opacity: 1;
        }

        .stTextInput input:focus {
            border-color: var(--blue);
            box-shadow: 0 0 0 1px var(--blue);
        }

        div[data-testid="stFormSubmitButton"] button,
        div[data-testid="stButton"] button {
            background: var(--blue);
            border: 1px solid var(--blue);
            border-radius: 6px;
            color: #07111f;
            font-weight: 700;
            min-height: 2.6rem;
        }

        div[data-testid="stFormSubmitButton"] button *,
        div[data-testid="stButton"] button * {
            color: #07111f !important;
        }

        div[data-testid="stFormSubmitButton"] button:hover,
        div[data-testid="stButton"] button:hover {
            background: var(--blue-hover);
            border-color: var(--blue-hover);
            color: #07111f;
        }

        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div {
            background: var(--page-bg) !important;
            border-right: 1px solid var(--border);
            color: var(--text) !important;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: var(--text);
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] .stMarkdown {
            color: var(--muted);
        }

        section[data-testid="stSidebar"] button,
        section[data-testid="stSidebar"] button * {
            color: #07111f !important;
        }

        .sidebar-note {
            color: var(--text);
            margin-bottom: 1rem;
            margin-top: 0.8rem;
            padding: 0.75rem;
        }

        .history-title {
            color: var(--text);
            margin-top: 0.5rem;
        }

        .chat-card {
            margin: 0.85rem 0;
            padding: 1rem;
        }

        .user-question {
            color: var(--blue-hover);
            font-weight: 600;
            margin-bottom: 0.75rem;
        }

        .bot-answer {
            color: var(--text);
            line-height: 1.55;
            margin-bottom: 0.9rem;
        }

        .meta-row {
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 0.92rem;
            padding-top: 0.7rem;
        }

        .status {
            border-radius: 6px;
            display: inline-block;
            font-size: 0.82rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            padding: 0.25rem 0.55rem;
        }

        .status-confident {
            background: rgba(35,205,125,.14);
            border: 1px solid rgba(35,205,125,.35);
            color: #62e5a5;
        }

        .status-fallback {
            background: rgba(255,185,75,.12);
            border: 1px solid rgba(255,185,75,.35);
            color: #ffd184;
        }

        div[data-testid="stAlert"][kind="warning"] {
            background: #07182a;
            border: 1px solid rgba(255,185,75,.35);
        }

        div[data-testid="stAlert"][kind="warning"] * {
            color: #ffd184 !important;
        }

        div[data-testid="stAlert"][kind="info"] {
            background: #071b32;
            border: 1px solid #bfdbfe;
        }

        div[data-testid="stAlert"][kind="info"] * {
            color: #75bcff !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def save_chat(user_question, bot_response):
    st.session_state.chat_history.insert(
        0,
        {
            "question": user_question,
            "response": bot_response,
        },
    )


def show_sidebar():
    with st.sidebar:
        st.header("Sample Questions")

        for question in SAMPLE_QUESTIONS:
            st.write(f"- {question}")

        st.divider()
        st.markdown(
            f"""
            <div class="sidebar-note">
                FAQ dataset contains <strong>{len(FAQ_DATA)}</strong>
                admission questions.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history cleared.")


def show_header():
    st.markdown(
        """
        <div class="app-header">
            <h1>FAQ Chatbot</h1>
            <div class="subtitle">
                Artificial Intelligence Internship - Task 2
            </div>
            <div class="description">
                Ask university admission related questions and get answers using
                an NLP-based FAQ matching chatbot.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_meta_details(response):
    status_text = response["status"]

    if response["is_confident"]:
        matched_question = escape(response["matched_question"])
        category = escape(response["category"])

        return (
            f"<strong>Matched FAQ:</strong> {matched_question}<br>"
            f"<strong>Category:</strong> {category}<br>"
            f"<strong>Confidence Score:</strong> {response['confidence_score']:.2f}<br>"
            f"<strong>Status:</strong> {status_text}"
        )

    return (
        f"<strong>Confidence Score:</strong> {response['confidence_score']:.2f}<br>"
        f"<strong>Status:</strong> {status_text}"
    )


def show_chat_card(chat_item):
    response = chat_item["response"]
    status_class = "status-confident" if response["is_confident"] else "status-fallback"
    question = escape(chat_item["question"])
    answer = escape(response["answer"])
    status_text = escape(response["status"])
    meta_details = build_meta_details(response)

    chat_card_html = (
        '<div class="chat-card">'
        f'<div class="user-question">You: {question}</div>'
        f'<div class="status {status_class}">{status_text}</div>'
        f'<div class="bot-answer">Chatbot: {answer}</div>'
        f'<div class="meta-row">{meta_details}</div>'
        "</div>"
    )

    st.markdown(chat_card_html, unsafe_allow_html=True)


def run_app():
    st.set_page_config(
        page_title="CodeAlpha FAQ Chatbot",
        page_icon="chat",
        layout="wide",
    )

    add_custom_styles()
    initialize_session_state()
    show_sidebar()
    show_header()

    with st.form("question_form", clear_on_submit=True):
        user_question = st.text_input(
            "Ask a university admission question",
            placeholder="Example: What documents are required for admission?",
        )
        submitted = st.form_submit_button("Ask Chatbot", use_container_width=True)

    if submitted:
        if not user_question.strip():
            st.warning("Please enter a question before asking the chatbot.")
        else:
            bot_response = get_bot_response(user_question)
            save_chat(user_question, bot_response)

    st.markdown('<h3 class="history-title">Chat History</h3>', unsafe_allow_html=True)

    if st.session_state.chat_history:
        for chat_item in st.session_state.chat_history:
            show_chat_card(chat_item)
    else:
        st.info("Ask a question to start the chat.")
