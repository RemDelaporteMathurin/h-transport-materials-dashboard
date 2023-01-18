import h_transport_materials as htm
import json
from jinja2 import Template


# TODO this is duplicated code from HTM. We could make use of the export_to_json function
def create_data_as_dict(group: htm.PropertiesGroup):
    keys = [
        "material",
        "pre_exp",
        "act_energy",
        "isotope",
        "author",
        "source",
        "range",
        "doi",
        "units",
    ]
    data = []
    for prop in group:

        prop_dict = {key: getattr(prop, key) for key in keys if hasattr(prop, key)}
        if "units" in prop_dict:
            prop_dict["units"] = f"{prop_dict['units']:~}"
        prop_dict["pre_exp"] = prop_dict["pre_exp"].magnitude
        prop_dict["act_energy"] = prop_dict["act_energy"].magnitude
        if prop_dict["range"]:
            prop_dict["range"] = (
                prop_dict["range"][0].magnitude,
                prop_dict["range"][1].magnitude,
            )
        data.append(prop_dict)
    return json.dumps(data, indent=2)


type_to_database = {
    "diffusivity": "htm.diffusivities",
    "solubility": "htm.solubilities",
    "permeability": "htm.permeabilities",
    "recombination_coeff": "htm.recombination_coeffs",
    "dissociation_coeff": "htm.dissociation_coeffs",
}


python_template = Template(
    """import h_transport_materials as htm
import matplotlib.pyplot as plt
import numpy as np

filtered_{{group}} = (
    {{database}}.filter(material={{materials}})
    .filter(author={{authors}})
    .filter(isotope={{isotopes}})
    .filter(year=np.arange({{yearmin}}, {{yearmax}}, step=1).tolist())
)

htm.plotting.plot(filtered_{{group}})

plt.legend()
plt.xlabel("1/T (K$^{-1}$)")
plt.yscale("log")
plt.show()

"""
)


def generate_python_code(materials, authors, isotopes, yearmin, yearmax, group):
    python_code = python_template.render(
        group=group,
        database=type_to_database[group],
        materials=[mat.lower() for mat in materials],
        authors=[author.lower() for author in authors],
        isotopes=[iso.lower() for iso in isotopes],
        yearmin="{}".format(yearmin),
        yearmax="{}".format(yearmax),
    )
    return python_code
