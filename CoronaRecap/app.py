import dash
import dash_bootstrap_components as dbc
external_stylesheets = [dbc.themes.BOOTSTRAP,"https://fonts.googleapis.com/css2?family=Montserrat:wght@500&display=swap"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True