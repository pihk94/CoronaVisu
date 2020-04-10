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

## Continent                                 
df_trend_continent_confirmed = df_confirmed_world.groupby('Continent').sum().iloc[:,2:].T
df_trend_continent_confirmed.index = pd.to_datetime(df_trend_continent_confirmed.index)
df_trend_continent_recovered = df_recovered_world.groupby('Continent').sum().iloc[:,2:].T
df_trend_continent_recovered.index = pd.to_datetime(df_trend_continent_recovered.index)
df_trend_continent_deaths = df_deaths_world.groupby('Continent').sum().iloc[:,2:].T
df_trend_continent_deaths.index = pd.to_datetime(df_trend_continent_deaths.index)
df_trend_continent_active_cases = df_trend_continent_confirmed - df_trend_continent_recovered - df_trend_continent_deaths

labels = df_trend_continent_confirmed.columns
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)', 'rgb(154, 14, 14)', 'rgb(100, 145, 122)']
line_size = [4, 4, 4, 4, 4, 4]

# Confirmed
fig_trend_continent_confirmed = go.Figure()
for i in range(6):
    fig_trend_continent_confirmed.add_trace(go.Scatter(x=df_trend_continent_confirmed.index, y=df_trend_continent_confirmed.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_confirmed.update_layout(
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
# Active Cases
fig_trend_continent_active_cases = go.Figure()
for i in range(6):
    fig_trend_continent_active_cases.add_trace(go.Scatter(x=df_trend_continent_active_cases.index, y=df_trend_continent_active_cases.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_active_cases.update_layout(
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
# Deaths
fig_trend_continent_deaths = go.Figure()
for i in range(6):
    fig_trend_continent_deaths.add_trace(go.Scatter(x=df_trend_continent_deaths.index, y=df_trend_continent_deaths.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_deaths.update_layout(
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
                           
# Recovered
fig_trend_continent_recovered = go.Figure()
for i in range(6):
    fig_trend_continent_recovered.add_trace(go.Scatter(x=df_trend_continent_recovered.index, y=df_trend_continent_recovered.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_recovered.update_layout(
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
                html.H4('COVID-19 CONTINENTAL TREND',id='titleConti',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','color':'rgb(87, 88, 90)','font-weight':'bolder'})
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
                                html.A([html.Div('Continental Trend'),html.Div(className='encoche',style={'top':'375px','margin-top':'0px'})],href ='/recap/continent',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Country Trend')],href ='/recap/country',className = "sousOnglet")
                            ]
                        ),
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row(
                        dbc.RadioItems(
                                    options=[
                                        {'label':'Active cases','value':1},
                                        {'label':'Confirmed cases','value':2},
                                        {'label':'Recovered cases','value':3},
                                        {'label':'Deaths cases','value':4}
                                    ],
                                    value=1,
                                    id='radiochoiceconti',
                                    inline=True
                                        ),className='justify-content-end',style={
                            'margin-right':'8em',
                            'margin-top':'2em',
                            'color':'rgb(87, 88, 90)'
                        }
                         ),
                    dcc.Loading(
                        dcc.Graph(id='choixContinent',style={'height':'850px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])
#CALLBACKS
@app.callback(
    [Output('choixContinent','figure'),
    Output('titleConti','children')],
    [Input('radiochoiceconti','value')]
)
def show_graph(value,fig1=fig_trend_continent_active_cases,fig2=fig_trend_continent_confirmed,fig3=fig_trend_continent_recovered,fig4=fig_trend_continent_deaths):
    if value == 1:
        return fig1,'COVID-19 CONTINENTAL TREND (ACTIVE)'
    elif value == 2:
        return fig2,'COVID-19 CONTINENTAL TREND (CONFIRMED)'
    elif value == 3:
        return fig3,'COVID-19 CONTINENTAL TREND (RECOVERED)'
    else:
        return fig4,'COVID-19 CONTINENTAL TREND (DEATHS)'