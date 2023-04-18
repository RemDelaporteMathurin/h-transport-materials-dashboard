import dash_bootstrap_components as dbc
from dash import html
import h_transport_materials as htm


def make_form(property_type: str):

    if property_type == "diffusivity":
        pre_exp_label = f"D_0 ({htm.Diffusivity().units:~P})"
        act_energy_label = "E_D (eV)"
    elif property_type == "solubility":
        sample_prop = htm.Solubility(law="sievert")
        pre_exp_label = f"S_0 ({sample_prop.units:~P})"
        act_energy_label = "E_S (eV)"
    elif property_type == "permeability":
        pre_exp_label = f"P_0 ({htm.Permeability(law='sievert').units:~P})"
        act_energy_label = "E_P (eV)"
    elif property_type == "recombination_coeff":
        pre_exp_label = f"Kr_0 ({htm.RecombinationCoeff().units:~P})"
        act_energy_label = "E_Kr (eV)"
    elif property_type == "dissociation_coeff":
        pre_exp_label = f"Kd_0 ({htm.DissociationCoeff().units:~P})"
        act_energy_label = "E_Kd (eV)"
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
            dbc.Label(act_energy_label, width=2),
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
