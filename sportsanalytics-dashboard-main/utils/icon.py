from dash import html


def return_icon(name="cycling", size="", class_name=""):
    return html.Div([
        html.Img(src=f"/assets/{name}.png", className="img-fluid")
    ], className=f"sport__icon justify-content-center align-items-center d-flex rounded-3 p-1 {size} {class_name}")


def render_icon_indicator(indicator="all"):
    icon_list = []
    for i in ["running", "cycling", "swimming"]:
        if "all" in indicator:
            icon_list.append(return_icon(i))
        elif i in indicator:
            icon_list.append(return_icon(i, class_name="icon__indicator--active"))
        else:
            icon_list.append(return_icon(i, class_name="icon__indicator--inactive"))

    return icon_list
