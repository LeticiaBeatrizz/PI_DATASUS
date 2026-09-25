"""
App Streamlit: evolução anual — casos humanos x epizootias em PNH x óbitos humanos.

Adaptado do notebook ocorrencias_obitos_anos.ipynb. A única mudança em relação
ao notebook original é o caminho dos arquivos JSON: em vez do caminho fixo do
Google Colab (/content/...), os dados são lidos da pasta data/ do projeto.
"""

import json
import os

import altair as alt
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

st.set_page_config(page_title="Casos humanos x Epizootias em PNH", page_icon="📊", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

with open(os.path.join(DATA_DIR, "fa_casoshumanos_1994-2026.json"), "r", encoding="utf-8") as arquivo:
    dados_humanos = json.load(arquivo)

with open(os.path.join(DATA_DIR, "fa_epizpnh_1994-2026.json"), "r", encoding="utf-8") as arquivo:
    dados_epizootias = json.load(arquivo)

df_humanos = pd.DataFrame(dados_humanos["data"])
df_epizootias = pd.DataFrame(dados_epizootias["data"])

df_humanos["ANO_IS"] = pd.to_numeric(df_humanos["ANO_IS"], errors="coerce").astype("Int64")
df_epizootias["ANO_OCOR"] = pd.to_numeric(df_epizootias["ANO_OCOR"], errors="coerce").astype("Int64")

anos_humanos = df_humanos["ANO_IS"].dropna().unique()
anos_epizootias = df_epizootias["ANO_OCOR"].dropna().unique()
anos_disponiveis = sorted(set(int(a) for a in anos_humanos).union(set(int(a) for a in anos_epizootias)))

ano = st.selectbox(
    "Selecione o ano:",
    ["Todos"] + anos_disponiveis
)

""" -------------------------------------------------------------------
Gráfico - casos humanos x epizootias e óbitos em humanos
"""

contagem_humanos = df_humanos["ANO_IS"].value_counts().sort_index()
contagem_epizootias = df_epizootias["ANO_OCOR"].value_counts().sort_index()
contagem_obitos = df_humanos[df_humanos["OBITO"] == "SIM"]["ANO_IS"].value_counts().sort_index()

df_comparativo = pd.DataFrame({
    "Casos Humanos": contagem_humanos,
    "Epizootias em PNH": contagem_epizootias,
    "Óbitos Humanos": contagem_obitos
}).fillna(0).astype(int)

df_comparativo.index.name = "Ano"
df_comparativo = df_comparativo.sort_index().reset_index()
df_comparativo["Ano"] = df_comparativo["Ano"].astype(str)

cores_categorias = alt.Scale(
    domain=["Casos Humanos", "Epizootias em PNH"],
    range=["#1c1a4a", "#e2951a"]
)

df_barras = df_comparativo.melt(
    id_vars="Ano",
    value_vars=["Casos Humanos", "Epizootias em PNH"],
    var_name="Categoria",
    value_name="Valor"
)

if ano != "Todos":
    opacidade = alt.condition(alt.datum.Ano == str(ano), alt.value(1.0), alt.value(0.25))
else:
    opacidade = alt.value(1.0)

barras = alt.Chart(df_barras).mark_bar().encode(
    x=alt.X("Ano:O", title="Ano"),
    xOffset=alt.XOffset("Categoria:N"),
    y=alt.Y("Valor:Q", title="Número de casos"),
    color=alt.Color("Categoria:N", scale=cores_categorias, legend=alt.Legend(title="Legenda")),
    opacity=opacidade,
    tooltip=["Ano", "Categoria", "Valor"]
)

df_linha = df_comparativo[["Ano", "Óbitos Humanos"]].copy()

if ano != "Todos":
    opacidade_linha = alt.condition(alt.datum.Ano == str(ano), alt.value(1.0), alt.value(0.15))
else:
    opacidade_linha = alt.value(1.0)

if ano != "Todos":
    opacidade_ponto = alt.condition(alt.datum.Ano == str(ano), alt.value(1.0), alt.value(0.3))
    tamanho_ponto = alt.condition(alt.datum.Ano == str(ano), alt.value(120), alt.value(30))
else:
    opacidade_ponto = alt.value(1.0)
    tamanho_ponto = alt.value(30)

linha = alt.Chart(df_linha).mark_line(strokeWidth=2.5, color="#E34948").encode(
    x=alt.X("Ano:O"),
    y=alt.Y("Óbitos Humanos:Q", title="Óbitos humanos"),
    opacity=opacidade_linha,
    tooltip=["Ano", "Óbitos Humanos"]
)

pontos = alt.Chart(df_linha).mark_point(filled=True, color="#F65C5C").encode(
    x=alt.X("Ano:O"),
    y=alt.Y("Óbitos Humanos:Q"),
    opacity=opacidade_ponto,
    size=tamanho_ponto,
    tooltip=["Ano", "Óbitos Humanos"]
)

grafico_combinado = alt.layer(barras, linha, pontos).resolve_scale(
    y="independent"
).properties(height=420)

st.altair_chart(grafico_combinado, use_container_width=True)
