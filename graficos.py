"""
Cruzamento de dados: Casos Humanos x Epizootias em Primatas Não-Humanos.

Todo o carregamento dos dados, contagem/filtragem com pandas e a geração das
imagens dos gráficos com matplotlib ficam isolados aqui, separados das rotas
do Flask (app.py).
"""

import base64
import io
import json
import os

import matplotlib

matplotlib.use("Agg")  # renderiza sem precisar de tela (necessário no servidor)
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

CORES = {
    "humanos": "#f5a623",  # laranja do projeto
    "epizootias": "#14123a",  # navy do projeto
}


def carregar_registros(nome_arquivo):
    """Lê um arquivo .json em data/ (formato {"data": [...]}) e devolve a lista de registros."""
    caminho = os.path.join(DATA_DIR, nome_arquivo)
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)["data"]


# ---------------------------------------------------------------------------
# Carregamento e preparação dos dados (equivalente ao notebook original)
# ---------------------------------------------------------------------------
_REGISTROS_HUMANOS = carregar_registros("fa_casoshumanos_1994-2026.json")
_REGISTROS_EPIZOOTIAS = carregar_registros("fa_epizpnh_1994-2026.json")

df_humanos = pd.DataFrame(_REGISTROS_HUMANOS)
df_epizootias = pd.DataFrame(_REGISTROS_EPIZOOTIAS)

# filtrando os valores de anos p/ contabilizar apenas entradas do tipo numérico
df_humanos["ANO_IS"] = pd.to_numeric(df_humanos["ANO_IS"], errors="coerce")
df_epizootias["ANO_OCOR"] = pd.to_numeric(df_epizootias["ANO_OCOR"], errors="coerce")

# descarta registros sem ano/UF definidos
df_humanos = df_humanos.dropna(subset=["ANO_IS", "UF_LPI"])
df_epizootias = df_epizootias.dropna(subset=["ANO_OCOR", "UF_OCOR"])

# ANO_IS/ANO_OCOR vinham como float64 (por causa do coerce lá em cima);
# sem esse cast pro eixo do gráfico saía "1994.0" em vez de "1994"
df_humanos["ANO_IS"] = df_humanos["ANO_IS"].astype(int)
df_epizootias["ANO_OCOR"] = df_epizootias["ANO_OCOR"].astype(int)

df_humanos["UF_LPI"] = df_humanos["UF_LPI"].str.upper()
df_epizootias["UF_OCOR"] = df_epizootias["UF_OCOR"].str.upper()


def gerar_grafico_barras(labels, valores, cor):
    """Desenha um gráfico de barras com matplotlib e devolve a imagem em base64."""
    labels = [str(l) for l in labels]
    fig, ax = plt.subplots(figsize=(5.2, 3.4), dpi=110)
    ax.bar(labels, valores, color=cor)
    ax.set_ylabel("Ocorrências")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.get_major_locator().set_params(integer=True)
    if len(labels) > 12:
        plt.setp(ax.get_xticklabels(), rotation=60, ha="right")
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", transparent=True)
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def montar_grafico_anual(ano_selecionado):
    """Gráfico 01: evolução anual — casos humanos x epizootias em PNH."""
    contagem_humanos = df_humanos["ANO_IS"].value_counts().sort_index()
    contagem_epizootias = df_epizootias["ANO_OCOR"].value_counts().sort_index()

    df_comparativo = pd.DataFrame(
        {"humanos": contagem_humanos, "epizootias": contagem_epizootias}
    ).fillna(0).astype(int)
    df_comparativo.index = df_comparativo.index.astype(int)  # garante rótulo "1994", não "1994.0"
    df_comparativo.index.name = "Ano"
    df_comparativo = df_comparativo.sort_index()

    anos_disponiveis = [int(a) for a in df_comparativo.index]

    if ano_selecionado != "Todos" and int(ano_selecionado) in df_comparativo.index:
        df_comparativo = df_comparativo.loc[[int(ano_selecionado)]]

    img_humanos = gerar_grafico_barras(df_comparativo.index, df_comparativo["humanos"], CORES["humanos"])
    img_epizootias = gerar_grafico_barras(df_comparativo.index, df_comparativo["epizootias"], CORES["epizootias"])

    return img_humanos, img_epizootias, anos_disponiveis


def montar_grafico_uf(ano_selecionado, uf_selecionada):
    """Gráfico 02: ocorrências por estado, com filtro de ano e UF."""
    anos_disponiveis = sorted(set(df_humanos["ANO_IS"]).union(df_epizootias["ANO_OCOR"]))
    ufs_disponiveis = sorted(set(df_humanos["UF_LPI"]).union(df_epizootias["UF_OCOR"]))

    df_hum_filtrado = df_humanos.copy()
    df_epi_filtrado = df_epizootias.copy()

    if ano_selecionado != "Todos":
        df_hum_filtrado = df_hum_filtrado[df_hum_filtrado["ANO_IS"] == int(ano_selecionado)]
        df_epi_filtrado = df_epi_filtrado[df_epi_filtrado["ANO_OCOR"] == int(ano_selecionado)]

    if uf_selecionada != "Todas":
        df_hum_filtrado = df_hum_filtrado[df_hum_filtrado["UF_LPI"] == uf_selecionada]
        df_epi_filtrado = df_epi_filtrado[df_epi_filtrado["UF_OCOR"] == uf_selecionada]

    # value_counts() já ordena da UF com mais ocorrências p/ a com menos,
    # igual ao comportamento padrão do pandas usado no notebook original
    ocorrencias_humanos = df_hum_filtrado["UF_LPI"].value_counts()
    ocorrencias_epizootias = df_epi_filtrado["UF_OCOR"].value_counts()

    img_humanos = gerar_grafico_barras(ocorrencias_humanos.index, ocorrencias_humanos.values, CORES["humanos"])
    img_epizootias = gerar_grafico_barras(
        ocorrencias_epizootias.index, ocorrencias_epizootias.values, CORES["epizootias"]
    )

    return (
        img_humanos,
        img_epizootias,
        len(df_hum_filtrado),
        len(df_epi_filtrado),
        anos_disponiveis,
        ufs_disponiveis,
    )
