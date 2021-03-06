import plotly.graph_objects as go
from dash import dcc

import h_transport_materials as htm

def make_citations_graph(group: htm.PropertiesGroup, per_year: bool=True):
    references = []
    nb_citations = []
    for prop in group:
        author = prop.author
        year = prop.year

        label = "{} ({})".format(author.capitalize(), year)
        if label not in references:

            references.append(label)
            if per_year:
                nb_citations.append(prop.nb_citations/(2022-year))
            else:
                nb_citations.append(prop.nb_citations)

    # sort values
    references = [val_y for _, val_y in sorted(zip(nb_citations, references))]
    nb_citations = sorted(nb_citations)

    bar = go.Bar(
            x=nb_citations,
            y=references,
            orientation='h')
    fig = go.Figure(bar)
    if per_year:
        x_label = "Average number of citations per year (Crossref)"
    else:
        x_label = "Number of citations (Crossref)"
    fig.update_xaxes(title=x_label)
    return fig


citations_graph_diffusivity = dcc.Graph(
    id="graph_nb_citations_diffusivity",
    figure=go.Figure(),
    # style={"width": "100vh", "height": "50vh"},
)

citations_graph_solubility = dcc.Graph(
    id="graph_nb_citations_solubility",
    figure=go.Figure(),
    # style={"width": "100vh", "height": "50vh"},
)


