import streamlit as st
import pandas as pd
import altair as alt
import json
import os
 
# --- Adaptação para VS Code: em vez do caminho fixo do Colab (/content/...),
# os JSON são lidos da pasta data/ do projeto. O restante é idêntico ao notebook.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
 
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
 
regioes = {
    "Sul": ["RS", "SC", "PR"],
    "Sudeste": ["SP", "RJ", "MG", "ES"],
    "Centro-Oeste": ["MS", "MT", "GO", "DF"],
    "Nordeste": ["BA", "SE", "AL", "PE", "PB", "RN", "CE", "PI", "MA"],
    "Norte": ["TO", "PA", "AP", "AM", "RR", "RO", "AC"],
}
uf_para_regiao = {uf: regiao for regiao, ufs in regioes.items() for uf in ufs}
 
ufs_ordenadas = [uf for ufs in regioes.values() for uf in ufs]
 
contagem_humanos_uf = df_humanos["UF_LPI"].value_counts().reindex(ufs_ordenadas, fill_value=0)
contagem_epizootias_uf = df_epizootias["UF_OCOR"].value_counts().reindex(ufs_ordenadas, fill_value=0)
contagem_obitos_uf = df_humanos[df_humanos["OBITO"] == "SIM"]["UF_LPI"].value_counts().reindex(ufs_ordenadas, fill_value=0)
 
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
 
if regiao_sel == "Todas":
    df_totais = df_comparativo_uf
    titulo_totais = "Totais gerais (Brasil)"
else:
    df_totais = df_comparativo_uf[df_comparativo_uf["Regiao"] == regiao_sel]
    titulo_totais = f"Totais da região {regiao_sel}"
 
st.markdown(f"**{titulo_totais}**")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Casos humanos (total)", fmt(df_totais["Casos Humanos"].sum()))
c2.metric("Casos humanos sem óbitos", fmt(df_totais["Casos Sem Óbito"].sum()))
c3.metric("Casos humanos com óbitos", fmt(df_totais["Óbitos Humanos"].sum()))
c4.metric("Epizootias em PNH", fmt(df_totais["Epizootias em PNH"].sum()))
 
 
# Filtra os estados exibidos: só os da região escolhida (ou todos)
if regiao_sel == "Todas":
    df_plot = df_comparativo_uf
    ufs_plot = ufs_ordenadas
else:
    df_plot = df_comparativo_uf[df_comparativo_uf["Regiao"] == regiao_sel]
    ufs_plot = regioes[regiao_sel]
 
df_casos_empilhado = pd.concat([
    df_plot[["Estado", "Casos Sem Óbito"]].rename(columns={"Casos Sem Óbito": "Valor"}).assign(Categoria="Casos humanos sem óbitos", Grupo="Casos Humanos"),
    df_plot[["Estado", "Óbitos Humanos"]].rename(columns={"Óbitos Humanos": "Valor"}).assign(Categoria="Casos humanos com óbitos", Grupo="Casos Humanos"),
], ignore_index=True)
 
# barra p/ epizootias
df_epi_barra = df_plot[["Estado", "Epizootias em PNH"]].rename(columns={"Epizootias em PNH": "Valor"}).assign(Categoria="Epizootias em PNH", Grupo="Epizootias em PNH")
 
df_barras_final = pd.concat([df_casos_empilhado, df_epi_barra], ignore_index=True)
df_barras_final["Regiao"] = df_barras_final["Estado"].map(uf_para_regiao)
 
cores_categorias = alt.Scale(
    domain=["Casos humanos sem óbitos", "Casos humanos com óbitos", "Epizootias em PNH"],
    range=["#1c1a4a", "#F74245", "#f5a623"]
)
 
ordem_pilha = alt.Order("Categoria:N", sort="ascending")
 
maximo_pilha = (df_plot["Casos Humanos"]).max() #aqui define a maior escala de acordo c os casos na regiao escolhida
maximo_epi = df_plot["Epizootias em PNH"].max()
maximo = max(maximo_pilha, maximo_epi, 1)
 
topo = int(((maximo * 1.05) // 100 + 1) * 100) #p/ escala adaptativa em cada regiao ou de valores mt baixos
 
grafico = alt.Chart(df_barras_final).mark_bar().encode(
    x=alt.X("Estado:N", sort=ufs_plot, title="Estado",
            scale=alt.Scale(paddingInner=0.4, paddingOuter=0.2)),
    xOffset=alt.XOffset("Grupo:N", scale=alt.Scale(paddingInner=0.2)),
    y=alt.Y("Valor:Q", title="Número de casos", stack="zero",
            scale=alt.Scale(domain=[0, topo])),
    color=alt.Color("Categoria:N", scale=cores_categorias, legend=alt.Legend(title="Legenda")),
    order=ordem_pilha,
    tooltip=["Estado", "Regiao", "Categoria", "Valor"]
).properties(height=450)
 
st.altair_chart(grafico, use_container_width=True)