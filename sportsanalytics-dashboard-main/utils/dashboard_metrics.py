from datetime import datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, Output, Input, State

from utils.db import DB
from utils.icon import return_icon, render_icon_indicator
from utils.star_rating import star_rating
from utils.universal_converter import simple_date, convert_duration, convert_distance, asses_training_effect


def get_all_activities(sport):
    with DB() as db:
        return db.get_all_activities(sport=sport)


FILTER_LINKS_GRAPH = {
    "filter-graph-all": "Alle",
    "filter-graph-running": "Laufen",
    "filter-graph-cycling": "Radfahren",
    "filter-graph-swimming": "Schwimmen"
}

CHART_OPTIONS = {
    "total_calories": "Kalorienverbrauch pro Tag",
    "total_distance": "Distanz pro Tag",
    "total_timer_time": "Bewegungsdauer pro Tag"
}


@dash.callback(
    Output("chart", "children"),
    Output("metrics", "children"),
    Output("filter-graph-container", "children"),
    Output("icon_indicator", "children"),
    Input("filter-graph-all", "n_clicks"),
    Input("filter-graph-running", "n_clicks"),
    Input("filter-graph-cycling", "n_clicks"),
    Input("filter-graph-swimming", "n_clicks"),
    Input("datepicker", 'start_date'),
    Input("datepicker", 'end_date'),
    Input("radio_calculation_type", "value"),
    Input("radio_metric_filter", "value"),
    State("filter-graph-all", "className"),
    State("filter-graph-running", "className"),
    State("filter-graph-cycling", "className"),
    State("filter-graph-swimming", "className")
)
def render_all_metrics(
        filter_all,
        filter_running,
        filter_cycling,
        filter_swimming,
        start_date,
        end_date,
        calculation_type,
        metric_filter,
        state_all,
        state_running,
        state_cycling,
        state_swimming,
):
    # FILTERING BY SPORT
    ctx = dash.callback_context

    filter_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Set the active class for the clicked filter
    filter_classes = {
        "filter-graph-all": "page-link",
        "filter-graph-running": "page-link",
        "filter-graph-cycling": "page-link",
        "filter-graph-swimming": "page-link"
    }

    if filter_id not in filter_classes.keys():
        filter_classes = {
            "filter-graph-all": state_all,
            "filter-graph-running": state_running,
            "filter-graph-cycling": state_cycling,
            "filter-graph-swimming": state_swimming
        }
    current_filter_class = False
    for key, value in filter_classes.items():
        if value == "page-link active":
            current_filter_class = key
    if filter_id == "":
        filter_classes["filter-graph-all"] = "page-link active"

    if current_filter_class is not False:
        filter_id = current_filter_class
    filter_classes[filter_id] = "page-link active"

    # RENDERING
    with DB() as db:
        if filter_id == "filter-graph-all":
            df = db.get_all_activities()
            icon_indicator = "all"
        elif filter_id == "filter-graph-running":
            df = db.get_all_activities(sport="running")
            icon_indicator = "running"
        elif filter_id == "filter-graph-cycling":
            df = db.get_all_activities(sport="cycling")
            icon_indicator = "cycling"
        elif filter_id == "filter-graph-swimming":
            df = db.get_all_activities(sport="swimming")
            icon_indicator = "swimming"
        else:
            df = db.get_all_activities()
            icon_indicator = "all"

        if df is not None:
            # filter orignal dataframe
            if (start_date is None or start_date == 0) and (end_date is None or end_date == 0):
                first_record = df.head(1)
                first_record_date = first_record['date'].values[0]
                date_from_first = simple_date(first_record_date)
                start_date_initial = datetime.strptime(date_from_first, '%d.%m.%Y')
                start_date_result = start_date_initial - timedelta(days=7)
                start_date_if_none = start_date_result.strftime('%Y-%m-%d')
                df = df[(df['date'] >= start_date_if_none)]
            elif start_date is not None and end_date is not None:
                df = df[(df['date'] >= (start_date + " 00:00:00")) & (df['date'] <= (end_date + " 23:59:59"))]

            mean_training_effect = df['total_training_effect'].mean()
            best_activity = df[df['total_training_effect'] == df['total_training_effect'].max()]

            metrics_df = df.copy()
            metrics_df = metrics_df.groupby('date_group').sum().reset_index()
            metrics_df['date_group'] = pd.to_datetime(metrics_df['date_group'])
            metrics_df['date_group'] = metrics_df['date_group'].apply(lambda x: simple_date(x))

            chart_df = metrics_df.copy()
            chart_df_data_labels = {}
            if metric_filter == "total_calories" or metric_filter is False:
                chart_df[metric_filter] = chart_df[metric_filter]
                chart_df_data_labels[metric_filter] = chart_df[metric_filter]
            elif metric_filter == "total_distance":
                chart_df[metric_filter] = chart_df[metric_filter].apply(
                    lambda x: convert_distance(x, remove_suffix=True))
                chart_df_data_labels[metric_filter] = chart_df[metric_filter]
            elif metric_filter == "total_timer_time":
                chart_df[metric_filter] = chart_df[metric_filter]
                chart_df_data_labels[metric_filter] = chart_df[metric_filter].apply(
                    lambda x: convert_duration(x, remove_suffix=True))

            # Generate the chart
            chart = dcc.Graph(
                id=icon_indicator + "-chart",
                responsive=True,
                figure={
                    "data": [
                        {
                            "x": chart_df['date_group'],
                            "y": chart_df[metric_filter],
                            "type": "bar",
                            "marker": {
                                "color": "#6e6af0"
                            },
                            "text": chart_df_data_labels[metric_filter],
                            "textposition": "auto",
                        }
                    ],
                    "layout": {
                        "xaxis": {
                            "title": "Datum"
                        },
                        "yaxis": {
                            "title": CHART_OPTIONS[metric_filter],
                            "ticktext": chart_df_data_labels[metric_filter],
                            "tickvals": chart_df[metric_filter]
                        },
                        "barmode": "group"
                    }
                }
            )

            # Generate the metrics
            if calculation_type == "sum":
                total_distance = convert_distance(round(metrics_df['total_distance'].sum(), 0))
                total_calories = round(metrics_df['total_calories'].sum(), 0)
                total_duration = convert_duration(metrics_df['total_timer_time'].sum())
            if calculation_type == "avg":
                total_distance = convert_distance(round(metrics_df['total_distance'].mean(), 0))
                total_calories = round(metrics_df['total_calories'].mean(), 0)
                total_duration = convert_duration(metrics_df['total_timer_time'].mean())

            metrics = html.Div([
                html.Div([
                    html.Div([
                        html.P(total_distance, className="line1 fw-bolder text m-0"),
                        html.P(["∅ Distanz" if calculation_type == "avg" else "Gesamte Distanz"],
                               className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2"),
                    html.Div([
                        html.P(total_calories, className="line1 fw-bolder text m-0"),
                        html.P(["∅ Kalorien" if calculation_type == "avg" else "Gesamte Kalorien"],
                               className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2"),
                    html.Div([
                        html.P(total_duration, className="line1 fw-bolder text m-0"),
                        html.P(["∅ Bewegungsdauer" if calculation_type == "avg" else "Gesamte Bewegungsdauer"],
                               className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2"),
                    html.Div([
                        html.P("Beste Aktivität", className="line1 fw-bolder text m-0"),
                        html.Div([
                            html.Div([return_icon(best_activity['sport'].values[0])], className="me-3 flex-fill"),
                            html.Div([
                                star_rating(best_activity["total_training_effect"].values[0], layout="small")
                            ],
                                className="me-3 flex-fill"
                            ),
                            dbc.Nav(
                                dbc.NavLink(
                                    "Details",
                                    href="/activity/{}".format(best_activity["id"].values[0]),
                                    className="btn btn-outline-info smallbtn"
                                )
                            )
                        ], className="d-flex align-items-center mt-3"),
                        html.P(simple_date(best_activity["date"].values[0]),
                               className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2") if len(best_activity) > 0 else html.Div([]),
                    html.Div([
                        html.P("Durchschnittlicher Trainingseffekt", className="line1 fw-bolder text m-0"),
                        html.P("(Aller Aktivitäten im Trainingszeitraum)", className="text-muted line2 h6 text m-0"),
                        html.Div(
                            html.Div([
                                star_rating(mean_training_effect, layout="small")
                            ], className="mt-3 mb-2 flex-fill"),
                            className="d-flex align-items-center"
                        ),
                        html.P(
                            asses_training_effect(mean_training_effect),
                            className="line3 fw-bolder text m-0"
                        ),
                    ], className="metric rounded-2")
                ], className="col-12 d-flex flex-wrap flex-row gap-3"),
            ], className="row")
            # Generate the filter link elements
            filter_links = []
            for link_id, label in FILTER_LINKS_GRAPH.items():
                filter_links.append(html.Li([
                    html.Button(label, id=link_id, className=filter_classes[link_id])
                ], className="page-item"))

            return chart, metrics, filter_links, render_icon_indicator(icon_indicator)
    return html.Div([]), []


def widget_metrics():
    all_activities = get_all_activities(sport=False)
    datepicker_data = all_activities['date'].tolist()
    datepicker_data = [simple_date(date) for date in datepicker_data]
    available_dates = sorted(
        [datetime.strptime(date_string, '%d.%m.%Y').date() for date_string in list(set(datepicker_data))])

    chart, metrics, filter_links, icon_indicator = render_all_metrics(
        None, None, None, None,
        0, 0, "sum", "total_calories",
        "page-link", "page-link", "page-link", "page-link"
    )
    return html.Div([
        html.Div([
            html.H3("Metriken", className="h5 fw-bold m-0 flex-fill")
        ], className="widget__header d-flex align-items-center flex-row px-3 py-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Ul(
                            filter_links,
                            id="filter-graph-container",
                            className="pagination pt-3"
                        ),
                        dcc.DatePickerRange(
                            id="datepicker",
                            display_format="YYYY-MM-DD",
                            clearable=True,
                            min_date_allowed=available_dates[0],
                            max_date_allowed=available_dates[-1],
                        ),
                    ], className="d-flex align-items-center flex-row justify-content-between flex-wrap"),
                ], className="col-12"),
                html.Div([
                    html.Div(["Berechnungstyp:"], className="me-3"),
                    dcc.RadioItems(
                        options=[
                            {"label": "Gesamt", "value": "sum"},
                            {"label": "Durchschnitt pro Tag", "value": "avg"},
                        ],
                        id="radio_calculation_type",
                        className="form-check form-switch d-flex gap-3 justify-content-center py-3",
                        value="sum",
                        labelClassName="form-check-label",
                        inputClassName="form-check-input mr-1",
                    )
                ], className="col-12 pt-3 d-flex align-items-center flex-row justify-content-start flex-wrap"),
            ], className="container"),
            html.Div(id="metrics", children=[], className="container"),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                dcc.RadioItems(
                                    options=[{"label": label, "value": value} for value, label in
                                             CHART_OPTIONS.items()],
                                    id="radio_metric_filter",
                                    className="form-check form-switch d-flex gap-3 justify-content-center",
                                    value="total_calories",
                                    labelClassName="form-check-label",
                                    inputClassName="form-check-input mr-1",
                                )
                            ],
                                className="flex-fill d-flex align-items-center flex-row justify-content-start flex-wrap"),
                            html.Div(
                                id="icon_indicator",
                                children=[],
                                className="d-inline-flex gap-2"
                            )
                        ], className="d-flex flex-row justify-content-between mt-3")
                    ], className="col-12"),
                    html.Div(id="chart", children=[], className="container pt-3")
                ], className="row"),
            ], className="container"),
        ], className="widget__content")
    ], className="widget")


FILTER_LINKS_ACTIVITIES = {
    "filter-link-all": "Alle",
    "filter-link-running": "Laufen",
    "filter-link-cycling": "Radfahren",
    "filter-link-swimming": "Schwimmen"
}


@dash.callback(
    Output("activities", "children"),
    Output("filter-links-container", "children"),
    Input("filter-link-all", "n_clicks"),
    Input("filter-link-running", "n_clicks"),
    Input("filter-link-cycling", "n_clicks"),
    Input("filter-link-swimming", "n_clicks"),
    State("filter-link-all", "className"),
    State("filter-link-running", "className"),
    State("filter-link-cycling", "className"),
    State("filter-link-swimming", "className"),
)
def filter_activities(
        filter_all,
        filter_running,
        filter_cycling,
        filter_swimming,
        state_all_class,
        state_running_class,
        state_cycling_class,
        state_swimming_class
):
    # FILTERING BY SPORT
    ctx = dash.callback_context

    filter_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # Set the active class for the clicked filter
    filter_classes = {
        "filter-link-all": "page-link",
        "filter-link-running": "page-link",
        "filter-link-cycling": "page-link",
        "filter-link-swimming": "page-link"
    }
    if filter_id == "":
        filter_classes["filter-link-all"] = "page-link active"
    filter_classes[filter_id] = "page-link active"

    # RENDERING
    with DB() as db:
        if filter_id == "filter-link-all":
            df = db.get_all_activities()
        elif filter_id == "filter-link-running":
            df = db.get_all_activities(sport="running")
        elif filter_id == "filter-link-cycling":
            df = db.get_all_activities(sport="cycling")
        elif filter_id == "filter-link-swimming":
            df = db.get_all_activities(sport="swimming")
        else:
            df = db.get_all_activities()

        if df is not None:
            row_list = []
            for index, row in df.iterrows():
                row_list.append(html.Tr([
                    html.Td(return_icon(row.sport)),
                    html.Td(simple_date(row.date), className="text-center text-nowrap"),
                    html.Td(row['total_calories'], className="text-center text-nowrap"),
                    html.Td(convert_duration(row['total_timer_time']), className="text-center text-nowrap"),
                    html.Td([
                        dbc.Nav(
                            dbc.NavLink(
                                "Details",
                                href=f"/activity/{row.id}",
                                className="btn btn-primary btn-lg me-md-2 nav-link active"
                            )
                        )
                    ])
                ]))

            # Generate the filter link elements
            filter_links = []
            for link_id, label in FILTER_LINKS_ACTIVITIES.items():
                filter_links.append(html.Li([
                    html.Button(label, id=link_id, className=filter_classes[link_id])
                ], className="page-item"))

            return row_list, filter_links

        return html.Div([]), []


def render_activities_table():
    activities, filter_links = filter_activities(
        None, None, None, None,
        "page-link", "page-link", "page-link", "page-link",
    )
    return (
        html.Div([
            html.Ul(
                filter_links,
                id="filter-links-container",
                className="pagination mt-3"
            )
        ], className="col-12"),
        html.Div([
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th(html.B("Training")),
                        html.Th(html.B("Datum"), className="text-center text-nowrap"),
                        html.Th(html.B("Kalorien"), className="text-center text-nowrap"),
                        html.Th(html.B("Zeit"), className="text-center text-nowrap"),
                        html.Th([""])
                    ])
                ]),
                html.Tbody(
                    id="activities",
                    children=[]
                ),
            ], className="table table-striped table-hover")
        ], className="max-content-big"),
    )


def widget_activities():
    return html.Div([
        html.Div([
            html.H3("Alle Aktivitäten", className="h5 fw-bold m-0 flex-fill")
        ], className="widget__header d-flex align-items-center flex-row px-3 py-3"),
        html.Div([
            html.Div([
                html.Div(children=render_activities_table(), className="row")
            ], className="container")
        ], className="widget__content")
    ], className="widget")
