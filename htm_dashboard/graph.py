import plotly.graph_objects as go
import plotly.io as pio
import h_transport_materials as htm
import numpy as np
import plotly.express as px
import json
from datetime import datetime


TEMPLATE_LIGHT = "plotly_white"
TEMPLATE_DARK = "cyborg"

pio.templates.default = TEMPLATE_LIGHT


colour_cycle = px.colors.qualitative.Plotly

type_to_database = {
    "diffusivity": htm.diffusivities,
    "solubility": htm.solubilities,
    "permeability": htm.permeabilities,
    "recombination_coeff": htm.recombination_coeffs,
    "dissociation_coeff": htm.dissociation_coeffs,
}


def add_mean_value(group: htm.PropertiesGroup, fig: go.Figure):
    mean_prop = group.mean()
    label = "Mean value"
    T = np.linspace(300, 1200, num=500) * htm.ureg.K
    hovertemplate = (
        "<b>%{text}</b><br><br>"
        + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
        + "T: %{customdata:.0f} K<br>"
    )
    if isinstance(group[0], htm.Solubility):
        hovertemplate += (
            "S: %{y:,.2e}"
            + f"{mean_prop.units:~H} <br>"
            + f"S_0: {mean_prop.pre_exp:.2e~H} <br>"
            + f"E_S : {mean_prop.act_energy:.2f~H}"
        )
    elif isinstance(group[0], htm.Diffusivity):
        hovertemplate += (
            "D: %{y:,.2e} "
            + f"{mean_prop.units:~H} <br>"
            + f"D_0: {mean_prop.pre_exp:.2e~H} <br>"
            + f"E_D : {mean_prop.act_energy:.2f~H}"
        )
    elif isinstance(group[0], htm.RecombinationCoeff):
        hovertemplate += (
            "Kr: %{y:,.2e}"
            + f"{mean_prop.units:~H} <br>"
            + f"Kr_0: {mean_prop.pre_exp:.2e~H} <br>"
            + f"E_Kr : {mean_prop.act_energy:.2f~H}"
        )
    hovertemplate += "<extra></extra>"
    fig.add_trace(
        go.Scatter(
            x=1 / T.magnitude,
            y=mean_prop.value(T).magnitude,
            name=label,
            mode="lines",
            text=[label] * len(T),
            line=dict(color="black", width=4),
            customdata=T,
            hovertemplate=hovertemplate,
        )
    )


def make_group_of_properties(
    type_of_prop: str, materials=[], authors=[], isotopes=[], years=None
):

    if len(materials) * len(authors) * len(isotopes) == 0:
        filtered_group = []
    else:
        database = type_to_database[type_of_prop]
        filtered_group = (
            database.filter(material=materials)
            .filter(author=[author.lower() for author in authors])
            .filter(isotope=[isotope.lower() for isotope in isotopes])
        )
        if years:
            filtered_group = filtered_group.filter(
                year=np.arange(years[0], years[1] + 1, step=1).tolist()
            )

    return filtered_group


def update_axes(fig, group_of_properties):
    if len(group_of_properties) == 0:
        return

    if isinstance(group_of_properties[0], htm.Solubility):
        all_units = np.unique([f"{S.units:~H}" for S in group_of_properties]).tolist()
        if len(all_units) == 1:
            yticks_suffix = all_units[0].replace("particle", " H")
            title_units = f"({yticks_suffix})"
        else:
            # if the group contains mixed units, display nothing
            title_units = "(mixed units)"
            yticks_suffix = ""
        ylabel = f"Solubility {title_units}"
    elif isinstance(group_of_properties[0], htm.Diffusivity):
        ylabel = "Diffusivity"
        yticks_suffix = f" {group_of_properties[0].units:~H}"
    elif isinstance(group_of_properties[0], htm.Permeability):
        ylabel = f"Permeability {group_of_properties[0].units:~H}"
        yticks_suffix = ""
    elif isinstance(group_of_properties[0], htm.RecombinationCoeff):
        ylabel = "Recombination coefficient"
        yticks_suffix = " m<sup>4</sup>/s"
    elif isinstance(group_of_properties[0], htm.DissociationCoeff):
        ylabel = f"Dissociation coefficient {group_of_properties[0].units:~H}"
        yticks_suffix = ""

    xticks_suffix = " K<sup>-1</sup>"

    fig.update_yaxes(
        title_text=ylabel, type="log", tickformat=".0e", ticksuffix=yticks_suffix
    )
    fig.update_xaxes(title_text="1/T", tickformat=".2e", ticksuffix=xticks_suffix)


def make_hovertemplate(prop):
    # TODO refactor this
    if isinstance(prop, htm.Solubility):
        return (
            "<b>%{text}</b><br><br>"
            + prop.material.name
            + "<br>"
            + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
            + "T: %{customdata:.0f} K<br>"
            + "S: %{y:,.2e} "
            + f"{prop.units:~H}<br>"
            + f"S_0: {prop.pre_exp:.2e~H} <br>"
            + f"E_S : {prop.act_energy:.2f~H}"
            + "<extra></extra>"
        )
    elif isinstance(prop, htm.Diffusivity):
        return (
            "<b>%{text}</b><br><br>"
            + prop.material.name
            + "<br>"
            + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
            + "T: %{customdata:.0f} K<br>"
            + "D: %{y:,.2e} "
            + f"{prop.units:~H} <br>"
            + f"D_0: {prop.pre_exp:.2e~H}<br>"
            + f"E_D : {prop.act_energy:.2f~H}"
            + "<extra></extra>"
        )
    else:
        return (
            "<b>%{text}</b><br><br>"
            + prop.material.name
            + "<br>"
            + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
            + "T: %{customdata:.0f} K<br>"
            + "value: %{y:,.2e} "
            + f"{prop.units:~H} <br>"
            + f"pre-exp: {prop.pre_exp:.2e~H}<br>"
            + f"act. energy : {prop.act_energy:.2f~H}"
            + "<extra></extra>"
        )


def make_figure_prop_per_year(
    group, step, selected_years=[1950, int(datetime.today().year)]
):

    counts, bins = np.histogram([prop.year for prop in group])

    bins_center = 0.5 * (bins[:-1] + bins[1:])
    selected = [
        i
        for i, year in enumerate(bins_center)
        if selected_years[0] <= year <= selected_years[1]
    ]

    fig = go.Figure(
        [
            go.Bar(
                x=bins_center,
                y=counts,
                selectedpoints=selected,
            )
        ]
    )
    template = []
    for i, year in enumerate(bins[:-1]):
        year_1 = year
        year_2 = bins[i + 1]
        template.append(
            f"<br>{year_1:.0f} - {year_2:.0f}</br>" + "<extra></extra>" + "%{y}"
        )

    fig.update_layout(bargap=0)
    fig.update_traces(
        hovertemplate=template,
        selector=dict(type="bar"),
    )
    fig.update_yaxes(title_text="Nb of properties")
    return fig


def make_citations_graph(group: htm.PropertiesGroup, per_year: bool = True):
    references = []
    nb_citations = []
    dois = []
    with open("htm_dashboard/citations.json") as f:
        citation_data = json.load(f)
    for prop in group:
        if prop.doi in citation_data["dois"]:
            nb_citations_prop = citation_data["dois"][prop.doi]
        else:
            nb_citations_prop = prop.nb_citations
        author = prop.author
        year = prop.year

        label = "{} ({})".format(author.capitalize(), year)

        if label not in references:

            references.append(label)
            if per_year:
                current_year = datetime.now().year
                nb_citations.append(nb_citations_prop / (current_year - year))
            else:
                nb_citations.append(nb_citations_prop)

            if prop.doi is None:
                dois.append("none")
            else:
                dois.append(prop.doi)

    # sort values
    references = [val_y for _, val_y in sorted(zip(nb_citations, references))]
    dois = [val_y for _, val_y in sorted(zip(nb_citations, dois))]
    nb_citations = sorted(nb_citations)

    bar = go.Bar(
        x=nb_citations,
        y=references,
        orientation="h",
        customdata=dois,
        hovertemplate="<b>DOI</b> " + ": %{customdata} <br>" + "<extra></extra>",
    )
    fig = go.Figure(bar)
    if per_year:
        x_label = "Average number of citations per year"
    else:
        x_label = "Number of citations"
    fig.update_xaxes(title=x_label)
    return fig


def make_piechart_materials(prop_group):
    list_of_mats = [prop.material.name for prop in prop_group]
    labels = np.unique(list_of_mats).tolist()

    values = [list_of_mats.count(mat) for mat in labels]

    colours = []
    prop_to_color = htm.plotting.get_prop_to_color(
        prop_group, colour_by="material", colour_cycle=colour_cycle
    )
    for mat in labels:
        for prop in prop_group:
            if prop.material == mat:
                colours.append(prop_to_color[prop])
                break
    assert len(colours) == len(labels)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                marker_colors=colours,
            )
        ]
    )
    return fig


def make_piechart_isotopes(prop_group):
    list_of_isotopes = [prop.isotope for prop in prop_group]
    labels = ["H", "D", "T"]

    values = [list_of_isotopes.count(isotope) for isotope in labels]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return fig


def make_piechart_author(prop_group):
    list_of_authors = [prop.author for prop in prop_group]
    labels = np.unique(list_of_authors).tolist()

    colours = []
    prop_to_color = htm.plotting.get_prop_to_color(
        prop_group, colour_by="author", colour_cycle=colour_cycle
    )
    for author in labels:
        for prop in prop_group:
            if prop.author == author:
                colours.append(prop_to_color[prop])
                break
    assert len(colours) == len(labels)

    values = [list_of_authors.count(isotope) for isotope in labels]

    labels = [lab.capitalize() for lab in labels]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                marker_colors=colours,
            )
        ]
    )
    return fig
