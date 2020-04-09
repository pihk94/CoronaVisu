import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import (maladies,historical,evolution,GoogleTrend,simulateur,recap,
world,continent,country,home)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/maladies':
        return maladies.layout
    elif pathname == '/':
        return home.layout
    elif pathname == '/maladies/historical':
        return historical.layout
    elif pathname == '/simulation':
        return simulateur.layout
    elif pathname == '/recap':
        return recap.layout
    elif pathname == '/recap/world':
        return world.layout
    elif pathname == '/recap/continent':
        return continent.layout
    elif pathname == '/recap/country':
        return country.layout
    elif pathname == '/maladies/evolution':
        return evolution.layout
    elif pathname == '/GoogleTrend':
        return GoogleTrend.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
