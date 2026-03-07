import streamlit as st
from supabase import create_client, Client

@st.cache_resource(show_spinner=False)
def getClient() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def registrarResultado(tipoFrase: str, fraseTexto: str, enganou: bool, partidaId: str = None):
    try:
        db = getClient()
        db.table("resultados").insert({
            "tipo_frase":  tipoFrase,
            "frase_texto": fraseTexto,
            "enganou":     enganou,
            "partida_id":  partidaId,
        }).execute()
    except Exception as e:
        print(f"[DB] Erro ao registrar resultado: {e}")

def registrarFraseEficaz(texto: str, tema: str):
    try:
        db = getClient()
        resp = db.table("frases_eficazes")\
            .select("id, vezes_gerada, vezes_enganou")\
            .eq("texto", texto)\
            .execute()

        if resp.data:
            row = resp.data[0]
            db.table("frases_eficazes").update({
                "vezes_gerada":  row["vezes_gerada"] + 1,
                "vezes_enganou": row["vezes_enganou"] + 1,
            }).eq("id", row["id"]).execute()
        else:
            db.table("frases_eficazes").insert({
                "texto":         texto,
                "tema":          tema,
                "vezes_gerada":  1,
                "vezes_enganou": 1,
            }).execute()
    except Exception as e:
        print(f"[DB] Erro ao registrar frase eficaz: {e}")

def registrarFraseGerada(texto: str, tema: str):
    try:
        db = getClient()
        resp = db.table("frases_eficazes")\
            .select("id, vezes_gerada")\
            .eq("texto", texto)\
            .execute()

        if resp.data:
            row = resp.data[0]
            db.table("frases_eficazes").update({
                "vezes_gerada": row["vezes_gerada"] + 1,
            }).eq("id", row["id"]).execute()
    except Exception as e:
        print(f"[DB] Erro ao registrar frase gerada: {e}")

@st.cache_data(ttl=60, show_spinner=False)
def getFrasesEficazes(limit: int = 5) -> list[str]:
    try:
        db = getClient()
        resp = db.table("frases_eficazes")\
            .select("texto")\
            .order("vezes_enganou", desc=True)\
            .limit(limit)\
            .execute()
        return [row["texto"] for row in resp.data]
    except Exception as e:
        print(f"[DB] Erro ao buscar frases eficazes: {e}")
        return []

@st.cache_data(ttl=300, show_spinner=False)
def getFraseHumanaAleatoria(textosUsados: list) -> dict:
    try:
        db = getClient()
        resp = db.table("frases_humanas")\
            .select("texto, autor")\
            .eq("ativa", True)\
            .execute()

        disponiveis = [
            r for r in resp.data
            if r["texto"] not in textosUsados
        ]
        
        if not disponiveis:
            disponiveis = resp.data

        import random
        escolha = random.choice(disponiveis)
        return {
            "texto":   escolha["texto"],
            "origem":  "humano",
            "autor":   escolha["autor"],
            "usado":   escolha["texto"],
            "tema":    None,
        }
    except Exception as e:
        print(f"[DB] Erro ao buscar frase humana: {e}")
        from frasesDb import textosHumanos
        import random
        disponiveis = [t for t in textosHumanos if t["texto"] not in textosUsados]
        if not disponiveis:
            disponiveis = textosHumanos
        h = random.choice(disponiveis)
        return {"texto": h["texto"], "origem": "humano", "autor": h["autor"], "usado": h["texto"], "tema": None}

@st.cache_data(ttl=30, show_spinner=False)
def getStats() -> dict:
    try:
        db = getClient()
        resp = db.table("stats").select("*").execute()
        if resp.data:
            return resp.data[0]
    except Exception as e:
        print(f"[DB] Erro ao buscar stats: {e}")

    return {
        "total_partidas":     0,
        "total_rodadas":      0,
        "total_enganos":      0,
        "ia_enganou":         0,
        "humana_enganou":     0,
        "taxa_engano_ia":     0,
        "taxa_engano_geral":  0,
    }