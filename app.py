import streamlit as st

# CONFIGURACAO INICIAL
st.set_page_config(
    page_title="Captcha Filosófico | Humano ou IA?",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": (
            "**Captcha Filosófico** — Você consegue distinguir a mente humana "
            "de uma Inteligência Artificial? Descubra aqui."
        ),
    },
)

# CSS GLOBAL
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

    :root {
        --bg:        #0a0a0f;
        --surface:   #13131a;
        --border:    #2a2a3a;
        --accent:    #00e5ff;
        --accent2:   #ff4081;
        --text:      #e8e8f0;
        --muted:     #888899;
        --font-head: 'Syne', sans-serif;
        --font-mono: 'Space Mono', monospace;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg) !important;
        color: var(--text) !important;
        font-family: var(--font-mono) !important;
    }

    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { font-family: var(--font-mono) !important; }

    h1, h2, h3, h4 {
        font-family: var(--font-head) !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }

    .stButton > button[kind="primary"] {
        background: transparent !important;
        color: var(--accent) !important;
        border: 1px solid var(--accent) !important;
        font-family: var(--font-mono) !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        transition: background 0.2s, color 0.2s !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--accent) !important;
        color: var(--bg) !important;
    }

    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: var(--muted) !important;
        border: 1px solid var(--border) !important;
        font-family: var(--font-mono) !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.06em !important;
        transition: border-color 0.2s, color 0.2s !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--muted) !important;
        color: var(--text) !important;
    }

    [data-testid="stMetric"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        padding: 0.75rem 1rem !important;
    }
    [data-testid="stMetricValue"] {
        font-family: var(--font-head) !important;
        color: var(--accent) !important;
    }

    [data-testid="stChatMessage"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
    }

    [data-testid="stAlert"] {
        border-radius: 4px !important;
        font-family: var(--font-mono) !important;
        font-size: 0.85rem !important;
    }

    hr { border-color: var(--border) !important; }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

    .material-symbols-rounded, [data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded" !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

paginaIA = st.Page("genAi.py", title="IA Generativa")
paginaHome = st.Page("home.py", title="O Teste de Turing", default=True)
paginaJogo = st.Page("frases.py", title="Humano ou IA?")

pg = st.navigation([paginaIA, paginaHome, paginaJogo], position="hidden")

with st.sidebar:
    st.markdown(
        """
        <h2 style='font-family:"Syne",sans-serif;font-weight:800;
                   letter-spacing:-0.02em;margin-bottom:0;color:#e8e8f0;'>
            CAPTCHA<br>FILOSÓFICO
        </h2>
        <p style='font-size:0.75rem;color:#888899;margin-top:0.3rem;
                  font-family:"Space Mono",monospace;'>
            — você consegue distinguir?
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown(
        "<p style='font-size:0.8rem;color:#888899;line-height:1.6;'>"
        "Simulação do Teste de Turing explorando a fronteira entre a "
        "mente humana e a Inteligência Artificial."
        "</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    st.page_link(paginaIA, label="IA Generativa")
    st.page_link(paginaHome, label="O Teste de Turing")
    st.page_link(paginaJogo, label="Humano ou IA?")
    
    st.divider()

    st.markdown(
        "<p style='font-size:0.7rem;color:#888899;font-family:\"Space Mono\",monospace;'>"
        "EQUIPE</p>",
        unsafe_allow_html=True,
    )
    membros = [
        "João Pedro da Silva Araújo",
        "Tarsis Lima Gomes da Silva",
        "Álefe Brito Monteiro",
        "Gabriel Henrique Cavalcante de Sousa",
        "António José Batista Salazar",
    ]
    for m in membros:
        st.markdown(
            f"<p style='font-size:0.72rem;color:#aaaabc;margin:0.1rem 0;'>- {m}</p>",
            unsafe_allow_html=True,
        )

    st.divider()
    st.caption("Powered by Google Gemini & Streamlit")
pg.run()