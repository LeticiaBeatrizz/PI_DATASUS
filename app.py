import os

import markdown
from flask import Flask, abort, jsonify, render_template, request

from graficos import montar_grafico_anual, montar_grafico_uf

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")


def carregar_markdown(nome_arquivo):
    """Lê um arquivo .md em content/ e devolve o HTML já renderizado."""
    caminho = os.path.join(CONTENT_DIR, nome_arquivo)
    with open(caminho, "r", encoding="utf-8") as arquivo:
        texto_md = arquivo.read()
    return markdown.markdown(texto_md, extensions=["tables", "extra"])


ESTUDO_TEORICO_HTML = carregar_markdown("estudo_teorico.md")
DEFINICAO_BASE_DADOS_HTML = carregar_markdown("definicao_base_dados.md")

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
        "graficos": True,
    },
    3: {"titulo": "Distribuição geográfica", "subtitulo": "Febre Amarela", "texto": "..."},
}


@app.route('/')
def home():
    return render_template("index.html", dados={"subtitulo": "Febre Amarela"})


@app.route("/opcao/<int:num>")
def opcao(num):
    dados = OPCOES.get(num)
    if not dados:
        abort(404)

    graficos = None
    if dados.get("graficos"):
        # renderização inicial da página sempre com "Todos"/"Todas";
        # as trocas de filtro depois disso são feitas via JS (fetch),
        # sem recarregar a página — ver /api/grafico-anual e /api/grafico-uf
        img_hum_anual, img_epi_anual, anos_disponiveis = montar_grafico_anual("Todos")
        (
            img_hum_uf,
            img_epi_uf,
            total_humanos,
            total_epizootias,
            anos_disponiveis_g2,
            ufs_disponiveis,
        ) = montar_grafico_uf("Todos", "Todas")

        graficos = {
            "anos_disponiveis": anos_disponiveis,
            "anos_disponiveis_g2": anos_disponiveis_g2,
            "ufs_disponiveis": ufs_disponiveis,
            "img_hum_anual": img_hum_anual,
            "img_epi_anual": img_epi_anual,
            "img_hum_uf": img_hum_uf,
            "img_epi_uf": img_epi_uf,
            "total_humanos": total_humanos,
            "total_epizootias": total_epizootias,
        }

    return render_template("opcao.html", numero=num, dados=dados, graficos=graficos)


@app.route("/api/grafico-anual")
def api_grafico_anual():
    """Usado pelo graficos.js: recebe ?ano=... e devolve as imagens já filtradas."""
    ano = request.args.get("ano", "Todos")
    img_humanos, img_epizootias, anos_disponiveis = montar_grafico_anual(ano)
    return jsonify({
        "img_humanos": img_humanos,
        "img_epizootias": img_epizootias,
        "anos_disponiveis": anos_disponiveis,
    })


@app.route("/api/grafico-uf")
def api_grafico_uf():
    """Usado pelo graficos.js: recebe ?ano=...&uf=... e devolve as imagens já filtradas."""
    ano = request.args.get("ano", "Todos")
    uf = request.args.get("uf", "Todas")
    (
        img_humanos,
        img_epizootias,
        total_humanos,
        total_epizootias,
        anos_disponiveis,
        ufs_disponiveis,
    ) = montar_grafico_uf(ano, uf)
    return jsonify({
        "img_humanos": img_humanos,
        "img_epizootias": img_epizootias,
        "total_humanos": total_humanos,
        "total_epizootias": total_epizootias,
        "anos_disponiveis": anos_disponiveis,
        "ufs_disponiveis": ufs_disponiveis,
    })


@app.route("/destaque")
def destaque():
    return render_template(
        "opcao.html",
        numero=None,
        dados={"titulo": "Destaque", "texto": "Conteúdo em destaque"},
    )


if __name__ == "__main__":
    app.run(debug=True)
