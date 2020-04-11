import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from pytrends.request import TrendReq
import plotly.graph_objects as go
from plotly.offline import plot
from app import app
from apps import sidebar
#fct

#FIGURE SLIDE COMPARAIRAISON

layout = html.Div([
    sidebar.sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'50em'}),
                html.H4('FINANCIAL IMPACT OF COVID-19',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','color':'rgb(87, 88, 90)','font-weight':'bolder'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('CORONAVIRUS IMPACT')],href ='/finance',className = "sousOnglet"),
                            ]
                        ), 
                        dbc.Row(
                            [
                                html.A([html.Div('RECESSIONS COMPARISON'),html.Div(className='encoche',style={'top':'213px','margin-top':'0px'})],href ='/finance/compare',className = "sousOngletActived")
                            ]
                        ), 
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    dcc.Loading(
                        dcc.Graph(id='trend',style={'height':'800px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])

#CALLBACKS
