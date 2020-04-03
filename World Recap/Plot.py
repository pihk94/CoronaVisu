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





#### Cartes Map : Evolution du nombre de cas confirmés, de morts et de recovery avec animation

df_confirmed_world = get_world('confirmed')

mapping = get_mappings(URL_MAPPING_COUNTRIES)
df_cases_world = get_frame('confirmed')
df_cases_world.rename(columns = {'Country/Region' : 'Country'}, inplace = True)
df_cases_world = df_cases_world.merge(mapping['df'], on = 'Country')
df_cases_world['region'] = df_cases_world['Province/State'].fillna(df_cases_world['Country'])

lst = []
for pays in df_confirmed_world['Country/Region'].unique():
    for col in df_confirmed_world.columns[5:]:
        continent = df_confirmed_world.set_index(')
        nb = df_cases_world.set_index('region')[col][pays]
        continent = df_cases_world.set_index('region')['Continent'][pays]
        lat = df_cases_world.set_index('region')['Lat'][pays]
        lon = df_cases_world.set_index('region')['Long'][pays]
        lst += [(pays,col,nb,continent,lat,lon)]
df_ = pd.DataFrame(lst, columns=['region', 'date', 'nombre', 'continent', 'lat', 'lon'])
df_.replace(-1, 0, inplace = True)


lst = []


df_['text'] = df_['region'] + '<br>Confirmés: ' + (df_['nombre']).astype(str)
limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey","lightskyblue"]
countries = []

continents = df_['continent'].unique()

df_['date'] = pd.to_datetime(df_['date']).astype('str')

dates = list(df_['date'].unique())
date = min(dates)

#make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

#fill in most of layout
print_date = datetime.strptime(date, '%Y-%m-%d').date()
print_date = (print_date.strftime("%a") + ' ' +  print_date.strftime("%b") + ' ' + print_date.strftime("%d") + ' ' + print_date.strftime("%Y")).upper()

fig_dict['layout']['title'] = '<b> EVOLUTION OF THE NUMBER OF CONFIRMED CASES SINCE ' + print_date +'</b>'
fig_dict['layout']['titlefont'] = dict(family='Arial', size=35, color='rgb(37, 37, 37)')
fig_dict['layout']['legend_title'] ='<b> Continents </b>'

fig_dict['layout']['sliders'] = {
    'args': [
        'transition', {
            'duration':400,
            'easing':'cubic-in-out'
        }
    ],
    'initialValue': date,
    'plotlycommand': 'animate',
    'values': dates,
    'visible': True
}

fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]
     
sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Date : ",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

j=0
for continent in continents:
    df_sub = df_[(df_['date'] == date) & (df_['continent'] == continent)]

    data_dict = dict(
        type='scattergeo',
        lon= df_sub['lon'],
        lat= df_sub['lat'],
        text= df_sub['text'],
        marker= dict(
            size = df_sub['nombre']/100,
            color = colors[j],
            line_color = 'rgb(40,40,40)',
            line_width = 0.5,
            sizemode = 'area'),
         name= continent)
    
    fig_dict["data"].append(data_dict)
    j+=1

fig_dict["layout"]["sliders"] = [sliders_dict]

# make frames
for date in dates:
    frame = {"data": [], "name": str(date)}
    j=0
    for continent in continents:
        df_sub = df_[(df_['date'] == date) & (df_['continent'] == continent)]
        
        data_dict = dict(
            type='scattergeo',
            lon= df_sub['lon'],
            lat= df_sub['lat'],
            text= df_sub['text'],
            marker= dict(
                size = df_sub['nombre']/100,
                sizemin = 3,
                color = colors[j],
                line_color = 'rgb(40,40,40)',
                line_width = 0.5,
                sizemode = 'area'),
            name= continent)
        
        frame['data'].append(data_dict)
        j+=1
        
    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [date],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": date,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)
    
fig_dict["layout"]["sliders"] = [sliders_dict]
fig_dict['layout']['geo'] = dict(
        showland = True,        
        landcolor = "rgb(212, 212, 212)",
        showlakes = True,
        lakecolor = "rgb(255, 255, 255)",
        showsubunits = True,
        subunitcolor = "rgb(255, 255, 255)",
        showcountries = True,
        countrycolor = "rgb(255, 255, 255)")
plot(fig_dict, False, filename = 'World Recap/confirmed_map.html')  
                       
                                 




