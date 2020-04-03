# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 13:23:03 2020

@author: eleon
"""

import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
from datetime import datetime, date, time
import plotly.graph_objects as go

pytrend = TrendReq()

# Interest by region: dans quelles régions le mot 'Coronavirus' a le plus de recherches
pytrend.build_payload(kw_list=['Coronavirus'])
df = pytrend.interest_by_region()
df = df.sort_values(by=['Coronavirus'], ascending=False)
df = df[:53]
df = df.reset_index()
#plt.bar(df.index, df.Coronavirus)
df.columns = ['country', 'Trend']
df2 = px.data.gapminder()[['country', 'iso_alpha']].drop_duplicates()
df = df.merge(df2, on='country')

fig = px.choropleth(df, locations="iso_alpha", color="Trend", hover_name="country", color_continuous_scale='Blues')
fig.update_layout(
    title="GOOGLE RESEARCH INTERESTS FOR CORONAVIRUS",
    titlefont=dict(family='Arial',
              size=40,
              color='rgb(37, 37, 37)'))
plot(fig, filename = 'google_trend_bycountry.html')


# Evolution des recherches coronavirus sur un an
pytrend = TrendReq()
lst_corona = ['coronavirus']
pytrend.build_payload(kw_list=lst_corona, timeframe='today 12-m')

interest_corona = pytrend.interest_over_time() 
interest_corona = interest_corona.reset_index()

fig_trend_corona = go.Figure()
for i in range(1):
    fig_trend_corona.add_trace(go.Scatter(x=interest_corona['date'], y=interest_corona.iloc[:,i+1], mode='lines', name=lst_corona[i]))
    
fig_trend_corona.update_layout(
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
                              text='<b>GOOGLE RESEARCH INTERESTS FOR CORONAVIRUS</b>',
                              font=dict(family='Arial',
                                        size=40,
                                        color='rgb(37, 37, 37)'),
                              showarrow=False))
                              
fig_trend_corona.update_layout(annotations=annotations)                             
plot(fig_trend_corona, filename = 'google_trend_corona.html')



# Comparaison symptomes corona vs grippe vs allergies
pytrend = TrendReq()
lst_symptoms = ['coronavirus symptoms', 'flu symptoms', 'allergies symptoms']
pytrend.build_payload(kw_list=lst_symptoms, timeframe='today 12-m')

interest_symptoms = pytrend.interest_over_time() 
interest_symptoms = interest_symptoms.reset_index()

fig_trend_symptoms = go.Figure()
for i in range(3):
    fig_trend_symptoms.add_trace(go.Scatter(x=interest_symptoms['date'], y=interest_symptoms.iloc[:,i+1], mode='lines', name=lst_symptoms[i]))
    
fig_trend_symptoms.update_layout(
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
                              text='<b>GOOGLE RESEARCH INTERESTS FOR SYMPTOMS</b>',
                              font=dict(family='Arial',
                                        size=40,
                                        color='rgb(37, 37, 37)'),
                              showarrow=False))
                              
fig_trend_symptoms.update_layout(annotations=annotations)                             
plot(fig_trend_symptoms, filename = 'google_trend_symptoms.html')



# Evolution des recherches hand sanitizer, face mask, quarantine, social distancing sur un an
pytrend = TrendReq()
lst_related_topics = ['hand sanitizer', 'face mask', 'quarantine', 'social distancing']
pytrend.build_payload(kw_list=lst_related_topics, timeframe='today 12-m')

interest_related_topics = pytrend.interest_over_time() 
interest_related_topics = interest_related_topics.reset_index()

fig_trend_related_topics = go.Figure()
for i in range(4):
    fig_trend_related_topics.add_trace(go.Scatter(x=interest_related_topics['date'], y=interest_related_topics.iloc[:,i+1], mode='lines', name=lst_related_topics[i]))
    
fig_trend_related_topics.update_layout(
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
                              text='<b>GOOGLE RESEARCH INTERESTS FOR CORONAVIRUS RELATED TOPICS</b>',
                              font=dict(family='Arial',
                                        size=40,
                                        color='rgb(37, 37, 37)'),
                              showarrow=False))
                              
fig_trend_related_topics.update_layout(annotations=annotations)                             
plot(fig_trend_related_topics, filename = 'google_trend_related topics.html')
