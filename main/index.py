import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import recap,sim,recapv2,AutresMaladies,Finance,GoogleTrend


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return recapv2.layout
    elif pathname == '/simulation':
        return sim.layout
    elif pathname == '/recap':
        return recapv2.layout
    elif pathname == '/AutresMaladies':
        return AutresMaladies.layout
    elif pathname == '/Finance':
        return Finance.layout
    elif pathname == '/GoogleTrend':
        return GoogleTrend.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)