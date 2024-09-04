import dash
import dash_bootstrap_components as dbc

""" CREDITS
    https://dash.plotly.com/urls
    
    DEFINE APP 
"""
# Create app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    use_pages=True
)

app.layout = dash.page_container

if __name__ == '__main__':
    app.run_server()
