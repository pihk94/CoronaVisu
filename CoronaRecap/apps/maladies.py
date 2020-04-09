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

from app import app

sidebar = html.Div(id='mySidebar',className ="sidebar",children=[
            html.A(href='/',children = [html.Img(src='assets/png/home.png',style={'width':'32px','height':'32px','margin-left':'3.6em'}),html.Div('Home',style={
                'font-size':'14px',
                'text-align':'center'
            })],style={'background-color':'#036'}),
            html.A(href='#',children='Récapitulatif',style={'text-align':'left'}),
            html.A(href='#',children='Autres épidémies',style={'text-align':'left'}),
            html.A(href='#',children='Finance',style={'text-align':'left'}),
            html.A(href='#',children='GoogleTrend',style={'text-align':'left'}),
        ])

layout = html.Div([
    sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'50em'}),
                html.H4('maladies',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Comparison diseases'),html.Div(className='encoche',style={'top':'36px','margin-top':'0px'})],href ='#',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Historical Epidemics')],href ='#',className = "sousOnglet")
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A([html.Div('Evolution')],href ='#',className = "sousOnglet")
                            ]
                        ),
                    ],className ='sideBarOnglet',width = 4),
                dbc.Col(width = 8),
            ]
        )
        
    ],style={'padding-top':'0px'})
])




#CALLBACKS
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
                'width':'250px'
            },{
                'margin-left':'250px',
            }
    elif n_clicks == 'None':
        return {
                'width':'0px'
            },{
                'margin-left':'0px'
            }