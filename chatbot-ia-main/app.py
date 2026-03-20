import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

st.set_page_config(
    page_title="NEXUS — Chat IA",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,600;1,300&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

/* ───── RESET & BASE ───── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #050a0e !important;
    color: #c8d8e0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

[data-testid="stSidebar"] {
    background-color: #080e13 !important;
    border-right: 1px solid #0d2233 !important;
}

/* ───── SIDEBAR ───── */
[data-testid="stSidebar"] * {
    font-family: 'IBM Plex Mono', monospace !important;
    color: #7aacbe !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p {
    color: #3d7d96 !important;
    font-size: 0.7rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #0a1520 !important;
    border: 1px solid #0d3349 !important;
    border-radius: 2px !important;
    color: #7aacbe !important;
    font-size: 0.78rem !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #0a1520 !important;
    border-color: #0d3349 !important;
}

/* Slider */
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: #00d4ff !important;
    box-shadow: 0 0 8px #00d4ff88 !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] div[data-testid="stTickBar"] > div {
    background: #0d3349 !important;
}

/* Divider */
[data-testid="stSidebar"] hr {
    border-color: #0d2233 !important;
}

/* Sidebar button */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid #0d3349 !important;
    border-radius: 2px !important;
    color: #3d7d96 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #00d4ff !important;
    color: #00d4ff !important;
    background: #00d4ff08 !important;
    box-shadow: 0 0 12px #00d4ff22 !important;
}

/* ───── HEADER AREA ───── */
.nexus-header {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    padding: 1.6rem 0 0.4rem 0;
    border-bottom: 1px solid #0d2233;
    margin-bottom: 2rem;
}

.nexus-logo {
    width: 44px;
    height: 44px;
    border: 1.5px solid #00d4ff;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 0 16px #00d4ff33, inset 0 0 8px #00d4ff11;
    flex-shrink: 0;
}

.nexus-title {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.nexus-title h1 {
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600;
    font-size: 1.05rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #e8f4f8;
    line-height: 1;
}

.nexus-title span {
    font-size: 0.65rem;
    color: #2d6a80;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

.nexus-status {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.65rem;
    color: #2d6a80;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.nexus-status::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 8px #00ff88;
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ───── CHAT MESSAGES ───── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 0;
    padding-bottom: 6rem;
}

.msg-row {
    display: flex;
    padding: 1.1rem 0;
    border-bottom: 1px solid #0a1a24;
    animation: fadeUp 0.25s ease-out both;
    gap: 1.2rem;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

.msg-row.user { flex-direction: row-reverse; }

.msg-badge {
    flex-shrink: 0;
    width: 30px;
    height: 30px;
    border-radius: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-top: 2px;
}

.msg-badge.user-badge {
    background: #0a1a24;
    border: 1px solid #1d4d63;
    color: #4d9ab5;
}

.msg-badge.ai-badge {
    background: #001a12;
    border: 1px solid #003d22;
    color: #00d477;
    box-shadow: 0 0 8px #00d47722;
}

.msg-body {
    max-width: 72%;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}

.msg-label {
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #1d4d63;
}

.msg-row.user .msg-label {
    text-align: right;
    color: #1d4d63;
}

.msg-text {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.88rem;
    line-height: 1.65;
    color: #b8cfd8;
    padding: 0.85rem 1rem;
    border-radius: 2px;
    position: relative;
}

.msg-text.user-text {
    background: #080f16;
    border: 1px solid #0d2a3a;
    border-right: 2px solid #1d4d63;
    text-align: left;
}

.msg-text.ai-text {
    background: #020c09;
    border: 1px solid #003321;
    border-left: 2px solid #00993a;
}

/* ───── EMPTY STATE ───── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5rem 2rem;
    gap: 1.5rem;
    text-align: center;
}

.empty-grid {
    width: 80px;
    height: 80px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px;
    opacity: 0.25;
}

.empty-grid span {
    background: #00d4ff;
    border-radius: 1px;
    animation: grid-pulse 3s ease-in-out infinite;
}

.empty-grid span:nth-child(odd) { animation-delay: 0.3s; }
.empty-grid span:nth-child(3n) { animation-delay: 0.6s; }

@keyframes grid-pulse {
    0%, 100% { opacity: 0.2; }
    50% { opacity: 1; }
}

.empty-title {
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #1d4d63;
    font-family: 'IBM Plex Mono', monospace;
}

.empty-hint {
    font-size: 0.7rem;
    color: #0d2a3a;
    letter-spacing: 0.1em;
    font-family: 'IBM Plex Mono', monospace;
}

/* ───── INPUT AREA ───── */
.stTextInput > div > div > input {
    background-color: #060c12 !important;
    border: 1px solid #0d2a3a !important;
    border-radius: 2px !important;
    color: #c8d8e0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    padding: 0.75rem 1rem !important;
    caret-color: #00d4ff !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 1px #00d4ff22, 0 0 16px #00d4ff11 !important;
}

.stTextInput > div > div > input::placeholder {
    color: #0d2a3a !important;
}

.stTextInput label {
    display: none !important;
}

/* Send button */
.stButton > button {
    background: #001a30 !important;
    border: 1px solid #00d4ff !important;
    border-radius: 2px !important;
    color: #00d4ff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.75rem !important;
    height: 46px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 12px #00d4ff22 !important;
}

.stButton > button:hover {
    background: #00d4ff18 !important;
    box-shadow: 0 0 20px #00d4ff44 !important;
}

/* ───── SPINNER ───── */
[data-testid="stSpinner"] {
    color: #00d4ff !important;
}

/* ───── ALERTS ───── */
[data-testid="stAlert"] {
    background: #0a0810 !important;
    border: 1px solid #2d1a3d !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
}

/* ───── MISC CLEANUP ───── */
[data-testid="stDecoration"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 960px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #050a0e; }
::-webkit-scrollbar-thumb { background: #0d2233; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #1d4d63; }

/* Input row alignment */
.input-row { 
    display: flex; 
    align-items: flex-end; 
    gap: 0.5rem; 
}

.prompt-prefix {
    font-size: 0.75rem;
    color: #00d4ff;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.05em;
    padding-bottom: 0.5rem;
    white-space: nowrap;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### CONFIG")
    st.markdown("<br>", unsafe_allow_html=True)

    model_name = st.selectbox(
        "MODELO",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma-2-9b-it"],
        help="Selecione o modelo Groq"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    temperature = st.slider(
        "CRIATIVIDADE",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Mais alto = respostas mais criativas"
    )

    max_tokens = st.slider(
        "TOKENS MÁX.",
        min_value=256,
        max_value=2048,
        value=1024,
        step=256
    )

    st.divider()

    if st.button("LIMPAR SESSÃO", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    n_msgs = len(st.session_state.get("messages", []))
    st.markdown(f"""
<div style='font-size:0.65rem; color:#1d4d63; letter-spacing:0.12em; line-height:2.2;'>
MENSAGENS &nbsp;&nbsp;{n_msgs:03d}<br>
MODELO &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;GROQ<br>
STATUS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ONLINE<br>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GROQ_API_KEY", "")

# ── HEADER ───────────────────────────────────────────────
st.markdown("""
<div class="nexus-header">
    <div class="nexus-logo">⬡</div>
    <div class="nexus-title">
        <h1>NEXUS</h1>
        <span>Conversational AI Interface · Groq Engine</span>
    </div>
    <div class="nexus-status">Sistema ativo</div>
</div>
""", unsafe_allow_html=True)

# ── CHAT HISTORY ─────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
<div class="empty-state">
    <div class="empty-grid">
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
    </div>
    <div class="empty-title">Sessão iniciada</div>
    <div class="empty-hint">Digite uma mensagem para começar</div>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for i, message in enumerate(st.session_state.messages):
        if isinstance(message, HumanMessage):
            st.markdown(f"""
<div class="msg-row user">
    <div class="msg-badge user-badge">EU</div>
    <div class="msg-body">
        <div class="msg-label">usuário</div>
        <div class="msg-text user-text">{message.content}</div>
    </div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class="msg-row ai">
    <div class="msg-badge ai-badge">IA</div>
    <div class="msg-body">
        <div class="msg-label">nexus</div>
        <div class="msg-text ai-text">{message.content}</div>
    </div>
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── INPUT ────────────────────────────────────────────────
col1, col2 = st.columns([0.88, 0.12])

with col1:
    user_input = st.text_input(
        "input",
        placeholder="› insira seu prompt...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    submit_button = st.button("SEND", use_container_width=True)

# ── PROCESS ──────────────────────────────────────────────
if submit_button and user_input:
    if not st.session_state.api_key:
        st.error("GROQ_API_KEY não configurada — adicione no arquivo .env")
    else:
        st.session_state.messages.append(HumanMessage(content=user_input))

        try:
            llm = ChatGroq(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=st.session_state.api_key
            )

            with st.spinner("processando..."):
                response = llm.invoke(st.session_state.messages)

            st.session_state.messages.append(AIMessage(content=response.content))
            st.rerun()

        except Exception as e:
            st.session_state.messages.pop()
            st.error(f"Erro na requisição: {str(e)}")
