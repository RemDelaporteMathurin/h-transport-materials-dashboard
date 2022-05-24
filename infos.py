import h_transport_materials
from dash import html

try:
    version = h_transport_materials.__version__
except AttributeError:
    version = "[unknown]"

text_infos = [
    html.Div(
        [
            "Finding material properties for ",
            html.B("hydrogen transport"),
            " is often tedious as many different values can be found in literature. ",
            "The goal of this tool is to help scientists visualise material properties and compare them.",
        ]
    ),
    html.Br(),
    html.Div(
        "On the left-hand side of the screen, properties can be filtered by material, author, isotope or by year of publication."
    ),
    html.Br(),
    html.Div(
        [
            html.B("Compute mean curve"),
            ": calculates the mean curve of the displayed properties.",
        ]
    ),
    html.Br(),
    html.Div(
        [
            html.B("Add property"),
            ": adds a custom diffusivity or solubility to the dataset.",
        ]
    ),
    html.Br(),
    html.Div(
        [html.B("Extract data"), ": downloads the displayed properties to a JSON file."]
    ),
    html.Br(),
    html.Div(
        [
            html.B("Python"),
            ": generates a python script using h-transport-materials to plot the displayed data.",
        ]
    ),
    html.Br(),
    html.Div(
        "This dashboard relies on the library H-transport-materials (HTM) v{} and Plotly dash.".format(
            version
        )
    ),
]
