import streamlit as st
import pandas as pd
import altair as alt
import json
import os
 
# --- Adaptação para VS Code: em vez do caminho fixo do Colab (/content/...),
# os JSON são lidos da pasta data/ do projeto. O restante é idêntico ao notebook,
# exceto o título/legenda/subtítulo, que já aparecem na página do Flask (opcao.html),
# e as cores, ajustadas para a paleta do site.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
 
st.set_page_config(page_title="Ocorrências e óbitos por estado - Humanos x PNH", page_icon="🗺️", layout="wide")
 
# --- Ajuste de largura: no modo embed (iframe do Flask) o Streamlit ignora o layout="wide"
# e limita o conteúdo a 736px. Este CSS libera a largura total do iframe.
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
 
regioes = {
    "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro-Oeste": ["DF", "GO", "MT", "MS"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"],
}
uf_para_regiao = {uf: regiao for regiao, ufs in regioes.items() for uf in ufs}
 
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
df_comparativo_uf["Regiao"] = df_comparativo_uf["Estado"].map(uf_para_regiao)
 
regiao_sel = st.selectbox(
    "Selecione a macrorregião:",
    ["Todas"] + list(regioes.keys())
)
 
def fmt(n):
    return f"{int(n):,}".replace(",", ".")
 
# os totais só aparecem quando uma macrorregião é selecionada
if regiao_sel != "Todas":
    df_regiao = df_comparativo_uf[df_comparativo_uf["Regiao"] == regiao_sel]
 
    st.markdown(f"**Totais da região {regiao_sel}**")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Casos humanos (total)", fmt(df_regiao["Casos Humanos"].sum()))
    c2.metric("Casos humanos sem óbitos", fmt(df_regiao["Casos Sem Óbito"].sum()))
    c3.metric("Casos humanos com óbitos", fmt(df_regiao["Óbitos Humanos"].sum()))
    c4.metric("Epizootias em PNH", fmt(df_regiao["Epizootias em PNH"].sum()))
 
# barra p/ casos humanos: fatia sem óbitos + fatia com óbitos (empilhadas)
df_casos_empilhado = pd.concat([
    df_comparativo_uf[["Estado", "Casos Sem Óbito"]].rename(columns={"Casos Sem Óbito": "Valor"}).assign(Categoria="Casos humanos sem óbitos", Grupo="Casos Humanos"),
    df_comparativo_uf[["Estado", "Óbitos Humanos"]].rename(columns={"Óbitos Humanos": "Valor"}).assign(Categoria="Casos humanos com óbitos", Grupo="Casos Humanos"),
], ignore_index=True)
 
# barra p/ epizootias
df_epi_barra = df_comparativo_uf[["Estado", "Epizootias em PNH"]].rename(columns={"Epizootias em PNH": "Valor"}).assign(Categoria="Epizootias em PNH", Grupo="Epizootias em PNH")
 
df_barras_final = pd.concat([df_casos_empilhado, df_epi_barra], ignore_index=True)
df_barras_final["Regiao"] = df_barras_final["Estado"].map(uf_para_regiao)
 
cores_categorias = alt.Scale(
    domain=["Casos humanos sem óbitos", "Casos humanos com óbitos", "Epizootias em PNH"],
    range=["#1c1a4a", "#F74245", "#f5a623"]
)
 
ordem_pilha = alt.Order("Categoria:N", sort="ascending")
 
if regiao_sel != "Todas":
    opacidade = alt.condition(alt.datum.Regiao == regiao_sel, alt.value(1.0), alt.value(0.2))
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
    tooltip=["Estado", "Regiao", "Categoria", "Valor"]
).properties(height=450)
 
st.altair_chart(grafico, use_container_width=True)