from GetData import * 
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd

#### Tableaux récapitulatifs ####

date = 'today' #date = '3/25/20'
previous = 1 #previous = 5
df_recap_by_country = get_recap_by_country(date, previous)
df_recap_by_continent = get_recap_by_continent(date, previous)

#### Graphiques des tendances "Confirmed", "Deaths", "Recovered" pour le monde, par continent et par pays (top 10)

df_confirmed_world = get_world('confirmed')
df_deaths_world = get_world('deaths')
df_recovered_world = get_world('recovered')

## World
df_trend_world = pd.DataFrame()
df_trend_world['Date'] = pd.to_datetime(df_confirmed_world.iloc[:,5:].columns)
df_trend_world['Confirmed'] = df_confirmed_world.iloc[:,5:].sum().values
df_trend_world['Recovered'] = df_recovered_world.iloc[:,5:].sum().values
df_trend_world['Active Cases'] = df_trend_world['Confirmed'] - df_trend_world['Recovered']
df_trend_world['Deaths'] = df_deaths_world.iloc[:,5:].sum().values

labels = ['Confirmed', 'Recovered', 'Active Cases', 'Deaths']
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)']
line_size = [4, 4, 4, 4]

fig_trend_world = go.Figure()
for i in range(0, 4):
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

annotations = []
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='<b>WORLD CASES TRENDING</b>',
                              font=dict(family='Arial',
                                        size=40,
                                        color='rgb(37, 37, 37)'),
                              showarrow=False))
                              
fig_trend_world.update_layout(annotations=annotations)                             
plot(fig_trend_world, filename = 'world_cases_trend.html')

## Continent                                 
df_trend_continent_confirmed = df_confirmed_world.groupby('Continent').sum().iloc[:,2:].T
df_trend_continent_confirmed.index = pd.to_datetime(df_trend_continent_confirmed.index)
df_trend_continent_recovered = df_recovered_world.groupby('Continent').sum().iloc[:,2:].T
df_trend_continent_recovered.index = pd.to_datetime(df_trend_continent_recovered.index)
df_trend_continent_active_cases = df_trend_continent_confirmed - df_trend_continent_recovered
df_trend_continent_deaths = df_deaths_world.groupby('Continent').sum().iloc[:,2:].T
df_trend_continent_deaths.index = pd.to_datetime(df_trend_continent_deaths.index)

labels = df_trend_continent_confirmed.columns
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)', 'rgb(154, 14, 14)', 'rgb(100, 145, 122)']
line_size = [4, 4, 4, 4, 4, 4]

# Confirmed
fig_trend_continent_confirmed = go.Figure()
for i in range(0, 6):
    fig_trend_continent_confirmed.add_trace(go.Scatter(x=df_trend_continent_confirmed.index, y=df_trend_continent_confirmed.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_confirmed.update_layout(
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
                              text='<b>NUMBER OF CONFIRMED CASES BY CONTINENT</b>',
                              font=dict(family='Arial',
                                        size=40,
                                        color='rgb(37, 37, 37)'),
                              showarrow=False))
                              
fig_trend_continent_confirmed.update_layout(annotations=annotations)                             
plot(fig_trend_continent_confirmed, filename = 'continent_confirmed_cases.html')

# Active Cases
fig_trend_continent_active_cases = go.Figure()
for i in range(0, 6):
    fig_trend_continent_active_cases.add_trace(go.Scatter(x=df_trend_continent_active_cases.index, y=df_trend_continent_active_cases.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_active_cases.update_layout(
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
                              text='<b>NUMBER OF ACTIVE CASES BY CONTINENT</b>',
                              font=dict(family='Arial',
                                        size=40,
                                        color='rgb(37, 37, 37)'),
                              showarrow=False))
                              
fig_trend_continent_active_cases.update_layout(annotations=annotations)                             
plot(fig_trend_continent_active_cases, filename = 'continent_active_cases.html')

# Deaths
fig_trend_continent_deaths = go.Figure()
for i in range(0, 6):
    fig_trend_continent_deaths.add_trace(go.Scatter(x=df_trend_continent_deaths.index, y=df_trend_continent_deaths.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_deaths.update_layout(
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
                              text='<b>NUMBER OF DEATHS CASES BY CONTINENT</b>',
                              font=dict(family='Arial',
                                        size=40,
                                        color='rgb(37, 37, 37)'),
                              showarrow=False))
                              
fig_trend_continent_deaths.update_layout(annotations=annotations)                             
plot(fig_trend_continent_deaths, filename = 'continent_deaths_cases.html')           

# Recovered
fig_trend_continent_recovered = go.Figure()
for i in range(0, 6):
    fig_trend_continent_recovered.add_trace(go.Scatter(x=df_trend_continent_recovered.index, y=df_trend_continent_recovered.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_recovered.update_layout(
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
                              text='<b>NUMBER OF RECOVERED CASES BY CONTINENT</b>',
                              font=dict(family='Arial',
                                        size=40,
                                        color='rgb(37, 37, 37)'),
                              showarrow=False))
                              
fig_trend_continent_recovered.update_layout(annotations=annotations)                             
plot(fig_trend_continent_recovered, filename = 'continent_recovered_cases.html')                          
                                 




