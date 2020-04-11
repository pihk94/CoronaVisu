import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from datetime import datetime
from pytrends.request import TrendReq
import plotly.graph_objects as go
from plotly.offline import plot
from app import app
from apps import GetData
from apps import sidebar
import yfinance as yf
import plotly.express as px
#plot 
#COnfirmed

df = pd.read_csv('data/data_finance.csv')
# Impact des confirmés
fig_impact_confirmed_finance = px.scatter(df, x = 'Confirmed', y = 'Price', animation_frame = 'Date', animation_group = 'Name', color = 'Name', hover_name = 'Name', size = 'Size', size_max = 25, facet_col = 'Asset class', range_x = [0, df['Confirmed'].max() + 10000], range_y = [df['Price'].min(), df['Price'].max()])
fig_impact_confirmed_finance['layout'].update(
    font=dict(
            family='Montserrat',
            size=15,
            color='rgb(87, 88, 90)'
            ),
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=3,
        ticks='outside'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
    ),
    showlegend=True,
    plot_bgcolor='white'
)
#DEATH
fig_impact_deaths_finance = px.scatter(df, x = 'Deaths', y = 'Price', animation_frame = 'Date', animation_group = 'Name', color = 'Name', hover_name = 'Name', size = 'Size', size_max = 25, facet_col = 'Asset class', range_x = [0, df['Deaths'].max() + 10000], range_y = [df['Price'].min(), df['Price'].max()])
fig_impact_deaths_finance['layout'].update(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=15,
            color='rgb(37, 37, 37)',
        ),
    ),
    xaxis2=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=15,
            color='rgb(37, 37, 37)',
        ),
    ),
    xaxis3=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=15,
            color='rgb(37, 37, 37)',
        ),
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
        tickfont=dict(
                family='Arial',
                size=15,
                color='rgb(37, 37, 37)')
    ),
    yaxis2=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
        tickfont=dict(
                family='Arial',
                size=15,
                color='rgb(37, 37, 37)')
    ),
    yaxis3=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
        tickfont=dict(
                family='Arial',
                size=15,
                color='rgb(37, 37, 37)')
    ),
    showlegend=True,
    plot_bgcolor='white'
)

#FIGURE SLIDE COMPARAIRAISON

layout = html.Div([
    sidebar.sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'25em'}),
                html.H4('FINANCIAL IMPACT OF COVID-19',id='titleFi',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','color':'rgb(87, 88, 90)','font-weight':'bolder'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('COVID-19 IMPACT'),html.Div(className='encoche',style={'top':'52px','margin-top':'0px'})],href ='/finance',className = "sousOngletActived"),
                            ]
                        ), 
                        dbc.Row(
                            [
                                html.A([html.Div('RECESSIONS COMPARISON')],href ='/finance/compare',className = "sousOnglet")
                            ]
                        ), 
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row(
                        [
                            html.Button('Confirmed',id='BtnFigureDoubleGraphFi1',className='btnChoixActive',n_clicks=1),
                            html.Button('Deaths',id='BtnFigureDoubleGraphFi2',className='btnChoixNonActive',n_clicks=0),
                        ],className='justify-content-end',style={
                            'margin-right':'8em',
                            'margin-top':'2em'
                        }
                    ),
                    dcc.Loading(
                        dcc.Graph(id='dbleGraphFi',style={'height':'800px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])

#CALLBACKS

#CALLBACKS
@app.callback(
    [Output('dbleGraphFi','figure'),
    Output('titleFi','children')],
    [Input('BtnFigureDoubleGraphFi1','className')]
)
def show_graph(className,fig1=fig_impact_confirmed_finance,fig2=fig_impact_deaths_finance):
    if className == 'btnChoixActive':
        return fig1,'FINANCIAL IMPACT OF COVID-19 (CONFIRMED CASES)'
    else:
        return fig2,'FINANCIAL IMPACT OF COVID-19 (DEATHS CASES)'


@app.callback(
    [Output('BtnFigureDoubleGraphFi1','className'),
    Output('BtnFigureDoubleGraphFi2','className')],
    [Input('BtnFigureDoubleGraphFi1','n_clicks'),
    Input('BtnFigureDoubleGraphFi2','n_clicks')
    ]
)
def change_color(n_clicks1,n_clicks2):
    if n_clicks1 > n_clicks2:
        return 'btnChoixActive','btnChoixNonActive'
    else:
        return 'btnChoixNonActive','btnChoixActive'