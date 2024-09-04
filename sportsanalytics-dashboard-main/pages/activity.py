import dash
import numpy as np
import plotly.graph_objects as go
from dash import html, dcc, Output, Input

from utils.db import DB
from utils.detail_metrics import widget_metrics, widget_map, widget_lap_data
from utils.icon import return_icon
from utils.navigation import navigation
from utils.universal_converter import sport_to_text, get_time_of_day, friendly_date

dash.register_page(
    __name__,
    path_template="/activity/<activity_id>"
)


def get_activity_by_id(activity_id):
    with DB() as db:
        data = db.get_activity_by_id(activity_id)
        return data


def get_activity_data_by_id(activity_id):
    with DB() as db:
        data = db.get_activity_data_by_id(activity_id)
        return data

""" Linegraph Options
"""
colors = {
    0: "#6e6af0",
    1: "#43c5f0",
    2: "#00e390",
}
options_running = {
    'enhanced_altitude': "Höhenmeter",
    'heartrate': "Herzfrequenz"
}
options_cycling = options_running.copy()
options_cycling['power'] = "Watt"

select_options_running = [
    {'label': 'Distanz in km', 'value': 'distance'},
    {'label': 'Verstrichene Zeit in Minuten', 'value': 'timestamp'}
]
select_options_cycling = select_options_running.copy()
select_options_swimming = [
    {'label': 'Verstrichene Zeit in Minuten', 'value': 'timestamp'}
]


@dash.callback(
    Output("chart_running", "figure"),
    Input("checkbox_running", "value"),
    Input("dropdown_running", "value"),
    Input("url", "pathname")
)
def callback_running(checkbox, dropdown, pathname):
    activity_id = pathname.split('/')[-1]
    activity_data = get_activity_data_by_id(activity_id)
    fig = go.Figure()
    if all([x in activity_data.columns for x in ["timestamp"] + checkbox]):
        activity_data['distance'] = activity_data['distance'].apply(lambda x: x / 1000)
        activity_data['timestamp'] = activity_data['timestamp'].astype('datetime64[s]')
        activity_data['duration'] = (activity_data['timestamp'] - activity_data['timestamp'].min()).dt.total_seconds()
        activity_data['duration'] = activity_data['duration'].astype(np.float64).apply(lambda x: x / 60)

        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                linecolor="#9193a0",
                tickfont=dict(color="#9193a0")
            ),
            yaxis=dict(
                linecolor="#9193a0",
                tickfont=dict(color="#9193a0"),
            ),
            yaxis2=dict(
                linecolor="#9193a0",
                tickfont=dict(color="#9193a0"),
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        i = 0
        for feature in checkbox:
            if feature == checkbox[0]:
                fig.add_trace(
                    go.Scatter(
                        x=activity_data["duration"] if dropdown == "timestamp" else activity_data["distance"],
                        y=activity_data[feature],
                        mode="lines",
                        name=options_running[feature],
                        yaxis='y',
                        line=dict(color=colors[i])
                    )
                )
            else:
                if len(checkbox) > 1:
                    fig.add_trace(
                        go.Scatter(
                            x=activity_data["duration"] if dropdown == "timestamp" else activity_data["distance"],
                            y=activity_data[feature],
                            mode="lines",
                            name=options_running[feature],
                            yaxis='y2',
                            line=dict(color=colors[i])
                        )
                    )
            i = i + 1
        if len(checkbox) > 0:
            fig.update_layout(
                title="Ausgewählte Metriken",
                yaxis=dict(title=options_running[checkbox[0]]),
                yaxis2=dict(title=options_running[checkbox[1]], overlaying='y', side='right') if len(
                    checkbox) > 1 else {},
            )
        dropdown_label = select_options_running[0]['label'] if dropdown == "distance" else select_options_running[1][
            'label']
        fig.update_xaxes(title_text=dropdown_label)
        return fig
    return fig


def widget_linegraph_running(activity):
    options_list = list(options_running.keys())
    return html.Div([
        html.Div([
            html.H3("Grafische Ansicht", className="h5 fw-bold m-0 flex-fill")
        ], className="widget__header d-flex align-items-center flex-row px-3 py-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id="dropdown_running",
                            options=select_options_running,
                            value="timestamp",
                            clearable=False
                        )
                    ], className="col-6 pt-2"),
                ], className="container d-flex justify-content-end"),
                html.Div([
                    dcc.Checklist(
                        options=[{"label": options_running[col], 'value': col} for col in options_running],
                        id="checkbox_running",
                        className="form-check form-switch d-flex gap-3 justify-content-center py-3",
                        value=[options_list[0], options_list[1]],
                        labelClassName="form-check-label",
                        inputClassName="form-check-input mr-1",
                    ),
                ], className="d-flex-inline justify-content-center"),
            ], className=""),
            dcc.Graph(id="chart_running")
        ], className="widget__content")
    ], className="widget")


@dash.callback(
    Output("chart_cycling", "figure"),
    Input("checkbox_cycling", "value"),
    Input("dropdown_cycling", "value"),
    Input("url", "pathname")
)
def callback_cycling(checkbox, dropdown, pathname):
    activity_id = pathname.split('/')[-1]
    activity_data = get_activity_data_by_id(activity_id)
    fig = go.Figure()
    if all([x in activity_data.columns for x in ["timestamp"] + checkbox]):
        activity_data['distance'] = activity_data['distance'].apply(lambda x: x / 1000)
        activity_data['timestamp'] = activity_data['timestamp'].astype('datetime64[s]')
        activity_data['duration'] = (activity_data['timestamp'] - activity_data['timestamp'].min()).dt.total_seconds()
        activity_data['duration'] = activity_data['duration'].astype(np.float64).apply(lambda x: x / 60)

        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                linecolor="#9193a0",
                tickfont=dict(color="#9193a0")
            ),
            yaxis=dict(
                linecolor="#9193a0",
                tickfont=dict(color="#9193a0"),
            ),
            yaxis2=dict(
                linecolor="#9193a0",
                tickfont=dict(color="#9193a0"),
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        i = 0
        for feature in checkbox:
            if feature == checkbox[0]:
                fig.add_trace(
                    go.Scatter(
                        x=activity_data["duration"] if dropdown == "timestamp" else activity_data["distance"],
                        y=activity_data[feature],
                        mode="lines",
                        name=options_cycling[feature],
                        yaxis='y',
                        line=dict(color=colors[i])
                    )
                )
            else:
                if len(checkbox) > 1:
                    fig.add_trace(
                        go.Scatter(
                            x=activity_data["duration"] if dropdown == "timestamp" else activity_data["distance"],
                            y=activity_data[feature],
                            mode="lines",
                            name=options_cycling[feature],
                            yaxis='y2',
                            line=dict(color=colors[i])
                        )
                    )
            i = i + 1
        if len(checkbox) > 0:
            fig.update_layout(
                title="Ausgewählte Metriken",
                yaxis=dict(title=options_cycling[checkbox[0]]),
                yaxis2=dict(title=options_cycling[checkbox[1]], overlaying='y', side='right') if len(
                    checkbox) > 1 else {},
            )
        dropdown_label = select_options_cycling[0]['label'] if dropdown == "distance" else select_options_cycling[1][
            'label']
        fig.update_xaxes(title_text=dropdown_label)
        return fig
    return fig


def widget_linegraph_cycling(activity):
    options_list = list(options_cycling.keys())
    return html.Div([
        html.Div([
            html.H3("Grafische Ansicht", className="h5 fw-bold m-0 flex-fill")
        ], className="widget__header d-flex align-items-center flex-row px-3 py-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id="dropdown_cycling",
                            options=select_options_cycling,
                            value="timestamp",
                            clearable=False
                        )
                    ], className="col-6 pt-2"),
                ], className="container d-flex justify-content-end"),
                html.Div([
                    dcc.Checklist(
                        options=[{"label": options_cycling[col], 'value': col} for col in options_cycling],
                        id="checkbox_cycling",
                        className="form-check form-switch d-flex gap-3 justify-content-center py-3",
                        value=[options_list[0], options_list[1]],
                        labelClassName="form-check-label",
                        inputClassName="form-check-input mr-1",
                    ),
                ], className="d-flex-inline justify-content-center"),
            ], className=""),
            dcc.Graph(id="chart_cycling")
        ], className="widget__content")
    ], className="widget")


@dash.callback(
    Output("chart_swimming", "figure"),
    Input("dropdown_swimming", "value"),
    Input("url", "pathname")
)
def callback_swimming(dropdown, pathname):
    activity_id = pathname.split('/')[-1]
    activity_data = get_activity_data_by_id(activity_id)
    fig = go.Figure()
    if all([x in activity_data.columns for x in ["timestamp"]]):
        activity_data['distance'] = activity_data['distance'].apply(lambda x: x / 1000)
        activity_data['timestamp'] = activity_data['timestamp'].astype('datetime64[s]')
        activity_data['duration'] = (activity_data['timestamp'] - activity_data['timestamp'].min()).dt.total_seconds()
        activity_data['duration'] = activity_data['duration'].astype(np.float64).apply(lambda x: x / 60)

        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                linecolor="#9193a0",
                tickfont=dict(color="#9193a0")
            ),
            yaxis=dict(
                linecolor="#9193a0",
                tickfont=dict(color="#9193a0"),
            ),
            yaxis2=dict(
                linecolor="#9193a0",
                tickfont=dict(color="#9193a0"),
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        i = 0
        fig.add_trace(
            go.Scatter(
                x=activity_data["duration"],
                y=activity_data["heartrate"],
                mode="lines",
                name="Herzfrequenz",
                yaxis='y',
                line=dict(color=colors[i])
            )
        )
        fig.update_layout(
            title="Ausgewählte Metriken",
            yaxis=dict(title="Herzfrequenz")
        )
        dropdown_label = select_options_swimming[0]['label']
        fig.update_xaxes(title_text=dropdown_label)
        return fig
    return fig


def widget_linegraph_swimming(activity):
    return html.Div([
        html.Div([
            html.H3("Grafische Ansicht", className="h5 fw-bold m-0 flex-fill")
        ], className="widget__header d-flex align-items-center flex-row px-3 py-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id="dropdown_swimming",
                            options=select_options_swimming,
                            value="timestamp",
                            clearable=False
                        )
                    ], className="col-6 pt-2"),
                ], className="container d-flex justify-content-end"),
            ], className=""),
            dcc.Graph(id="chart_swimming")
        ], className="widget__content")
    ], className="widget")


def layout(activity_id=None):
    activity = get_activity_by_id(activity_id)
    activity_data = get_activity_data_by_id(activity_id)
    sport = activity["sport"]
    return html.Div([
        dcc.Location(id='url', refresh=False),
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
                                html.H2("Details", className="fw-bolder")
                            ], className="col-12 d-flex justify-content-end"),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                html.H4(
                                                    [
                                                        sport_to_text(activity["sport"]),
                                                        f" {get_time_of_day(activity['date'])}"
                                                    ],
                                                    className="h5 fw-bold mb-0"
                                                )
                                            ], className="col-12 d-flex justify-content-end"),
                                            html.Div([
                                                html.P(friendly_date(activity["date"]), className="mb-0")
                                            ], className="col-12 d-flex justify-content-end"),
                                        ], className="row")
                                    ], className="col-10"),
                                    html.Div([
                                        return_icon(activity["sport"], "big")
                                    ], className="col-2")
                                ], className="row")
                            ], className="col-12 mt-3")
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
                            widget_metrics(activity, activity_data),
                            widget_linegraph_running(activity) if sport == "running" else None,
                            widget_linegraph_cycling(activity) if sport == "cycling" else None,
                            widget_linegraph_swimming(activity) if sport == "swimming" else None,
                        ], className="col-12 d-inline-flex gap-3"),
                    ], className="row"),
                ], className="container-fw container mb-3"),
                html.Div([
                    html.Div([
                        html.Div([
                            widget_lap_data(activity, activity_data),
                            widget_map(activity, activity_data),
                        ], className="col-12 d-inline-flex gap-3"),
                    ], className="row"),
                ], className="container-fw container"),
            ]
        )
    ])
