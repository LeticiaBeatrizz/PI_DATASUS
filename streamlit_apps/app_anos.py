import streamlit as st
import pandas as pd
import altair as alt
import json
import numpy as np
import os
 
# --- Adaptação para VS Code: em vez do caminho fixo do Colab (/content/...),
# os JSON são lidos da pasta data/ do projeto. O restante é idêntico ao notebook.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
 
st.set_page_config(page_title="Casos humanos x Epizootias em PNH", page_icon="📊", layout="wide")
 
 
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
 
df_humanos["ANO_IS"] = pd.to_numeric(df_humanos["ANO_IS"], errors="coerce").astype("Int64")
df_epizootias["ANO_OCOR"] = pd.to_numeric(df_epizootias["ANO_OCOR"], errors="coerce").astype("Int64")
 
anos_humanos = df_humanos["ANO_IS"].dropna().unique()
anos_epizootias = df_epizootias["ANO_OCOR"].dropna().unique()
anos_com_dados = sorted(set(int(a) for a in anos_humanos).union(set(int(a) for a in anos_epizootias)))
 
anos_disponiveis = list(range(min(anos_com_dados), max(anos_com_dados) + 1))
anos_disponiveis_str = [str(a) for a in anos_disponiveis]
 
ano = st.selectbox(
    "Selecione o ano:",
    ["Todos"] + anos_disponiveis
)
 
todas_categorias = ["Casos Humanos", "Epizootias em PNH", "Óbitos Humanos"]
 
if "chk_Todos" not in st.session_state:
    st.session_state["chk_Todos"] = True
    for categoria in todas_categorias:
        st.session_state[f"chk_{categoria}"] = True
 
def ao_mudar_todos():
    valor = st.session_state["chk_Todos"]
    for categoria in todas_categorias:
        st.session_state[f"chk_{categoria}"] = valor
 
def ao_mudar_categoria():
    todas_marcadas = all(st.session_state[f"chk_{c}"] for c in todas_categorias)
    st.session_state["chk_Todos"] = todas_marcadas
 
with st.expander("Selecione a(s) categoria(s)", expanded=False):
    st.checkbox("Todos", key="chk_Todos", on_change=ao_mudar_todos)
    for categoria in todas_categorias:
        st.checkbox(categoria, key=f"chk_{categoria}", on_change=ao_mudar_categoria)
 
categorias_selecionadas = [c for c in todas_categorias if st.session_state[f"chk_{c}"]]
 
if not categorias_selecionadas:
    st.caption("Nenhuma categoria foi selecionada, o gráfico está vazio.")
 
 
contagem_humanos = df_humanos["ANO_IS"].value_counts().reindex(anos_disponiveis, fill_value=0)
contagem_epizootias = df_epizootias["ANO_OCOR"].value_counts().reindex(anos_disponiveis, fill_value=0)
contagem_obitos = df_humanos[df_humanos["OBITO"] == "SIM"]["ANO_IS"].value_counts().reindex(anos_disponiveis, fill_value=0)
 
df_comparativo = pd.DataFrame({
    "Casos Humanos": contagem_humanos,
    "Epizootias em PNH": contagem_epizootias,
    "Óbitos Humanos": contagem_obitos
}).astype(int)
 
df_comparativo.index.name = "Ano"
df_comparativo = df_comparativo.sort_index().reset_index()
df_comparativo["Ano"] = df_comparativo["Ano"].astype(str)
 
cores_categorias = alt.Scale(
    domain=todas_categorias,
    range=["#1c1a4a", "#f5a623", "#F74245"]
)
 
def monta_serie(nome_coluna, nome_categoria):
    """vai mostrar todos os anos na parte de anos disponíveis,
    transformando o valor 0, caso exista, em NaN. Ou seja, não vai mostrar nenhuma linha no gráfico """
    df_serie = df_comparativo[["Ano", nome_coluna]].copy()
    df_serie[nome_coluna] = df_serie[nome_coluna].astype(float)
    df_serie.loc[df_serie[nome_coluna] == 0, nome_coluna] = np.nan
    df_serie = df_serie.rename(columns={nome_coluna: "Valor"})
    df_serie["Categoria"] = nome_categoria
    return df_serie
 
df_casos = monta_serie("Casos Humanos", "Casos Humanos")
df_epi = monta_serie("Epizootias em PNH", "Epizootias em PNH")
df_obitos_bruto = monta_serie("Óbitos Humanos", "Óbitos Humanos")
 
df_casos = df_casos if "Casos Humanos" in categorias_selecionadas else df_casos.iloc[0:0]
df_epi = df_epi if "Epizootias em PNH" in categorias_selecionadas else df_epi.iloc[0:0]
df_obitos_bruto = df_obitos_bruto if "Óbitos Humanos" in categorias_selecionadas else df_obitos_bruto.iloc[0:0]
 
df_linhas_principais = pd.concat([df_casos, df_epi], ignore_index=True)
 
if ano != "Todos":
    opacidade = alt.condition(alt.datum.Ano == str(ano), alt.value(1.0), alt.value(0.25))
    opacidade_obitos = alt.condition(alt.datum.Ano == str(ano), alt.value(1.0), alt.value(0.3))
    tamanho_ponto_obitos = alt.condition(alt.datum.Ano == str(ano), alt.value(120), alt.value(30))
else:
    opacidade = alt.value(1.0)
    opacidade_obitos = alt.value(1.0)
    tamanho_ponto_obitos = alt.value(30)
 
escala_ano = alt.Scale(domain=anos_disponiveis_str)
escala_y_fixa = alt.Scale(domain=[0, 1400])
 
linhas_principais = alt.Chart(df_linhas_principais).mark_line(
    strokeWidth=2.5, point=alt.OverlayMarkDef(filled=True, size=45), interpolate="monotone"
).encode(
    x=alt.X("Ano:O", title="Ano", sort=anos_disponiveis_str, scale=escala_ano),
    y=alt.Y("Valor:Q", title="Número de casos / óbitos", scale=escala_y_fixa),
    order=alt.Order("Ano:N", sort="ascending"),
    color=alt.Color("Categoria:N", scale=cores_categorias, legend=alt.Legend(title="Legenda")),
    opacity=opacidade,
    tooltip=["Ano", "Categoria", "Valor"]
)
 
linha_obitos = alt.Chart(df_obitos_bruto).mark_line(strokeWidth=2.5, interpolate="monotone").encode(
    x=alt.X("Ano:O", sort=anos_disponiveis_str, scale=escala_ano),
    y=alt.Y("Valor:Q", scale=escala_y_fixa),
    order=alt.Order("Ano:N", sort="ascending"),
    color=alt.Color("Categoria:N", scale=cores_categorias),
    opacity=opacidade_obitos,
    tooltip=["Ano", alt.Tooltip("Valor:Q", title="Óbitos Humanos")]
)
 
pontos_obitos = alt.Chart(df_obitos_bruto).mark_point(filled=True).encode(
    x=alt.X("Ano:O", sort=anos_disponiveis_str, scale=escala_ano),
    y=alt.Y("Valor:Q", scale=escala_y_fixa),
    color=alt.Color("Categoria:N", scale=cores_categorias),
    opacity=opacidade_obitos,
    size=tamanho_ponto_obitos,
    tooltip=["Ano", alt.Tooltip("Valor:Q", title="Óbitos Humanos")]
)
 
grafico_combinado = alt.layer(linhas_principais, linha_obitos, pontos_obitos).properties(height=420)
 
st.altair_chart(grafico_combinado, use_container_width=True)