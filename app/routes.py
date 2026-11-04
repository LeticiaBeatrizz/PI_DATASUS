from app import app
from flask import abort, render_template

from app.services.ConteudoService import ConteudoService
from config import Config


ESTUDO_TEORICO_HTML = ConteudoService.carregar_markdown("estudo_teorico.md")
DEFINICAO_BASE_DADOS_HTML = ConteudoService.carregar_markdown("def_dados.md")
ANALISE_DADOS_HTML = ConteudoService.carregar_markdown("analise_dados.md")
DEFINICAO_BASE_DADOS_VACINAS_HTML = ConteudoService.carregar_markdown("def_dados_vacinas.md")


OPCOES = {
    1: {
        "titulo": "Estudo Teórico",
        "subtitulo": "Febre Amarela",
        "texto": ESTUDO_TEORICO_HTML,
        "html": True,
    },
    2: {
        "titulo": "Definição da Base de Dados",
        "subtitulo": "Febre Amarela",
        "texto": DEFINICAO_BASE_DADOS_HTML,
        "html": True,
    },
    4: {
        "titulo": "Análise de Dados",
        "subtitulo": "Febre Amarela",
        "texto": ANALISE_DADOS_HTML,
        "graficos_streamlit": True,
        "html": True,
    },
    5: {
        "titulo": "Definição da Base de Dados: Dados Vacinais",
        "subtitulo": "Febre Amarela",
        "texto": DEFINICAO_BASE_DADOS_VACINAS_HTML,
        "html": True,
    },
}


@app.route('/')
def home():
    return render_template("index.html", dados={"subtitulo": "Febre Amarela"})


@app.route("/opcao/<int:num>")
def opcao(num):
    dados = OPCOES.get(num)
    if not dados:
        abort(404)

    graficos_streamlit = None
    if dados.get("graficos_streamlit"):
        graficos_streamlit = {
            "url_anos": f"http://localhost:{Config.PORTA_STREAMLIT_ANOS}",
            "url_estado": f"http://localhost:{Config.PORTA_STREAMLIT_ESTADO}",
        }

    return render_template(
        "opcao.html", dados=dados, graficos_streamlit=graficos_streamlit
    )
