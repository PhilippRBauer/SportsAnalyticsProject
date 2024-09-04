import locale
from datetime import datetime

from dash import html

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')


def convert_number(number):
    return locale.format_string("%.2f", number, grouping=True)


def sport_to_text(sport):
    if sport == "cycling":
        return "Fahrrad fahren"
    if sport == "running":
        return "Laufen"
    if sport == "swimming":
        return "Schwimmen"


def get_time_of_day(date):
    """
        Uhrzeit morgens - 7 bis 11 Uhr.
        Uhrzeit vormittags - 11 bis 13 Uhr.
        Uhrzeit mittags - 13 bis 15 Uhr.
        Uhrzeit nachmittags - 15 bis 18 Uhr.
        Uhrzeit abends - 18 bis 23 Uhr.
        Uhrzeit nachts - 23 bis 7 Uhr.
    """

    if type(date) == str:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    if 7 <= date.hour < 11:
        return "am Morgen"
    elif 11 <= date.hour < 13:
        return "am Vormittag"
    elif 13 <= date.hour < 15:
        return "am Mittag"
    elif 15 <= date.hour < 18:
        return "am Nachmittag"
    elif 18 <= date.hour < 23:
        return "am Abend"
    elif date.hour >= 23 or date.hour < 7:
        return "in der Nacht"
    else:
        return "unknown"


def get_weekday(date):
    if type(date) == str:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return date.strftime("%A")


def friendly_date(date):
    if type(date) == str:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return date.strftime("%H:%M") + f" {get_weekday(date)}, den " + date.strftime("%d %B %Y")


def simple_date(date):
    if type(date) == str:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return date.strftime("%d.%m.%Y")


def convert_elapsed_time(time):
    total_seconds = int(time)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return "{:02d}:{:02d}".format(minutes, seconds)


def convert_distance(distance, sport=False, remove_suffix=None):
    if sport == "swimming":
        distance = str(int(distance))
        return distance if remove_suffix else str(distance) + " m"
    distance = round(distance / 1000, 2)
    return distance if remove_suffix else str(distance) + " km"


def convert_duration(duration, remove_suffix=None):
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)

    if duration > 3600:
        suffix = "h"
        time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    elif duration > 60:
        suffix = "min"
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
    else:
        suffix = "s"
        time_str = "{:02d}".format(seconds)

    return time_str if remove_suffix else time_str + " " + suffix


def asses_training_effect(training_effect):
    if training_effect >= 3.75:
        return html.Span("Sehr guter Trainingseffekt!", className="text-success")
    if training_effect >= 2.5:
        return html.Span("Guter Trainingseffekt!", className="text-primary")
    if training_effect >= 1.25:
        return html.Span("Mäßiger Trainingseffekt!", className="text-warning")
    else:
        return html.Span("Schlechter Trainingseffekt!", className="text-muted")
