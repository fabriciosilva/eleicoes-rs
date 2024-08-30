

import streamlit as st
import pandas as pd
from babel.numbers import format_currency
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import math
from millify import millify
from src import util
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_theme import st_theme
import time


# Configuração inicial

st.set_page_config(
     page_title='Eleições 2024',
     layout="wide",
     initial_sidebar_state="expanded",
)

theme = st_theme()
time.sleep(3)

@st.cache_data
def load_data(url, sep=',', encoding='latin1'):
    df = pd.read_csv(url, sep=sep, encoding=encoding)    
    return df

background_color = '#fff'
logo_dark = False
if theme is not None and theme['base'] == 'dark':
    background_color = '#02060c'
    logo_dark = True

cidade = st.selectbox(
    "Trocar Cidade",
    ("PARAÍ", "CASCA", "NOVA ARAÇÁ", "SERAFINA CORREA", "NOVA BASSANO", "NOVA PRATA", "CANGUÇU", 'PELOTAS', 'PASSO FUNDO', 'PORTO ALEGRE'),
    index=0
)



st.write("# Eleições 2024 - ", cidade)



"""
#### Acompanhe os dados divulgados pelo TSE sobre os candidatos e candidatas a prefeito e vereadores na região.


###### 🟢⚪🔴

 


"""


#with st.expander("Show past quarters"):
#    "Teste"



df = load_data('data/consulta_cand_2024_RS.csv', sep=';')


"""
Estes são os dados de candidatos disponibilizados pelo TSE. Mas só a tabela, assim, não diz muito, vamos analisar mais a fundo!
"""

df = df[(df['NM_UE'] == cidade ) & (df['DS_CARGO'] != 'VICE-PREFEITO')]



"""
###  Número de Candidatos 

"""
st.markdown("")

pref, ver, partidos = st.columns(3)
pref.metric("Candidatos a Prefeito(a)", df[df.DS_CARGO == 'PREFEITO'].shape[0], help=f"Candidatos a prefeito em {cidade}")
ver.metric("Candidatos a Vereador(a)", df[df.DS_CARGO == 'VEREADOR'].shape[0], help=f"Candidatos a vereadores em {cidade}")
partidos.metric("Qtde Partidos)", len(df['SG_PARTIDO'].unique()), help=f"Número de partidos políticos concorrendo em {cidade}")


# Cria um dicionário para mapear o tipo de candidato ao cargo correspondente
cargo_map = {
    "Prefeito(a)": "PREFEITO",
    "Vereador(a)": "VEREADOR"
}

# Obtem o tipo de candidato selecionado pelo usuário
tipo_candidato = st.radio(
    "Você deseja ver dados de candidatos a:",
    ["Todos", "Prefeito(a)", "Vereador(a)"],    
    index=0,
    horizontal=True
)

# Filtra o DataFrame com base na seleção do usuário
if tipo_candidato == "Todos":
    df = df[(df['NM_UE'] == cidade) & (df['DS_CARGO'] != 'VICE-PREFEITO')]
else:
    cargo = cargo_map[tipo_candidato]
    df = df[(df['NM_UE'] == cidade) & (df['DS_CARGO'] == cargo)]




col1, col2 = st.columns(2)

with col1:
    
    df_partidos = df.groupby(['SG_PARTIDO']).agg({'DS_CARGO': 'count'}).sort_values(by='DS_CARGO', ascending=True).reset_index()
    partidos = util.bar_chart(
        title='Candidatos por Partido',
        x_value=df_partidos["DS_CARGO"],
        y_value=df_partidos["SG_PARTIDO"],
        xaxis_title="Quantidade de Candidatos (Exceto candidatos a vice-prefeito)",
        yaxis_title="Partido",
        currence_format=False
        )
    st.plotly_chart(partidos, use_container_width=True)
    


with col2:
    df_grau_instrucao = df.groupby(['DS_GRAU_INSTRUCAO']).agg({'DS_CARGO': 'count'}).sort_values(by='DS_CARGO', ascending=True).reset_index()
    partidos = util.bar_chart(
        title='Candidatos por Grau de Instrução',
        x_value=df_grau_instrucao["DS_CARGO"],
        y_value=df_grau_instrucao["DS_GRAU_INSTRUCAO"],
        xaxis_title="Quantidade de Candidatos (Exceto candidatos a vice-prefeito)",
        yaxis_title="Grau de Instrução",
        currence_format=False
        )
    st.plotly_chart(partidos, use_container_width=True)


col3, col4, col5 = st.columns(3)
with col3:
    df_genero = df.groupby(['DS_GENERO']).agg({'DS_CARGO': 'count'}).sort_values(by='DS_CARGO', ascending=True).reset_index()
    partidos = util.bar_chart(
        title='Candidatos por Gênero',
        x_value=df_genero["DS_CARGO"],
        y_value=df_genero["DS_GENERO"],
        xaxis_title="Quantidade de Candidatos (Exceto candidatos a vice-prefeito)",
        yaxis_title="Gênero",
        currence_format=False
        )
    st.plotly_chart(partidos, use_container_width=True)

with col4:
    df_raca = df.groupby(['DS_COR_RACA']).agg({'DS_CARGO': 'count'}).sort_values(by='DS_CARGO', ascending=True).reset_index()
    partidos = util.bar_chart(
        title='Candidatos por Cor/Raça',
        x_value=df_raca["DS_CARGO"],
        y_value=df_raca["DS_COR_RACA"],
        xaxis_title="Quantidade de Candidatos (Exceto candidatos a vice-prefeito)",
        yaxis_title="Cor/Raça",
        currence_format=False
        )
    st.plotly_chart(partidos, use_container_width=True)



with col5:
    df_estado_civil = df.groupby(['DS_ESTADO_CIVIL']).agg({'DS_CARGO': 'count'}).sort_values(by='DS_CARGO', ascending=True).reset_index()
    partidos = util.bar_chart(
        title='Candidatos por Estado Civil',
        x_value=df_estado_civil["DS_CARGO"],
        y_value=df_estado_civil["DS_ESTADO_CIVIL"],
        xaxis_title="Quantidade de Candidatos (Exceto candidatos a vice-prefeito)",
        yaxis_title="Estado Civil",
        currence_format=False
        )
    st.plotly_chart(partidos, use_container_width=True)



@st.cache_data
def get_min(data_frame, column):
    return data_frame[column].min()

@st.cache_data
def get_max(data_frame, column):
    return data_frame[column].max()




logo_image =  "src/imgs/eleicoes.png"

st.sidebar.image(logo_image, width=150)

st.sidebar.header('Análise dos dados das eleições 2024')



st.sidebar.markdown('''
<small>🏰⛪🎲 <br> O TSE disponibiliza e atualiza frequentemente os dados sobre as eleições. Decidi analisá-los e disponibilizar aqui as informações que considero relevatnes</small>
    ''', unsafe_allow_html=True)


st.sidebar.markdown('''
<small>Acredito que isso pode ajudar a conhecer melhor os candidatos que quererm adiministrar nossas cidades.</small>
    ''', unsafe_allow_html=True)


st.sidebar.markdown('''
<small>Antes de qualquer coisa, quero dizer que aqui tem ZERO INFLUÊNCIA POLÍTICA. O objetivo da página é apenas dar luz aos dados para que cada cidadão tire suas próprias conclusões!</small>
    ''', unsafe_allow_html=True)







st.sidebar.markdown('<small>Este projeto é uma iniciativa individual. A única fonte de dados é o [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/dataset/candidatos-2024). ', unsafe_allow_html=True)

st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
st.sidebar.markdown('''<small>[Eleicoes2024 v0.1](https://github.com/fabriciosilva/serafina-em-dados)  | 2024 | [Fabrício Silva](https://www.linkedin.com/in/fabriciofsilva/)</small>''', unsafe_allow_html=True)



