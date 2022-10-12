import numpy as np
import dash

from .export import create_data_as_dict, generate_python_code

from .tab import materials_options, TABLE_KEYS

from .graph import (
    make_group_of_properties,
    make_piechart_author,
    make_piechart_isotopes,
    make_graph,
    make_piechart_materials,
    add_mean_value,
    make_figure_prop_per_year,
    make_citations_graph,
)

import h_transport_materials as htm


type_to_database = {
    "diffusivity": htm.diffusivities,
    "solubility": htm.solubilities,
    "recombination_coeff": htm.recombination_coeffs,
}


def create_make_citations_figure_function(group):
    def make_citations_figure(
        figure,
        per_year,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        properties_group = make_group_of_properties(
            type_of_prop=group,
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )

        return make_citations_graph(properties_group, per_year=per_year)

    return make_citations_figure


def create_add_all_materials_function(group):
    def add_all_materials(n_clicks):
        if n_clicks:
            return materials_options
        else:
            return dash.no_update

    return add_all_materials


def create_add_all_authors_function(group):
    def add_all_authors(n_clicks):

        if n_clicks:
            return np.unique(
                [prop.author.capitalize() for prop in type_to_database[group]]
            ).tolist()
        else:
            return dash.no_update

    return add_all_authors


def create_update_entries_per_year_graph_function(group):
    def update_entries_per_year_graph(
        figure, material_filter, isotope_filter, author_filter, year_filter
    ):

        all_time_properties = make_group_of_properties(
            type_of_prop=group,
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
        )
        return make_figure_prop_per_year(
            all_time_properties, step=5, selected_years=year_filter
        )

    return update_entries_per_year_graph


def create_update_graph_function(group):
    def update_graph(
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
        mean_button,
        colour_by,
    ):

        properties_group = make_group_of_properties(
            type_of_prop=group,
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )

        figure = make_graph(properties_group, colour_by)
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"mean_button_{group}.n_clicks":
            add_mean_value(properties_group, figure)

        return figure

    return update_graph


def create_make_download_data_function(group):
    def make_download_data(
        n_clicks,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):

        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"extract_button_{group}.n_clicks":
            properties_group = make_group_of_properties(
                type_of_prop=group,
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

            if group == "diffusivity":
                new_property = htm.Diffusivity(
                    D_0=new_pre_exp,
                    E_D=new_act_energy,
                )
            elif group == "solubility":
                new_property = htm.Solubility(
                    units="m-3 Pa-1/2",  # TODO expose this (see #68)
                    S_0=new_pre_exp,
                    E_S=new_act_energy,
                )
            elif group == "recombination_coeff":
                new_property = htm.RecombinationCoeff(
                    pre_exp=new_pre_exp,
                    act_energy=new_act_energy,
                )

            new_property.author = new_author.lower()
            new_property.year = new_year
            new_property.isotope = new_isotope
            new_property.material = new_material
            new_property.range = (new_range_low, new_range_high)

            type_to_database[group].append(new_property)

        all_authors = np.unique(
            [
                prop.author.capitalize()
                for prop in type_to_database[group]
                if prop.material in material_filter
            ]
        ).tolist()
        all_materials = np.unique(
            [prop.material.lower() for prop in type_to_database[group]]
        ).tolist()

        return all_materials, all_authors, ""

    return add_property


def create_update_piechart_material_function(group):
    def update_piechart_material(
        figure,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        properties_group = make_group_of_properties(
            type_of_prop=group,
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )
        return make_piechart_materials(properties_group)

    return update_piechart_material


def create_update_piechart_isotopes_function(group):
    def update_piechart_isotope(
        figure,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        properties_group = make_group_of_properties(
            type_of_prop=group,
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )
        return make_piechart_isotopes(properties_group)

    return update_piechart_isotope


def create_update_piechart_authors_function(group):
    def update_piechart_author(
        figure,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        properties_group = make_group_of_properties(
            type_of_prop=group,
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )
        return make_piechart_author(properties_group)

    return update_piechart_author


def create_update_table_data_function(group):
    def update_table_data(
        figure, material_filter, isotope_filter, author_filter, year_filter
    ):
        data = []

        properties_group = make_group_of_properties(
            type_of_prop=group,
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )

        for prop in properties_group:
            entry = {}
            for key in TABLE_KEYS:
                if hasattr(prop, key):
                    val = getattr(prop, key)
                    if key == "range":
                        if val is None:
                            val = "none"
                        else:
                            val = f"{val[0]:.0f}-{val[1]:.0f}"
                    elif key == "pre_exp" and hasattr(prop, "units"):
                        val = f"{val: .2e} {prop.units}"
                    elif key == "act_energy":
                        val = f"{val:.2f}"
                    elif key == "doi":
                        entry[key] = prop.source
                        if prop.bibsource:
                            if prop.doi:
                                clickable_doi = (
                                    f"[{prop.doi}](https://doi.org/{prop.doi})"
                                )
                                val = clickable_doi

                entry[key] = val

            data.append(entry)

        return data

    return update_table_data
