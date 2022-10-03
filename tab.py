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

    authors_options = np.unique(
        [prop.author.capitalize() for prop in all_properties]
    ).tolist()

    years_options = [prop.year for prop in all_properties]
    min_year = min(years_options)
    max_year = max(years_options)

    tab = dcc.Tab(
        label=property.capitalize(),
        value="tab_{}".format(property),
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Filter by material:"),
                            dcc.Dropdown(
                                options=materials_options,
                                value=["tungsten"],
                                multi=True,
                                id="material_filter_{}".format(property),
                            ),
                            html.Div(
                                dbc.Button(
                                    "All",
                                    id="add_all_materials_{}".format(property),
                                    style={"font-size": "12px"},
                                )
                            ),
                            html.Br(),
                            html.Label("Filter by isotope:"),
                            dcc.Checklist(
                                value=isotope_options,
                                options=isotope_options,
                                inline=True,
                                id="isotope_filter_{}".format(property),
                                inputStyle={
                                    "margin-left": "20px",
                                    "margin-right": "4px",
                                },
                            ),
                            html.Br(),
                            html.Label("Filter by author:"),
                            dcc.Dropdown(
                                value=np.unique(
                                    [
                                        prop.author.capitalize()
                                        for prop in all_properties
                                        if prop.material == "tungsten"
                                    ]
                                ).tolist(),
                                options=authors_options,
                                multi=True,
                                id="author_filter_{}".format(property),
                            ),
                            html.Div(
                                dbc.Button(
                                    "All",
                                    id="add_all_authors_{}".format(property),
                                    style={"font-size": "12px"},
                                )
                            ),
                            html.Br(),
                            html.Label("Filter by year:"),
                            dcc.RangeSlider(
                                id="year_filter_{}".format(property),
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
                                        id="mean_button_{}".format(property),
                                        color="primary",
                                        style={"margin": "5px"},
                                        n_clicks="0",
                                    ),
                                    dbc.Button(
                                        "Add property",
                                        id="add_property_{}".format(property),
                                        color="primary",
                                        style={"margin": "5px"},
                                        n_clicks="0",
                                    ),
                                    dbc.Button(
                                        [
                                            "Extract data",
                                            dcc.Download(
                                                id="download-text_{}".format(property)
                                            ),
                                        ],
                                        id="extract_button_{}".format(property),
                                        color="primary",
                                        style={"margin": "5px"},
                                        n_clicks="0",
                                    ),
                                    dbc.Button(
                                        [
                                            "Python",
                                            dcc.Download(
                                                id="download-python_{}".format(property)
                                            ),
                                        ],
                                        id="python_button_{}".format(property),
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
                                id="graph_{}".format(property),
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
                            dcc.Graph(id="graph_prop_per_year_{}".format(property)),
                        ],
                        className="pretty_container",
                        width=4,
                    ),
                    dbc.Col(
                        [
                            dcc.RadioItems(
                                options=["Total", "Per year"],
                                value="Total",
                                id="radio_citations_{}".format(property),
                                inline=True,
                                inputStyle={
                                    "margin-left": "20px",
                                    "margin-right": "5px",
                                },
                            ),
                            dcc.Graph(id="graph_nb_citations_{}".format(property)),
                        ],
                        className="pretty_container",
                    ),
                ]
            ),
        ],
    )
    return tab
