import dash
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.express as px
from app import app
from apps import GetData
from apps import graph 
import plotly.graph_objects as go
#dataLoad

#FCT 
sidebar = html.Div(id='mySidebar',className ="sidebar",children=[
            html.A(href='/',children = [html.Img(src='../assets/png/home.png',style={'width':'32px','height':'32px','margin-left':'5.6em'}),html.Div('Home',style={
                'font-size':'14px',
                'text-align':'center'
            })],style={'background-color':'#036','margin-top':' 0px'}),
            html.A(href='/recap',children=[html.Span('Summary')],style={'text-align':'left'}),
            html.A(href='/simulation',children='SIMULATION',style={'text-align':'left'}),
            html.A(href='/maladies',children='DISEASE COMPARISON',style={'text-align':'left'}),
            html.A(href='/finance',children='FINANCE',style={'text-align':'left'}),
            html.A(href='/GoogleTrend',children='INTERNET',style={'text-align':'left'}),
        ])
layout = html.Div([
    sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'56em'}),
                html.H4('COVID-19 CONTINENTAL TREND',id='titleMaladie',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Overview')],href ='/recap',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('World Trend')],href ='/recap/world',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Continental Trend'),html.Div(className='encoche',style={'top':'294px','margin-top':'0px'})],href ='/recap/continent',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Country Trend')],href ='/recap/country',className = "sousOnglet")
                            ]
                        ),
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    html.Div(
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])

#CALLBACKS
# @app.callback(
#     [Output('doubleGraph','figure'),
#     Output('titleMaladie','children')],
#     [Input('BtnFigureDoubleGraph1','className')]
# )
# def show_graph(className,fig1=fig1,fig2=fig2):
#     if className == 'btnChoixActive':
#         return fig1,'Comparison of Differents Infectious Diseases (Annual total cases)'
#     else:
#         return fig2,'Comparison of Differents Infectious Diseases (Annual total fatalities)'


# @app.callback(
#     [Output('BtnFigureDoubleGraph1','className'),
#     Output('BtnFigureDoubleGraph2','className')],
#     [Input('BtnFigureDoubleGraph1','n_clicks'),
#     Input('BtnFigureDoubleGraph2','n_clicks')
#     ]
# )
# def change_color(n_clicks1,n_clicks2):
#     if n_clicks1 > n_clicks2:
#         return 'btnChoixActive','btnChoixNonActive'
#     else:
#         return 'btnChoixNonActive','btnChoixActive'
