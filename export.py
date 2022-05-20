import h_transport_materials as htm
import json


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
