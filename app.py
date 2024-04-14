

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



theme = st_theme()
time.sleep(2)



"""
# Serafina em dados 
# 🏰⛪🎲





Todo mundo sabe que as entidades públicas são obrigadas por [lei](https://www.planalto.gov.br/ccivil_03/_Ato2011-2014/2011/Lei/L12527.htm) a disponibilizar seus dados na internet. Aqui em Serafina não é diferente e a Prefeitura os disponibliza em sei site. E tá tudo certo!

Só que, gente, é um monte de planilhazinha que dá uma tristeza só de olhar. Aí, pra deixar isso mais fácil, resolvi dar uma  compilada nos dados e vou mostrar tudo bonitinho em gráficos e números, pra gente entender direitinho como o dinheiro da cidade tá sendo usado. 

Acredito que isso vai nos ajudar a fiscalizar e cobrar mais responsabilidade da galera que tá cuidando do nosso dinheiro.

Antes de qualquer coisa, quero dizer que aqui tem ZERO INFLUÊNCIA POLÍTICA. O objetivo da página é apenas dar luz aos gastos da prefeitura para que cada cidadão tire suas próprias conclusões!

🟢⚪🔴

 


"""





df = pd.read_excel('data/dados_agrupados-q1.xlsx')
df_completo = pd.read_csv('data/despesas_fornecedor_com_municipios_Q1.csv')

df_completo = df_completo[~df_completo['Código'].isna()]
df_completo = df_completo[~df_completo['CNPJ/CPF'].isna()]



valor_empenhado = df.valor_empenhado.sum()
valor_liquidado = df.valor_liquidado.sum()
valor_pago = df.valor_pago.sum()




"""
---

### 💸 Para onde foi o seu dinheiro? 

Totais apurados no **primeiro trimestre de 2024**: 
"""



background_color = '#fff'
if theme['base'] == 'dark':
    background_color = '#02060c'
style_metric_cards(background_color=background_color)
col_estados, col_cidades, col_empresas = st.columns(3)
col_estados.metric("🔰 Estados", df.uf.unique().size)
col_cidades.metric("🏙 Cidades", df.municipio.unique().size)
col_empresas.metric("🏦 Empresas", df.cnpj.sum())



st.markdown("")
st.markdown("")

"""

###  👀 E o total, dá quanto? 

"""
st.markdown("")

col1, col2, col3, col_qtde = st.columns(4)
col1.metric("Valor empenhado (R$)", millify(valor_empenhado), help=util.brl(valor_empenhado))
col2.metric("Valor liquidado (R$)", millify(valor_liquidado), help=util.brl(valor_liquidado))
col3.metric("Valor pago (R$)", millify(valor_pago), help=util.brl(valor_pago))
col_qtde.metric("Quantidade de empenhos",  df_completo.valor_empenhado.count())

col_max, col_min, col_media = st.columns(3)

col_max.metric("Maior valor de empenho (R$)", util.moeda(df_completo.valor_empenhado.max()), help=util.brl(df_completo.valor_empenhado.max()))
col_min.metric("Menor valor de empenho (R$)", util.moeda(df_completo.valor_empenhado.min()), help=util.brl(df_completo.valor_empenhado.min()))
col_media.metric("Valor médio de empenho (R$)", util.moeda(df_completo.valor_empenhado.mean()), help=util.brl(df_completo.valor_empenhado.mean()))

  


"""
---

### Análise das empresas que possuem algum valor empenhado em Serafina Corrêa de janeiro à março de 2024
"""


df_top = df[0:10].sort_values(by="valor_empenhado", ascending=True)


# Gráfico das cidades maiores empenhos
empresas = util.bar_chart(
    title='De onde são as empresas que mais tiveram valores empenhos em 2024T1?',
    x_value=df_top["valor_empenhado"],
    y_value=df_top["municipio"] +'/'+df_top["uf"],
    xaxis_title="Valor Empenhado (R$)",
    yaxis_title="Cidade"
    )
st.plotly_chart(empresas, use_container_width=True)




df_tail = df.tail(10).sort_values(by="valor_empenhado", ascending=True)
# Gráfico das cidades menores empenhos
empresas = util.bar_chart(
    title='E o contrário? Quais as cidades que menos tiveram empenhos em 2024T1?',
    x_value=df_tail["valor_empenhado"],
    y_value=df_tail["municipio"]+'/'+df_tail["uf"],
    xaxis_title="Valor Empenhado (R$)",
    yaxis_title="Cidade"
    )
st.plotly_chart(empresas, use_container_width=True)


"""

### E eu consigo ver todas as cidades? 
### _Tá na mão!_

Navegue no mapa abaixo para buscar mais detalhes. Ao clicar no município, o valor emepenhado é exibido. 

Tenta aí :)
"""


mapa = folium.Map(location=(-23.2527698,-50.4279182), zoom_start=5,  tiles='cartodbdark_matter')

#mapa
valor_empenhado_min = df['valor_empenhado'].min()
valor_empenhado_max = df['valor_empenhado'].max()

print(valor_empenhado_max, valor_empenhado_min)

for index, a in df.iterrows():    
    municipio = a['municipio']
    latitude = a['latitude']
    longitude = a['longitude']
    valor_empenhado = a['valor_empenhado']
        
    
    radius = valor_empenhado / valor_empenhado_max 
    popup_valor = util.brl(valor_empenhado)
    if not math.isnan(latitude) and not math.isnan(longitude) and valor_empenhado > 0:
        folium.CircleMarker(
          location=[latitude, longitude],
          radius=radius*10,
          color="red",
          weight=5,
          fill_opacity=0.6,
          opacity=1,
          fill_color="#E8710A",
          fill=False,  # gets overridden by fill_color
          popup = f'Valor Empenhado {popup_valor}',
          tooltip=municipio,
          zoom_control=False,
          scrollWheelZoom=False,
        ).add_to(mapa)


st_data = st_folium(mapa, width=600, height=600)



df_dados_agrupados = pd.read_excel('data/dados_agrupados-q1.xlsx').sort_values(by='valor_empenhado', ascending=False)[:10]


df_empresas = df_completo.sort_values(by= 'valor_empenhado', ascending=False)[0:10].sort_values(by= 'valor_empenhado', ascending=True)



df_empresas = df_empresas[~df_empresas['Código'].isna()]
df_empresas = df_empresas[~df_empresas['CNPJ/CPF'].isna()]


"""

### E as empresas, quais são? 

Veja abaixo as top 10 empresas em valor de empenho entre janeiro e março de 2024

"""

# Gráfico das empresas
empresas = util.bar_chart(
    title='Empresas com maiores empenhos em Serafina',
    x_value=df_empresas["valor_empenhado"],
    y_value=df_empresas["Descrição"] + ' <br />' + df_empresas["municipio"] + '/' + df_empresas["uf"] + ' - ' + df_empresas["CNPJ/CPF"],
    xaxis_title="Valor Empenhado (R$)",
    yaxis_title="Empresa"
    )
st.plotly_chart(empresas, use_container_width=True)




dados_agrupados_meses = pd.read_csv('data/dados_agrupados_meses.csv')


fig_meses = go.Figure()
fig_meses.add_trace(go.Bar(
    x=dados_agrupados_meses['mes'],
    y=dados_agrupados_meses['valor_empenhado'],
    name='Valor empenhado',
    #marker_color='indianred',   
    text=dados_agrupados_meses['valor_empenhado'].apply(lambda x: util.moeda(x))
))
fig_meses.add_trace(go.Bar(
    x=dados_agrupados_meses['mes'],
    y=dados_agrupados_meses['valor_liquidado'],
    name='Valor Liquidado',
    #marker_color='lightsalmon',
    text=dados_agrupados_meses['valor_liquidado'].apply(lambda x: util.moeda(x))
))

fig_meses.add_trace(go.Bar(
    x=dados_agrupados_meses['mes'],
    y=dados_agrupados_meses['valor_pago'],
    name='Valor pago',
    #marker_color='green',
    text=dados_agrupados_meses['valor_pago'].apply(lambda x: util.moeda(x))
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
#fig_meses.update_layout(barmode='group', xaxis_tickangle=0)

fig_meses.update_layout(title="Comparativo de valores empenhado e liquidado 2024T1",
                  xaxis_title="Mês",
                  yaxis_title="Valor",
                  bargap=0.2,
                  barmode='group',
                  xaxis_showgrid=True,
                  yaxis_showgrid=True
                  )



st.plotly_chart(fig_meses, use_container_width=True)