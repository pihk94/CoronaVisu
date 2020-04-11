from GetData import * 
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

#### Tableaux récapitulatifs ####

#date = 'today' #date = '3/25/20'
#previous = 1 #previous = 5
#df_recap_by_country = get_recap_by_country(date, previous)
#df_recap_by_continent = get_recap_by_continent(date, previous)

#### Graphiques des tendances "Confirmed", "Deaths", "Recovered" pour le monde, par continent et par pays (top 10)

df_confirmed_world = get_world('confirmed')
df_deaths_world = get_world('deaths')
df_recovered_world = get_world('recovered')

## World
df_trend_world = pd.DataFrame()
df_trend_world['Date'] = pd.to_datetime(df_confirmed_world.iloc[:,5:].columns)
df_trend_world['Confirmed'] = df_confirmed_world.iloc[:,5:].sum().values
df_trend_world['Recovered'] = df_recovered_world.iloc[:,5:].sum().values
df_trend_world['Deaths'] = df_deaths_world.iloc[:,5:].sum().values
df_trend_world['Active Cases'] = df_trend_world['Confirmed'] - df_trend_world['Recovered'] - df_trend_world['Deaths']

labels = ['Confirmed', 'Recovered', 'Deaths', 'Active Cases']
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)']
line_size = [4, 4, 4, 4]

fig_trend_world = go.Figure()
for i in range(4):
    fig_trend_world.add_trace(go.Scatter(x=df_trend_world['Date'], y=df_trend_world.iloc[:,i+1], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_world.update_layout(
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
                            
plot(fig_trend_world, filename = 'World Recap/world_cases_trend.html')

## Continent                                 
df_trend_continent_confirmed = df_confirmed_world.groupby('Continent').sum().iloc[:,2:].T
df_trend_continent_confirmed.index = pd.to_datetime(df_trend_continent_confirmed.index)
df_trend_continent_recovered = df_recovered_world.groupby('Continent').sum().iloc[:,2:].T
df_trend_continent_recovered.index = pd.to_datetime(df_trend_continent_recovered.index)
df_trend_continent_deaths = df_deaths_world.groupby('Continent').sum().iloc[:,2:].T
df_trend_continent_deaths.index = pd.to_datetime(df_trend_continent_deaths.index)
df_trend_continent_active_cases = df_trend_continent_confirmed - df_trend_continent_recovered - df_trend_continent_deaths

labels = df_trend_continent_confirmed.columns
colors = ['rgb(44, 62, 80)', 'rgb(84, 153, 199)', 'rgb(244, 208, 63)', 'rgb(192, 57, 43)', 'rgb(154, 14, 14)', 'rgb(100, 145, 122)']
line_size = [4, 4, 4, 4, 4, 4]

# Confirmed
fig_trend_continent_confirmed = go.Figure()
for i in range(6):
    fig_trend_continent_confirmed.add_trace(go.Scatter(x=df_trend_continent_confirmed.index, y=df_trend_continent_confirmed.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_confirmed.update_layout(
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
                         
plot(fig_trend_continent_confirmed, filename = 'World Recap/continent_confirmed_cases.html')

# Active Cases
fig_trend_continent_active_cases = go.Figure()
for i in range(6):
    fig_trend_continent_active_cases.add_trace(go.Scatter(x=df_trend_continent_active_cases.index, y=df_trend_continent_active_cases.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_active_cases.update_layout(
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
                      
plot(fig_trend_continent_active_cases, filename = 'World Recap/continent_active_cases.html')

# Deaths
fig_trend_continent_deaths = go.Figure()
for i in range(6):
    fig_trend_continent_deaths.add_trace(go.Scatter(x=df_trend_continent_deaths.index, y=df_trend_continent_deaths.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_deaths.update_layout(
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
                           
plot(fig_trend_continent_deaths, filename = 'World Recap/continent_deaths.html')           

# Recovered
fig_trend_continent_recovered = go.Figure()
for i in range(6):
    fig_trend_continent_recovered.add_trace(go.Scatter(x=df_trend_continent_recovered.index, y=df_trend_continent_recovered.iloc[:,i], mode='lines',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i])))
    
fig_trend_continent_recovered.update_layout(
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
                        
plot(fig_trend_continent_recovered, filename = 'World Recap/continent_recovered_cases.html')   

## Pays
df_trend_country_confirmed = df_confirmed_world.groupby('Country/Region').sum().iloc[:,2:].T
df_trend_country_confirmed = df_trend_country_confirmed[df_trend_country_confirmed.iloc[-1].sort_values(ascending = False).index[0:10].values]
df_trend_country_confirmed.index = pd.to_datetime(df_trend_continent_confirmed.index)
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
                      
plot(fig_trend_country_confirmed, filename = 'World Recap/country_confirmed_cases.html')

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
                         
plot(fig_trend_country_active_cases, filename = 'World Recap/country_active_cases.html')

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
                         
plot(fig_trend_country_deaths, filename = 'World Recap/country_deaths_cases.html')           

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
                          
plot(fig_trend_country_recovered, filename = 'World Recap/country_recovered_cases.html')       

#### Cartes Map : Evolution du nombre de cas confirmés, de morts et de recovered avec animation

# Confirmed
df_confirmed_world = get_world('confirmed')
lst = []
for i in range(df_confirmed_world.shape[0]):
    for j in range(5, df_confirmed_world.shape[1]):
        lst += [(df_confirmed_world.iloc[i,0], df_confirmed_world.iloc[i,1], df_confirmed_world.iloc[i,2], df_confirmed_world.iloc[i,3], df_confirmed_world.iloc[i,4], df_confirmed_world.columns[j], df_confirmed_world.iloc[i,j])]
df_confirmed_world_duplicate = pd.DataFrame(lst, columns=['Continent', 'Country/Region', 'Province/State', 'Lat', 'Long', 'Date', 'Number'])
df_confirmed_world_duplicate['text'] = df_confirmed_world_duplicate['Province/State'].fillna(df_confirmed_world_duplicate['Country/Region']) + '<br>Confirmés: ' + (df_confirmed_world_duplicate['Number']).astype(str)

limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
countries = []

df_confirmed_world_duplicate['Date'] = pd.to_datetime(df_confirmed_world_duplicate['Date']).astype('str')

dates = list(df_confirmed_world_duplicate['Date'].unique())
date = min(dates)

fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

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
                "args": [None, {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "⯈",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "⯀",
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
        "font": {"size": 15, "family" : "Montserrat"},
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

df_sub = df_confirmed_world_duplicate[df_confirmed_world_duplicate['Date'] == date]

data_dict = dict(
    type = 'scattergeo',
    lon = df_sub['Long'],
    lat = df_sub['Lat'],
    text = df_sub['text'],
    marker = dict(
        size = df_sub['Number']/100,
        color = 'crimson',
        line_color = 'rgb(40,40,40)',
        line_width = 0.5,
        sizemode = 'area'))
    
fig_dict["data"].append(data_dict)


fig_dict["layout"]["sliders"] = [sliders_dict]

for date in dates:
    frame = {"data": [], "name": str(date)}

    df_sub = df_confirmed_world_duplicate[df_confirmed_world_duplicate['Date'] == date]
        
    data_dict = dict(
        type ='scattergeo',
        lon = df_sub['Long'],
        lat = df_sub['Lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['Number']/100,
            sizemin = 3,
            color = 'crimson',
            line_color = 'rgb(40,40,40)',
            line_width = 0.5,
            sizemode = 'area'))
        
    frame['data'].append(data_dict)
        
    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [date],
        {"frame": {"duration": 300, "redraw": True},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": date,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)
    
fig_dict["layout"]["sliders"] = [sliders_dict]
fig_dict['layout']['geo'] = dict(
        showland = True,        
        landcolor = "rgb(25, 25, 25)",
        showlakes = True,
        lakecolor = "rgb(25, 25, 25)",
        showsubunits = True,
        subunitcolor = "rgb(60, 60, 60)",
        showcountries = True,
        countrycolor = "rgb(100, 100, 100)",
        showocean = True,
        oceancolor = "rgb(60, 60, 60)")

plot(fig_dict, False, filename = 'World Recap/confirmed_map.html')

# Recovered
df_recovered_world = get_world('recovered')
lst = []
for i in range(df_recovered_world.shape[0]):
    for j in range(5, df_recovered_world.shape[1]):
        lst += [(df_recovered_world.iloc[i,0], df_recovered_world.iloc[i,1], df_recovered_world.iloc[i,2], df_recovered_world.iloc[i,3], df_recovered_world.iloc[i,4], df_recovered_world.columns[j], df_recovered_world.iloc[i,j])]
df_recovered_world_duplicate = pd.DataFrame(lst, columns=['Continent', 'Country/Region', 'Province/State', 'Lat', 'Long', 'Date', 'Number'])
df_recovered_world_duplicate['text'] = df_recovered_world_duplicate['Province/State'].fillna(df_recovered_world_duplicate['Country/Region']) + '<br>Confirmés: ' + (df_recovered_world_duplicate['Number']).astype(str)

limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
countries = []

df_recovered_world_duplicate['Date'] = pd.to_datetime(df_recovered_world_duplicate['Date']).astype('str')

dates = list(df_recovered_world_duplicate['Date'].unique())
date = min(dates)

fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

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
                "args": [None, {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "⯈",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "⯀",
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
        "font": {"size": 15, "family" : "Montserrat"},
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

df_sub = df_recovered_world_duplicate[df_recovered_world_duplicate['Date'] == date]

data_dict = dict(
    type = 'scattergeo',
    lon = df_sub['Long'],
    lat = df_sub['Lat'],
    text = df_sub['text'],
    marker = dict(
        size = df_sub['Number']/100,
        color = 'lightgreen',
        line_color = 'rgb(40,40,40)',
        line_width = 0.5,
        sizemode = 'area')) 
fig_dict["data"].append(data_dict)

fig_dict["layout"]["sliders"] = [sliders_dict]

for date in dates:
    frame = {"data": [], "name": str(date)}
    
    df_sub = df_recovered_world_duplicate[df_recovered_world_duplicate['Date'] == date]
        
    data_dict = dict(
        type ='scattergeo',
        lon = df_sub['Long'],
        lat = df_sub['Lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['Number']/100,
            sizemin = 3,
            color = 'lightgreen',
            line_color = 'rgb(40,40,40)',
            line_width = 0.5,
            sizemode = 'area'))
        
    frame['data'].append(data_dict)
  
    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [date],
        {"frame": {"duration": 300, "redraw": True},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": date,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)
    
fig_dict["layout"]["sliders"] = [sliders_dict]
fig_dict['layout']['geo'] = dict(
        showland = True,        
        landcolor = "rgb(25, 25, 25)",
        showlakes = True,
        lakecolor = "rgb(25, 25, 25)",
        showsubunits = True,
        subunitcolor = "rgb(60, 60, 60)",
        showcountries = True,
        countrycolor = "rgb(100, 100, 100)",
        showocean = True,
        oceancolor = "rgb(60, 60, 60)")
plot(fig_dict, False, filename = 'World Recap/recovered_map.html')

# Deaths
df_deaths_world = get_world('deaths')
lst = []
for i in range(df_deaths_world.shape[0]):
    for j in range(5, df_deaths_world.shape[1]):
        lst += [(df_deaths_world.iloc[i,0], df_deaths_world.iloc[i,1], df_deaths_world.iloc[i,2], df_deaths_world.iloc[i,3], df_deaths_world.iloc[i,4], df_deaths_world.columns[j], df_deaths_world.iloc[i,j])]
df_deaths_world_duplicate = pd.DataFrame(lst, columns=['Continent', 'Country/Region', 'Province/State', 'Lat', 'Long', 'Date', 'Number'])
df_deaths_world_duplicate['text'] = df_deaths_world_duplicate['Province/State'].fillna(df_deaths_world_duplicate['Country/Region']) + '<br>Confirmés: ' + (df_deaths_world_duplicate['Number']).astype(str)

limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
countries = []

df_deaths_world_duplicate['Date'] = pd.to_datetime(df_deaths_world_duplicate['Date']).astype('str')

dates = list(df_deaths_world_duplicate['Date'].unique())
date = min(dates)

fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

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
                "args": [None, {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "⯈",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "⯀",
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
        "font": {"size": 15, "family" : "Montserrat"},
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

df_sub = df_deaths_world_duplicate[df_deaths_world_duplicate['Date'] == date]

data_dict = dict(
    type = 'scattergeo',
    lon = df_sub['Long'],
    lat = df_sub['Lat'],
    text = df_sub['text'],
    marker = dict(
        size = df_sub['Number']/100,
        color = 'lightgreen',
        line_color = 'rgb(40,40,40)',
        line_width = 0.5,
        sizemode = 'area')) 
fig_dict["data"].append(data_dict)

fig_dict["layout"]["sliders"] = [sliders_dict]

for date in dates:
    frame = {"data": [], "name": str(date)}
    
    df_sub = df_deaths_world_duplicate[df_deaths_world_duplicate['Date'] == date]
        
    data_dict = dict(
        type ='scattergeo',
        lon = df_sub['Long'],
        lat = df_sub['Lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['Number']/100,
            sizemin = 3,
            color = 'lightgreen',
            line_color = 'rgb(40,40,40)',
            line_width = 0.5,
            sizemode = 'area'))
        
    frame['data'].append(data_dict)
  
    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [date],
        {"frame": {"duration": 300, "redraw": True},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": date,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)
    
fig_dict["layout"]["sliders"] = [sliders_dict]
fig_dict['layout']['geo'] = dict(
        showland = True,        
        landcolor = "rgb(25, 25, 25)",
        showlakes = True,
        lakecolor = "rgb(25, 25, 25)",
        showsubunits = True,
        subunitcolor = "rgb(60, 60, 60)",
        showcountries = True,
        countrycolor = "rgb(100, 100, 100)",
        showocean = True,
        oceancolor = "rgb(60, 60, 60)")
plot(fig_dict, False, filename = 'World Recap/deaths_map.html')