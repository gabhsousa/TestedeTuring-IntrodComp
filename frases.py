import streamlit as st
import requests
import random
import threading
import uuid
import time
from streamlit.runtime.scriptrunner import add_script_run_ctx
from database import registrarResultado, registrarFraseEficaz, getFrasesEficazes, getFraseHumanaAleatoria

st.markdown(
    """
    <meta name="description"
          content="Joguinho das Frases: descubra se a frase foi escrita por um humano ou uma IA. Parte do Captcha Filosófico." />
    <meta name="robots" content="index, follow" />
    """,
    unsafe_allow_html=True,
)

# Configuracao Gemma via REST
MODELO_IA  = "gemma-3-27b-it"
GEMMA_URL  = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO_IA}:generateContent"

@st.cache_resource(show_spinner=False)
def carregarApiKey():
    try:
        key = st.secrets["GEMINI_API_KEY"]
        return key, True
    except Exception:
        return None, False

model, apiFuncionando = carregarApiKey()

# Configuracao do jogo
PROB_IA = 0.6   

TEMAS_IA = [
    "os labirintos da mente humana",
    "a imensidao do universo cosmico",
    "a essencia de um cafe arabica perfeito",
    "o fluxo incontrolavel do tempo",
    "a evolucao da sociedade",
    "a solidao nas grandes cidades",
    "a fragilidade da memoria humana",
    "a inevitabilidade da morte",
    "o paradoxo da liberdade",
    "a natureza efemera da beleza",
    "o peso do silencio",
    "a busca pelo sentido da existencia",
]

# Estado da sessao
DEFAULTS = {
    "pontos":           0,
    "rodada":           1,
    "questaoAtual":     None,
    "proximaQuestao":   None,
    "prefetchPronto":   False,
    "textosUsados":     [],
    "feedback":         None,
    "fase":             "init",
    "partidaId":        None,   
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Geracao de questao
def gerarHumano(textosUsados: list) -> dict:
    # Atraso para simular o tempo de resposta da API
    time.sleep(random.uniform(3.0, 7.0))
    return getFraseHumanaAleatoria(textosUsados)

def gerarIa(api_key) -> dict:
    tema = random.choice(TEMAS_IA)
    exemplos = getFrasesEficazes(limit=4)

    if exemplos:
        blocoExemplos = "\n".join(f'- "{e}"' for e in exemplos)
        instrucaoExemplos = (
            f"Aqui estao frases que ja foram confundidas com frases humanas:\n"
            f"{blocoExemplos}\n\n"
            "Escreva uma nova frase no mesmo estilo e nivel de qualidade."
        )
    else:
        instrucaoExemplos = "Escreva uma frase poetica e filosofica que pareca escrita por um pensador humano classico."

    prompt = (
        f"{instrucaoExemplos}\n\n"
        f"Tema: {tema}\n"
        "Requisitos: maximo 15 palavras, sem aspas, sem emojis, sem hashtags. "
        "Responda apenas com a frase, nada mais."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 100},
    }
    try:
        resp = requests.post(
            GEMMA_URL,
            params={"key": api_key},
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        texto = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        return {"texto": texto, "origem": "ia", "autor": "Gemma", "usado": None, "tema": tema}
    except Exception as e:
        return {"texto": f"[ERRO API: {e}]",
                "origem": "ia", "autor": "IA (Erro)", "usado": None, "tema": tema}

def gerarSincrono(textosUsados: list) -> dict:
    usarIa = random.random() < PROB_IA and apiFuncionando
    return gerarIa(model) if usarIa else gerarHumano(textosUsados)

def iniciarPrefetch():
    usarIa = random.random() < PROB_IA and apiFuncionando
    snapshot = list(st.session_state.textosUsados)
    modeloRef = model

    container = {"resultado": None}
    evento = threading.Event()

    def worker():
        try:
            q = gerarIa(modeloRef) if usarIa else gerarHumano(snapshot)
            container["resultado"] = q
        except Exception as e:
            print(f"[Thread Error] Falha ao gerar frase: {e}")
        finally:
            # Garante que o evento sempre seja liberado
            evento.set()

    # Cria a thread, injeta o contexto do Streamlit nela, e inicia
    thread = threading.Thread(target=worker, daemon=True)
    add_script_run_ctx(thread)
    thread.start()

    st.session_state.prefetchContainer = container
    st.session_state.prefetchEvento    = evento

def consumirPrefetch() -> dict:
    evento    = st.session_state.get("prefetchEvento")
    container = st.session_state.get("prefetchContainer")

    if evento and container:
        if not evento.is_set():
            with st.spinner("Processando analise neural..."):
                evento.wait(timeout=10.0)
        
        q = container.get("resultado")
        
        if q is None:
            q = gerarSincrono(st.session_state.textosUsados)
    else:
        q = gerarSincrono(st.session_state.textosUsados)

    st.session_state.prefetchContainer = None
    st.session_state.prefetchEvento    = None

    if q and q.get("usado"):
        st.session_state.textosUsados.append(q["usado"])
    return q

# Handler de resposta
def responder(escolha: str):
    q       = st.session_state.questaoAtual
    correta = q["origem"]
    autor   = q["autor"]
    acertou = escolha == correta
    enganou = not acertou  

    if acertou:
        st.session_state.pontos += 1

    registrarResultado(
        tipoFrase  = correta,
        fraseTexto = q["texto"],
        enganou     = enganou,
        partidaId  = st.session_state.partidaId,
    )
    
    if correta == "ia" and enganou:
        registrarFraseEficaz(
            texto = q["texto"],
            tema  = q.get("tema", ""),
        )

    st.session_state.feedback = {"acertou": acertou, "autor": autor}
    st.session_state.rodada  += 1

    if st.session_state.rodada > 10:
        st.session_state.fase = "fim"
    else:
        st.session_state.fase = "feedback"
        iniciarPrefetch()

# Header
st.markdown(
    """
    <h1 style='font-family:"Syne",sans-serif;font-weight:800;
               letter-spacing:-0.03em;font-size:2.4rem;margin-bottom:0;'>
        CAPTCHA FILOSÓFICO
    </h1>
    <p style='font-size:0.8rem;color:#888899;font-family:"Space Mono",monospace;
              margin-top:0.2rem;margin-bottom:1.5rem;'>
        — cada frase esconde um segredo
    </p>
    """,
    unsafe_allow_html=True,
)

# Maquina de estados
fase = st.session_state.fase

if fase == "init":
    st.session_state.partidaId = str(uuid.uuid4())
    q = gerarSincrono([])
    if q and q.get("usado"):
        st.session_state.textosUsados.append(q["usado"])
    st.session_state.questaoAtual = q
    st.session_state.fase = "jogando"
    st.rerun()

elif fase == "jogando":
    q = st.session_state.questaoAtual
    
    # Trava de seguranca: se a questao sumiu, reinicia a rodada automaticamente
    if q is None:
        st.session_state.fase = "init"
        st.rerun()

    colRodada, colPontos = st.columns(2)
    colRodada.metric("Rodada", f"{st.session_state.rodada} / 10")
    colPontos.metric("Pontuação", st.session_state.pontos)
    st.divider()

    st.markdown(
        f"""
        <div style='
            background:#13131a;border:1px solid #2a2a3a;
            border-left:3px solid #00e5ff;border-radius:4px;
            padding:1.2rem 1.5rem;margin:1rem 0 1.5rem;
            font-family:"Syne",sans-serif;font-size:1.1rem;
            font-weight:700;line-height:1.5;color:#e8e8f0;
        '>"{q['texto']}"</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size:0.8rem;color:#888899;text-transform:uppercase;"
        "letter-spacing:0.1em;'>Quem escreveu?</p>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Humano", use_container_width=True, type="primary", key="btnHumano"):
            responder("humano")
            st.rerun()
    with col2:
        if st.button("Inteligência Artificial", use_container_width=True, type="primary", key="btnIa"):
            responder("ia")
            st.rerun()

elif fase == "feedback":
    colRodada, colPontos = st.columns(2)
    colRodada.metric("Rodada", f"{st.session_state.rodada} / 10")
    colPontos.metric("Pontuação", st.session_state.pontos)
    st.divider()

    fb = st.session_state.feedback
    if fb["acertou"]:
        st.success(f"Acertou! O autor era: {fb['autor']}.")
    else:
        st.error(f"Errou! Na verdade foi escrito por: {fb['autor']}.")

    if st.button("Próxima frase", type="primary"):
        st.session_state.questaoAtual = consumirPrefetch()
        st.session_state.feedback      = None
        st.session_state.fase          = "jogando"
        st.rerun()

elif fase == "fim":
    pontos = st.session_state.pontos
    st.markdown(
        f"""
        <div style='background:#13131a;border:1px solid #2a2a3a;
                    border-radius:4px;padding:2rem;text-align:center;margin:1rem 0;'>
            <p style='font-size:0.75rem;color:#888899;text-transform:uppercase;
                      letter-spacing:0.12em;font-family:"Space Mono",monospace;'>
                Pontuação Final
            </p>
            <p style='font-size:3.5rem;font-family:"Syne",sans-serif;
                      font-weight:800;color:#00e5ff;margin:0;line-height:1;'>
                {pontos}<span style='font-size:1.5rem;color:#888899;'>/10</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if pontos == 10:
        st.success("Perfeito! A máquina não conseguiu te enganar.")
    elif pontos >= 7:
        st.warning("Bom resultado, mas a IA ainda conseguiu te enganar algumas vezes.")
    elif pontos >= 4:
        st.error("Resultado mediano. A IA te confundiu bastante desta vez.")
    else:
        st.error("A IA venceu dessa vez. Tente novamente!")

    st.divider()
    if st.button("Jogar Novamente", type="primary"):
        for k, v in DEFAULTS.items():
            st.session_state[k] = v
        st.rerun()