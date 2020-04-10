import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from apps import GetData
from apps import graph 
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.express as px
from app import app
from datetime import datetime, timedelta
import time


# Confirmed
df_confirmed_world = GetData.get_world('confirmed')
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

fig1 = {
    "data": [],
    "layout": {},
    "frames": []
}

print_date = datetime.strptime(date, '%Y-%m-%d').date()
print_date = (print_date.strftime("%a") + ' ' +  print_date.strftime("%b") + ' ' + print_date.strftime("%d") + ' ' + print_date.strftime("%Y")).upper()

fig1['layout']['sliders'] = {
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

fig1["layout"]["updatemenus"] = [
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

df_sub = df_confirmed_world_duplicate[df_confirmed_world_duplicate['Date'] == date]

data_dict = dict(
    type = 'scattergeo',
    lon = df_sub['Long'],
    lat = df_sub['Lat'],
    text = df_sub['text'],
    marker = dict(
        size = df_sub['Number']/100,
        color = 'rgb(255, 152, 1)',
        line_color = 'rgb(40,40,40)',
        line_width = 0.5,
        sizemode = 'area'))
    
fig1["data"].append(data_dict)


fig1["layout"]["sliders"] = [sliders_dict]

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
            color = 'rgb(255, 152, 1)',
            line_color = 'rgb(40,40,40)',
            line_width = 0.5,
            sizemode = 'area'))
        
    frame['data'].append(data_dict)
        
    fig1["frames"].append(frame)
    slider_step = {"args": [
        [date],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": date,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)
    
fig1["layout"]["sliders"] = [sliders_dict]
fig1['layout']['geo'] = dict(
        showland = True,        
        landcolor = "rgb(64, 64, 64)",
        showlakes = True,
        lakecolor = "rgb(64, 64, 64)",
        showsubunits = True,
        subunitcolor = "rgb(255, 255, 255)",
        showcountries = True,
        countrycolor = "rgb(255, 255, 255)",
        showocean = True,
        oceancolor = "rgb(255, 255, 255)")

# Recovered
df_recovered_world = GetData.get_world('recovered')
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

fig2 = {
    "data": [],
    "layout": {},
    "frames": []
}

print_date = datetime.strptime(date, '%Y-%m-%d').date()
print_date = (print_date.strftime("%a") + ' ' +  print_date.strftime("%b") + ' ' + print_date.strftime("%d") + ' ' + print_date.strftime("%Y")).upper()


fig2['layout']['sliders'] = {
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

fig2["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "⯈",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
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
fig2["data"].append(data_dict)

fig2["layout"]["sliders"] = [sliders_dict]

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
  
    fig2["frames"].append(frame)
    slider_step = {"args": [
        [date],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": date,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)
    
fig2["layout"]["sliders"] = [sliders_dict]
fig2['layout']['geo'] = dict(
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
# Deaths
df_deaths_world = GetData.get_world('deaths')
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

fig3 = {
    "data": [],
    "layout": {},
    "frames": []
}

print_date = datetime.strptime(date, '%Y-%m-%d').date()
print_date = (print_date.strftime("%a") + ' ' +  print_date.strftime("%b") + ' ' + print_date.strftime("%d") + ' ' + print_date.strftime("%Y")).upper()

fig3['layout']['sliders'] = {
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

fig3["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "⯈",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
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

df_sub = df_deaths_world_duplicate[df_deaths_world_duplicate['Date'] == date]

data_dict = dict(
    type = 'scattergeo',
    lon = df_sub['Long'],
    lat = df_sub['Lat'],
    text = df_sub['text'],
    marker = dict(
        size = df_sub['Number']/100,
        color = 'lightskyblue',
        line_color = 'rgb(40,40,40)',
        line_width = 0.5,
        sizemode = 'area'))
    
fig3["data"].append(data_dict)

fig3["layout"]["sliders"] = [sliders_dict]

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
            color = 'lightskyblue',
            line_color = 'rgb(40,40,40)',
            line_width = 0.5,
            sizemode = 'area'))
        
    frame['data'].append(data_dict)
        
    fig3["frames"].append(frame)
    slider_step = {"args": [
        [date],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": date,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)
    
fig3["layout"]["sliders"] = [sliders_dict]
fig3['layout']['geo'] = dict(
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



 
                       


#DATA


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

#def
layout = html.Div([  dcc.Graph(figure=fig1,id='dbleMap2',style={"height":"800px"})
                        ])
        
# #CALLBACKS
# @app.callback(
#     Output('dbleMap2','figure'),
#     [Input('radiochoice2','value')]
# )
# def show_graph(value,fig1=fig1,fig2=fig2,fig3=fig3):
#     if value == 1:
#         return fig1
#     elif value == 2:
#         return fig2
#     else:
#         return fig3