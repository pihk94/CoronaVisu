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
#FCT 

## Pays
df_trend_country_confirmed = df_confirmed_world.groupby('Country/Region').sum().iloc[:,2:].T
df_trend_country_confirmed = df_trend_country_confirmed[df_trend_country_confirmed.iloc[-1].sort_values(ascending = False).index[0:10].values]
df_trend_country_confirmed.index = pd.to_datetime(df_trend_country_confirmed.index)
df_trend_country_recovered = df_recovered_world.groupby('Country/Region').sum().iloc[:,2:].T
df_trend_country_recovered = df_trend_country_recovered[df_trend_country_recovered.iloc[-1].sort_values(ascending = False).index[0:10].values]
df_trend_country_recovered.index = pd.to_datetime(df_trend_country_recovered.index)
df_trend_country_deaths = df_deaths_world.groupby('Country/Region').sum().iloc[:,2:].T
df_trend_country_deaths = df_trend_country_deaths[df_trend_country_deaths.iloc[-1].sort_values(ascending = False).index[0:10].values]
df_trend_country_deaths.index = pd.to_datetime(df_trend_country_deaths.index)
df_trend_country_active_cases = df_confirmed_world.groupby('Country/Region').sum().iloc[:,2:].T - df_recovered_world.groupby('Country/Region').sum().iloc[:,2:].T - df_deaths_world.groupby('Country/Region').sum().iloc[:,2:].T
df_trend_country_active_cases = df_trend_country_active_cases[df_trend_country_active_cases.iloc[-1].sort_values(ascending = False).index[0:10].values]
df_trend_country_active_cases.index = pd.to_datetime(df_trend_country_active_cases.index)

# Confirmed
labels = df_trend_country_confirmed.columns
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)', 'rgb(154, 14, 14)', 'rgb(100, 145, 122)', 'rgb(120, 124, 124)', 'rgb(140, 20, 34)', 'rgb(25, 140, 20)', 'rgb(210, 144, 154)']
line_size = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

fig_trend_country_confirmed = go.Figure()
for i in range(10):
    fig_trend_country_confirmed.add_trace(go.Scatter(x=df_trend_country_confirmed.index, y=df_trend_country_confirmed.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_country_confirmed.update_layout(
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
labels = df_trend_country_active_cases.columns
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)', 'rgb(154, 14, 14)', 'rgb(100, 145, 122)', 'rgb(120, 124, 124)', 'rgb(140, 20, 34)', 'rgb(25, 140, 20)', 'rgb(210, 144, 154)']
line_size = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

fig_trend_country_active_cases = go.Figure()
for i in range(10):
    fig_trend_country_active_cases.add_trace(go.Scatter(x=df_trend_country_active_cases.index, y=df_trend_country_active_cases.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_country_active_cases.update_layout(
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
labels = df_trend_country_deaths.columns
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)', 'rgb(154, 14, 14)', 'rgb(100, 145, 122)', 'rgb(120, 124, 124)', 'rgb(140, 20, 34)', 'rgb(25, 140, 20)', 'rgb(210, 144, 154)']
line_size = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

fig_trend_country_deaths = go.Figure()
for i in range(10):
    fig_trend_country_deaths.add_trace(go.Scatter(x=df_trend_country_deaths.index, y=df_trend_country_deaths.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_country_deaths.update_layout(
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
labels = df_trend_country_recovered.columns
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)', 'rgb(154, 14, 14)', 'rgb(100, 145, 122)', 'rgb(120, 124, 124)', 'rgb(140, 20, 34)', 'rgb(25, 140, 20)', 'rgb(210, 144, 154)']
line_size = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

fig_trend_country_recovered = go.Figure()
for i in range(10):
    fig_trend_country_recovered.add_trace(go.Scatter(x=df_trend_country_recovered.index, y=df_trend_country_recovered.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_country_recovered.update_layout(
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
                html.Div(style={'width':'32em'}),
                html.H4('COVID-19 TOP 10 COUNTRY TREND',id='titleCountry',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','color':'rgb(87, 88, 90)','font-weight':'bolder'})
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
                                html.A([html.Div('Continental Trend')],href ='/recap/continent',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Country Trend'),html.Div(className='encoche',style={'top':'537px','margin-top':'0px'})],href ='/recap/country',className = "sousOngletActived")
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
                                    id='radiochoicecountry',
                                    inline=True
                                        ),className='justify-content-end',style={
                            'margin-right':'8em',
                            'margin-top':'2em',
                            'color':'rgb(87, 88, 90)'
                        }
                         ),
                    dcc.Loading(
                        dcc.Graph(id='choixCuntry',style={'height':'850px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])
#CALLBACKS
@app.callback(
    [Output('choixCuntry','figure'),
    Output('titleCountry','children')],
    [Input('radiochoicecountry','value')]
)
def show_graph(value,fig1=fig_trend_country_active_cases,fig2=fig_trend_country_confirmed,fig3=fig_trend_country_recovered,fig4=fig_trend_country_deaths):
    if value == 1:
        return fig1,'COVID-19 TOP 10 COUNTRY TREND (ACTIVE)'
    elif value == 2:
        return fig2,'COVID-19 TOP 10 COUNTRY TREND (CONFIRMED)'
    elif value == 3:
        return fig3,'COVID-19 TOP 10 COUNTRY TREND (RECOVERED)'
    else:
        return fig4,'COVID-19 TOP 10 COUNTRY TREND (DEATHS)'