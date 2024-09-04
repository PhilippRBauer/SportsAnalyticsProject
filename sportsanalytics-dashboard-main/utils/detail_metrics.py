import dash_leaflet as dl
import pandas as pd
from dash import html

from utils.icon import return_icon
from utils.star_rating import star_rating
from utils.universal_converter import get_time_of_day, friendly_date, sport_to_text, convert_duration, \
    convert_elapsed_time, convert_distance


def show_wattage(activity, activity_data):
    if activity['sport'] == "cycling" and activity_data["power"].mean() > 0:
        return html.Div([
            html.P(round(activity_data["power"].mean(), 0), className="line1 fw-bolder text m-0"),
            html.P("∅ Watt", className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
        ], className="metric rounded-2",
            style={"display": "none"} if activity['sport'] == "cycling" and activity_data[
                "power"].mean() == 0 else None)
    else:
        return None


def show_ascent(activity):
    if activity['sport'] == "swimming":
        return None
    if "total_ascent" in activity.keys():
        return html.Div([
            html.P(str(activity['total_ascent']) + " m", className="line1 fw-bolder text m-0"),
            html.P("Gesamter Anstieg",
                   className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
        ], className="metric rounded-2")
    else:
        return None


def show_descent(activity):
    if activity['sport'] == "swimming":
        return
    if "total_descent" in activity.keys():
        return html.Div([
            html.P(str(activity['total_descent']) + " m", className="line1 fw-bolder text m-0"),
            html.P("Gesamter Abstieg",
                   className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
        ], className="metric rounded-2")
    else:
        return None


def show_pace(activity):
    # Berechnung basierend auf total_timer_time (Bewegungszeit)
    duration = activity['total_timer_time']
    distance = activity['total_distance']

    if activity['sport'] == "cycling":
        # in km/h, deshalb wird die Duration in h benötigt und Distance in km
        duration = duration / 60 / 60
        distance = distance / 1000
        pace = round(distance / duration, 1)
        return html.Div([
            html.P(str(pace) + " km/h", className="line1 fw-bolder text m-0"),
            html.P("∅ Tempo",
                   className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
        ], className="metric rounded-2")

    elif activity['sport'] == "running":
        # Einheit in min pro km
        distance = distance / 1000
        pace = convert_duration(round(duration / distance, 2), remove_suffix=True)
        return html.Div([
            html.P(str(pace) + " min/km", className="line1 fw-bolder text m-0"),
            html.P("∅ Tempo",
                   className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
        ], className="metric rounded-2")

    elif activity['sport'] == "swimming":
        # Einheit in min pro 100m
        distance = distance / 100
        pace = convert_duration(round(duration / distance, 2), remove_suffix=True)
        return html.Div([
            html.P(str(pace) + " min/100m", className="line1 fw-bolder text m-0"),
            html.P("∅ Tempo",
                   className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
        ], className="metric rounded-2")

    else:
        return None


def widget_metrics(activity, activity_data):
    return html.Div([
        html.Div([
            html.H3("Metriken", className="h5 fw-bold m-0 flex-fill"),
            html.P(friendly_date(activity["date"]), className="text-body-tertiary m-0")
        ], className="widget__header d-flex align-items-center flex-row px-3 py-3"),
        html.Div([
            html.Div([
                return_icon(activity["sport"]),
                html.H3([
                    sport_to_text(activity["sport"]),
                    f" {get_time_of_day(activity['date'])}"
                ], className="h5 ms-3 m-0 flex-fill"),
                star_rating(activity["total_training_effect"])
            ], className="d-flex align-items-center flex-row"),
            html.Div([
                html.Div([
                    html.Div([
                        html.P(convert_duration(activity['total_timer_time']),
                               className="line1 fw-bolder text m-0"),
                        html.P("Bewegungszeit",
                               className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2"),
                    html.Div([
                        html.P(convert_duration(activity['total_elapsed_time']),
                               className="line1 fw-bolder text m-0"),
                        html.P("Verstrichene Zeit",
                               className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2"),
                    html.Div([
                        html.P(convert_distance(activity['total_distance'], activity['sport']),
                               className="line1 fw-bolder text m-0"),
                        html.P("Distanz", className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2"),
                    html.Div([
                        html.P(activity["total_calories"], className="line1 fw-bolder text m-0"),
                        html.P("Kalorien",
                               className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2"),
                    html.Div([
                        html.P(int(activity['avg_heart_rate']), className="line1 fw-bolder text m-0"),
                        html.P("∅ Herzfrequenz",
                               className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2"),
                    html.Div([
                        html.P(round(activity['max_heart_rate'], 0), className="line1 fw-bolder text m-0"),
                        html.P("Max. Herzfrequenz",
                               className="line2 text-body-tertiary fw-bold text m-0 text-uppercase"),
                    ], className="metric rounded-2"),
                    show_ascent(activity),
                    show_descent(activity),
                    show_wattage(activity, activity_data),
                    show_pace(activity)
                ], className="row gap-3 mt-3")
            ], className="container mt-3")
        ], className="widget__content p-3")
    ], className="widget")


def widget_map(activity, activity_data):
    if all(key in activity for key in ['center_longitude', 'center_latitude']):
        if activity["sport"] == "swimming":
            return html.Div([], className="widget invisible")
        return html.Div([
            html.Div([
                html.H3("Kartenansicht der Strecke", className="h5 fw-bold m-0 flex-fill")
            ], className="widget__header d-flex align-items-center flex-row px-3 py-3"),
            html.Div([
                html.Div([
                    html.H3([

                    ], className="h5 ms-3 m-0 flex-fill")
                ], className="d-flex align-items-center flex-row"),
                html.Div([
                    dl.Map(
                        children=[
                            dl.TileLayer(),
                            dl.LayerGroup(
                                id="layer",
                                children=[
                                    dl.Polyline(
                                        positions=activity_data[['latitude', 'longitude']].values.tolist(),
                                        color='#6e6af0',
                                        weight=3
                                    )
                                ]
                            )
                        ],
                        style={'width': '100%', 'height': '400px'},
                        center=[activity["center_latitude"], activity["center_longitude"]],
                        zoom=activity["zoom_level"]
                    )
                ], className="container px-0"),
                html.Div([
                    html.Div(["Gesamtstrecke: ", convert_distance(activity["total_distance"])],
                             className="fw-bolder quiet-text"),
                    html.Div(["Gesamtdauer: ", convert_duration(activity["total_elapsed_time"])],
                             className="fw-bolder quiet-text"),
                ], className="container py-2 px-3 d-inline-flex justify-content-between")
            ], className="widget__content")
        ], className="widget")


def widget_lap_data(activity, activity_data):
    activity_data['timestamp'] = pd.to_datetime(activity_data['timestamp'])

    mean_heartrate_per_lap = activity_data.groupby('lap')['heartrate'].mean().reset_index()
    max_heartrate_per_lap = activity_data.groupby('lap')['heartrate'].max().reset_index()
    distance_per_lap = activity_data.groupby('lap')['distance'].max().reset_index()
    time_per_lap = activity_data.groupby('lap')['timestamp'].agg(
        lambda x: (x.max() - x.min()).total_seconds()).reset_index()
    table_data = pd.merge(time_per_lap, distance_per_lap, on='lap')
    table_data = pd.merge(table_data, mean_heartrate_per_lap, on='lap')
    table_data = pd.merge(table_data, max_heartrate_per_lap, on='lap')

    return html.Div([
        html.Div([
            html.H3("Rundenansicht", className="h5 fw-bold m-0 flex-fill")
        ], className="widget__header d-flex align-items-center flex-row px-3 py-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th(html.B("Runden"), className="text-center"),
                                html.Th(html.B("Zeit"), className="text-center"),
                                html.Th(html.B("Distanz"), className="text-center") if activity['sport'] != "swimming" else None,
                                html.Th(html.B("Ø Herzfrequenz"), className="text-center"),
                                html.Th(html.B("Max Herzfrequenz"), className="text-center"),
                            ])
                        ]),
                        html.Tbody(
                            children=table_data.apply(lambda row: html.Tr([
                                html.Td(row['lap'] + 1, className="text-center"),
                                html.Td(convert_elapsed_time(row['timestamp']) + " min",
                                        className="text-center"),
                                html.Td(convert_distance(row['distance']), className="text-center") if activity['sport'] != "swimming" else None,
                                html.Td(int(row['heartrate_x']), className="text-center"),
                                html.Td(int(row['heartrate_y']), className="text-center"),
                            ]), axis=1).tolist()
                        ),
                    ], className="table table-laps")
                ], className="table-laps-container rounded-3 max-content")
            ], className="container p-3")
        ], className="widget__content")
    ], className="widget")
