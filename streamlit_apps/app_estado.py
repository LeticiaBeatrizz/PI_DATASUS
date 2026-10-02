import streamlit as st
import pandas as pd
import altair as alt
import json
import os
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
 
st.markdown("""
    <style>
        .block-container { max-width: 100% !important; padding-left: 1.5rem; padding-right: 1.5rem; }
    </style>
""", unsafe_allow_html=True)
 
 
with open(os.path.join(DATA_DIR, "fa_casoshumanos_1994-2026.json"), "r", encoding="utf-8") as arquivo:
    dados_humanos = json.load(arquivo)
 
with open(os.path.join(DATA_DIR, "fa_epizpnh_1994-2026.json"), "r", encoding="utf-8") as arquivo:
    dados_epizootias = json.load(arquivo)
 
df_humanos = pd.DataFrame(dados_humanos["data"])
df_epizootias = pd.DataFrame(dados_epizootias["data"])
 
ufs_disponiveis = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]
 
uf = st.selectbox(
    "Selecione a UF:",
    ["Todas"] + list(ufs_disponiveis)
)
 
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
df_comparativo_uf["Casos Sem Óbito"] = df_comparativo_uf["Casos Humanos"] - df_comparativo_uf["Óbitos Humanos"]
 
# barra p/ "Casos Humanos": ocorrências + óbitos)
df_casos_empilhado = pd.concat([
    df_comparativo_uf[["Estado", "Casos Sem Óbito"]].rename(columns={"Casos Sem Óbito": "Valor"}).assign(Categoria="Casos humanos", Grupo="Casos Humanos"),
    df_comparativo_uf[["Estado", "Óbitos Humanos"]].rename(columns={"Óbitos Humanos": "Valor"}).assign(Categoria="Óbitos humanos", Grupo="Casos Humanos"),
], ignore_index=True)
 
 
df_epi_barra = df_comparativo_uf[["Estado", "Epizootias em PNH"]].rename(columns={"Epizootias em PNH": "Valor"}).assign(Categoria="Epizootias em PNH", Grupo="Epizootias em PNH")
 
df_barras_final = pd.concat([df_casos_empilhado, df_epi_barra], ignore_index=True)
 
cores_categorias = alt.Scale(
    domain=["Casos humanos", "Óbitos humanos", "Epizootias em PNH"],
    range=["#1c1a4a", "#F74245", "#f5a623"]
)
 
ordem_pilha = alt.Order("Categoria:N", sort="descending")
 
if uf != "Todas":
    opacidade = alt.condition(alt.datum.Estado == uf, alt.value(1.0), alt.value(0.2))
else:
    opacidade = alt.value(1.0)
 
grafico = alt.Chart(df_barras_final).mark_bar().encode(
    x=alt.X("Estado:N", sort=ufs_disponiveis, title="Estado",
            scale=alt.Scale(paddingInner=0.4, paddingOuter=0.2)),
    xOffset=alt.XOffset("Grupo:N", scale=alt.Scale(paddingInner=0.2)),
    y=alt.Y("Valor:Q", title="Número de casos", stack="zero"),
    color=alt.Color("Categoria:N", scale=cores_categorias, legend=alt.Legend(title="Legenda")),
    order=ordem_pilha,
    opacity=opacidade,
    tooltip=["Estado", "Categoria", "Valor"]
).properties(height=450)
 
st.altair_chart(grafico, use_container_width=True)