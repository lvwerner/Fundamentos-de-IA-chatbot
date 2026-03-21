import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from datetime import datetime

st.set_page_config(
    page_title="terminal://chat",
    page_icon="▶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── ESTILOS GLOBAIS ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,600;0,700;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #1a1b1e !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background-color: #16171a !important;
    border-right: 1px solid #2d3139 !important;
}
[data-testid="stSidebar"] * {
    font-family: 'JetBrains Mono', monospace !important;
    color: #39d353 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] .stMarkdown p {
    color: #8b949e !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #1e2024 !important;
    border: 1px solid #30363d !important;
    border-radius: 0 !important;
    color: #e2e8f0 !important;
    font-size: 0.78rem !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: #39d353 !important;
    box-shadow: 0 0 8px #39d35388 !important;
}
[data-testid="stSidebar"] hr { border-color: #2d3139 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid #30363d !important;
    border-radius: 0 !important;
    color: #8b949e !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #39d353 !important;
    color: #39d353 !important;
    background: #39d35312 !important;
}

/* ── MAIN ── */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 1000px !important;
}

/* ── TERMINAL WINDOW ── */
.term-window {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 24px 64px rgba(0,0,0,0.7), 0 0 0 1px #ffffff08;
}
.term-titlebar {
    background: #21262d;
    border-bottom: 1px solid #30363d;
    padding: 0.65rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    user-select: none;
}
.term-dot { width: 13px; height: 13px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.dot-red { background: #ff5f57; box-shadow: 0 0 6px #ff5f5799; }
.dot-yel { background: #ffbd2e; box-shadow: 0 0 6px #ffbd2e99; }
.dot-grn { background: #28c840; box-shadow: 0 0 6px #28c84099; }
.term-title-text {
    flex: 1;
    text-align: center;
    font-size: 0.72rem;
    color: #8b949e;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin-left: -2rem;
}
.term-body {
    padding: 1.6rem 1.8rem;
    min-height: 58vh;
    max-height: 66vh;
    overflow-y: auto;
    background: #0d1117;
}

/* ── LOGIN SCREEN ── */
.login-body {
    padding: 3rem 2rem;
    background: #0d1117;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 50vh;
    justify-content: center;
}
.login-ascii {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #39d353;
    line-height: 1.4;
    text-align: center;
    margin-bottom: 2rem;
    opacity: 0.85;
}
.login-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #8b949e;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    text-align: left;
    width: 100%;
    max-width: 440px;
}
.login-hint {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #484f58;
    margin-top: 0.6rem;
    text-align: center;
}
.login-hint a { color: #58a6ff; text-decoration: none; }
.login-hint a:hover { text-decoration: underline; }

/* ── MESSAGES ── */
.term-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875rem;
    line-height: 1.75;
    margin-bottom: 1.6rem;
    animation: fadeIn 0.18s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to   { opacity: 1; transform: translateY(0); }
}
.term-prompt-user {
    color: #39d353; font-weight: 700; margin-bottom: 0.3rem;
    font-size: 0.8rem; letter-spacing: 0.02em;
}
.term-prompt-ai {
    color: #58a6ff; font-weight: 700; margin-bottom: 0.3rem;
    font-size: 0.8rem; letter-spacing: 0.02em;
}
.term-tag-user {
    display: inline-block; background: #1a3a22; border: 1px solid #2ea04326;
    color: #39d353; font-size: 0.6rem; padding: 0 0.4rem;
    letter-spacing: 0.08em; margin-left: 0.5rem; vertical-align: middle; font-weight: 600;
}
.term-tag-ai {
    display: inline-block; background: #1a2a3a; border: 1px solid #388bfd26;
    color: #58a6ff; font-size: 0.6rem; padding: 0 0.4rem;
    letter-spacing: 0.08em; margin-left: 0.5rem; vertical-align: middle; font-weight: 600;
}
.term-text-user {
    color: #f0f6fc; padding: 0.65rem 1.1rem; border-left: 3px solid #39d353;
    margin-left: 0.2rem; background: #161b22; font-size: 0.875rem; line-height: 1.7;
}
.term-text-ai {
    color: #cdd9e5; padding: 0.65rem 1.1rem; border-left: 3px solid #58a6ff;
    margin-left: 0.2rem; background: #131a24; white-space: pre-wrap;
    font-size: 0.875rem; line-height: 1.7;
}

/* ── BOOT STATE ── */
.term-boot {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem; line-height: 2.2; padding: 1rem 0; color: #8b949e;
}
.term-boot .ok   { color: #39d353; font-weight: 700; }
.term-boot .warn { color: #e3b341; font-weight: 700; }
.term-boot .info { color: #58a6ff; font-weight: 700; }
.term-boot .dim  { color: #30363d; }
.term-boot .hint { color: #6e7681; }
.term-boot .msg  { color: #adbac7; }

/* ── INPUT ── */
.stTextInput > div > div > input {
    background-color: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 4px !important;
    color: #f0f6fc !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.875rem !important;
    padding: 0.55rem 0.9rem !important;
    caret-color: #39d353 !important;
    transition: border-color 0.15s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #388bfd !important;
    box-shadow: 0 0 0 2px #388bfd22 !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: #484f58 !important; }
.stTextInput label { display: none !important; }
.stTextInput > div { border: none !important; box-shadow: none !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: #21262d !important;
    border: 1px solid #39d353 !important;
    border-radius: 4px !important;
    color: #39d353 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1rem !important;
    height: 42px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #2a3a2e !important;
    border-color: #46ef63 !important;
    box-shadow: 0 0 16px #39d35330 !important;
    color: #46ef63 !important;
}

/* ── MISC ── */
[data-testid="stSpinner"] { color: #39d353 !important; }
[data-testid="stDecoration"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; border-bottom: none !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #484f58; }
[data-testid="stAlert"] {
    background: #1a0f0f !important;
    border: 1px solid #f8514926 !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #f85149 !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ══════════════════════════════════════════════════════════
# TELA DE LOGIN — exibida enquanto não há chave válida
# ══════════════════════════════════════════════════════════
if not st.session_state.authenticated:

    st.markdown("""
<div class="term-window">
  <div class="term-titlebar">
    <span class="term-dot dot-red"></span>
    <span class="term-dot dot-yel"></span>
    <span class="term-dot dot-grn"></span>
    <span class="term-title-text">groq-chat — autenticação — 80×24</span>
  </div>
  <div class="term-body" style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:50vh;">
    <div style="width:100%; max-width:440px;">
      <pre style="font-family:JetBrains Mono,monospace; font-size:0.68rem; color:#39d353; line-height:1.35; text-align:center; margin-bottom:2rem; opacity:0.9;">
  ██████╗ ██████╗  ██████╗  ██████╗
 ██╔════╝ ██╔══██╗██╔═══██╗██╔═══██╗
 ██║  ███╗██████╔╝██║   ██║██║   ██║
 ██║   ██║██╔══██╗██║   ██║██║▄▄ ██║
 ╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══▀▀═╝
      chat · powered by groq</pre>

      <div style="font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#8b949e;
           letter-spacing:0.14em; text-transform:uppercase; margin-bottom:0.5rem;">
        ▶ &nbsp;groq api key
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # centraliza o input
    _, col_center, _ = st.columns([0.15, 0.7, 0.15])
    with col_center:
        api_input = st.text_input(
            "api_key_input",
            placeholder="gsk_••••••••••••••••••••••••••••••••",
            type="password",
            label_visibility="collapsed",
            key="api_key_field"
        )
        col_btn, col_link = st.columns([0.45, 0.55])
        with col_btn:
            entrar = st.button("AUTENTICAR ↵", use_container_width=True)
        with col_link:
            st.markdown("""
<div style='font-family:JetBrains Mono,monospace; font-size:0.63rem; color:#484f58;
     padding-top:0.75rem; padding-left:0.5rem;'>
sem chave? &nbsp;<a href="https://console.groq.com" target="_blank"
style="color:#58a6ff; text-decoration:none;">console.groq.com ↗</a>
</div>
""", unsafe_allow_html=True)

        if entrar and api_input:
            # valida a chave fazendo uma chamada real
            with st.spinner("▶ validando chave..."):
                try:
                    test_llm = ChatGroq(
                        model="llama-3.1-8b-instant",
                        max_tokens=10,
                        api_key=api_input
                    )
                    test_llm.invoke([HumanMessage(content="hi")])
                    st.session_state.api_key = api_input
                    st.session_state.authenticated = True
                    st.rerun()
                except Exception:
                    st.error("chave inválida ou sem conexão — tente novamente")
        elif entrar and not api_input:
            st.error("insira sua API key antes de continuar")

    st.stop()  # não renderiza nada mais enquanto não autenticado

# ══════════════════════════════════════════════════════════
# CHAT — exibido após autenticação
# ══════════════════════════════════════════════════════════

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style='font-family:JetBrains Mono,monospace; font-size:0.62rem; color:#484f58;
     letter-spacing:0.22em; text-transform:uppercase; margin-bottom:1.4rem;
     border-bottom:1px solid #21262d; padding-bottom:0.8rem;'>
▶ &nbsp;config.sys
</div>
""", unsafe_allow_html=True)

    model_name = st.selectbox(
        "modelo",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma-2-9b-it"],
    )
    st.markdown("<br>", unsafe_allow_html=True)
    temperature = st.slider("criatividade", 0.0, 1.0, 0.7, 0.1)
    max_tokens  = st.slider("tokens máx.", 256, 2048, 1024, 256)
    st.divider()

    if st.button("▶ limpar sessão", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("⏻ sair / trocar chave", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.api_key = ""
        st.session_state.messages = []
        st.rerun()

    st.divider()
    n_msgs = len(st.session_state.messages)
    now    = datetime.now().strftime("%H:%M:%S")
    # mascara a chave: mostra só os últimos 4 chars
    key_masked = "••••" + st.session_state.api_key[-4:] if len(st.session_state.api_key) >= 4 else "••••"
    st.markdown(f"""
<div style='font-family:JetBrains Mono,monospace; font-size:0.66rem; line-height:2.4; letter-spacing:0.08em;'>
<span style='color:#484f58;'>msgs&nbsp;&nbsp;&nbsp;&nbsp;</span><span style='color:#e2e8f0;'>{n_msgs:03d}</span><br>
<span style='color:#484f58;'>modelo&nbsp;&nbsp;</span><span style='color:#e2e8f0;'>groq</span><br>
<span style='color:#484f58;'>status&nbsp;&nbsp;</span><span style='color:#39d353;'>&#9679; autenticado</span><br>
<span style='color:#484f58;'>chave&nbsp;&nbsp;&nbsp;</span><span style='color:#e2e8f0;'>{key_masked}</span><br>
<span style='color:#484f58;'>hora&nbsp;&nbsp;&nbsp;&nbsp;</span><span style='color:#e2e8f0;'>{now}</span>
</div>
""", unsafe_allow_html=True)

# ── TERMINAL WINDOW ───────────────────────────────────────
st.markdown("""
<div class="term-window">
  <div class="term-titlebar">
    <span class="term-dot dot-red"></span>
    <span class="term-dot dot-yel"></span>
    <span class="term-dot dot-grn"></span>
    <span class="term-title-text">groq-chat — bash — 80×24</span>
  </div>
  <div class="term-body" id="term-body">
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
<div class="term-boot">
<span class="dim">─────────────────────────────────────────────────────────</span><br>
<span class="ok">  [  OK  ]</span>  <span class="msg">iniciando <strong>groq-chat</strong>.service</span><br>
<span class="ok">  [  OK  ]</span>  <span class="msg">carregando modelo llm</span><br>
<span class="ok">  [  OK  ]</span>  <span class="msg">api key autenticada com sucesso</span><br>
<span class="info">  [ INFO ]</span>  <span class="msg">sessão iniciada — pronto para input</span><br>
<span class="dim">─────────────────────────────────────────────────────────</span><br>
<br>
<span class="hint">▶  digite sua mensagem abaixo e pressione ENTER ↵</span>
</div>
""", unsafe_allow_html=True)
else:
    for i, msg in enumerate(st.session_state.messages):
        idx = (i // 2) + 1
        if isinstance(msg, HumanMessage):
            st.markdown(f"""
<div class="term-line">
  <div class="term-prompt-user">user@groq-chat:~$<span class="term-tag-user">INPUT #{idx:03d}</span></div>
  <div class="term-text-user">{msg.content}</div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class="term-line">
  <div class="term-prompt-ai">assistant@groq:~$<span class="term-tag-ai">OUTPUT #{idx:03d}</span></div>
  <div class="term-text-ai">{msg.content}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

# ── INPUT ROW ────────────────────────────────────────────
col_prefix, col_input, col_btn = st.columns([0.035, 0.835, 0.13])

with col_prefix:
    st.markdown("""
<div style='font-family:JetBrains Mono,monospace; color:#39d353; font-size:1rem;
     padding-top:0.52rem; white-space:nowrap; font-weight:700;'>$</div>
""", unsafe_allow_html=True)

with col_input:
    user_input = st.text_input(
        "input",
        placeholder="insira seu comando...",
        label_visibility="collapsed",
        key="user_input"
    )

with col_btn:
    submit_button = st.button("EXEC ↵", use_container_width=True)

# ── PROCESS ──────────────────────────────────────────────
if (submit_button or user_input) and user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))
    try:
        llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=st.session_state.api_key
        )
        with st.spinner("▶ processando..."):
            response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
        st.rerun()
    except Exception as e:
        st.session_state.messages.pop()
        st.error(f"erro: {str(e)}")
