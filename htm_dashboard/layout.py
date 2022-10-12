from .infos import text_infos
from .new_property_form import make_form

from .tab import make_tab

from dash import html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO


def make_modal_add_property(property: str):

    modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(html.H2(f"Add a {property}"))),
            dbc.ModalBody(make_form(property)),
            dbc.ModalFooter(
                [
                    html.Div("", id=f"error_message_new_{property}"),
                    dbc.Button(
                        "Submit",
                        id=f"submit_new_{property}",
                        color="primary",
                        n_clicks="0",
                    ),
                ]
            ),
        ],
        id=f"modal_add_{property}",
        is_open=False,
        # size="lg",
    )
    return modal


template_theme1 = "plotly_white"
template_theme2 = "plotly_dark"
url_theme1 = dbc.themes.MINTY
url_theme2 = dbc.themes.DARKLY
theme_switch = ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])

header = dbc.Row(
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
                            dbc.ModalFooter("Contact: rdelaportemathurin@gmail.com"),
                        ],
                        id="modal-infos",
                        is_open=False,
                        size="lg",
                    ),
                    html.A(
                        [
                            "View it on GitHub",
                            html.Img(
                                src="https://cdn-icons-png.flaticon.com/512/25/25231.png",
                                height=40,
                            ),
                        ],
                        href="https://github.com/RemDelaporteMathurin/h-transport-materials-dashboard",
                        target="_blank",  # opens in a new tab
                    ),
                    theme_switch,
                ]
            ),
            align="end",
            width=3,
        ),
    ],
    align="end",
)

layout = dbc.Container(
    [
        header,
        html.Hr(),
        dbc.Tabs(
            id="tabs-example-graph",
            children=[
                make_tab("diffusivity"),
                make_tab("solubility"),
                dbc.Tab(
                    label="Permeability",
                    children=[html.Div([dbc.Label("Work in progress", id="wip_1")])],
                ),
                make_tab("recombination_coeff"),
                dbc.Tab(
                    label="Dissociation coeff.",
                    children=[html.Div([dbc.Label("Work in progress", id="wip_3")])],
                ),
            ],
        ),
        make_modal_add_property("diffusivity"),
        make_modal_add_property("solubility"),
        make_modal_add_property("recombination_coeff"),
    ],
    fluid=True,
    className="dbc bg-opacity-10 bg-black mb-2",
)
