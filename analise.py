import pandas as pd
import matplotlib.pyplot as plt

def carregar_dados():
    anos = range(2020, 2026)
    dfs = []

    for ano in anos:
        parte1 = f'HIST_PAINEL_COVIDBR_{ano}_Parte1_25abr2025.csv'
        parte2 = f'HIST_PAINEL_COVIDBR_{ano}_Parte2_25abr2025.csv'

        try:
            df1 = pd.read_csv(parte1, sep=';', encoding='utf-8')
            df2 = pd.read_csv(parte2, sep=';', encoding='utf-8')
            dfs.append(pd.concat([df1, df2]))
        except FileNotFoundError:
            pass

    df = pd.concat(dfs)
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df['ano'] = df['data'].dt.year
    df_brasil = df[df['regiao'] == 'Brasil'].copy()
    df_estados = df[(df['regiao'] != 'Brasil') & (df['estado'].notna())]
    return df, df_brasil, df_estados

def grafico_casos_por_ano(df_brasil):
    casos_ano = df_brasil.groupby('ano')['casosNovos'].sum()
    fig, ax = plt.subplots()
    casos_ano.plot(kind='bar', ax=ax)
    ax.set_title('Casos novos por ano no Brasil')
    ax.set_ylabel('Casos')
    return fig

def grafico_obitos_por_ano(df_brasil):
    obitos_ano = df_brasil.groupby('ano')['obitosNovos'].sum()
    fig, ax = plt.subplots()
    obitos_ano.plot(kind='bar', color='red', ax=ax)
    ax.set_title('Óbitos por ano no Brasil')
    ax.set_ylabel('Óbitos')
    return fig

def grafico_top5_estados_obitos(df_estados):
    obitos_estado = df_estados.groupby('estado')['obitosAcumulado'].max().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots()
    obitos_estado.plot(kind='bar', color='purple', ax=ax)
    ax.set_title('Top 5 estados com mais óbitos acumulados')
    return fig

def grafico_obitos_por_faixa(df_brasil):
    if 'faixaEtaria' in df_brasil.columns:
        obitos_faixa = df_brasil.groupby('faixaEtaria')['obitosNovos'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots()
        obitos_faixa.plot(kind='bar', color='orange', ax=ax)
        ax.set_title('Óbitos por faixa etária no Brasil')
        return fig
    return None

def grafico_letalidade(df_brasil):
    casos = df_brasil.groupby('ano')['casosNovos'].sum()
    obitos = df_brasil.groupby('ano')['obitosNovos'].sum()
    letalidade = (obitos / casos) * 100
    fig, ax = plt.subplots()
    letalidade.plot(kind='line', marker='o', color='darkgreen', ax=ax)
    ax.set_title('Taxa de Letalidade por Ano no Brasil')
    ax.set_ylabel('Letalidade (%)')
    return fig
