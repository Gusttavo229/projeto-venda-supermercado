import dash_bootstrap_components as dbc 
from dash import html
import dash 


app = dash.Dash(external_stylesheets=[dbc.themes.MINTY],
                
        suppress_callback_exceptions=True)

app.scripts.config.serve_locally = True
server = app.server