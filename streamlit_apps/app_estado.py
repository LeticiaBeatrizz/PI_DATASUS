"""
App Streamlit: ocorrências por estado — casos humanos x epizootias em PNH x óbitos humanos.

Adaptado do notebook ocorrencias_obitos_estados.ipynb. Única mudança em relação
ao notebook original: caminho dos arquivos JSON lido da pasta data/ do
projeto, em vez do caminho fixo do Google Colab (/content/...).
"""

import json
import os

import altair as alt
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

st.set_page_config(page_title="Ocorrências e óbitos por estado - Humanos x PNH", page_icon="🗺️", layout="wide")

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

ufs_humanos = df_humanos["UF_LPI"].dropna().unique()
ufs_epizootias = df_epizootias["UF_OCOR"].dropna().unique()
ufs_disponiveis = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

uf = st.selectbox(
    "Selecione a UF:",
    ["Todas"] + list(ufs_disponiveis)
)

""" -------------------------------------------------------------------
Gráfico: casos humanos, epizootias em PNH e óbitos humanos, por estado
"""

contagem_humanos_uf = df_humanos["UF_LPI"].value_counts().reindex(ufs_disponiveis, fill_value=0)
contagem_epizootias_uf = df_epizootias["UF_OCOR"].value_counts().reindex(ufs_disponiveis, fill_value=0)
contagem_obitos_uf = df_humanos[df_humanos["OBITO"] == "SIM"]["UF_LPI"].value_counts().reindex(ufs_disponiveis, fill_value=0)

df_comparativo_uf = pd.DataFrame({
    "Casos Humanos": contagem_humanos_uf,
    "Epizootias em PNH": contagem_epizootias_uf,
    "Óbitos Humanos": contagem_obitos_uf
}).astype(int)

df_comparativo_uf.index.name = "Estado"
df_comparativo_uf = df_comparativo_uf.reset_index()

df_linhas_uf = df_comparativo_uf.melt(
    id_vars="Estado",
    value_vars=["Casos Humanos", "Epizootias em PNH", "Óbitos Humanos"],
    var_name="Categoria",
    value_name="Valor"
)

cores_categorias = alt.Scale(
    domain=["Casos Humanos", "Epizootias em PNH", "Óbitos Humanos"],
    range=["#1c1a4a", "#e2951a", "#F65C5C"]
)

if uf != "Todas":
    opacidade = alt.condition(alt.datum.Estado == uf, alt.value(1.0), alt.value(0.2))
else:
    opacidade = alt.value(1.0)

grafico = alt.Chart(df_linhas_uf).mark_line(
    strokeWidth=2.5,
    point=alt.OverlayMarkDef(filled=True, size=45),
    interpolate="monotone"
).encode(
    x=alt.X("Estado:N", sort=ufs_disponiveis, title="Estado"),
    y=alt.Y("Valor:Q", title="Número de casos / óbitos"),
    color=alt.Color("Categoria:N", scale=cores_categorias, legend=alt.Legend(title="Legenda")),
    opacity=opacidade,
    tooltip=["Estado", "Categoria", "Valor"]
).properties(height=450)

st.altair_chart(grafico, use_container_width=True)
