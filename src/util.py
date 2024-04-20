from babel.numbers import format_currency
import plotly.graph_objects as go
from millify import millify


def moeda(valor):    
    return format_currency(valor, '', locale='pt_BR')


def brl(valor):
    return format_currency(valor, 'BRL', locale='pt_BR')


def bar_chart(x_value, y_value, title, xaxis_title, yaxis_title):
    fig = go.Figure(data=[go.Bar(
    x=x_value, 
    y=y_value, 
    text=x_value.apply(lambda x: brl(x)),
    orientation='h',
   # marker=dict(color='skyblue')  # Definindo a cor das barras
    )])

    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        bargap=0.2,
        barmode='group',
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        titlefont=dict(size=18),  # Ajuste o tamanho do título
        margin=dict(t=80),
        dragmode='pan',
    #    titlepad=20,  # Ajuste o espaçamento entre o título e o gráfico
    #    title_x=0.5,  # Centraliza o título horizontalmente
        # Adiciona subtítulo
        annotations=[
            dict(
                text="",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=-0.2,
                y=1.1,
                font=dict(size=16),
                bgcolor="rgba(255, 255, 255, 0)",
                bordercolor="rgba(255, 255, 255, 0)"        
            )
        ]
    )
    return fig
