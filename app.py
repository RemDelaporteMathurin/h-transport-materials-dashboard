import numpy as np
from layout import layout
from graph import (
    all_diffusivities,
    all_solubilities,
    make_diffusivities,
    make_solubilities,
    make_graph_diffusivities,
    make_graph_solubilities,
    add_mean_value,
    add_mean_value_solubilities,
    MIN_YEAR_SOL,
    MAX_YEAR_SOL,
    MIN_YEAR_DIFF,
    MAX_YEAR_DIFF,
    make_figure_prop_per_year,
)

from citations import make_citations_graph

import h_transport_materials as htm

from export import create_data_as_dict, generate_python_code

from tab import materials_options

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

server = app.server

app.layout = layout


def create_make_figure_function(group):
    def make_figure(
        figure,
        radio_citations,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        if group == "diffusivity":
            diffusitivites = make_diffusivities(
                materials=material_filter,
                authors=author_filter,
                isotopes=isotope_filter,
                years=year_filter,
            )
            return make_citations_graph(
                diffusitivites, per_year=radio_citations == "Per year"
            )
        elif group == "solubility":
            solubilities = make_solubilities(
                materials=material_filter,
                authors=author_filter,
                isotopes=isotope_filter,
                years=year_filter,
            )
            return make_citations_graph(
                solubilities, per_year=radio_citations == "Per year"
            )

    return make_figure


def create_add_all_materials_function(group):
    def add_all_materials(n_clicks):
        if n_clicks:
            return materials_options
        else:
            return dash.no_update

    return add_all_materials


def create_add_all_authors_function(group):
    def add_all_authors(n_clicks):
        if group == "diffusivity":
            properties_group = all_diffusivities
        elif group == "solubility":
            properties_group = all_solubilities
        if n_clicks:
            return np.unique(
                [prop.author.capitalize() for prop in properties_group]
            ).tolist()
        else:
            return dash.no_update

    return add_all_authors


def create_update_graph_function(group):
    def update_graph(
        material_filter, isotope_filter, author_filter, year_filter, mean_button
    ):
        if group == "diffusivity":
            make_group = make_diffusivities
            make_graph = make_graph_diffusivities
        elif group == "solubility":
            make_group = make_solubilities
            make_graph = make_graph_solubilities

        properties_group = make_group(
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )

        all_time_properties = make_group(
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=[MIN_YEAR_DIFF, MAX_YEAR_DIFF],
        )

        figure = make_graph(properties_group)
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"mean_button_{group}.n_clicks":
            add_mean_value(properties_group, figure)

        return figure, make_figure_prop_per_year(
            all_time_properties, step=5, selected_years=year_filter
        )

    return update_graph


def create_make_download_data_function(group):
    def make_download_data(
        n_clicks,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        if group == "diffusivity":
            make_group = make_diffusivities
        elif group == "solubility":
            make_group = make_solubilities
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"extract_button_{group}.n_clicks":
            properties_group = make_group(
                materials=material_filter,
                authors=author_filter,
                isotopes=isotope_filter,
                years=year_filter,
            )
            return dict(
                content=create_data_as_dict(properties_group),
                filename="data.json",
            )

    return make_download_data


def make_download_python_callback(group):
    def download_python(
        n_clicks,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"python_button_{group}.n_clicks":

            return dict(
                content=generate_python_code(
                    materials=material_filter,
                    isotopes=isotope_filter,
                    authors=author_filter,
                    yearmin=year_filter[0],
                    yearmax=year_filter[1],
                    group=group,
                ),
                filename="script.py",
            )

    return download_python


def make_toggle_modal_function(group):
    def toggle_modal(
        n1,
        n2,
        is_open,
        new_prop_pre_exp,
        new_prop_act_energy,
        new_prop_author,
        new_prop_year,
        new_prop_isotope,
        new_prop_material,
    ):
        if is_open and None in [
            new_prop_pre_exp,
            new_prop_act_energy,
            new_prop_author,
            new_prop_year,
            new_prop_isotope,
            new_prop_material,
        ]:
            return is_open
        if n1 or n2:
            return not is_open
        return is_open

    return toggle_modal


def make_add_property(group):
    def add_property(
        n_clicks,
        material_filter,
        new_pre_exp,
        new_act_energy,
        new_author,
        new_year,
        new_isotope,
        new_material,
        new_range_low,
        new_range_high,
    ):
        if group == "diffusivity":
            properties_group = all_diffusivities
            prop_class = htm.ArrheniusProperty
        elif group == "solubility":
            properties_group = all_solubilities
            prop_class = htm.Solubility
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"submit_new_{group}.n_clicks":
            if None in [
                new_pre_exp,
                new_act_energy,
                new_author,
                new_year,
                new_isotope,
                new_material,
            ]:
                return dash.no_update, dash.no_update, "Error!"
            if (new_range_low, new_range_high) == (None, None):
                (new_range_low, new_range_high) = (300, 1200)
            new_property = htm.ArrheniusProperty(
                pre_exp=new_pre_exp,
                act_energy=new_act_energy,
                author=new_author.lower(),
                year=new_year,
                isotope=new_isotope,
                material=new_material,
                range=(new_range_low, new_range_high),
            )
            properties_group.properties.append(new_property)

        all_authors = np.unique(
            [
                prop.author.capitalize()
                for prop in properties_group
                if prop.material in material_filter
            ]
        ).tolist()
        all_materials = np.unique(
            [prop.material.lower() for prop in properties_group]
        ).tolist()

        return all_materials, all_authors, ""

    return add_property


@app.callback(
    dash.Output("modal-infos", "is_open"),
    dash.Input("open-sm", "n_clicks"),
    dash.State("modal-infos", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


for group in ["diffusivity", "solubility"]:

    app.callback(
        dash.Output(f"graph_nb_citations_{group}", "figure"),
        dash.Input(f"graph_{group}", "figure"),
        dash.Input(f"radio_citations_{group}", "value"),
        dash.State(f"material_filter_{group}", "value"),
        dash.State(f"isotope_filter_{group}", "value"),
        dash.State(f"author_filter_{group}", "value"),
        dash.State(f"year_filter_{group}", "value"),
    )(create_make_figure_function(group))

    app.callback(
        dash.Output(f"material_filter_{group}", "value"),
        dash.Input(f"add_all_materials_{group}", "n_clicks"),
    )(create_add_all_materials_function(group))

    app.callback(
        dash.Output(f"author_filter_{group}", "value"),
        dash.Input(f"add_all_authors_{group}", "n_clicks"),
    )(create_add_all_authors_function(group))

    app.callback(
        dash.Output(f"graph_{group}", "figure"),
        dash.Output(f"graph_prop_per_year_{group}", "figure"),
        dash.Input(f"material_filter_{group}", "value"),
        dash.Input(f"isotope_filter_{group}", "value"),
        dash.Input(f"author_filter_{group}", "value"),
        dash.Input(f"year_filter_{group}", "value"),
        dash.Input(f"mean_button_{group}", "n_clicks"),
    )(create_update_graph_function(group))

    app.callback(
        dash.Output(f"download-text_{group}", "data"),
        dash.Input(f"extract_button_{group}", "n_clicks"),
        dash.Input(f"material_filter_{group}", "value"),
        dash.Input(f"isotope_filter_{group}", "value"),
        dash.Input(f"author_filter_{group}", "value"),
        dash.Input(f"year_filter_{group}", "value"),
        prevent_initial_call=True,
    )(create_make_download_data_function(group))

    app.callback(
        dash.Output(f"download-python_{group}", "data"),
        dash.Input(f"python_button_{group}", "n_clicks"),
        dash.Input(f"material_filter_{group}", "value"),
        dash.Input(f"isotope_filter_{group}", "value"),
        dash.Input(f"author_filter_{group}", "value"),
        dash.Input(f"year_filter_{group}", "value"),
        prevent_initial_call=True,
    )(make_download_python_callback(group))

    app.callback(
        dash.Output(f"modal_add_{group}", "is_open"),
        dash.Input(f"add_property_{group}", "n_clicks"),
        dash.Input(f"submit_new_{group}", "n_clicks"),
        dash.State(f"modal_add_{group}", "is_open"),
        dash.State(f"new_{group}_pre_exp", "value"),
        dash.State(f"new_{group}_act_energy", "value"),
        dash.State(f"new_{group}_author", "value"),
        dash.State(f"new_{group}_year", "value"),
        dash.State(f"new_{group}_isotope", "value"),
        dash.State(f"new_{group}_material", "value"),
        prevent_initial_call=True,
    )(make_toggle_modal_function(group))

    app.callback(
        dash.Output(f"material_filter_{group}", "options"),
        dash.Output(f"author_filter_{group}", "options"),
        dash.Output(f"error_message_new_{group}", "children"),
        dash.Input(f"submit_new_{group}", "n_clicks"),
        dash.Input(f"material_filter_{group}", "value"),
        dash.State(f"new_{group}_pre_exp", "value"),
        dash.State(f"new_{group}_act_energy", "value"),
        dash.State(f"new_{group}_author", "value"),
        dash.State(f"new_{group}_year", "value"),
        dash.State(f"new_{group}_isotope", "value"),
        dash.State(f"new_{group}_material", "value"),
        dash.State(f"new_{group}_range_low", "value"),
        dash.State(f"new_{group}_range_high", "value"),
        prevent_initial_call=True,
    )(make_add_property(group))

if __name__ == "__main__":
    app.run_server(debug=True)
