import streamlit as st
from database import getStats, getFrasesEficazes

st.markdown(
    """
    <meta name="description"
          content="Captcha Filosófico: aprenda sobre o Teste de Turing e veja estatísticas reais de quem foi enganado por uma IA." />
    <meta name="robots" content="index, follow" />
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
    <h1 style='font-family:"Syne",sans-serif;font-weight:800;
               letter-spacing:-0.03em;font-size:2.6rem;margin-bottom:0;'>
        O TESTE DE TURING
    </h1>
    <p style='font-size:0.8rem;color:#888899;font-family:"Space Mono",monospace;
              margin-top:0.2rem;margin-bottom:2rem;'>
       — pode uma máquina pensar?
    </p>
    """,
    unsafe_allow_html=True,
)

# O que e o Teste de Turing
st.markdown(
    """
    <div style='
        background:#13131a;border:1px solid #2a2a3a;
        border-left:3px solid #00e5ff;border-radius:4px;
        padding:1.5rem 1.8rem;margin-bottom:1.5rem;
    '>
        <p style='font-family:"Syne",sans-serif;font-weight:700;
                  font-size:1rem;color:#e8e8f0;margin:0 0 0.8rem;'>
            O que é o Teste de Turing?
        </p>
        <p style='font-size:0.85rem;color:#aaaabc;line-height:1.7;margin:0;'>
            Em 1950, o matemático britânico <strong style='color:#e8e8f0;'>Alan Turing</strong> 
            propôs uma questão provocadora: <em>"Can machines think?"</em> Para responder, 
            ele criou o <strong style='color:#e8e8f0;'>Jogo da Imitação</strong>, um experimento 
            onde um humano conversa com dois interlocutores desconhecidos, um humano e uma máquina, 
            e tenta identificar qual é qual. Se a máquina for indistinguível do humano, 
            ela teria passado no teste.
        </p>
    </div>

    <div style='
        background:#13131a;border:1px solid #2a2a3a;
        border-left:3px solid #ff4081;border-radius:4px;
        padding:1.5rem 1.8rem;margin-bottom:1.5rem;
    '>
        <p style='font-family:"Syne",sans-serif;font-weight:700;
                  font-size:1rem;color:#e8e8f0;margin:0 0 0.8rem;'>
            Por que ainda importa?
        </p>
        <p style='font-size:0.85rem;color:#aaaabc;line-height:1.7;margin:0;'>
            Mais de 70 anos depois, o teste de Turing continua sendo um dos conceitos mais 
            debatidos da inteligência artificial. Com o surgimento de modelos de linguagem 
            como GPT e Gemini, a linha entre o humano e a máquina ficou mais tênue do que nunca. 
            Hoje, IAs escrevem poesia, filosofia e literatura, e humanos frequentemente 
            não conseguem distinguir.
        </p>
    </div>

    <div style='
        background:#13131a;border:1px solid #2a2a3a;
        border-left:3px solid #888899;border-radius:4px;
        padding:1.5rem 1.8rem;margin-bottom:2rem;
    '>
        <p style='font-family:"Syne",sans-serif;font-weight:700;
                  font-size:1rem;color:#e8e8f0;margin:0 0 0.8rem;'>
            Como funciona este experimento?
        </p>
        <p style='font-size:0.85rem;color:#aaaabc;line-height:1.7;margin:0;'>
            No <strong style='color:#e8e8f0;'>Captcha Filosófico</strong>, você lê frases 
            filosóficas e tenta identificar se foram escritas por um humano ou geradas por 
            uma IA. A cada rodada que a IA te engana, ela aprende, as frases mais convincentes 
            são usadas como referência para gerar frases ainda melhores. 
            É um Teste de Turing em evolução contínua.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Estatisticas ao vivo
st.markdown(
    "<p style='font-size:0.75rem;color:#888899;text-transform:uppercase;"
    "letter-spacing:0.12em;font-family:\"Space Mono\",monospace;margin-bottom:0.8rem;'>"
    "Estatísticas ao vivo</p>",
    unsafe_allow_html=True,
)

stats = getStats()

totalPartidas = int(stats.get("total_partidas") or 0)
totalRodadas  = int(stats.get("total_rodadas") or 0)
iaEnganou     = int(stats.get("ia_enganou") or 0)
taxaIa        = float(stats.get("taxa_engano_ia") or 0)
taxaGeral     = float(stats.get("taxa_engano_geral") or 0)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Partidas jogadas",   f"{totalPartidas:,}".replace(",", "."))
col2.metric("Rodadas totais",     f"{totalRodadas:,}".replace(",", "."))
col3.metric("IA enganou",         f"{iaEnganou:,}".replace(",", "."), help="Vezes que a IA passou por humano")
col4.metric("Taxa de engano (IA)", f"{taxaIa}%", help="% das rodadas com IA em que o jogador errou")

# Frases que mais enganaram
st.divider()

frasesTop = getFrasesEficazes(limit=5)

if frasesTop:
    st.markdown(
        "<p style='font-size:0.75rem;color:#888899;text-transform:uppercase;"
        "letter-spacing:0.12em;font-family:\"Space Mono\",monospace;margin-bottom:1rem;'>"
        "Frases da IA que mais enganaram jogadores</p>",
        unsafe_allow_html=True,
    )
    for frase in frasesTop:
        st.markdown(
            f"""
            <div style='
                background:#13131a;border:1px solid #2a2a3a;
                border-radius:4px;padding:0.9rem 1.2rem;margin-bottom:0.5rem;
                font-family:"Syne",sans-serif;font-size:0.95rem;
                font-style:italic;color:#aaaabc;
            '>"{frase}"</div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        "<p style='font-size:0.85rem;color:#888899;'>Nenhuma frase ainda. "
        "Jogue algumas rodadas para ver quais frases da IA mais enganam!</p>",
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    """
    <p style='font-size:0.85rem;color:#888899;text-align:center;'>
        Pronto para ser testado?
    </p>
    """,
    unsafe_allow_html=True,
)