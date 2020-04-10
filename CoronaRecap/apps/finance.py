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
import yfinance as yf
import plotly.express as px
#plot 
#COnfirmed

df_confirmed_world = GetData.get_world('confirmed')
df_deaths_world = GetData.get_world('deaths')
df = pd.DataFrame()
df['Date'] = pd.to_datetime(df_confirmed_world.iloc[:,5:].columns)
df['Confirmed'] = df_confirmed_world.iloc[:,5:].sum().values
df['Deaths'] = df_deaths_world.iloc[:,5:].sum().values
df.set_index('Date', inplace = True)
list_tickers = ['^FCHI', '^GSPC', '^DJI', '^GDAXI', '^IXIC', '^N225', '^HSI', '^IBEX', 'BTC-USD', 'ETHUSD=X', 'EURUSD=X', 'EURGBP=X', 'EURJPY=X', 'EURCNY=X', 'EURCHF=X',
                'HG=F', 'EH=F', 'GC=F', 'NG=F', 'CL=F', 'PL=F', 'SI=F']
title = ['CAC40', 'SP500', 'Dow Jones', 'Dax', 'Nasdaq', 'Nikkei', 'Hangseng', 'Ibex', 'BTC/USD', 'ETH/USD', 'EUR/USD', 'EUR/GBP', 'EUR/JPY', 'EUR/CNY', 'EUR/CHF', 'Copper', 'Ethanol',
         'Gold', 'Natural Gas', 'Oil', 'Platinum', 'Silver']
title = np.array(title)
title = title[np.argsort(list_tickers)].tolist()

data = yf.download(list_tickers, start=df.index[0], group_by="ticker")
data = data.sort_index(axis = 1)
data.fillna(method = 'backfill', inplace = True)

index_to_keep_price = [i for i in range(0, data.shape[1], 6)]
df_price = data.iloc[:, index_to_keep_price]
df_price.columns = title
df_price = df_price.apply(lambda x : x / x[0] * 100)

dict_asset_classes = {'CAC40' : 'Index', 'SP500' : 'Index', 'Dow Jones': 'Index', 'Dax': 'Index', 'Nasdaq': 'Index', 'Nikkei': 'Index', 'Hangseng': 'Index', 'Ibex': 'Index', 
                      'BTC/USD': 'Currency', 'ETH/USD': 'Currency', 'EUR/USD': 'Currency', 'EUR/GBP': 'Currency', 'EUR/JPY': 'Currency', 'EUR/CNY': 'Currency', 'EUR/CHF': 'Currency', 
                      'Copper' : 'Commodity', 'Ethanol': 'Commodity', 'Gold': 'Commodity', 'Natural Gas': 'Commodity', 'Oil': 'Commodity', 'Platinum': 'Commodity', 'Silver': 'Commodity'}

lst = []
for asset in title:
    for i in range(df.shape[0]):
        lst += [(dict_asset_classes[asset], asset, df.index[i].strftime('%d/%m/%y'), df.iloc[i,0], df.iloc[i,1], df_price[asset][i], 100)]     
df = pd.DataFrame(lst, columns=['Asset class', 'Name', 'Date', 'Confirmed', 'Deaths', 'Price', 'Size'])

# Impact des confirmés
fig_impact_confirmed_finance = px.scatter(df, x = 'Confirmed', y = 'Price', animation_frame = 'Date', animation_group = 'Name', color = 'Name', hover_name = 'Name', size = 'Size', size_max = 25, facet_col = 'Asset class', range_x = [0, df['Confirmed'].max() + 10000], range_y = [df['Price'].min(), df['Price'].max()])
fig_impact_confirmed_finance['layout'].update(
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
                html.Div(style={'width':'50em'}),
                html.H4('FINANCIAL IMPACT OF COVID-19',id='titleFi',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('CORONAVIRUS IMPACT'),html.Div(className='encoche',style={'top':'36px','margin-top':'0px'})],href ='/finance',className = "sousOngletActived"),
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