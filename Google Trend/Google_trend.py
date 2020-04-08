# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 13:23:03 2020

@author: eleon
"""
from pytrends.request import TrendReq
import plotly.graph_objects as go
from plotly.offline import plot

def google_trend_graph(w):
    pytrend = TrendReq()

    pytrend = TrendReq()
    lst = [w]
    pytrend.build_payload(kw_list=lst, timeframe='today 12-m')

    interest_w = pytrend.interest_over_time() 
    interest_w = interest_w.reset_index()

    fig_trend_w = go.Figure()
    for i in range(1):
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
                            text='<b>GOOGLE RESEARCH INTERESTS FOR {}</b>'.format(w.upper()),
                            font=dict(family='Arial',
                            size=40,
                            color='rgb(37, 37, 37)'),
                            showarrow=False))
                              
    fig_trend_w.update_layout(annotations=annotations)                             
    plot(fig_trend_w, filename = 'google_trend_{}.html'.format(w))
    return fig_trend_w

fig = google_trend_graph('nintendo switch')
