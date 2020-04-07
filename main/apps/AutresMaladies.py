import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from apps import GetData
from apps import graph 
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd 
import plotly.express as px
import plotly.graph_objs as go
import time
from app import app
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import os

### GRAPH 
#fig
df = pd.read_csv('data/World Infectious Diseases.csv')
df['Diseases'] = 'Infectious Diseases'
fig = px.treemap(df, path=['Diseases', 'Epidemic','InfectiousDiseases'], values='ann_total_fatalities',
                  color = np.log10(df["CFR"]), hover_data=['R0'],
                  color_continuous_scale='RdBu', range_color=[-4,0],
                  color_continuous_midpoint=np.average(df['CFR']))

fig.update_layout(coloraxis_colorbar=dict(
    title="CFR",
    tickvals = np.arange(-4, 1),
    ticktext = np.around(np.exp(np.arange(-4, 1)),2),
))
#loading dataframe
df1 = pd.read_csv('data/InfectiousDiseasesTS.csv')
df1.fillna(0, inplace = True)
df2 = pd.read_csv('data/InfectiousDiseasesTS2.csv')
df2.fillna(0, inplace = True)
df2['Death toll log'] = np.log(df2['Death toll'])
df2['Average Death'] = df2['Death toll']/df2.Duration
df2['Average Death log'] = np.log(df2['Death toll']/df2.Duration)
df2['First epidemie'] =df2.groupby('Disease')['Beginning time'].transform(min)
df2['Total death log'] = np.log(df2.groupby('Disease')['Death toll'].transform(sum))
df2['Duration x'] = df2['Beginning time'] - df2['First epidemie'] + 1
df3 = pd.DataFrame(columns=['Beginning time', 'Disease', 'Death toll'])
c = 0
for col in df1.columns[1:]:
    for l in np.arange(df1.shape[0]):
        df3.loc[c * df1.shape[0] + l,'Disease'] = col
        df3.loc[c * df1.shape[0] + l,'Beginning time'] = df1.loc[l,'Year']
        df3.loc[c * df1.shape[0] + l,'Death toll'] = df1.loc[l,col]
    c += 1
objs = [df2, df3]
df_new = pd.concat(objs, axis=0, join='outer', ignore_index=True, keys=['Disease', 'Beginning time', 'Death toll'])
df_new.fillna(0, inplace = True)
df_new['Century'] = np.floor(df_new['Beginning time']/100) + 1
df_new['Years'] = df_new['Beginning time'] - (df_new['Century']-1)*100
df_new['Decade'] = np.floor(df_new['Years']/10)*10
df_new.loc[df_new['Duration']==0,'Duration'] = 1
df_new.loc[df_new['Death toll']==0, 'Death toll log'] = 0
df_new.loc[df_new['Death toll'] > 0,'Death toll log'] = np.log(df_new.loc[df_new['Death toll'] > 0,'Death toll'])
df_new['Average Death'] = df_new['Death toll']/df_new.Duration
df_new.loc[df_new['Death toll']==0,'Average Death log'] = 0
df_new.loc[df_new['Death toll'] > 0,'Average Death log'] = np.log(df_new.loc[df_new['Death toll'] > 0,'Death toll']/df_new.Duration)
colorway = ['#CA4664', '#045A8D', 
           '#A6BDDB', '#D0D1E6', '#74A9CF', '#2B8CBE', '#c2d2e9', '#94C1BF', '#CADBC8',
           '#A1A499', '#C5DB8E', '#DDDB8E', '#DAC38E', '#DAB8A9', '#E5B3C9', '#C2B3C9',
           '#C6BEDF', '#E4DAF5', '#C1CCEC', '#C0D5E3', '#D0E7BE', '#B5E6A9', '#A1DE93',
           '#A6E1CC', '#9EF1E9', '#8DD6E5', '#88C3E5', '#7AACDB', '#5A8CDE','#f3cec9',
           '#e7a4b6', '#cd7eaf',]
fig_death = px.scatter(df2, x="Beginning time", y="Average Death log", # animation_frame="Century", # animation_group="Disease",
           size="Duration x", hover_name="Disease", color="Disease", color_discrete_sequence = colorway, 
           range_x=[1800,2020], range_y=[0,max(df2['Death toll log'])]) #, , size_max=45,
fig_death_time = px.bar(df_new, x="Disease", y="Average Death log", animation_frame="Beginning time", color = "Disease",# animation_group="Disease",
           color_discrete_sequence = colorway, #size="Duration x",
           range_y=[0,max(df_new['Death toll log'])])
fig_death_what = px.scatter(df_new, x="Years", y="Average Death log", animation_frame="Beginning time", # animation_group="Disease",
           size="Duration x", hover_name="Disease", color="Disease", color_discrete_sequence = colorway, 
           range_x=[0,100], range_y=[0,max(df_new['Death toll log'])])
df = px.data.gapminder()
fig_quatre = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country", facet_col="continent",
           log_x=True, size_max=45, range_x=[100,100000], range_y=[25,90])
#css
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

dropdown = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem('Autres maladies',href='AutresMaladies',header=True),
        dbc.DropdownMenuItem('Finance',href='/Finance'),
        dbc.DropdownMenuItem('Google Trend',href='/GoogleTrend')
    ],
    nav=True,
    in_navbar=True,
    label = 'Comparatif',
    style = {'margin-right':'3em'}
)

navbar = dbc.Navbar(
        [
        html.A(
            dbc.Row(
            [
                dbc.Col(html.Img(src= app.get_asset_url('png/008-virus.png'),height='32px',width ='32px')),
                dbc.Col(dbc.NavbarBrand('CoronaRecap',className="ml-2"))
            ],
                align="center",
                no_gutters=True,
                ),
                href="/"),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Récapitulatif",href="/")),
                    dbc.NavItem(dbc.NavLink("Simulateur",href="/simulation")),
                    dropdown
                ],className="ml-auto",navbar=True
            ),
            
        ],
    color="dark",
    dark=True,
)

layout = html.Div(children=[
    navbar,
    dbc.Row(
        dcc.Graph(figure = fig)
    ),
    dbc.Row(
        dcc.Graph(figure = fig_death)
    ),
    dbc.Row(
        dcc.Graph(figure = fig_death_time)
    ),
    dbc.Row(
        dcc.Graph(figure = fig_death_what)
    ),
    dbc.Row(
        dcc.Graph(figure = fig_quatre)
    )
    ]
)