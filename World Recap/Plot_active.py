# -*- coding: utf-8 -*-
from GetData import * 
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np
import pandas as pd
from datetime import datetime

URL_MAPPING_COUNTRIES = 'https://raw.githubusercontent.com/pratapvardhan/notebooks/master/covid19/mapping_countries.csv'

mapping = get_mappings(URL_MAPPING_COUNTRIES)

df_cases_world_confirmed = get_frame('confirmed')
df_cases_world_confirmed.rename(columns = {'Country/Region' : 'Country'}, inplace = True)
df_cases_world_confirmed = df_cases_world_confirmed.merge(mapping['df'], on = 'Country')
df_cases_world_confirmed['region'] = df_cases_world_confirmed['Province/State'].fillna(df_cases_world_confirmed['Country'])

df_cases_world_deaths = get_frame('deaths')
df_cases_world_deaths.rename(columns = {'Country/Region' : 'Country'}, inplace = True)
df_cases_world_deaths = df_cases_world_deaths.merge(mapping['df'], on = 'Country')
df_cases_world_deaths['region'] = df_cases_world_deaths['Province/State'].fillna(df_cases_world_deaths['Country'])

df_cases_world_recovered = get_frame('recovered')
df_cases_world_recovered.rename(columns = {'Country/Region' : 'Country'}, inplace = True)
df_cases_world_recovered = df_cases_world_recovered.merge(mapping['df'], on = 'Country')
df_cases_world_recovered['region'] = df_cases_world_recovered['Province/State'].fillna(df_cases_world_recovered['Country'])

lst = []
for pays in df_cases_world_confirmed.region.unique():
    for col in df_cases_world_confirmed.columns[4:-5]:
        nb_confirmed = df_cases_world_confirmed.set_index('region')[col][pays] 
        #nb_deaths = df_cases_world_deaths.set_index('region')[col][pays]
        if df_cases_world_recovered.region.isin([pays]).sum() != 0: 
            nb_recovered = df_cases_world_recovered.set_index('region')[col][pays]
        else:
            nb_recovered=0
        nb = nb_confirmed - nb_deaths - nb_recovered

        continent = df_cases_world_confirmed.set_index('region')['Continent'][pays]
        lat = df_cases_world_confirmed.set_index('region')['Lat'][pays]
        lon = df_cases_world_confirmed.set_index('region')['Long'][pays]
        lst += [(pays,col,nb,continent,lat,lon)]
df_ = pd.DataFrame(lst, columns=['region', 'date', 'nombre', 'continent', 'lat', 'lon'])
df_.replace(-1, 0, inplace = True)
df_
df_['text'] = df_['region'] + '<br>Active: ' + (df_['nombre']).astype(str)
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

fig_dict['layout']['title'] = '<b> EVOLUTION OF THE NUMBER OF ACTIVE CASES SINCE ' + print_date +'</b>'
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
            size = df_sub['nombre']/50,
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
                size = df_sub['nombre']/50,
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

plot(fig_dict, False, filename = 'World Recap/active_map.html')  

# comment retourner en arrière sur une date précise
# taille ronds légende



