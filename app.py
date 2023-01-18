from htm_dashboard.layout import layout
from htm_dashboard import ACTIVE_GROUPS
import htm_dashboard.callbacks as cb

import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO

# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc_css])

server = app.server

app.layout = layout


@app.callback(
    dash.Output("modal-infos", "is_open"),
    dash.Input("open-sm", "n_clicks"),
    dash.State("modal-infos", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


for group in ACTIVE_GROUPS:

    app.callback(
        dash.Output(f"graph_nb_citations_{group}", "figure"),
        dash.Input(f"graph_{group}", "figure"),
        dash.Input(f"per_year_citations_{group}", "on"),
        dash.State(f"material_filter_{group}", "value"),
        dash.State(f"isotope_filter_{group}", "value"),
        dash.State(f"author_filter_{group}", "value"),
        dash.State(f"year_filter_{group}", "value"),
    )(cb.create_make_citations_figure_function(group))

    app.callback(
        dash.Output(f"material_filter_{group}", "value"),
        dash.Input(f"add_all_materials_{group}", "n_clicks"),
    )(cb.create_add_all_materials_function(group))

    app.callback(
        dash.Output(f"author_filter_{group}", "value"),
        dash.Input(f"add_all_authors_{group}", "n_clicks"),
    )(cb.create_add_all_authors_function(group))

    app.callback(
        dash.Output(f"graph_{group}", "figure"),
        dash.Input(f"material_filter_{group}", "value"),
        dash.Input(f"isotope_filter_{group}", "value"),
        dash.Input(f"author_filter_{group}", "value"),
        dash.Input(f"year_filter_{group}", "value"),
        dash.Input(f"mean_button_{group}", "n_clicks"),
        dash.Input(f"colour-by_{group}", "value"),
        dash.Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    )(cb.create_update_graph_function(group))

    app.callback(
        dash.Output(f"graph_prop_per_year_{group}", "figure"),
        dash.Input(f"graph_{group}", "figure"),
        dash.State(f"material_filter_{group}", "value"),
        dash.State(f"isotope_filter_{group}", "value"),
        dash.State(f"author_filter_{group}", "value"),
        dash.State(f"year_filter_{group}", "value"),
    )(cb.create_update_entries_per_year_graph_function(group))

    app.callback(
        dash.Output(f"graph_materials_{group}", "figure"),
        dash.Input(f"graph_{group}", "figure"),
        dash.State(f"material_filter_{group}", "value"),
        dash.State(f"isotope_filter_{group}", "value"),
        dash.State(f"author_filter_{group}", "value"),
        dash.State(f"year_filter_{group}", "value"),
    )(cb.create_update_piechart_material_function(group))

    app.callback(
        dash.Output(f"graph_isotopes_{group}", "figure"),
        dash.Input(f"graph_{group}", "figure"),
        dash.State(f"material_filter_{group}", "value"),
        dash.State(f"isotope_filter_{group}", "value"),
        dash.State(f"author_filter_{group}", "value"),
        dash.State(f"year_filter_{group}", "value"),
    )(cb.create_update_piechart_isotopes_function(group))

    app.callback(
        dash.Output(f"graph_authors_{group}", "figure"),
        dash.Input(f"graph_{group}", "figure"),
        dash.State(f"material_filter_{group}", "value"),
        dash.State(f"isotope_filter_{group}", "value"),
        dash.State(f"author_filter_{group}", "value"),
        dash.State(f"year_filter_{group}", "value"),
    )(cb.create_update_piechart_authors_function(group))

    app.callback(
        dash.Output(f"download-text_{group}", "data"),
        dash.Input(f"extract_button_{group}", "n_clicks"),
        dash.Input(f"material_filter_{group}", "value"),
        dash.Input(f"isotope_filter_{group}", "value"),
        dash.Input(f"author_filter_{group}", "value"),
        dash.Input(f"year_filter_{group}", "value"),
        prevent_initial_call=True,
    )(cb.create_make_download_data_function(group))

    app.callback(
        dash.Output(f"download-python_{group}", "data"),
        dash.Input(f"python_button_{group}", "n_clicks"),
        dash.Input(f"material_filter_{group}", "value"),
        dash.Input(f"isotope_filter_{group}", "value"),
        dash.Input(f"author_filter_{group}", "value"),
        dash.Input(f"year_filter_{group}", "value"),
        prevent_initial_call=True,
    )(cb.make_download_python_callback(group))

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
    )(cb.make_toggle_modal_function(group))

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
    )(cb.make_add_property(group))

    app.callback(
        dash.Output(f"table_{group}", "data"),
        dash.Input(f"graph_{group}", "figure"),
        dash.State(f"material_filter_{group}", "value"),
        dash.State(f"isotope_filter_{group}", "value"),
        dash.State(f"author_filter_{group}", "value"),
        dash.State(f"year_filter_{group}", "value"),
    )(cb.create_update_table_data_function(group))

if __name__ == "__main__":
    # app.run_server(debug=True, host="0.0.0.0", port=8080)
    app.run_server(debug=True)
