import streamlit as st
import pandas as pd
import altair as alt
import json
import numpy as np
import os
 
# --- Adaptação para VS Code: em vez do caminho fixo do Colab (/content/...),
# os JSON são lidos da pasta data/ do projeto. O restante é idêntico ao notebook,
# exceto o título/legenda/subtítulo, que já aparecem na página do Flask (opcao.html),
# e as cores, ajustadas para a paleta do site.
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
 
regioes = {
    "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro-Oeste": ["DF", "GO", "MT", "MS"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"],
}
 
regiao_sel = st.selectbox(
    "Selecione a macrorregião:",
    ["Todas"] + list(regioes.keys())
)
 
if regiao_sel != "Todas":
    df_humanos_f = df_humanos[df_humanos["UF_LPI"].isin(regioes[regiao_sel])]
    df_epizootias_f = df_epizootias[df_epizootias["UF_OCOR"].isin(regioes[regiao_sel])]
else:
    df_humanos_f = df_humanos
    df_epizootias_f = df_epizootias
 
def fmt(n):
    return f"{int(n):,}".replace(",", ".")
 
# os totais só aparecem quando uma macrorregião é selecionada
if regiao_sel != "Todas":
    total_casos = len(df_humanos_f)
    total_obitos = int((df_humanos_f["OBITO"] == "SIM").sum())
 
    st.markdown(f"**Totais da região {regiao_sel}**")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Casos humanos (total)", fmt(total_casos))
    c2.metric("Casos humanos sem óbitos", fmt(total_casos - total_obitos))
    c3.metric("Casos humanos com óbitos", fmt(total_obitos))
    c4.metric("Epizootias em PNH", fmt(len(df_epizootias_f)))
 
# Gráfico
 
contagem_humanos = df_humanos_f["ANO_IS"].value_counts().reindex(anos_disponiveis, fill_value=0)
contagem_epizootias = df_epizootias_f["ANO_OCOR"].value_counts().reindex(anos_disponiveis, fill_value=0)
contagem_obitos = df_humanos_f[df_humanos_f["OBITO"] == "SIM"]["ANO_IS"].value_counts().reindex(anos_disponiveis, fill_value=0)
 
df_comparativo = pd.DataFrame({
    "Casos Humanos": contagem_humanos,
    "Epizootias em PNH": contagem_epizootias,
    "Óbitos Humanos": contagem_obitos
}).astype(int)
 
df_comparativo.index.name = "Ano"
df_comparativo = df_comparativo.sort_index().reset_index()
df_comparativo["Ano"] = df_comparativo["Ano"].astype(str)
 
todas_categorias = ["Casos Humanos", "Epizootias em PNH", "Óbitos Humanos"]
 
cores_categorias = alt.Scale(
    domain=todas_categorias,
    range=["#1c1a4a", "#f5a623", "#F74245"]
)
 
def monta_serie(nome_coluna, nome_categoria):
    """mantém todos os anos e troca o valor 0 por NaN,
    o que cria o 'buraco' na linha nos anos sem registro"""
    df_serie = df_comparativo[["Ano", nome_coluna]].copy()
    df_serie[nome_coluna] = df_serie[nome_coluna].astype(float)
    df_serie.loc[df_serie[nome_coluna] == 0, nome_coluna] = np.nan
    df_serie = df_serie.rename(columns={nome_coluna: "Valor"})
    df_serie["Categoria"] = nome_categoria
    return df_serie
 
df_linhas = pd.concat(
    [monta_serie(c, c) for c in todas_categorias],
    ignore_index=True
)
 
escala_ano = alt.Scale(domain=anos_disponiveis_str)
escala_y_fixa = alt.Scale(domain=[0, 1400])
 
grafico = alt.Chart(df_linhas).mark_line(
    strokeWidth=2.5, point=alt.OverlayMarkDef(filled=True, size=45), interpolate="monotone"
).encode(
    x=alt.X("Ano:O", title="Ano", sort=anos_disponiveis_str, scale=escala_ano),
    y=alt.Y("Valor:Q", title="Número de casos / óbitos", scale=escala_y_fixa),
    order=alt.Order("Ano:N", sort="ascending"),
    color=alt.Color("Categoria:N", scale=cores_categorias, legend=alt.Legend(title="Legenda")),
    tooltip=["Ano", "Categoria", "Valor"]
).properties(height=420)
 
st.altair_chart(grafico, use_container_width=True)