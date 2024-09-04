import math

from dash import html
from dash_svg import Svg, Path


def star(type, decimal=0.0):
    if type == "filled":
        return html.Div([
            Svg([
                Path(
                    d='M13.295,1.656c-0.23,-0.478 -0.717,-0.782 -1.251,-0.782c-0.535,-0 -1.017,0.304 -1.252,0.782l-2.794,'
                      '5.749l-6.24,0.922c-0.522,0.078 -0.956,0.443 -1.117,0.943c-0.161,0.499 -0.031,1.051 0.343,'
                      '1.421l4.528,4.48l-1.069,6.332c-0.087,0.521 0.131,1.051 0.561,1.36c0.43,0.309 0.999,0.348 1.469,'
                      '0.1l5.575,-2.977l5.576,2.977c0.469,0.248 1.038,0.213 1.469,-0.1c0.43,-0.313 0.647,-0.839 0.56,'
                      '-1.36l-1.073,-6.332l4.528,-4.48c0.374,-0.37 0.508,-0.922 0.343,-1.421c-0.165,-0.5 -0.595,'
                      '-0.865 -1.116,-0.943l-6.245,-0.922l-2.795,-5.749Z" '
                      'style="fill-opacity:0;fill-rule:nonzero;"/><path d="M13.295,1.656l2.795,5.749l6.245,0.922c0.521,'
                      '0.078 0.951,0.443 1.116,0.943c0.165,0.499 0.031,1.051 -0.343,1.421l-4.528,4.48l1.073,6.332c0.087,'
                      '0.521 -0.13,1.047 -0.56,1.36c-0.431,0.313 -1,0.348 -1.469,0.1l-5.576,-2.977l-5.575,2.977c-0.47,'
                      '0.248 -1.039,0.209 -1.469,-0.1c-0.43,-0.309 -0.648,-0.839 -0.561,-1.36l1.069,-6.332l-4.528,'
                      '-4.48c-0.374,-0.37 -0.504,-0.922 -0.343,-1.421c0.161,-0.5 0.595,-0.865 1.117,-0.943l6.24,'
                      '-0.922l2.794,-5.749c0.235,-0.478 0.717,-0.782 1.252,-0.782c0.534,-0 1.021,0.304 1.251,0.782Zm-0.9,'
                      '0.434c-0.065,-0.133 -0.202,-0.216 -0.351,-0.216c-0.151,-0 -0.287,0.087 -0.354,0.222l-2.793,'
                      '5.746c-0.144,0.298 -0.426,0.504 -0.753,0.553l-6.238,0.921c-0.145,0.021 -0.268,0.121 -0.313,'
                      '0.26c-0.046,0.142 -0.012,0.299 0.094,0.403l4.529,4.481c0.231,0.229 0.337,0.557 0.282,0.878l-1.068,'
                      '6.329c-0.025,0.147 0.036,0.297 0.157,0.383c0.122,0.088 0.285,0.099 0.419,0.029l5.571,-2.975c0.295,'
                      '-0.157 0.648,-0.157 0.942,-0l5.572,2.975c0.132,0.069 0.292,0.063 0.413,-0.025c0.123,-0.089 0.188,'
                      '-0.238 0.163,-0.387l-1.073,-6.329c-0.055,-0.321 0.051,-0.649 0.282,-0.878l4.529,-4.481c0.104,'
                      '-0.103 0.143,-0.256 0.097,-0.396c-0.047,-0.141 -0.168,-0.245 -0.316,-0.267l-6.242,-0.921c-0.327,'
                      '-0.049 -0.609,-0.255 -0.754,-0.553l-2.794,-5.749l-0.001,-0.003Z',
                    fill="#FFA800"
                )
            ], viewBox="0 0 24 24", width="100%", height="100%", className="star_icon")
        ], className="star_icon_container star_icon_full")
    elif type == "half":
        return html.Div([
            html.Div([
                Svg([
                    Path(
                        d='M13.295,1.656c-0.23,-0.478 -0.717,-0.782 -1.251,-0.782c-0.535,-0 -1.017,0.304 -1.252,0.782l-2.794,'
                          '5.749l-6.24,0.922c-0.522,0.078 -0.956,0.443 -1.117,0.943c-0.161,0.499 -0.031,1.051 0.343,'
                          '1.421l4.528,4.48l-1.069,6.332c-0.087,0.521 0.131,1.051 0.561,1.36c0.43,0.309 0.999,0.348 1.469,'
                          '0.1l5.575,-2.977l5.576,2.977c0.469,0.248 1.038,0.213 1.469,-0.1c0.43,-0.313 0.647,-0.839 0.56,'
                          '-1.36l-1.073,-6.332l4.528,-4.48c0.374,-0.37 0.508,-0.922 0.343,-1.421c-0.165,-0.5 -0.595,'
                          '-0.865 -1.116,-0.943l-6.245,-0.922l-2.795,-5.749Z" '
                          'style="fill-opacity:0;fill-rule:nonzero;"/><path d="M13.295,1.656l2.795,5.749l6.245,0.922c0.521,'
                          '0.078 0.951,0.443 1.116,0.943c0.165,0.499 0.031,1.051 -0.343,1.421l-4.528,4.48l1.073,6.332c0.087,'
                          '0.521 -0.13,1.047 -0.56,1.36c-0.431,0.313 -1,0.348 -1.469,0.1l-5.576,-2.977l-5.575,2.977c-0.47,'
                          '0.248 -1.039,0.209 -1.469,-0.1c-0.43,-0.309 -0.648,-0.839 -0.561,-1.36l1.069,-6.332l-4.528,'
                          '-4.48c-0.374,-0.37 -0.504,-0.922 -0.343,-1.421c0.161,-0.5 0.595,-0.865 1.117,-0.943l6.24,'
                          '-0.922l2.794,-5.749c0.235,-0.478 0.717,-0.782 1.252,-0.782c0.534,-0 1.021,0.304 1.251,0.782Zm-0.9,'
                          '0.434c-0.065,-0.133 -0.202,-0.216 -0.351,-0.216c-0.151,-0 -0.287,0.087 -0.354,0.222l-2.793,'
                          '5.746c-0.144,0.298 -0.426,0.504 -0.753,0.553l-6.238,0.921c-0.145,0.021 -0.268,0.121 -0.313,'
                          '0.26c-0.046,0.142 -0.012,0.299 0.094,0.403l4.529,4.481c0.231,0.229 0.337,0.557 0.282,0.878l-1.068,'
                          '6.329c-0.025,0.147 0.036,0.297 0.157,0.383c0.122,0.088 0.285,0.099 0.419,0.029l5.571,-2.975c0.295,'
                          '-0.157 0.648,-0.157 0.942,-0l5.572,2.975c0.132,0.069 0.292,0.063 0.413,-0.025c0.123,-0.089 0.188,'
                          '-0.238 0.163,-0.387l-1.073,-6.329c-0.055,-0.321 0.051,-0.649 0.282,-0.878l4.529,-4.481c0.104,'
                          '-0.103 0.143,-0.256 0.097,-0.396c-0.047,-0.141 -0.168,-0.245 -0.316,-0.267l-6.242,-0.921c-0.327,'
                          '-0.049 -0.609,-0.255 -0.754,-0.553l-2.794,-5.749l-0.001,-0.003Z',
                        fill="#e3e5f3"
                    )
                ], viewBox="0 0 24 24", width="100%", height="100%", className="star_icon")
            ], className="star_bottom"),
            html.Div([
                Svg([
                    Path(
                        d='M13.295,1.656c-0.23,-0.478 -0.717,-0.782 -1.251,-0.782c-0.535,-0 -1.017,0.304 -1.252,0.782l-2.794,'
                          '5.749l-6.24,0.922c-0.522,0.078 -0.956,0.443 -1.117,0.943c-0.161,0.499 -0.031,1.051 0.343,'
                          '1.421l4.528,4.48l-1.069,6.332c-0.087,0.521 0.131,1.051 0.561,1.36c0.43,0.309 0.999,0.348 1.469,'
                          '0.1l5.575,-2.977l5.576,2.977c0.469,0.248 1.038,0.213 1.469,-0.1c0.43,-0.313 0.647,-0.839 0.56,'
                          '-1.36l-1.073,-6.332l4.528,-4.48c0.374,-0.37 0.508,-0.922 0.343,-1.421c-0.165,-0.5 -0.595,'
                          '-0.865 -1.116,-0.943l-6.245,-0.922l-2.795,-5.749Z" '
                          'style="fill-opacity:0;fill-rule:nonzero;"/><path d="M13.295,1.656l2.795,5.749l6.245,0.922c0.521,'
                          '0.078 0.951,0.443 1.116,0.943c0.165,0.499 0.031,1.051 -0.343,1.421l-4.528,4.48l1.073,6.332c0.087,'
                          '0.521 -0.13,1.047 -0.56,1.36c-0.431,0.313 -1,0.348 -1.469,0.1l-5.576,-2.977l-5.575,2.977c-0.47,'
                          '0.248 -1.039,0.209 -1.469,-0.1c-0.43,-0.309 -0.648,-0.839 -0.561,-1.36l1.069,-6.332l-4.528,'
                          '-4.48c-0.374,-0.37 -0.504,-0.922 -0.343,-1.421c0.161,-0.5 0.595,-0.865 1.117,-0.943l6.24,'
                          '-0.922l2.794,-5.749c0.235,-0.478 0.717,-0.782 1.252,-0.782c0.534,-0 1.021,0.304 1.251,0.782Zm-0.9,'
                          '0.434c-0.065,-0.133 -0.202,-0.216 -0.351,-0.216c-0.151,-0 -0.287,0.087 -0.354,0.222l-2.793,'
                          '5.746c-0.144,0.298 -0.426,0.504 -0.753,0.553l-6.238,0.921c-0.145,0.021 -0.268,0.121 -0.313,'
                          '0.26c-0.046,0.142 -0.012,0.299 0.094,0.403l4.529,4.481c0.231,0.229 0.337,0.557 0.282,0.878l-1.068,'
                          '6.329c-0.025,0.147 0.036,0.297 0.157,0.383c0.122,0.088 0.285,0.099 0.419,0.029l5.571,-2.975c0.295,'
                          '-0.157 0.648,-0.157 0.942,-0l5.572,2.975c0.132,0.069 0.292,0.063 0.413,-0.025c0.123,-0.089 0.188,'
                          '-0.238 0.163,-0.387l-1.073,-6.329c-0.055,-0.321 0.051,-0.649 0.282,-0.878l4.529,-4.481c0.104,'
                          '-0.103 0.143,-0.256 0.097,-0.396c-0.047,-0.141 -0.168,-0.245 -0.316,-0.267l-6.242,-0.921c-0.327,'
                          '-0.049 -0.609,-0.255 -0.754,-0.553l-2.794,-5.749l-0.001,-0.003Z',
                        fill="#FFA800"
                    )
                ], viewBox="0 0 24 24", width="100%", height="100%", className="star_icon"),
            ], className="star_top", style={"width": str(decimal) + "%"})
        ], className="star_icon_container star_icon_half")
    else:
        return html.Div([
            Svg([
                Path(
                    d='M13.295,1.656c-0.23,-0.478 -0.717,-0.782 -1.251,-0.782c-0.535,-0 -1.017,0.304 -1.252,0.782l-2.794,'
                      '5.749l-6.24,0.922c-0.522,0.078 -0.956,0.443 -1.117,0.943c-0.161,0.499 -0.031,1.051 0.343,'
                      '1.421l4.528,4.48l-1.069,6.332c-0.087,0.521 0.131,1.051 0.561,1.36c0.43,0.309 0.999,0.348 1.469,'
                      '0.1l5.575,-2.977l5.576,2.977c0.469,0.248 1.038,0.213 1.469,-0.1c0.43,-0.313 0.647,-0.839 0.56,'
                      '-1.36l-1.073,-6.332l4.528,-4.48c0.374,-0.37 0.508,-0.922 0.343,-1.421c-0.165,-0.5 -0.595,'
                      '-0.865 -1.116,-0.943l-6.245,-0.922l-2.795,-5.749Z" '
                      'style="fill-opacity:0;fill-rule:nonzero;"/><path d="M13.295,1.656l2.795,5.749l6.245,0.922c0.521,'
                      '0.078 0.951,0.443 1.116,0.943c0.165,0.499 0.031,1.051 -0.343,1.421l-4.528,4.48l1.073,6.332c0.087,'
                      '0.521 -0.13,1.047 -0.56,1.36c-0.431,0.313 -1,0.348 -1.469,0.1l-5.576,-2.977l-5.575,2.977c-0.47,'
                      '0.248 -1.039,0.209 -1.469,-0.1c-0.43,-0.309 -0.648,-0.839 -0.561,-1.36l1.069,-6.332l-4.528,'
                      '-4.48c-0.374,-0.37 -0.504,-0.922 -0.343,-1.421c0.161,-0.5 0.595,-0.865 1.117,-0.943l6.24,'
                      '-0.922l2.794,-5.749c0.235,-0.478 0.717,-0.782 1.252,-0.782c0.534,-0 1.021,0.304 1.251,0.782Zm-0.9,'
                      '0.434c-0.065,-0.133 -0.202,-0.216 -0.351,-0.216c-0.151,-0 -0.287,0.087 -0.354,0.222l-2.793,'
                      '5.746c-0.144,0.298 -0.426,0.504 -0.753,0.553l-6.238,0.921c-0.145,0.021 -0.268,0.121 -0.313,'
                      '0.26c-0.046,0.142 -0.012,0.299 0.094,0.403l4.529,4.481c0.231,0.229 0.337,0.557 0.282,0.878l-1.068,'
                      '6.329c-0.025,0.147 0.036,0.297 0.157,0.383c0.122,0.088 0.285,0.099 0.419,0.029l5.571,-2.975c0.295,'
                      '-0.157 0.648,-0.157 0.942,-0l5.572,2.975c0.132,0.069 0.292,0.063 0.413,-0.025c0.123,-0.089 0.188,'
                      '-0.238 0.163,-0.387l-1.073,-6.329c-0.055,-0.321 0.051,-0.649 0.282,-0.878l4.529,-4.481c0.104,'
                      '-0.103 0.143,-0.256 0.097,-0.396c-0.047,-0.141 -0.168,-0.245 -0.316,-0.267l-6.242,-0.921c-0.327,'
                      '-0.049 -0.609,-0.255 -0.754,-0.553l-2.794,-5.749l-0.001,-0.003Z',
                    fill="#e3e5f3"
                )
            ], viewBox="0 0 24 24", width="100%", height="100%", className="star_icon")
        ], className="star_icon_container star_icon_empty")


def has_decimal(number):
    return number % 1 != 0


def get_decimal(number):
    decimal = number - math.floor(number)
    return decimal


def star_rating(total_training_effect, layout=None):
    if isinstance(total_training_effect, float) and math.isnan(total_training_effect):
        total_training_effect = 0
    max = 5
    decimal = round(get_decimal(total_training_effect) * 100, 0)
    rating = round(total_training_effect, 1)
    list_stars = []
    for i in range(0, max):
        if i < int(str(total_training_effect)[0]):
            list_stars.append(star("filled"))
        elif i == int(str(total_training_effect)[0]):
            list_stars.append(star("half", decimal))
        else:
            list_stars.append(star("empty"))

    return html.Div([
        html.Div(children=list_stars, className="star-rating d-inline-flex {}".format(layout)),
        html.Div(f"{rating} / 5", className="star_container_text {}".format(layout))
    ], className="d-inline-flex justify-content-center align-items-center")
