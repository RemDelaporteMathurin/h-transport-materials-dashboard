import h_transport_materials as htm
from datetime import date
import json

citations_data = {"date": str(date.today()), "dois": {}}

for i, prop in enumerate(htm.database):
    if prop.doi not in citations_data["dois"]:
        citations_data["dois"][prop.doi] = prop.nb_citations
        print(i)

with open("htm_dashboard/citations.json", "w") as outfile:
    json.dump(citations_data, outfile, indent=4)
