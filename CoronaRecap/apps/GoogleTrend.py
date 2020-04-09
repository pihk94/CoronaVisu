import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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

#fct
mot_base = ['coronavirus','toilet','porno','china','twitch',]
def google_trend_graph(w):
    pytrend = TrendReq()
    lst = w
    pytrend.build_payload(kw_list=lst, timeframe='today 3-m')
    interest_w = pytrend.interest_over_time() 
    interest_w = interest_w.reset_index()
    fig_trend_w = go.Figure()
    for i in range(len(lst)):
        fig_trend_w.add_trace(go.Scatter(x=interest_w['date'], y=interest_w.iloc[:,i+1], mode='lines', name=lst[i]))
    fig_trend_w.update_layout(
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

    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left', yanchor='bottom',
                            text='',
                            font=dict(family='Arial',
                            size=40,
                            color='rgb(37, 37, 37)'),
                            showarrow=False))
                              
    fig_trend_w.update_layout(annotations=annotations)                             
    return fig_trend_w
fig = google_trend_graph(mot_base)

#FIGURE SLIDE COMPARAIRAISON

sidebar = html.Div(id='mySidebar',className ="sidebar",children=[
            html.A(href='/',children = [html.Img(src='assets/png/home.png',style={'width':'32px','height':'32px','margin-left':'3.6em'}),html.Div('Home',style={
                'font-size':'14px',
                'text-align':'center'
            })],style={'background-color':'#036'}),
            html.A(href='#',children='Récapitulatif',style={'text-align':'left'}),
            html.A(href='#',children='Autres épidémies',style={'text-align':'left'}),
            html.A(href='#',children='Finance',style={'text-align':'left'}),
            html.A(href='#',children='GoogleTrend',style={'text-align':'left'}),
        ])

layout = html.Div([
    sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'50em'}),
                html.H4('GOOGLE RESEARCH INTERESTS',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Internet Trend'),html.Div(className='encoche',style={'top':'36px','margin-top':'0px'})],href ='/GoogleTrend',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col( 
                                    dbc.Input(
                                    id='search',
                                    type='search',
                                    placeholder='Search...',
                                    style={
                                        'width':'100%',
                                    }
                                ),width = 9,style={'padding-right':'0px'}),
                                dbc.Col(
                                    dbc.Button(id='BtnSearch',n_clicks=1,children=html.Img(src ='https://img.icons8.com/ios/500/search--v1.png',style = {'width':'16px','height':'16px'}),color='primary',className='ml-2')
                                ,width = 3,style={'padding-left':'0px'})
                            ],style={
                                'margin-top':'4em',
                            }
                        ),
                        dbc.Row(
                           [ dbc.Label('Choose or add words (5 choices maximum)',style={'color':'white'}),
                            html.Div("",id='msgError',style={'color':'red','text-transform':'uppercase'}),
                            html.Div(style={'margin-left':'2em'},id='containerCheckList',children = 
                                dbc.Checklist(id='checklist',
                                options =
                                    [{'label':el,'value':el} for el in mot_base],
                                style={'color':'white'},
                                value = [el for el in mot_base]
                            ),
                            ),
                            html.Div(id='test'),
                            ]
                        )
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    dcc.Loading(
                        dcc.Graph(id='trend',figure=fig,style={'height':'800px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])

#CALLBACKS
@app.callback(
    [Output('trend','figure'),
    Output('msgError','children')],
    [Input('checklist','value'),
    Input('checklist','options')]
)
def change_search(elements,options):
    if len(elements)>5:
        elements = element[:5]
        return google_trend_graph(elements),"Too much word selected, only 5 has been displayed"
    else:
        return google_trend_graph(elements),""
# @app.callback(
#     Output("test",'children'),
#     [Input("BtnSearch",'n_clicks'),
#     Input('search','value'),
#     Input('checklist','options'),
#     Input('checklist','value')]
# )
# def add_elements(n_clicks,value,options,checked):
#     if n_clicks != 1:
#         cases = [el['label'] for el in options]
#         return dbc.Checklist(id='checklist',
#             options =
#                 [{'label':el,'value':el} for el in cases],
#             style={'color':'white'},
#             value = [el for el in checked])
#     else:
#         return dbc.Checklist(id='checklist',
#             options =
#                 [{'label':el,'value':el} for el in checked],
#             style={'color':'white'},
#             value = [el for el in checked])
    