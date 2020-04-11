from GetData import * 
import pandas as pd
import yfinance as yf
import numpy as np
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go

### Impact des cas confirmés et morts sur différents indices financiers

df_confirmed_world = get_world('confirmed')
df_deaths_world = get_world('deaths')
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
        ticks='outside',
    ),
    xaxis2=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=3,
        ticks='outside',
    ),
    xaxis3=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=3,
        ticks='outside',
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
    ),
    yaxis2=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
    ),
    yaxis3=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
    ),
    showlegend=True,
    plot_bgcolor='white'
)
plot(fig_impact_confirmed_finance, filename = 'Finance/impact_confirmed.html')

# Impact des morts 
fig_impact_deaths_finance = px.scatter(df, x = 'Deaths', y = 'Price', animation_frame = 'Date', animation_group = 'Name', color = 'Name', hover_name = 'Name', size = 'Size', size_max = 25, facet_col = 'Asset class', range_x = [0, df['Deaths'].max() + 10000], range_y = [df['Price'].min(), df['Price'].max()])
fig_impact_deaths_finance['layout'].update(
    font=dict(
        family='Montserrat',
        size=15,
        color='rgb(87, 88, 90)',
        
        ),
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=3,
        ticks='outside',
    ),
    xaxis2=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=3,
        ticks='outside',
    ),
    xaxis3=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=3,
        ticks='outside',
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
    ),
    yaxis2=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
    ),
    yaxis3=dict(
        showgrid=True,
        gridcolor='lightgray',
        showline=False,
        showticklabels=True,
    ),
    showlegend=True,
    plot_bgcolor='white'
)
plot(fig_impact_deaths_finance, filename = 'Finance/impact_deaths.html')

### Stock Market Returns, 2020 vs. Past Recessions

data = yf.download('^DJI')['Adj Close']

ret_now = data.loc['2020-01-30':].pct_change()[1:]
ret_2007_2009 = data.loc['2007-01-03':'2009-12-31'].pct_change()[1:]

fig = go.Figure()
fig.add_trace(go.Scatter(x = [1:754], y = ret_now, mode = 'lines', name = 'ret'))
fig.add_trace(go.Scatter(x = [1:754], y = ret_now, mode = 'lines', name = 'ret'))
plot(fig)





