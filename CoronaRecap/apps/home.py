import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from apps import GetData
from apps import graph 
from apps import sidebar
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
def get_top3_country(name):
    index_top3 = GetData.get_world(name).groupby('Country/Region').sum().iloc[:,2:].T.iloc[-1].sort_values(ascending = False).index[0:3].values
    df_confirmed_world = GetData.get_world('confirmed').groupby('Country/Region').sum().iloc[:,2:].T
    df_deaths_world = GetData.get_world('deaths').groupby('Country/Region').sum().iloc[:,2:].T
    df_recovered_world = GetData.get_world('recovered').groupby('Country/Region').sum().iloc[:,2:].T
    df = pd.DataFrame()
    df['Confirmed'] = df_confirmed_world[index_top3].iloc[-1,:]
    df['Recovered'] = df_recovered_world[index_top3].iloc[-1,:]
    df['Deaths'] = df_deaths_world[index_top3].iloc[-1,:]
    return df
top3 = get_top3_country('confirmed')
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
    "x": 0.12,
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
        oceancolor = "rgb(255, 255, 255)",
        framecolor='rgb(255,255,255)')
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
    "x": 0.12,
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
        landcolor = "rgb(64, 64, 64)",
        showlakes = True,
        lakecolor = "rgb(64, 64, 64)",
        showsubunits = True,
        subunitcolor = "rgb(255, 255, 255)",
        showcountries = True,
        countrycolor = "rgb(255, 255, 255)",
        showocean = True,
        oceancolor = "rgb(255, 255, 255)",
        framecolor='rgb(255,255,255)')
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
    "x": 0.12,
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
        landcolor = "rgb(64, 64, 64)",
        showlakes = True,
        lakecolor = "rgb(64, 64, 64)",
        showsubunits = True,
        subunitcolor = "rgb(255, 255, 255)",
        showcountries = True,
        countrycolor = "rgb(255, 255, 255)",
        showocean = True,
        oceancolor = "rgb(255, 255, 255)",
        framecolor='rgb(255,255,255)')
fig2 =fig_dict


#DATA
dt = (datetime.now() - timedelta(1)).strftime('%d/%m/%Y')
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
    for index,row in df_H5.head(10).iterrows():
        rows.append(html.Tr([html.Td(row.Pays,style={'font-weight':'bold','text-align':'center'}),
        html.Td(row['Total des cas']),html.Td(row['Total décès']),html.Td(row['Mortalité'])],style={
            'border-bottom':'1px solid #e8e8e8'
        }))
    return [
        html.Thead([
            html.Tr(
                [
                    html.Th(
                    'COuntry',style={'text-align':'center','width':'180px'}
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
sous_header = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                        dbc.CardBody(
                            [
                                html.Img(src='https://image.flaticon.com/icons/svg/2785/2785819.svg',width="70px",height="70px",style={'margin-top':'1em'}),
                                html.Div('{:,}'.format(confirmed),style={
                                    'color':'rgb(255, 152, 1)',
                                    'font-weight':"bolder",
                                    'font-size':'27px'
                                }),
                                html.Div('Total cases')
                            ]
                        ),style={"height":"219px","margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
                    ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='https://image.flaticon.com/icons/svg/2747/2747789.svg',width="70px",height="70px",style={'margin-top':'1em'}),
                        html.Div('{:,}'.format(deaths),style={
                            'color':'red',
                            'font-weight':"bolder",
                            'font-size':'27px'
                        }),
                        html.Div('Total deaths')
                    ]
                ),style={"height":"219px","margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='../assets/png/019-virus.png',width="70px",height="70px",style={'margin-top':'1em'}),
                        html.Div('{:,}'.format(GetData.get_world('recovered').iloc[:,-1].sum()),style={
                            'color':'#28a745',
                            'font-weight':"bolder",
                            'font-size':'27px'
                        }),
                        html.Div('Total recovered')
                    ]
                ),style={"height":"219px","margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='../assets/png/'+top3.index[0].replace(' ','-') +'.png',width="60px",height="54px"),
                        dbc.Row(
                            [
                                dbc.Table(
                                    [
                                        html.Thead(
                                            html.Tr(
                                                [
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2785/2785819.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2747/2747789.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='../assets/png/019-virus.png',width="32px",height="32px")
                                                    )
                                                ]
                                            )
                                        ),
                                        html.Tbody(
                                            [
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            '{:,}'.format(top3['Confirmed'].iloc[0]),style={'color':'rgb(255, 152, 1)',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '{:,}'.format(top3['Deaths'].iloc[0]),style={'color':'red',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '{:,}'.format(top3['Recovered'].iloc[0]),style={'color':'#28a745',
                                                                            'font-weight':"bolder"}
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),style={"margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='../assets/png/'+top3.index[1].replace(' ','-') +'.png',width="60px",height="54px"),
                        dbc.Row(
                            [
                                dbc.Table(
                                    [
                                        html.Thead(
                                            html.Tr(
                                                [
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2785/2785819.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2747/2747789.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='../assets/png/019-virus.png',width="32px",height="32px")
                                                    )
                                                ]
                                            )
                                        ),
                                        html.Tbody(
                                            [
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            '{:,}'.format(top3['Confirmed'].iloc[1]),style={'color':'rgb(255, 152, 1)',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '{:,}'.format(top3['Deaths'].iloc[1]),style={'color':'red',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '{:,}'.format(top3['Recovered'].iloc[1]),style={'color':'#28a745',
                                                                            'font-weight':"bolder"}
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),style={"margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            ),
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src='../assets/png/'+top3.index[2].replace(' ','-') +'.png',width="60px",height="54px"),
                        dbc.Row(
                            [
                                dbc.Table(
                                    [
                                        html.Thead(
                                            html.Tr(
                                                [
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2785/2785819.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='https://image.flaticon.com/icons/svg/2747/2747789.svg',width="32px",height="32px")
                                                    ),
                                                    html.Th(
                                                        html.Img(src='../assets/png/019-virus.png',width="32px",height="32px")
                                                    )
                                                ]
                                            )
                                        ),
                                        html.Tbody(
                                            [
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            '{:,}'.format(top3['Confirmed'].iloc[2]),style={'color':'rgb(255, 152, 1)',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '{:,}'.format(top3['Deaths'].iloc[2]),style={'color':'red',
                                                                            'font-weight':"bolder"}
                                                        ),
                                                        html.Td(
                                                            '{:,}'.format(top3['Recovered'].iloc[2]),style={'color':'#28a745',
                                                                            'font-weight':"bolder"}
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),style={"margin-top":"1em","text-align":"center",'font-family':'Montserrat'},
            )
        )
        
    ],style={
        'margin-right':'1em',
        'margin-left':'1em',
        'margin-bottom':'1em'
    }
    
)


layout = html.Div([
    sidebar.sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'36em'}),
                html.H4('COVID-19 GLOBAL CASES OVERVIEW',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','font-weight':'bolder','color':'rgb(87, 88, 90)','font-weight':'bolder'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        sous_header,
        dbc.Row(children=
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
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
                                ]
                            )
                        ) 
                    ],width=8),
                dbc.Col(children=[
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    html.H4(['TOP 10 OVERVIEW']),className='justify-content-center',style={'margin-top':'3em','margin-bottom':'1em'}
                                ),
                                dcc.Loading(
                                    dbc.Table(
                                        recap_table(),
                                        responsive =True
                                    )
                                )
                            ]
                        )
                    )
                ]
                ),
            ],style={'margin-top':'0px','margin-right':'2em',
                    'margin-left':'1em',
                    'text-align': 'center'}
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