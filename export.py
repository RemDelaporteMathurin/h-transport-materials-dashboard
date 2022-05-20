import h_transport_materials as htm
import json
from jinja2 import Template


def create_data_as_dict(group: htm.PropertiesGroup):
    data = {}
    for property in group:
        name = "{}_{}_{}".format(property.isotope, property.author, property.year)
        data_prop = {
            "pre_exp": property.pre_exp,
            "act_energy": property.act_energy,
            "year": property.year,
            "author": property.author,
            "isotope": property.isotope,
            "source": property.source,
        }
        data[name] = data_prop
    return json.dumps(data, indent=2)


python_template = Template(
    """import h_transport_materials as htm
import matplotlib.pyplot as plt
import numpy as np

filtered_{{group}} = (
    htm.{{group}}.filter(material={{materials}})
    .filter(author={{authors}})
    .filter(isotope={{isotopes}})
    .filter(year=np.arange({{yearmin}}, {{yearmax}}, step=1).tolist())
)

for property in filtered_{{group}}:
    label = "{} {} ({})".format(
        property.isotope, property.author.capitalize(), property.year
    )
    htm.plotting.plot(property, label=label)

plt.legend()
plt.xlabel("1/T (K$^{-1}$)")
plt.yscale("log")
plt.show()

"""
)


def generate_python_code(materials, authors, isotopes, yearmin, yearmax, group):
    python_code = python_template.render(
        group=group,
        materials=[mat.lower() for mat in materials],
        authors=[author.lower() for author in authors],
        isotopes=[iso.lower() for iso in isotopes],
        yearmin="{}".format(yearmin),
        yearmax="{}".format(yearmax),
    )
    return python_code
