from infos import text_infos
from new_diffusivity_form import form_new_diffusivity
from new_solubility_form import form_new_solubility

from tab import make_tab

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

tab_diffusivity = make_tab("diffusivity")
tab_solubility = make_tab("solubility")

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
        dcc.Tabs(
            id="tabs-example-graph",
            value="tab_diffusivity",
            children=[tab_diffusivity, tab_solubility],
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(html.H2("Add a diffusivity"))),
                dbc.ModalBody(form_new_diffusivity),
                dbc.ModalFooter(
                    [
                        html.Div("", id="error_message_new_diffusivity"),
                        dbc.Button(
                            "Submit",
                            id="submit_new_diffusivity",
                            color="primary",
                            n_clicks="0",
                        ),
                    ]
                ),
            ],
            id="modal_add_diffusivity",
            is_open=False,
            # size="lg",
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(html.H2("Add a solubility"))),
                dbc.ModalBody(form_new_solubility),
                dbc.ModalFooter(
                    [
                        html.Div("", id="error_message_new_solubility"),
                        dbc.Button(
                            "Submit",
                            id="submit_new_solubility",
                            color="primary",
                            n_clicks="0",
                        ),
                    ]
                ),
            ],
            id="modal_add_solubility",
            is_open=False,
        ),
    ],
    fluid=True,
)
