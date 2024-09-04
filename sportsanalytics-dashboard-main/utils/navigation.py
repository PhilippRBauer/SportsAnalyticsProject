import dash
import dash_bootstrap_components as dbc
from dash import html


def navigation():
    excluded_pages = ['Activity', 'Not found 404']
    return html.Div([
        dbc.Nav(
            [
                dbc.NavLink(
                    page['name'],
                    href=page["relative_path"],
                    active="exact",
                    className="btn btn-secondary btn-lg me-md-2"
                )
                for page in dash.page_registry.values()
                if page['name'] not in excluded_pages
            ],
            vertical=False,
        )
    ])
