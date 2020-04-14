import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

sidebar = html.Div(id='mySidebar',className ="sidebar",children=[
            html.A(href='/',children = [html.Img(src='https://image.flaticon.com/icons/svg/2813/2813318.svg',style={'height':'47px','text-align':'center'})
            ],style={'background-color':'white','margin-top':' 0px',"height": "56px",'text-align':'center'}),
            html.A(href='/recap',children=[html.Span('OVERVIEW')],style={'text-align':'left'}),
            html.A(href='/simulation',children='SIMULATION',style={'text-align':'left'}),
            html.A(href='/maladies',children='DISEASE COMPARISON',style={'text-align':'left'}),
            html.A(href='/finance',children='FINANCE',style={'text-align':'left'}),
            html.A(href='/GoogleTrend',children='INTERNET',style={'text-align':'left'}),
        ])