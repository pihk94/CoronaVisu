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
x = ['Smallpox', 'Plague', 'Sal. Enterica', 'Cholera', 'E Typhus',
 'Bubonic plague', 'Measles', 'Influenza', 'Nellysa Disease',
 'Poliomyelitis', 'InflzA H1N1',
 'InflzA H2N2', 'HIV/AIDS',
 'InflzA H3N2', 'Neonatal tetanus', 'Pertussis',
 'Yellow fever', 'Diphtheria', 'Nipah', 'Mumps',
 'Tuberculosis', 'SARS',
 'JPN encephalitis', 'Ebola', 'Chikungunya', 'Dengue fever',
 'Hepatitis B', 'Meningitis', 'Malaria',
 'MERS', 'Hepatitis E',
 'COVID 19']
df_new['Year'] = df_new['Beginning time']
#FIGURE SLIDE evolv
colorway = ['#CA4664', '#045A8D', 
           '#A6BDDB', '#D0D1E6', '#74A9CF', '#2B8CBE', '#c2d2e9', '#94C1BF', '#CADBC8',
           '#A1A499', '#C5DB8E', '#DDDB8E', '#DAC38E', '#DAB8A9', '#E5B3C9', '#C2B3C9',
           '#C6BEDF', '#E4DAF5', '#C1CCEC', '#C0D5E3', '#D0E7BE', '#B5E6A9', '#A1DE93',
           '#A6E1CC', '#9EF1E9', '#8DD6E5', '#88C3E5', '#7AACDB', '#5A8CDE','#f3cec9',
           '#e7a4b6', '#cd7eaf',]
################################# Evolution of Infectious Diseases in History ###############################

fig4 = px.bar(df_new, x="Disease", y="Average Death log", animation_frame="Year", 
              color = "Disease", color_discrete_sequence = colorway, 
              range_y=[0,max(df_new['Death toll log'])]) 

fig4.update_layout(
   font=dict(
            family='Montserrat',
            size=12,
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

fig4.update_xaxes(
    showticklabels=True,
    ticktext= x,
    tickvals= df_new.Disease.unique(),
    title_text = ""
)


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
                html.H4('Evolution of Infectious Diseases in History',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','color':'rgb(87, 88, 90)','font-weight':'bolder'})
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
                                html.A([html.Div('Historical Epidemics')],href ='/maladies/historical',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Evolution'),html.Div(className='encoche',style={'top':'375px','margin-top':'0px'})],href ='#',className = "sousOngletActived")
                            ]
                        ),
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    dcc.Loading(
                        dcc.Graph(id='evolv',figure=fig4,style={'height':'850px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])




#CALLBACKS
