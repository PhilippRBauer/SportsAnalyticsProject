import dash
from dash import html, dcc

from utils.dashboard_metrics import widget_metrics, widget_activities
from utils.navigation import navigation

dash.register_page(__name__, path='/')


def layout():
    return html.Div([
        dcc.Location(id="url-nav", refresh=True),
        html.Header(
            [
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H1("Sports Analytics", className="fw-bolder")
                            ], className="col-12"),
                            html.Div(navigation(), className="col-12 mb-2 pb-2 pt-3"),
                        ], className="row"),
                    ], className="col-7"),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H2("Dashboard", className="fw-bolder")
                            ], className="col-12 d-flex justify-content-end"),
                        ], className="row"),
                    ], className="col-5"),
                ], className="row mb-3"),
            ],
            className="mt-4 container-fw container"
        ),
        html.Main(
            [
                html.Div([
                    html.Div([
                        html.Div([
                            widget_metrics(),
                            widget_activities()
                        ], className="col-12 d-inline-flex gap-3"),
                    ], className="row"),
                ], className="container-fw container")
            ]
        )
    ])
