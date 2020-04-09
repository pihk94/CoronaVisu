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

# link fontawesome to get the chevron icons
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

app.layout = html.Div(
    [
        html.Div(id='mySidebar',className ="sidebar",children=[
            html.A(href='/',children = [html.Img(src='assets/png/home.png',style={'width':'32px','height':'32px','margin-left':'3.6em'}),html.Div('Home',style={
                'font-size':'14px',
                'text-align':'center'
            })],style={'background-color':'#036'}),
            html.A(href='#',children='Récapitulatif',style={'text-align':'left'}),
            html.A(href='#',children='Autres épidémies',style={'text-align':'left'}),
            html.A(href='#',children='Finance',style={'text-align':'left'}),
            html.A(href='#',children='GoogleTrend',style={'text-align':'left'}),
        ]),
    html.Div(id='main',children = [
        html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1)
    ])
    ])

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
        
if __name__ == "__main__":
    app.run_server(debug=True)