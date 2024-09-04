import dash
from dash import html, dcc

dash.register_page(__name__)


def layout():
    return html.Div([
        html.Header(
            [
                html.Div([], className="m-3")
            ],
            className="container-fw container"
        ),
        html.Main(
            [
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H1("404 Page not found", className="fw-bolder"),
                                html.P("The page you are looking for does not exist."),
                                dcc.Link("Go back to the dashboard", href="/", className="btn btn-primary btn-lg")
                            ], className="container404 justify-content-center d-flex flex-column align-items-center"),
                        ], className="col-12 my-2"),
                    ], className="row"),
                ], className="container-fw container"),
            ]
        )
    ])
