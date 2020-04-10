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

#FCT
df  =GetData.get_world('confirmed')
def make_bars(country,df = df):
    
    t =df[(df['Country/Region'] == country)].groupby('Country/Region').sum()
    lst=  [list(t[col].values)[0] for col in t.columns if col not in ['Continent','Country/Region','Province/State','Lat','Long']]
    variation = [lst[i] -  lst[i-1] for i in range(1,len(lst))]
    color = {
        '0':{
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        '1-10':{
            'background':'rgba(255, 152, 0, 0.1)',
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        '10-100':{
            'background':'rgba(255, 152, 0, 0.4)',
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        '100-1000':{
            'background':'rgba(255, 152, 0, 0.7)',
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        '+1000':{
            'background':'rgba(255, 152, 0, 1)',
            'border-right':'1px solid rgba(255,255,255,0.5)',
            'width':'3px',
        },
        
    }
    render = []
    for val in variation:
        if val == 0:
            render.append(html.Div(style=color['0']))
        elif val >0 and val <10:
            render.append(html.Div(style=color['1-10']))
        elif val>= 10 and val < 100:
            render.append(html.Div(style=color['10-100']))
        elif val >=100 and val <1000:
            render.append(html.Div(style=color['100-1000']))
        elif val >=1000:
            render.append(html.Div(style=color['+1000']))
    return html.Div(render,className='d-flex',style={'height':'15px'})

#FIGURE
#### Cartes Map : Evolution du nombre de cas confirmés, de morts et de recovered avec animation
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

fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

print_date = datetime.strptime(date, '%Y-%m-%d').date()
print_date = (print_date.strftime("%a") + ' ' +  print_date.strftime("%b") + ' ' + print_date.strftime("%d") + ' ' + print_date.strftime("%Y")).upper()

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
                "args": [None, {"frame": {"duration": 500, "redraw":True},
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
        "font": {"size": 15,'family':'Montserrat'},
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
            color = 'rgb(255, 152, 1)',
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
        landcolor = "rgb(64, 64, 64)",
        showlakes = True,
        lakecolor = "rgb(64, 64, 64)",
        showsubunits = True,
        subunitcolor = "rgb(255, 255, 255)",
        showcountries = True,
        countrycolor = "rgb(255, 255, 255)",
        showocean = True,
        oceancolor = "rgb(255, 255, 255)")
fig1=fig_dict
df_recovered_world =  GetData.get_world('recovered')
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

print_date = datetime.strptime(date, '%Y-%m-%d').date()
print_date = (print_date.strftime("%a") + ' ' +  print_date.strftime("%b") + ' ' + print_date.strftime("%d") + ' ' + print_date.strftime("%Y")).upper()


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
                "args": [None, {"frame": {"duration": 500, "redraw":True},
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
        "font": {"size": 15,'family':'Montserrat'},
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
fig3=fig_dict

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

fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

print_date = datetime.strptime(date, '%Y-%m-%d').date()
print_date = (print_date.strftime("%a") + ' ' +  print_date.strftime("%b") + ' ' + print_date.strftime("%d") + ' ' + print_date.strftime("%Y")).upper()

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
        "font": {"size": 15,'family':'Montserrat'},
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
            color = 'lightskyblue',
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
fig2 =fig_dict


#DATA
dt = (datetime.now() - timedelta(2)).strftime('%d/%m/%Y')
df_recap=GetData.get_recap_by_country(dt,previous=5)
df_confirmed=GetData.get_world('confirmed')
confirmed=df_confirmed.iloc[:,-1].sum()
df_deaths=GetData.get_world('deaths')
deaths=df_deaths.iloc[:,-1].sum()
confirmedp=df_recap['Cases (+)'].sum(axis=0)
us_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="US"]):,}'
china_cases=f'{int(df_recap["Cases"][df_recap["Country/Region"]=="China"]):,}'
columns = ['Pays','Nouveaux Cas','Total des cas','Total décès','Nouveau décès','Mortalité','Rétabli']
df_H5=pd.DataFrame(columns=columns)
df_H5["Pays"]=x = ['{0}'.format(i) for i in df_recap["Country/Region"]]
df_H5["Total des cas"]=df_recap["Cases"]
df_H5["Total décès"]=df_recap["Deaths"]
df_H5["Mortalité"]=df_H5["Total décès"]/df_H5["Total des cas"]
df_H5["Total décès"]=df_recap["Deaths"]
df_H5["Rétabli"]=df_recap["Recovered"]
df_H5["Nouveaux cas"]=[f'{i:,}'for i in df_recap["Cases (+)"]]
df_H5["Nouveaux cas"]=["(+{0})".format(str(i)) for i in df_H5["Nouveaux cas"]]
df_H5["Nouveau décès"]=[f'{i:,}'for i in df_recap['Deaths (+)']]
df_H5["Nouveau décès"]=["(+{0})".format(str(i)) for i in df_H5["Nouveau décès"]]
df_H5["Mortalité"]=["{:.2%}".format(i) for i in df_H5["Mortalité"]]
df_H5["Rétabli"]=[f'{i:,}'for i in df_H5["Rétabli"]]
df_H5["Total des cas"]=[f'{i:,}'for i in df_H5["Total des cas"]]
df_H5["Total décès"]=[f'{i:,}'for i in df_H5["Total décès"]]

us_death =df_H5[df_H5.Pays == 'US']["Total décès"].values[0]
china_death =df_H5[df_H5.Pays == 'China']["Total décès"].values[0]
paysUE = ['Spain','Italy','France','Germany','United Kingdom','Belgium',
'Switzerland','Portugal','Norway','Denmark','Poland','Czechia','Romania',
'Luxembourg','Finland','Greece','Ukraine','Croatia','Moldova','Iceland','Lithuania',
]
fr_death = df_H5[df_H5.Pays=='France']["Total décès"].sum()
fr_confirm = df_H5[df_H5.Pays=='France']["Total des cas"].sum()



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
def recap_table(dt=dt,previous=5):
    df_recap=GetData.get_recap_by_country(dt,previous=previous)
    columns = ['Pays','Nouveaux Cas','Total des cas','Total décès','Nouveau décès','Mortalité','Rétabli']
    df_H5=pd.DataFrame(columns=columns)
    df_H5["Pays"]=x = ['{0}'.format(i) for i in df_recap["Country/Region"]]
    df_H5["Total des cas"]=df_recap["Cases"]
    df_H5["Total décès"]=df_recap["Deaths"]
    df_H5["Mortalité"]=df_H5["Total décès"]/df_H5["Total des cas"]
    df_H5["Total décès"]=df_recap["Deaths"]
    df_H5["Rétabli"]=df_recap["Recovered"]
    df_H5["Nouveaux cas"]=[f'{i:,}'for i in df_recap["Cases (+)"]]
    df_H5["Nouveaux cas"]=["(+{0})".format(str(i)) for i in df_H5["Nouveaux cas"]]
    df_H5["Nouveau décès"]=[f'{i:,}'for i in df_recap['Deaths (+)']]
    df_H5["Nouveau décès"]=["(+{0})".format(str(i)) for i in df_H5["Nouveau décès"]]
    df_H5["Mortalité"]=["{:.2%}".format(i) for i in df_H5["Mortalité"]]
    df_H5["Rétabli"]=[f'{i:,}'for i in df_H5["Rétabli"]]
    df_H5["Total des cas"]=[f'{i:,}'for i in df_H5["Total des cas"]]
    df_H5["Total décès"]=[f'{i:,}'for i in df_H5["Total décès"]]
    rows =[]
    for index,row in df_H5.head(20).iterrows():
        rows.append(html.Tr([html.Td(row.Pays,style={'font-weight':'bold','text-align':'left'}),
        html.Td(row['Total des cas'],style={'font-weight':'bolder'}),html.Td(row['Total décès']),html.Td(row['Mortalité'])],style={
            'border-bottom':'1px solid #e8e8e8'
        }))
    return [
        html.Thead([
            html.Tr(
                [
                    html.Th(
                    'COuntry',style={'text-align':'right','width':'180px'}
                    ),
                    html.Th(
                        'CASES',style ={
                            'text-align':'center',
                        }
                    ),
                    html.Th(
                        'DEATHS',style={
                            'text-align':'center',
                        }
                    ),
                    html.Th(
                        'MORTALITY',style={
                            'text-align':'center',
                        }
                    ),
                ],
                style = {
                    'border-bottom': '2px solid',
                    'text-transform':'uppercase',
                    "font-size":"14px"
                }
            )
        ]),
        html.Tbody(
            rows
        )
    ]


layout = html.Div([
    sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'50em'}),
                html.H4('COVID-19 GLOBAL CASES OVERVIEW',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','font-weight':'bolder','color':'rgb(87, 88, 90)','font-weight':'bolder'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(className='toprow',children=
            [
                dbc.Col(className='topRowCol1',children=
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H4('Total cases',style={'margin-top': '1em','font-weight':'bolder'}),
                                    html.Span(
                                        children='{:,}'.format(confirmed),style={'color':'rgb(255, 152, 1)','font-weight':'bolder'}
                                    )
                                ]
                                ,width=6,style={'padding':'0px','border-right':'1px solid black','height':'108px'}
                            ),
                            dbc.Col(
                                [
                                    html.H4('Total deaths',style={'margin-top': '1em','font-weight':'bolder'}),
                                    html.Span(
                                        children='{:,}'.format(deaths),style={'color':'red','font-weight':'bolder'}
                                    )
                                ]
                                ,width=6,style={'padding':'0px',}
                            )
                        ]
                    )
                    ,width=4,style={'padding-left':'0px',
                    'padding-right':'0px',}
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.Div('Updated on : '),
                                html.Span('{}'.format((datetime.now() - timedelta(1)).strftime('%d/%m/%Y')),style={'margin-left':'2px'})
                            ],className='justify-content-center',style={
                                'border-bottom':'1px solid black',
                                'color':'rgb(64, 64, 64)',
                                'font-weight': 'bolder'
                            }
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5('China',style={
                                            'font-weight':'bolder',
                                            'font-size':'1.15rem'
                                        }),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H6('Confirmed',style={
                                                            'font-weight':'550',
                                                            'font-size':'0.85rem'
                                                        }),
                                                        html.Span('{}'.format(china_cases),style={
                                                            'color':'rgb(255, 152, 1)',
                                                            'font-size':'15px'
                                                        })
                                                    ]
                                                ,width = 6),
                                                dbc.Col(
                                                    [
                                                        html.H6('Deaths',style={
                                                            'font-weight':'550',
                                                            'font-size':'0.85rem'
                                                        }),
                                                        html.Span('{}'.format(china_death),style={
                                                            'color':'red',
                                                            'font-size':'15px'
                                                        })
                                                    ]
                                                ,width = 6)
                                            ]
                                        )
                                    ]
                                    ,width=4,style={
                                        'border-right':'1px solid black'
                                    }),
                                dbc.Col(
                                    [
                                        html.H5('France',style={
                                            'font-weight':'bolder',
                                            'font-size':'1.15rem'
                                        }),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H6('Confirmed',style={
                                                            'font-weight':'550',
                                                            'font-size':'0.85rem'
                                                        }),
                                                        html.Span('{}'.format(fr_confirm),style={
                                                            'color':'rgb(255, 152, 1)',
                                                            'font-size':'15px'
                                                        })
                                                    ]
                                                ,width = 6),
                                                dbc.Col(
                                                    [
                                                        html.H6('Deaths',style={
                                                            'font-weight':'550',
                                                            'font-size':'0.85rem'
                                                        }),
                                                        html.Span('{}'.format(fr_death),style={
                                                            'color':'red',
                                                            'font-size':'15px'
                                                        })
                                                    ]
                                                ,width = 6)
                                            ]
                                        )
                                    ]
                                    ,width=4,style={
                                        'border-right':'1px solid black'
                                    }),
                                dbc.Col(
                                    [
                                        html.H5('United States',style={
                                            'font-weight':'bolder',
                                            'font-size':'1.15rem'
                                        }),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H6('Confirmed',style={
                                                            'font-weight':'550',
                                                            'font-size':'0.85rem'
                                                        }),
                                                        html.Span('{}'.format(us_cases),style={
                                                            'color':'rgb(255, 152, 1)',
                                                            'font-size':'15px'
                                                        })
                                                    ]
                                                ,width = 6),
                                                dbc.Col(
                                                    [
                                                        html.H6('Deaths',style={
                                                            'font-weight':'550',
                                                            'font-size':'0.85rem'
                                                        }),
                                                        html.Span('{}'.format(us_death),style={
                                                            'color':'red',
                                                            'font-size':'15px'
                                                        })
                                                    ]
                                                ,width = 6)
                                            ]
                                        )
                                    ]
                                    ,width=4)
                            ]
                        )
                    ]
                    ,width=8,style={'border-left':'1px solid black',
                    'border-right':'1px solid black',
                    'border-top':'1px solid black',
                    }
                )
            ]
        ),
        dbc.Row(className='toprow',children=
            [
                dbc.Col(
                    [
                        dbc.Row(
                        [
                            dbc.RadioItems(
                                options=[
                                    {'label':'Confirmed cases','value':1},
                                    {'label':'Deaths cases','value':2},
                                    {'label':'Recovered cases','value':3}
                                ],
                                value=1,
                                id='radiochoice',
                                inline=True
                            )
                        ],className='justify-content-end',style={
                            'margin-right':'8em',
                            'margin-top':'2em',
                            'color':'rgb(87, 88, 90)'
                        }
                        ),
                        dcc.Loading(
                            dcc.Graph(id='dbleMap',style={'height':'650px'}),
                            type='circle'
                        ),
                    ],width = 8,style={ 
                        'border':'1px solid black'
                    }),
                dbc.Col(children=[
                    dbc.Row(
                        html.H4('TOP 20 OVERVIEW'),className='justify-content-center'
                    ),
                    dcc.Loading(
                        dbc.Table(
                            recap_table(),
                            responsive =True
                        )
                    )
                ],width = 4,style={
                    'border-right':'1px solid black',
                    'border-top':'1px solid black',
                    'border-bottom':'1px solid black',
                }),
            ],style={'margin-top':'0px'}
        )
        
    ],style={'padding-top':'0px'})
])
#CALLBACKS
@app.callback(
    Output('dbleMap','figure'),
    [Input('radiochoice','value')]
)
def show_graph(value,fig1=fig1,fig2=fig2,fig3=fig3):
    if value == 1:
        return fig1
    elif value == 2:
        return fig2
    else:
        return fig3