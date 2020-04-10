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
from datetime import datetime

#dataLoad
df_confirmed_world = GetData.get_world('confirmed')
df_deaths_world = GetData.get_world('deaths')
df_recovered_world = GetData.get_world('recovered')

## World
df_trend_world = pd.DataFrame()
df_trend_world['Date'] = pd.to_datetime(df_confirmed_world.iloc[:,5:].columns)
df_trend_world['Confirmed'] = df_confirmed_world.iloc[:,5:].sum().values
df_trend_world['Recovered'] = df_recovered_world.iloc[:,5:].sum().values
df_trend_world['Deaths'] = df_deaths_world.iloc[:,5:].sum().values
df_trend_world['Active Cases'] = df_trend_world['Confirmed'] - df_trend_world['Recovered'] - df_trend_world['Deaths']

labels = ['Confirmed', 'Recovered', 'Deaths', 'Active Cases']
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)']
line_size = [4, 4, 4, 4]

fig_trend_world = go.Figure()
for i in range(4):
    fig_trend_world.add_trace(go.Scatter(x=df_trend_world['Date'], y=df_trend_world.iloc[:,i+1], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_world.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickangle = 15,
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
    showlegend=True,
    plot_bgcolor='white'
)
   
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
                html.H4('COVID-19 WORLD TREND',id='titleMaladie',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px'})
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
                                html.A([html.Div('World Trend'),html.Div(className='encoche',style={'top':'162px','margin-top':'0px'})],href ='/recap/world',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Continental Trend')],href ='/recap/continent',className = "sousOnglet")
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
                    dcc.Loading(
                        dcc.Graph(figure=fig_trend_world,style={'height':'850px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])

