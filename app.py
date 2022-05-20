from plotly.colors import DEFAULT_PLOTLY_COLORS
import numpy as np
from graph import (
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
                    width=True,
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
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                            id="isotope_all_radio_diffusivities",
                                        ),
                                        dcc.Dropdown(
                                            all_isotopes,
                                            ["H"],
                                            multi=True,
                                            id="isotope_filter_diffusivities",
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
                                                    "Extract data",
                                                    id="extract_button_diffusivity",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks="0",
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
                                        ),
                                        dcc.Dropdown(
                                            all_materials,
                                            all_materials,
                                            multi=True,
                                            id="material_filter_solubilities",
                                        ),
                                        html.Br(),
                                        html.Label("Filter by isotope:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            all_isotopes,
                                            all_isotopes,
                                            multi=True,
                                            id="isotope_filter_solubilities",
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
                                                    "Extract data",
                                                    id="extract_button_solubility",
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
    dash.Output("isotope_filter_diffusivities", "value"),
    dash.Input("isotope_all_radio_diffusivities", "value"),
)
def add_all_isotopes(isotope_all_radio):
    if isotope_all_radio == "All":
        return all_isotopes
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


if __name__ == "__main__":
    app.run_server(debug=True)
