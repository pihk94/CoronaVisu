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
df = pd.read_csv('data/World Infectious Diseases.csv')
df['Diseases'] = 'Infectious Diseases'


#FIGURE SLIDE COMPARAIRAISON
fig1 = px.treemap(df, path=['Diseases', 'Epidemic','InfectiousDiseases'], values='ann_total_cases',
                  color = np.log10(df["CFR"]), hover_data=['R0'],
                  color_continuous_scale='RdBu', range_color=[-4,0],
                  color_continuous_midpoint=np.average(df['CFR']))

fig1.update_layout(coloraxis_colorbar=dict(
    title="CFR",
    tickvals = np.arange(-4, 1),
    ticktext = np.around(np.exp(np.arange(-4, 1)),2),
))
fig2 = px.treemap(df, path=['Diseases', 'Epidemic','InfectiousDiseases'], values='ann_total_fatalities',
                  color = np.log10(df["CFR"]), hover_data=['R0'],
                  color_continuous_scale='RdBu', range_color=[-4,0],
                  color_continuous_midpoint=np.average(df['CFR']))

fig2.update_layout(coloraxis_colorbar=dict(
    title="CFR",
    tickvals = np.arange(-4, 1),
    ticktext = np.around(np.exp(np.arange(-4, 1)),2),
))

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
                html.Div(style={'width':'25em'}),
                html.H4('maladies',id='titleMaladie',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Comparison diseases'),html.Div(className='encoche',style={'top':'36px','margin-top':'0px'})],href ='/maladies',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Historical Epidemics')],href ='/maladies/historical',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Evolution')],href ='/maladies/evolution',className = "sousOnglet")
                            ]
                        ),
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row(
                        [
                            html.Button('Cases',id='BtnFigureDoubleGraph1',className='btnChoixActive',n_clicks=1),
                            html.Button('Fatality',id='BtnFigureDoubleGraph2',className='btnChoixNonActive',n_clicks=0),
                        ],className='justify-content-end',style={
                            'margin-right':'8em',
                            'margin-top':'2em'
                        }
                    ),
                    dcc.Loading(
                        dcc.Graph(id='doubleGraph',style={'height':'800px'}),
                        type='circle'
                    )
                ],style={'padding':'0px'},width = 10),
            ]
        )
        
    ],style={'padding-top':'0px'})
])




#CALLBACKS
@app.callback(
    [Output('doubleGraph','figure'),
    Output('titleMaladie','children')],
    [Input('BtnFigureDoubleGraph1','className')]
)
def show_graph(className,fig1=fig1,fig2=fig2):
    if className == 'btnChoixActive':
        return fig1,'Comparison of Differents Infectious Diseases (Annual total cases)'
    else:
        return fig2,'Comparison of Differents Infectious Diseases (Annual total fatalities)'


@app.callback(
    [Output('BtnFigureDoubleGraph1','className'),
    Output('BtnFigureDoubleGraph2','className')],
    [Input('BtnFigureDoubleGraph1','n_clicks'),
    Input('BtnFigureDoubleGraph2','n_clicks')
    ]
)
def change_color(n_clicks1,n_clicks2):
    if n_clicks1 > n_clicks2:
        return 'btnChoixActive','btnChoixNonActive'
    else:
        return 'btnChoixNonActive','btnChoixActive'
#Callback menu déroulant
@app.callback(
    [Output('mySidebar','style'),
    Output('btnOpen','style')],
    [Input('btnOpen','n_clicks')]
)
def show_side_bar(n_clicks):
    if n_clicks is not None:
        if (n_clicks % 2) != 0:
            return  {
                'width':'0px'
            },{
                'margin-left':'0px'
            }
        else:
            return {
                'width':'350px'
            },{
                'margin-left':'350px',
            }
    elif n_clicks == 'None':
        return {
                'width':'0px'
            },{
                'margin-left':'0px'
            }