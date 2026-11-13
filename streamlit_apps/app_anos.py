import streamlit as st
import pandas as pd
import altair as alt
 
from comum import carregar_dados, fmt, liberar_largura_total
 
liberar_largura_total()
 
dados_humanos, dados_epizootias = carregar_dados()
 
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
 
todas_categorias = ["Casos Humanos", "Epizootias em PNH", "Óbitos Humanos"]
 
cores_categorias = alt.Scale(
    domain=todas_categorias,
    range=["#1c1a4a", "#f5a623", "#F74245"]
)
 
df_linhas = df_comparativo.melt(
    id_vars="Ano",
    value_vars=todas_categorias,
    var_name="Categoria",
    value_name="Valor"
)
 
maximo = max(int(df_comparativo[todas_categorias].max().max()), 1)
escala_y = alt.Scale(domain=[0, maximo * 1.1], nice=True)
 
escala_ano = alt.Scale(domain=anos_exibidos_str)
 
grafico = alt.Chart(df_linhas).mark_line(
    strokeWidth=2.5, point=alt.OverlayMarkDef(filled=True, size=45), interpolate="monotone"
).encode(
    x=alt.X("Ano:O", title="Ano", sort=anos_exibidos_str, scale=escala_ano),
    y=alt.Y("Valor:Q", title="Número de casos / óbitos", scale=escala_y),
    order=alt.Order("Ano:N", sort="ascending"),
    color=alt.Color("Categoria:N", scale=cores_categorias, legend=alt.Legend(title="Legenda")),
    tooltip=["Ano", "Categoria", "Valor"]
).properties(height=420)
 
st.altair_chart(grafico, use_container_width=True)
