from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import h_transport_materials as htm
import numpy as np

all_diffusivities = htm.diffusivities
all_solubilities = htm.solubilities

materials_options = np.unique(
    [
        prop.material
        for prop in all_diffusivities.properties + all_solubilities.properties
    ]
).tolist()
isotope_options = ["H", "D", "T"]


def make_tab(property):
    """_summary_

    Args:
        property (_type_): _description_

    Returns:
        _type_: _description_
    """

    assert property in ["diffusivity", "solubility"]

    property_to_group = {
        "diffusivity": htm.diffusivities,
        "solubility": htm.solubilities,
    }

    all_properties = property_to_group[property]

    initial_material = "tungsten"

    authors_options = np.unique(
        [
            prop.author.capitalize()
            for prop in all_properties
            if prop.material == "tungsten"
        ]
    ).tolist()

    years_options = [prop.year for prop in all_properties]
    min_year = min(years_options)
    max_year = max(years_options)

    tab = dbc.Tab(
        label=property.capitalize(),
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Filter by material:"),
                            dcc.Dropdown(
                                options=materials_options,
                                value=[initial_material],
                                multi=True,
                                id=f"material_filter_{property}",
                            ),
                            html.Div(
                                dbc.Button(
                                    "All",
                                    id=f"add_all_materials_{property}",
                                    style={"font-size": "12px"},
                                )
                            ),
                            html.Br(),
                            dbc.Label("Filter by isotope:"),
                            dbc.Checklist(
                                value=isotope_options,
                                options=[
                                    {"label": i, "value": i} for i in isotope_options
                                ],
                                inline=True,
                                id=f"isotope_filter_{property}",
                            ),
                            html.Br(),
                            html.Label("Filter by author:"),
                            dcc.Dropdown(
                                value=authors_options,
                                options=authors_options,
                                multi=True,
                                id=f"author_filter_{property}",
                            ),
                            html.Div(
                                dbc.Button(
                                    "All",
                                    id=f"add_all_authors_{property}",
                                    style={"font-size": "12px"},
                                )
                            ),
                            html.Br(),
                            html.Label("Filter by year:"),
                            dcc.RangeSlider(
                                id=f"year_filter_{property}",
                                min=min_year,
                                max=max_year,
                                step=1,
                                value=[min_year, max_year],
                                marks={
                                    int(i): str(i)
                                    for i in np.arange(min_year, max_year)
                                    if int(i) % 10 == 0
                                },
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True,
                                },
                            ),
                            html.Br(),
                            html.Div(
                                [
                                    dbc.Button(
                                        "Compute mean curve",
                                        id=f"mean_button_{property}",
                                        color="primary",
                                        style={"margin": "5px"},
                                        n_clicks="0",
                                    ),
                                    dbc.Button(
                                        "Add property",
                                        id=f"add_property_{property}",
                                        color="primary",
                                        style={"margin": "5px"},
                                        n_clicks="0",
                                    ),
                                    dbc.Button(
                                        [
                                            "Extract data",
                                            dcc.Download(
                                                id=f"download-text_{property}"
                                            ),
                                        ],
                                        id=f"extract_button_{property}",
                                        color="primary",
                                        style={"margin": "5px"},
                                        n_clicks="0",
                                    ),
                                    dbc.Button(
                                        [
                                            "Python",
                                            dcc.Download(
                                                id=f"download-python_{property}"
                                            ),
                                        ],
                                        id=f"python_button_{property}",
                                        color="primary",
                                        style={"margin": "5px"},
                                        n_clicks_timestamp="0",
                                    ),
                                ]
                            ),
                        ],
                        className="pretty_container",
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(
                                id=f"graph_{property}",
                                style={"width": "120vh", "height": "70vh"},
                            ),
                        ],
                        className="pretty_container",
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(id=f"graph_prop_per_year_{property}"),
                        ],
                        className="pretty_container",
                        width=4,
                    ),
                    dbc.Col(
                        [
                            dcc.RadioItems(
                                options=["Total", "Per year"],
                                value="Total",
                                id=f"radio_citations_{property}",
                                inline=True,
                                inputStyle={
                                    "margin-left": "20px",
                                    "margin-right": "5px",
                                },
                            ),
                            dcc.Graph(id=f"graph_nb_citations_{property}"),
                        ],
                        className="pretty_container",
                    ),
                ]
            ),
        ],
    )
    return tab
