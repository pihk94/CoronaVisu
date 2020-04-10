import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.express as px
from app import app

#dataLoad
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

#FIGURE SLIDE COMPARAIRAISON

##################################### Epidemics in History #########################################
colorway = ['#CA4664', '#045A8D', 
           '#A6BDDB', '#D0D1E6', '#74A9CF', '#2B8CBE', '#c2d2e9', '#94C1BF', '#CADBC8',
           '#A1A499', '#C5DB8E', '#DDDB8E', '#DAC38E', '#DAB8A9', '#E5B3C9', '#C2B3C9',
           '#C6BEDF', '#E4DAF5', '#C1CCEC', '#C0D5E3', '#D0E7BE', '#B5E6A9', '#A1DE93',
           '#A6E1CC', '#9EF1E9', '#8DD6E5', '#88C3E5', '#7AACDB', '#5A8CDE','#f3cec9',
           '#e7a4b6', '#cd7eaf',]
fig3 = px.scatter(df2, x="Beginning time", y="Average Death log",
           size="Duration x", hover_name="Disease", color="Disease", color_discrete_sequence = colorway, 
           range_x=[1800,2020], range_y=[0,max(df2['Death toll log'])]) 
fig3.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=True,
        showticklabels=True,
        linecolor = 'lightgray',
        ticks='inside'
    ),
    yaxis=dict(
        gridcolor = 'lightgray',
        showgrid=True,
        zeroline=False,
        showline=False,
    ),
    plot_bgcolor='white')

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

layout = html.Div([
    sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'50em'}),
                html.H4('Epidemics in History ',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Comparison diseases')],href ='/maladies',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Historical Epidemics'),html.Div(className='encoche',style={'top':'213px','margin-top':'0px'})],href ='/maladies/historical',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Evolution')],href ='/maladies/evolution',className = "sousOnglet")
                            ]
                        ),
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    dcc.Loading(
                        dcc.Graph(id='historical',figure=fig3,style={'height':'850px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])




#CALLBACKS
