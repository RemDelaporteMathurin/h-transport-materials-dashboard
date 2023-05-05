from htm_dashboard.callbacks import create_make_download_data_function
import h_transport_materials as htm

from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict

from htm_dashboard.callbacks import create_make_download_data_function


def test_export_groups():
    """Tests the export to json callback"""
    export_fun = create_make_download_data_function("diffusivity")

    def run_callback():
        context_value.set(
            AttributeDict(
                **{
                    "triggered_inputs": [
                        {"prop_id": "extract_button_diffusivity.n_clicks"}
                    ]
                }
            )
        )
        return export_fun(
            1,
            material_filter=["tungsten"],
            author_filter=["frauenfelder"],
            isotope_filter=["H", "D", "T"],
            year_filter=None,
        )

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert type(output["content"]) == str
