from dash import dcc, dash_table
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq

import h_transport_materials as htm
import numpy as np
import json

materials_options = list(set([prop.material.name for prop in htm.database]))
materials_options += list(set([prop.material.family for prop in htm.database]))

isotope_options = ["H", "D", "T"]

pretty_label = {
    "diffusivity": "Diffusivity",
    "solubility": "Solubility",
    "permeability": "Permeability",
    "recombination_coeff": "Recombination coeff.",
    "dissociation_coeff": "Dissociation coeff.",
}


def make_tab(property: str):
    """_summary_

    Args:
        property (str): _description_

    Returns:
        dbc.Tab: the tab
    """

    assert property in [
        "diffusivity",
        "solubility",
        "permeability",
        "recombination_coeff",
        "dissociation_coeff",
    ]

    property_to_group = {
        "diffusivity": htm.diffusivities,
        "solubility": htm.solubilities,
        "permeability": htm.permeabilities,
        "recombination_coeff": htm.recombination_coeffs,
        "dissociation_coeff": htm.dissociation_coeffs,
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

    table = make_table(property)

    table_tab = dbc.Tab([table], label="Table")

    graph_tab = dbc.Tab(
        [
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Colour by:"),
                                    dcc.Dropdown(
                                        ["property", "material", "author", "isotope"],
                                        "property",
                                        id=f"colour-by_{property}",
                                        style=dict(width="150px"),
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    dcc.Graph(
                                        id=f"graph_{property}",
                                        style={"height": "600px"},
                                    )
                                ],
                                width=10,
                            ),
                        ],
                    ),
                ],
                body=True,
                className="mb-2",
            )
        ],
        label="Graph",
    )

    sub_tabs = dbc.Tabs([graph_tab, table_tab], id=f"subtabs_{property}")

    controls = dbc.Card(
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
                options=[{"label": i, "value": i} for i in isotope_options],
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
                            dcc.Download(id=f"download-text_{property}"),
                        ],
                        id=f"extract_button_{property}",
                        color="primary",
                        style={"margin": "5px"},
                        n_clicks="0",
                    ),
                    dbc.Button(
                        [
                            "Python",
                            dcc.Download(id=f"download-python_{property}"),
                        ],
                        id=f"python_button_{property}",
                        color="primary",
                        style={"margin": "5px"},
                        n_clicks_timestamp="0",
                    ),
                ]
            ),
        ],
        body=True,
    )
    with open("htm_dashboard/citations.json") as f:
        citation_data = json.load(f)
    date_citations = citation_data["date"]
    graph_prop_per_year = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Number of properties per year", className="card-title"),
                    dcc.Graph(id=f"graph_prop_per_year_{property}"),
                ]
            )
        ],
        className="mb-2",
    )

    graph_citations = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Number of citations", className="card-title"),
                    html.H6(
                        f"source: Crossref {date_citations}", className="card-subtitle"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    daq.BooleanSwitch(
                                        label="Per year",
                                        on=False,
                                        id=f"per_year_citations_{property}",
                                    ),
                                ],
                                width=1,
                            ),
                            dbc.Col(
                                [dcc.Graph(id=f"graph_nb_citations_{property}")],
                                width=11,
                            ),
                        ],
                        align="center",
                    ),
                ]
            )
        ],
        className="mb-2",
    )

    piechart_materials = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Repartition by materials", className="card-title"),
                    dcc.Graph(id=f"graph_materials_{property}"),
                ]
            )
        ],
        className="mb-2",
    )
    piechart_isotopes = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Repartition by isotopes", className="card-title"),
                    dcc.Graph(id=f"graph_isotopes_{property}"),
                ]
            )
        ],
        className="mb-2",
    )
    piechart_authors = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Repartition by authors", className="card-title"),
                    dcc.Graph(id=f"graph_authors_{property}"),
                ]
            )
        ],
        className="mb-2",
    )

    tab = dbc.Tab(
        label=pretty_label[property],
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [controls],
                        width=3,
                        style={"overflow-y": "auto", "maxHeight": "600px"},
                    ),
                    dbc.Col([sub_tabs]),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col([graph_prop_per_year], width=3),
                    dbc.Col([graph_citations], width=4),
                    dbc.Col([piechart_materials], width=4),
                ],
                justify="evenly",
            ),
            dbc.Row(
                [
                    dbc.Col([piechart_isotopes], width=4),
                    dbc.Col([piechart_authors], width=4),
                ],
                justify="evenly",
            ),
        ],
    )
    return tab


TABLE_KEYS = ["material", "pre_exp", "act_energy", "range", "author", "doi"]

prop_key_to_label = {
    "diffusivity": {"pre_exp": "D_0", "act_energy": "E_D"},
    "solubility": {"pre_exp": "S_0", "act_energy": "E_S"},
    "permeability": {"pre_exp": "P_0", "act_energy": "E_P"},
    "recombination_coeff": {"pre_exp": "Kr_0", "act_energy": "E_Kr"},
    "dissociation_coeff": {"pre_exp": "Kd_0", "act_energy": "E_Kd"},
}

key_to_label = {
    "material": "Material",
    "range": "Range",
    "author": "Author",
    "doi": "DOI",
}


def make_table_labels(property):
    labels = []
    for key in TABLE_KEYS:
        if key in key_to_label:
            labels.append(key_to_label[key])
        else:
            labels.append(prop_key_to_label[property][key])
    return labels


def make_table(property):

    table = dash_table.DataTable(
        id=f"table_{property}",
        columns=[
            {
                "name": label,
                "id": key,
                "presentation": "markdown",
            }  # markdown is needed to have clickable links
            if key == "doi"
            else {"name": label, "id": key}
            for key, label in zip(TABLE_KEYS, make_table_labels(property))
        ],
        data=[],
        page_size=10,
        editable=False,
        cell_selectable=True,
        # filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
    )

    return table
