import streamlit as st
from analise import (
    carregar_dados,
    grafico_casos_por_ano,
    grafico_obitos_por_ano,
    grafico_top5_estados_obitos,
    grafico_obitos_por_faixa,
    grafico_letalidade,
)

st.set_page_config(page_title="COVID-19 no Brasil", layout="wide")
st.title("📊 Análise de Mortalidade por COVID-19 no Brasil")

with st.spinner("Carregando dados..."):
    df, df_brasil, df_estados = carregar_dados()

aba = st.sidebar.radio("Escolha a análise:", [
    "Casos por ano",
    "Óbitos por ano",
    "Top 5 Estados com mais óbitos",
    "Óbitos por faixa etária",
    "Taxa de letalidade"
])

if aba == "Casos por ano":
    st.pyplot(grafico_casos_por_ano(df_brasil))

elif aba == "Óbitos por ano":
    st.pyplot(grafico_obitos_por_ano(df_brasil))

elif aba == "Top 5 Estados com mais óbitos":
    st.pyplot(grafico_top5_estados_obitos(df_estados))

elif aba == "Óbitos por faixa etária":
    fig = grafico_obitos_por_faixa(df_brasil)
    if fig:
        st.pyplot(fig)
    else:
        st.warning("Coluna 'faixaEtaria' não encontrada nos dados.")

elif aba == "Taxa de letalidade":
    st.pyplot(grafico_letalidade(df_brasil))
