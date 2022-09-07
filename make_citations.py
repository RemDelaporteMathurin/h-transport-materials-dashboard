import json

import h_transport_materials as htm

for property in htm.diffusivities:
    print(property.source)
    try:
        print(property.nb_citations)
    except json.JSONDecodeError:
        next

# doi = property.bibsource.fields["doi"]
