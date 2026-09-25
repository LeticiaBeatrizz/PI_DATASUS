import atexit
import os
import subprocess
import sys

import markdown
from flask import Flask, abort, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
STREAMLIT_APPS_DIR = os.path.join(BASE_DIR, "streamlit_apps")

# Portas onde os apps Streamlit ficam disponíveis. São embutidos na página
# de "Definição da Base de Dados" via <iframe> (ver templates/opcao.html).
PORTA_STREAMLIT_ANOS = 8501
PORTA_STREAMLIT_ESTADO = 8502

_processos_streamlit = []


def carregar_markdown(nome_arquivo):
    """Lê um arquivo .md em content/ e devolve o HTML já renderizado."""
    caminho = os.path.join(CONTENT_DIR, nome_arquivo)
    with open(caminho, "r", encoding="utf-8") as arquivo:
        texto_md = arquivo.read()
    return markdown.markdown(texto_md, extensions=["tables", "extra"])


def iniciar_apps_streamlit():
    """Sobe os dois apps Streamlit (evolução anual e por estado) em segundo
    plano, cada um na sua porta, para serem exibidos via <iframe>.

    --server.enableCORS false e --server.enableXsrfProtection false são
    necessários porque, por padrão, o Streamlit bloqueia ser exibido dentro
    de um <iframe> de outra origem (nesse caso, a página servida pelo Flask).
    """
    apps = [
        ("app_anos.py", PORTA_STREAMLIT_ANOS),
        ("app_estado.py", PORTA_STREAMLIT_ESTADO),
    ]

    for nome_arquivo, porta in apps:
        caminho_app = os.path.join(STREAMLIT_APPS_DIR, nome_arquivo)
        processo = subprocess.Popen(
            [
                sys.executable, "-m", "streamlit", "run", caminho_app,
                "--server.port", str(porta),
                "--server.headless", "true",
                "--server.enableCORS", "false",
                "--server.enableXsrfProtection", "false",
                "--browser.gatherUsageStats", "false",
            ]
        )
        _processos_streamlit.append(processo)


def encerrar_apps_streamlit():
    for processo in _processos_streamlit:
        processo.terminate()


ESTUDO_TEORICO_HTML = carregar_markdown("estudo_teorico.md")
DEFINICAO_BASE_DADOS_HTML = carregar_markdown("def_dados.md")
DEFINICAO_BASE_DADOS_REFERENCIAS_HTML = carregar_markdown("def_dados_ref.md")
DEFINICAO_BASE_DADOS_G1_HTML = carregar_markdown("def_dados_g1.md")
DEFINICAO_BASE_DADOS_G2_HTML = carregar_markdown("def_dados_g2.md")

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
        "referencias": DEFINICAO_BASE_DADOS_REFERENCIAS_HTML,
        "graficos_streamlit": True,
    },
    3: {"titulo": "Sobre", "subtitulo": "Febre Amarela", "texto": "..."},
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
            "url_anos": f"http://localhost:{PORTA_STREAMLIT_ANOS}",
            "url_estado": f"http://localhost:{PORTA_STREAMLIT_ESTADO}",
        }

    return render_template(
        "opcao.html", numero=num, dados=dados, graficos_streamlit=graficos_streamlit
    )


@app.route("/destaque")
def destaque():
    return render_template(
        "opcao.html",
        numero=None,
        dados={"titulo": "Destaque", "texto": "Conteúdo em destaque"},
    )


if __name__ == "__main__":
    # evita subir os apps Streamlit duas vezes por causa do reloader do Flask
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        iniciar_apps_streamlit()
        atexit.register(encerrar_apps_streamlit)

    app.run(debug=True)
