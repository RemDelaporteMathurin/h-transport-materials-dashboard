import h_transport_materials as htm
import json
from jinja2 import Template


def create_data_as_dict(group: htm.PropertiesGroup):
    data = {}
    for property in group:
        name = "{}_{}_{}".format(property.isotope, property.author, property.year)
        if property.bibsource:
            source = property.bibdata.to_string("bibtex")
        else:
            source = property.source
        data_prop = {
            "pre_exp": property.pre_exp,
            "act_energy": property.act_energy,
            "year": property.year,
            "author": property.author,
            "isotope": property.isotope,
            "source": source,
        }
        data[name] = data_prop
    return json.dumps(data, indent=2)


type_to_database = {
    "diffusivity": "htm.diffusivities",
    "solubility": "htm.solubilities",
    "recombination_coeff": "htm.recombination_coeffs",
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
