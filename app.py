from plotly.colors import DEFAULT_PLOTLY_COLORS
import numpy as np
from graph import (
    all_diffusivities,
    all_solubilities,
    make_diffusivities,
    make_solubilities,
    all_authors_diffusivities,
    all_authors_solubilities,
    make_graph,
    make_graph_solubilities,
    add_mean_value,
    add_mean_value_solubilities,
    min_year_solubilities,
    max_year_solubilities,
)

import h_transport_materials as htm

from export import create_data_as_dict, generate_python_code
from infos import text_infos

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

server = app.server

all_materials = ["tungsten", "copper", "cucrzr"]
all_isotopes = ["H", "D", "T"]

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("H-transport properties dashboard"),
                        html.H5("Rémi Delaporte-Mathurin"),
                    ],
                    width=9,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.A(
                                [
                                    "Infos",
                                    html.Img(
                                        src="https://dash.gallery/dash-world-cell-towers/assets/question-circle-solid.svg",
                                        height=20,
                                        style={"margin-left": "5px"},
                                    ),
                                ],
                                style={
                                    "margin-right": "45px",
                                    "cursor": "pointer",
                                },
                                id="open-sm",
                            ),
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(
                                        dbc.ModalTitle(
                                            html.H2(
                                                "Welcome to the H-transport materials dashboard!"
                                            )
                                        )
                                    ),
                                    dbc.ModalBody(text_infos),
                                    dbc.ModalFooter(
                                        "Contact: rdelaportemathurin@gmail.com"
                                    ),
                                ],
                                id="modal",
                                is_open=False,
                                size="lg",
                            ),
                            html.A(
                                [
                                    "View it on GitHub",
                                    html.Img(
                                        src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
                                        height=40,
                                    ),
                                ],
                                href="https://github.com/RemDelaporteMathurin/h-transport-materials-dashboard",
                                target="_blank",  # opens in a new tab
                            ),
                        ]
                    ),
                    align="end",
                    width=3,
                ),
            ],
            align="end",
        ),
        html.Hr(),
        dcc.Tabs(
            id="tabs-example-graph",
            value="tab-1",
            children=[
                dcc.Tab(
                    label="Diffusivity",
                    value="tab-1",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Filter by material:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                            id="material_all_radio_diffusivities",
                                        ),
                                        dcc.Dropdown(
                                            all_materials,
                                            ["tungsten"],
                                            multi=True,
                                            id="material_filter_diffusivities",
                                        ),
                                        html.Br(),
                                        html.Label("Filter by isotope:"),
                                        dcc.Checklist(
                                            all_isotopes,
                                            all_isotopes,
                                            inline=True,
                                            id="isotope_filter_diffusivities",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "4px",
                                            },
                                        ),
                                        html.Br(),
                                        html.Label("Filter by author:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                            id="author_all_radio_diffusivities",
                                        ),
                                        dcc.Dropdown(
                                            all_authors_diffusivities,
                                            ["Frauenfelder"],
                                            multi=True,
                                            id="author_filter_diffusivities",
                                        ),
                                        html.Br(),
                                        html.Label("Filter by year:"),
                                        dcc.RangeSlider(
                                            id="year_filter_diffusivities",
                                            min=1950,
                                            max=2021,
                                            step=1,
                                            value=[1950, 2021],
                                            marks={
                                                int(i): str(i)
                                                for i in np.arange(1950, 2021, step=10)
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
                                                    id="mean_button_diffusivity",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks="0",
                                                ),
                                                dbc.Button(
                                                    "Add property",
                                                    id="add_property_diffusivity",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks="0",
                                                ),
                                                dbc.Button(
                                                    [
                                                        "Extract data",
                                                        dcc.Download(
                                                            id="download-text_diffusivity"
                                                        ),
                                                    ],
                                                    id="extract_button_diffusivity",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks="0",
                                                ),
                                                dbc.Button(
                                                    [
                                                        "Python",
                                                        dcc.Download(
                                                            id="download-python_diffusivity"
                                                        ),
                                                    ],
                                                    id="python_button_diffusivity",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks_timestamp="0",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="graph_diffusivity",
                                            figure=make_graph(
                                                make_diffusivities(
                                                    materials=all_materials,
                                                    authors=all_authors_diffusivities,
                                                    isotopes=all_isotopes,
                                                    years=[1950, 2021],
                                                )
                                            ),
                                            style={"width": "150vh", "height": "70vh"},
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Solubility",
                    value="tab-2",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Filter by material:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                            id="material_all_radio_solubilities",
                                        ),
                                        dcc.Dropdown(
                                            all_materials,
                                            all_materials,
                                            multi=True,
                                            id="material_filter_solubilities",
                                        ),
                                        html.Br(),
                                        html.Label("Filter by isotope:"),
                                        dcc.Checklist(
                                            all_isotopes,
                                            all_isotopes,
                                            inline=True,
                                            id="isotope_filter_solubilities",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "4px",
                                            },
                                        ),
                                        html.Br(),
                                        html.Label("Filter by author:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                            id="author_all_radio_solubilities",
                                        ),
                                        dcc.Dropdown(
                                            all_authors_solubilities,
                                            all_authors_solubilities,
                                            multi=True,
                                            id="author_filter_solubilities",
                                        ),
                                        html.Br(),
                                        html.Label("Filter by year:"),
                                        dcc.RangeSlider(
                                            id="year_filter_solubilities",
                                            min=1950,
                                            max=2021,
                                            step=1,
                                            value=[1950, 2021],
                                            marks={
                                                int(i): str(i)
                                                for i in np.arange(1950, 2021, step=10)
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
                                                    id="mean_button_solubility",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks_timestamp="0",
                                                ),
                                                dbc.Button(
                                                    "Add property",
                                                    id="add_property_solubility",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks="0",
                                                ),
                                                dbc.Button(
                                                    [
                                                        "Extract data",
                                                        dcc.Download(
                                                            id="download-text_solubility"
                                                        ),
                                                    ],
                                                    id="extract_button_solubility",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks_timestamp="0",
                                                ),
                                                dbc.Button(
                                                    [
                                                        "Python",
                                                        dcc.Download(
                                                            id="download-python_solubility"
                                                        ),
                                                    ],
                                                    id="python_button_solubility",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks_timestamp="0",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="graph_solubilities",
                                            figure=make_graph_solubilities(
                                                make_solubilities(
                                                    materials=all_materials,
                                                    authors=all_authors_diffusivities,
                                                    isotopes=all_isotopes,
                                                    years=[1950, 2021],
                                                )
                                            ),
                                            style={"width": "150vh", "height": "70vh"},
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
    ],
    fluid=True,
)
app.layout = layout


@app.callback(
    dash.Output("material_filter_diffusivities", "value"),
    dash.Input("material_all_radio_diffusivities", "value"),
)
def add_all_material(material_all_radio):
    if material_all_radio == "All":
        return all_materials
    else:
        return []


@app.callback(
    dash.Output("author_filter_diffusivities", "value"),
    dash.Input("author_all_radio_diffusivities", "value"),
)
def add_all_authors(author_all_radio_diffusivities):
    if author_all_radio_diffusivities == "All":
        return all_authors_diffusivities
    else:
        return []


# callback filter material diffusivity
@app.callback(
    dash.Output("graph_diffusivity", "figure"),
    dash.Input("material_filter_diffusivities", "value"),
    dash.Input("isotope_filter_diffusivities", "value"),
    dash.Input("author_filter_diffusivities", "value"),
    dash.Input("year_filter_diffusivities", "value"),
    dash.Input("mean_button_diffusivity", "n_clicks"),
)
def update_graph(
    material_filter_diffusivities,
    isotope_filter_diffusivities,
    author_filter_diffusivities,
    year_filter_diffusivities,
    mean_button_diffusivity,
):
    diffusitivites = make_diffusivities(
        materials=material_filter_diffusivities,
        authors=author_filter_diffusivities,
        isotopes=isotope_filter_diffusivities,
        years=year_filter_diffusivities,
    )
    figure = make_graph(diffusitivites)
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "mean_button_diffusivity.n_clicks":
        add_mean_value(diffusitivites, figure)

    return figure


@app.callback(
    dash.Output("material_filter_solubilities", "value"),
    dash.Input("material_all_radio_solubilities", "value"),
)
def add_all_material(material_all_radio):
    if material_all_radio == "All":
        return all_materials
    else:
        return []


@app.callback(
    dash.Output("author_filter_solubilities", "value"),
    dash.Input("author_all_radio_solubilities", "value"),
)
def add_all_authors(author_all_radio_solubilities):
    if author_all_radio_solubilities == "All":
        return all_authors_solubilities
    else:
        return []


# callback filters solubility
@app.callback(
    dash.Output("graph_solubilities", "figure"),
    dash.Input("material_filter_solubilities", "value"),
    dash.Input("isotope_filter_solubilities", "value"),
    dash.Input("author_filter_solubilities", "value"),
    dash.Input("year_filter_solubilities", "value"),
    dash.Input("mean_button_solubility", "n_clicks"),
)
def update_solubility_graph(
    material_filter_solubilities,
    isotope_filter_solubilities,
    author_filter_solubilities,
    year_filter_solubilities,
    mean_button_solubility,
):
    solubilities = make_solubilities(
        materials=material_filter_solubilities,
        authors=author_filter_solubilities,
        isotopes=isotope_filter_solubilities,
        years=year_filter_solubilities,
    )
    figure = make_graph_solubilities(solubilities)
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "mean_button_solubility.n_clicks":
        add_mean_value_solubilities(solubilities, figure)

    return figure


# extract data buttons
@app.callback(
    dash.Output("download-text_diffusivity", "data"),
    dash.Input("extract_button_diffusivity", "n_clicks"),
    dash.Input("material_filter_diffusivities", "value"),
    dash.Input("isotope_filter_diffusivities", "value"),
    dash.Input("author_filter_diffusivities", "value"),
    dash.Input("year_filter_diffusivities", "value"),
    prevent_initial_call=True,
)
def func(
    n_clicks,
    material_filter_diffusivities,
    isotope_filter_diffusivities,
    author_filter_diffusivities,
    year_filter_diffusivities,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "extract_button_diffusivity.n_clicks":
        diffusivities = make_diffusivities(
            materials=material_filter_diffusivities,
            authors=author_filter_diffusivities,
            isotopes=isotope_filter_diffusivities,
            years=year_filter_diffusivities,
        )
        return dict(
            content=create_data_as_dict(diffusivities),
            filename="data.json",
        )


@app.callback(
    dash.Output("download-text_solubility", "data"),
    dash.Input("extract_button_solubility", "n_clicks"),
    dash.Input("material_filter_solubilities", "value"),
    dash.Input("isotope_filter_solubilities", "value"),
    dash.Input("author_filter_solubilities", "value"),
    dash.Input("year_filter_solubilities", "value"),
    prevent_initial_call=True,
)
def func(
    n_clicks,
    material_filter_solubilities,
    isotope_filter_solubilities,
    author_filter_solubilities,
    year_filter_solubilities,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "extract_button_solubility.n_clicks":
        solubilities = make_solubilities(
            materials=material_filter_solubilities,
            authors=author_filter_solubilities,
            isotopes=isotope_filter_solubilities,
            years=year_filter_solubilities,
        )
        return dict(
            content=create_data_as_dict(solubilities),
            filename="data.json",
        )


# callbacks for python buttons
@app.callback(
    dash.Output("download-python_solubility", "data"),
    dash.Input("python_button_solubility", "n_clicks"),
    dash.Input("material_filter_solubilities", "value"),
    dash.Input("isotope_filter_solubilities", "value"),
    dash.Input("author_filter_solubilities", "value"),
    dash.Input("year_filter_solubilities", "value"),
    prevent_initial_call=True,
)
def func(
    n_clicks,
    material_filter_solubilities,
    isotope_filter_solubilities,
    author_filter_solubilities,
    year_filter_solubilities,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "python_button_solubility.n_clicks":

        return dict(
            content=generate_python_code(
                materials=material_filter_solubilities,
                isotopes=isotope_filter_solubilities,
                authors=author_filter_solubilities,
                yearmin=year_filter_solubilities[0],
                yearmax=year_filter_solubilities[1],
                group="solubilities",
            ),
            filename="script.py",
        )


@app.callback(
    dash.Output("download-python_diffusivity", "data"),
    dash.Input("python_button_diffusivity", "n_clicks"),
    dash.Input("material_filter_diffusivities", "value"),
    dash.Input("isotope_filter_diffusivities", "value"),
    dash.Input("author_filter_diffusivities", "value"),
    dash.Input("year_filter_diffusivities", "value"),
    prevent_initial_call=True,
)
def func(
    n_clicks,
    material_filter_diffusivities,
    isotope_filter_diffusivities,
    author_filter_diffusivities,
    year_filter_diffusivities,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "python_button_diffusivity.n_clicks":

        return dict(
            content=generate_python_code(
                materials=material_filter_diffusivities,
                isotopes=isotope_filter_diffusivities,
                authors=author_filter_diffusivities,
                yearmin=year_filter_diffusivities[0],
                yearmax=year_filter_diffusivities[1],
                group="diffusivities",
            ),
            filename="script.py",
        )


@app.callback(
    dash.Output("modal", "is_open"),
    dash.Input("open-sm", "n_clicks"),
    dash.State("modal", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    dash.Output("material_filter_diffusivities", "options"),
    dash.Output("author_filter_diffusivities", "options"),
    dash.Input("add_property_diffusivity", "n_clicks"),
    prevent_initial_call=True,
)
def add_diffusivity(n_clicks):
    new_property = htm.ArrheniusProperty(
        pre_exp=1,
        act_energy=0.2,
        author="new_author",
        year=1950,
        isotope="h",
        material="new_mat",
    )
    all_diffusivities.properties.append(new_property)
    all_authors = np.unique([D.author.capitalize() for D in all_diffusivities]).tolist()
    all_materials = np.unique([D.material.lower() for D in all_diffusivities]).tolist()
    return all_materials, all_authors


if __name__ == "__main__":
    app.run_server(debug=True)
