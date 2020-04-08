import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from apps import GetData
from apps import graph 
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import time
from app import app
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import yfinance as yf
### PLOT

df_confirmed_world = GetData.get_world('confirmed')
df = pd.DataFrame()
df['Date'] = pd.to_datetime(df_confirmed_world.iloc[:,5:].columns)
df['Confirmed_World'] = df_confirmed_world.iloc[:,5:].sum().values
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
        lst += [(dict_asset_classes[asset], asset, df.index[i].strftime('%d/%m/%y'), df.iloc[i,0], df_price[asset][i], 100)]     
df = pd.DataFrame(lst, columns=['Asset class', 'Name', 'Date', 'Confirmed', 'Price', 'Size'])

fig_confirmed = px.scatter(df, x = 'Confirmed', y = 'Price', animation_frame = 'Date', animation_group = 'Name', color = 'Name', hover_name = 'Name', size = 'Size', size_max = 25, facet_col = 'Asset class', range_x = [0, df['Confirmed'].max() + 10000], range_y = [df['Price'].min(), df['Price'].max()])


## CSS

CSS =  {
    'danger':{
        'font-size':'15px',
        'color':'#cc1100',
        'font-weight':'bolder'
    },
    'important':{
        'font-size':'15px',
        'font-weight':'bold'
    }
}

dropdown = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem('Autres maladies',href='AutresMaladies'),
        dbc.DropdownMenuItem('Finance',href='/Finance',header=True),
        dbc.DropdownMenuItem('Google Trend',href='/GoogleTrend')
    ],
    nav=True,
    in_navbar=True,
    label = 'Comparatif',
    style = {'margin-right':'3em'}
)

navbar = dbc.Navbar(
        [
        html.A(
            dbc.Row(
            [
                dbc.Col(html.Img(src= app.get_asset_url('png/008-virus.png'),height='32px',width ='32px')),
                dbc.Col(dbc.NavbarBrand('CoronaRecap',className="ml-2"))
            ],
                align="center",
                no_gutters=True,
                ),
                href="/"),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Récapitulatif",href="/")),
                    dbc.NavItem(dbc.NavLink("Simulateur",href="/simulation")),
                    dropdown
                ],className="ml-auto",navbar=True
            ),
            
        ],
    color="dark",
    dark=True,
)

layout = html.Div(children=[
    navbar,
    dbc.Row(
        dcc.Graph(figure = fig_confirmed)
    )
    ]
)