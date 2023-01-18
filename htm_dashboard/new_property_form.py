import dash_bootstrap_components as dbc
from dash import html


def make_form(property_type: str):

    if property_type == "diffusivity":
        pre_exp_label = "D_0 (m2/s)"
    elif property_type == "solubility":
        pre_exp_label = "S_0"
    elif property_type == "permeability":
        pre_exp_label = "P_0"
    elif property_type == "recombination_coeff":
        pre_exp_label = "Kr_0 (m4/s)"
    elif property_type == "dissociation_coeff":
        pre_exp_label = "Kd_0"

    preexponential_input = html.Div(
        [
            dbc.Label(pre_exp_label, width=2),
            dbc.Col(
                dbc.Input(
                    type="number",
                    id=f"new_{property_type}_pre_exp",
                    placeholder="Enter pre-exponential factor",
                    required=True,
                ),
                width=10,
            ),
        ],
    )

    activation_energy_input = html.Div(
        [
            dbc.Label("E_D (eV)", width=2),
            dbc.Col(
                dbc.Input(
                    type="number",
                    id=f"new_{property_type}_act_energy",
                    placeholder="Enter activation energy",
                    required=True,
                ),
                width=10,
            ),
        ],
    )

    author_input = html.Div(
        [
            dbc.Label("Author", width=2),
            dbc.Col(
                dbc.Input(
                    type="text",
                    id=f"new_{property_type}_author",
                    placeholder="Enter author",
                    required=True,
                ),
                width=10,
            ),
        ],
    )

    year_input = html.Div(
        [
            dbc.Label("Year", width=2),
            dbc.Col(
                dbc.Input(
                    type="number",
                    id=f"new_{property_type}_year",
                    placeholder="Enter year of publication",
                    required=True,
                ),
                width=10,
            ),
        ],
    )

    isotope_input = html.Div(
        [
            dbc.Label("Isotope", width=2),
            dbc.Col(
                dbc.RadioItems(
                    id=f"new_{property_type}_isotope",
                    value="H",
                    options=[
                        {"label": "H", "value": "H"},
                        {"label": "D", "value": "D"},
                        {"label": "T", "value": "T"},
                    ],
                ),
                width=10,
            ),
        ],
    )

    material_input = html.Div(
        [
            dbc.Label("Material", width=2),
            dbc.Col(
                dbc.Input(
                    type="text",
                    id=f"new_{property_type}_material",
                    placeholder="Enter material",
                    required=True,
                ),
                width=10,
            ),
        ],
    )

    temperature_input = html.Div(
        [
            dbc.Label("Temperature range", width="auto"),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(
                            type="number",
                            id=f"new_{property_type}_range_low",
                            placeholder="300 K",
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Input(
                            type="number",
                            id=f"new_{property_type}_range_high",
                            placeholder="1200 K",
                        ),
                        width=3,
                    ),
                ]
            ),
        ],
    )
    form = dbc.Form(
        [
            preexponential_input,
            activation_energy_input,
            author_input,
            year_input,
            isotope_input,
            material_input,
            temperature_input,
        ]
    )
    return form
