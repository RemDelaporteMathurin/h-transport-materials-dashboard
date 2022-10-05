import dash_bootstrap_components as dbc
from dash import html

preexponential_input = html.Div(
    [
        dbc.Label("D_0 (m2/s)", width=2),
        dbc.Col(
            dbc.Input(
                type="number",
                id="new_diffusivity_pre_exp",
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
                id="new_diffusivity_act_energy",
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
                id="new_diffusivity_author",
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
                id="new_diffusivity_year",
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
                id="new_diffusivity_isotope",
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
                id="new_diffusivity_material",
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
                        id="new_diffusivity_range_low",
                        placeholder="300 K",
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Input(
                        type="number",
                        id="new_diffusivity_range_high",
                        placeholder="1200 K",
                    ),
                    width=3,
                ),
            ]
        ),
    ],
)


form_new_diffusivity = dbc.Form(
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
