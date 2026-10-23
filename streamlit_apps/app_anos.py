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
 
df_humanos["ANO_IS"] = pd.to_numeric(df_humanos["ANO_IS"], errors="coerce").astype("Int64")
df_epizootias["ANO_OCOR"] = pd.to_numeric(df_epizootias["ANO_OCOR"], errors="coerce").astype("Int64")
 
anos_humanos = df_humanos["ANO_IS"].dropna().unique()
anos_epizootias = df_epizootias["ANO_OCOR"].dropna().unique()
anos_com_dados = sorted(set(int(a) for a in anos_humanos).union(set(int(a) for a in anos_epizootias)))
 
anos_disponiveis = list(range(min(anos_com_dados), max(anos_com_dados) + 1))
 
regioes = {
    "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro-Oeste": ["DF", "GO", "MT", "MS"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"],
}
 
col_f1, col_f2 = st.columns(2)
 
with col_f1:
    regiao_sel = st.selectbox(
        "Selecione a macrorregião:",
        ["Todas"] + list(regioes.keys())
    )
 
with col_f2:
    ano_ini, ano_fim = st.select_slider(
        "Selecione o recorte temporal:",
        options=anos_disponiveis,
        value=(anos_disponiveis[0], anos_disponiveis[-1])
    )
 
anos_exibidos = list(range(ano_ini, ano_fim + 1))
anos_exibidos_str = [str(a) for a in anos_exibidos]
 
df_humanos_f = df_humanos[df_humanos["ANO_IS"].between(ano_ini, ano_fim).fillna(False)]
df_epizootias_f = df_epizootias[df_epizootias["ANO_OCOR"].between(ano_ini, ano_fim).fillna(False)]
 
if regiao_sel != "Todas":
    df_humanos_f = df_humanos_f[df_humanos_f["UF_LPI"].isin(regioes[regiao_sel])]
    df_epizootias_f = df_epizootias_f[df_epizootias_f["UF_OCOR"].isin(regioes[regiao_sel])]
 
def fmt(n):
    return f"{int(n):,}".replace(",", ".")
 
periodo_txt = f"{ano_ini}" if ano_ini == ano_fim else f"{ano_ini}–{ano_fim}"
if regiao_sel == "Todas":
    titulo_totais = f"Totais gerais (Brasil) — {periodo_txt}"
else:
    titulo_totais = f"Totais da região {regiao_sel} — {periodo_txt}"
 
total_casos = len(df_humanos_f)
total_obitos = int((df_humanos_f["OBITO"] == "SIM").sum())
 
st.markdown(f"**{titulo_totais}**")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Casos humanos (total)", fmt(total_casos))
c2.metric("Casos humanos sem óbitos", fmt(total_casos - total_obitos))
c3.metric("Casos humanos com óbitos", fmt(total_obitos))
c4.metric("Epizootias em PNH", fmt(len(df_epizootias_f)))
 

 
contagem_humanos = df_humanos_f["ANO_IS"].value_counts().reindex(anos_exibidos, fill_value=0)
contagem_epizootias = df_epizootias_f["ANO_OCOR"].value_counts().reindex(anos_exibidos, fill_value=0)
contagem_obitos = df_humanos_f[df_humanos_f["OBITO"] == "SIM"]["ANO_IS"].value_counts().reindex(anos_exibidos, fill_value=0)
 
df_comparativo = pd.DataFrame({
    "Casos Humanos": contagem_humanos,
    "Epizootias em PNH": contagem_epizootias,
    "Óbitos Humanos": contagem_obitos
}).astype(int)
 
df_comparativo.index.name = "Ano"
df_comparativo = df_comparativo.sort_index().reset_index()
df_comparativo["Ano"] = df_comparativo["Ano"].astype(str)
df_comparativo["Ano_num"] = pd.to_numeric(df_comparativo["Ano"])
 
todas_categorias = ["Casos Humanos", "Epizootias em PNH", "Óbitos Humanos"]
 
cores_categorias = alt.Scale(
    domain=todas_categorias + ["Sem registros"],
    range=["#1c1a4a", "#f5a623", "#F74245", "#8A8F98"]
)
 
def monta_serie(nome_coluna, nome_categoria):
    df_serie = df_comparativo[["Ano", "Ano_num", nome_coluna]].copy()
    df_serie[nome_coluna] = df_serie[nome_coluna].astype(float)
    df_serie.loc[df_serie[nome_coluna] == 0, nome_coluna] = np.nan
    df_serie = df_serie.rename(columns={nome_coluna: "Valor"})
    df_serie["Categoria"] = nome_categoria
    return df_serie
 
def monta_cinza(df, categorias):
    anos = df["Ano"].tolist()
    segmentos = {}
    anos_zero = set()
 
    for categoria in categorias:
        valores = df[categoria].fillna(0).astype(float).tolist()
 
        for i, v in enumerate(valores):
            if v == 0:
                anos_zero.add(anos[i])
 
        for i in range(len(anos) - 1):
            if valores[i] == 0 or valores[i + 1] == 0:
                segmentos[(anos[i], valores[i], anos[i + 1], valores[i + 1])] = None
 
    linhas = []
    for n, (a1, v1, a2, v2) in enumerate(segmentos):
        inicio = float(a1)
        fim = float(a2)
        diferenca = v2 - v1
        linhas.extend([
            (inicio, v1, n),
            (inicio + (fim - inicio) / 3, v1 + diferenca * (1 / 3) ** 2 * (3 - 2 / 3), n),
            (inicio + 2 * (fim - inicio) / 3, v1 + diferenca * (2 / 3) ** 2 * (3 - 4 / 3), n),
            (fim, v2, n),
        ])
 
    df_seg = pd.DataFrame(linhas, columns=["Ano_num", "Valor", "Segmento"])
    df_seg["Categoria"] = "Sem registros"
 
    df_pts = pd.DataFrame({"Ano": sorted(anos_zero), "Valor": 0.0})
    df_pts["Ano_num"] = pd.to_numeric(df_pts["Ano"])
    df_pts["Categoria"] = "Sem registros"
 
    return df_seg, df_pts
 
df_linhas = pd.concat(
    [monta_serie(c, c) for c in todas_categorias],
    ignore_index=True
)
 
df_cinza_seg, df_cinza_pts = monta_cinza(df_comparativo, todas_categorias)
 
maximo = max(int(df_comparativo[todas_categorias].max().max()), 1)
escala_y = alt.Scale(domain=[0, maximo * 1.1], nice=True)
 
escala_ano = alt.Scale(domain=[ano_ini, ano_fim], nice=False)
eixo_ano = alt.Axis(
    values=anos_exibidos, format="d", labelAngle=270, grid=False, domain=False
)
eixo_y = alt.Axis(grid=True, domain=True)
 
opacidade = 0.4
 
cinza_linhas = alt.Chart(df_cinza_seg).mark_line(
    strokeWidth=2.5, opacity=opacidade, interpolate="monotone"
).encode(
    x=alt.X("Ano_num:Q", title="Ano", axis=eixo_ano, scale=escala_ano),
    y=alt.Y("Valor:Q", title="Número de casos / óbitos", axis=eixo_y, scale=escala_y),
    detail=alt.Detail("Segmento:N"),
    order=alt.Order("Ano_num:Q"),
    color=alt.Color("Categoria:N", scale=cores_categorias, legend=alt.Legend(title="Legenda")),
    tooltip=[
        alt.Tooltip("Ano_num:Q", title="Ano", format="d"),
        alt.Tooltip("Categoria:N", title="Categoria"),
        alt.Tooltip("Valor:Q", title="Valor"),
    ],
)

cinza_pontos = alt.Chart(df_cinza_pts).mark_point(filled=True, size=45, opacity=opacidade).encode(
    x=alt.X("Ano_num:Q", sort="ascending", scale=escala_ano),
    y=alt.Y("Valor:Q", axis=eixo_y, scale=escala_y),
    color=alt.Color("Categoria:N", scale=cores_categorias),
    tooltip=[
        alt.Tooltip("Ano:O", title="Ano"),
        alt.Tooltip("Categoria:N", title="Categoria"),
        alt.Tooltip("Valor:Q", title="Valor"),
    ],
)
 
linhas_coloridas = alt.Chart(df_linhas).mark_line(
    strokeWidth=2.5, point=alt.OverlayMarkDef(filled=True, size=45), interpolate="monotone"
).encode(
    x=alt.X("Ano_num:Q", title="Ano", axis=eixo_ano, scale=escala_ano),
    y=alt.Y("Valor:Q", title="Número de casos / óbitos", axis=eixo_y, scale=escala_y),
    order=alt.Order("Ano_num:Q", sort="ascending"),
    color=alt.Color("Categoria:N", scale=cores_categorias, legend=alt.Legend(title="Legenda")),
    tooltip=[
        alt.Tooltip("Ano:O", title="Ano"),
        alt.Tooltip("Categoria:N", title="Categoria"),
        alt.Tooltip("Valor:Q", title="Valor"),
    ]
)
 
grafico = alt.layer(cinza_linhas, cinza_pontos, linhas_coloridas).properties(height=420)
 
st.altair_chart(grafico, use_container_width=True)