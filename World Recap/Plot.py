from GetData import * 
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd

#### Tableaux récapitulatifs ####
date = 'today' #date = '3/25/20'
previous = 1 #previous = 5
df_recap_by_country = get_recap_by_country(date, previous)
df_recap_by_continent = get_recap_by_continent(date, previous)

#### Graphiques tendances "Confirmed", "Deaths", "Recovered" en normal et en logarithmique
df_confirmed_world = clean_df('confirmed')
df_deaths_world = clean_df('deaths')
df_recovered_world = clean_df('recovered')
df_trend_world = pd.DataFrame()
df_trend_world['Date'] = df_confirmed_world.iloc[:,5:].columns
df_trend_world['Confirmed'] = df_confirmed_world.iloc[:,5:].sum().values
df_trend_world['Recovered'] = df_recovered_world.iloc[:,5:].sum().values
df_trend_world['Active Cases'] = df_trend_world['Confirmed'] - df_trend_world['Recovered']
df_trend_world['Deaths'] = df_deaths_world.iloc[:,5:].sum().values

title = 'Tendances'
labels = ['Confirmed', 'Recovered', 'Active Cases', 'Deaths']
colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

mode_size = [8, 8, 12, 8]
line_size = [2, 2, 4, 2]

fig = go.Figure()

for i in range(0, 4):
    fig.add_trace(go.Scatter(x=df_trend_world['Date'], y=df_trend_world.iloc[:,i+1], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
    ))

    # endpoints
    fig.add_trace(go.Scatter(
        x=[x_data[i][0], x_data[i][-1]],
        y=[y_data[i][0], y_data[i][-1]],
        mode='markers',
        marker=dict(color=colors[i], size=mode_size[i])
    ))

fig.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=False,
    plot_bgcolor='white'
)

annotations = []

# Adding labels
for y_trace, label, color in zip(y_data, labels, colors):
    # labeling the left_side of the plot
    annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                  xanchor='right', yanchor='middle',
                                  text=label + ' {}%'.format(y_trace[0]),
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))
    # labeling the right_side of the plot
    annotations.append(dict(xref='paper', x=0.95, y=y_trace[11],
                                  xanchor='left', yanchor='middle',
                                  text='{}%'.format(y_trace[11]),
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))
# Title
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='Main Source for News',
                              font=dict(family='Arial',
                                        size=30,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Source: PewResearch Center & ' +
                                   'Storytelling with data',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))

fig.update_layout(annotations=annotations)

fig.show()




