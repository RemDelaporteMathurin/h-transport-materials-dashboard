import plotly.graph_objects as go
import plotly.io as pio
import h_transport_materials as htm
import numpy as np
import plotly.express as px

pio.templates.default = "plotly_white"

all_diffusivities = htm.diffusivities
all_solubilities = htm.solubilities

all_years_solubilities = [S.year for S in all_solubilities]
MIN_YEAR_SOL = min(all_years_solubilities)
MAX_YEAR_SOL = max(all_years_solubilities)

all_years_diffusivities = [S.year for S in all_diffusivities]
MIN_YEAR_DIFF = min(all_years_diffusivities)
MAX_YEAR_DIFF = max(all_years_diffusivities)


colours = px.colors.qualitative.Plotly


def add_mean_value_diffusivities(group: htm.PropertiesGroup, fig: go.Figure):
    D_0, E_D = group.mean()
    mean_prop = htm.ArrheniusProperty(D_0, E_D)
    label = "Mean value"
    T = np.linspace(300, 1200, num=500)
    fig.add_trace(
        go.Scatter(
            x=1 / T,
            y=mean_prop.value(T),
            name=label,
            mode="lines",
            text=[label] * len(T),
            line=dict(color="black", width=4),
            customdata=T,
            hovertemplate="<b>%{text}</b><br><br>"
            + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
            + "T: %{customdata:.0f} K<br>"
            + "D: %{y:,.2e} m<sup>2</sup>/s <br>"
            + "D_0: {:.2e} m<sup>2</sup>/s <br>".format(mean_prop.pre_exp)
            + "E_D : {:.2f} eV".format(mean_prop.act_energy)
            + "<extra></extra>",
        )
    )


def add_mean_value_solubilities(group: htm.PropertiesGroup, fig: go.Figure):
    S_0, E_S = group.mean()
    mean_prop = htm.ArrheniusProperty(S_0, E_S)
    label = "Mean value"
    T = np.linspace(470, 1200, num=500)
    fig.add_trace(
        go.Scatter(
            x=1 / T,
            y=mean_prop.value(T),
            name=label,
            mode="lines",
            text=[label] * len(T),
            line=dict(color="black", width=4),
            customdata=T,
            hovertemplate="<b>%{text}</b><br><br>"
            + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
            + "T: %{customdata:.0f} K<br>"
            + "S: %{y:,.2e}"
            + "S_0: {:.2e} <br>".format(mean_prop.pre_exp)
            + "E_S : {:.2f} eV".format(mean_prop.act_energy)
            + "<extra></extra>",
        )
    )


def make_diffusivities(materials=[], authors=[], isotopes=[], years=[]):
    if len(materials) * len(authors) * len(isotopes) * len(years) == 0:
        diffusivities = []
    else:
        diffusivities = (
            all_diffusivities.filter(material=materials)
            .filter(author=[author.lower() for author in authors])
            .filter(isotope=[isotope.lower() for isotope in isotopes])
            .filter(year=np.arange(years[0], years[1], step=1).tolist())
        )
    return diffusivities


def list_of_colours(prop_group, colour_by):
    """Returns a list of colours for the properties

    Args:
        prop_group (list): _description_
        colour_by (str): "property", "material", "isotope", "author"

    Returns:
        list: list of colours the same size as prop_group
    """
    if colour_by == "property":
        return [colours[i % 10] for i, _ in enumerate(prop_group)]
    elif colour_by == "material":
        list_of_mats = [prop.material for prop in prop_group]
        unique_mats = np.unique(list_of_mats).tolist()
        mats_idx = [unique_mats.index(prop.material) for prop in prop_group]
        return [colours[i % 10] for i in mats_idx]
    elif colour_by == "author":
        list_of_auths = [prop.author for prop in prop_group]
        unique_auths = np.unique(list_of_auths).tolist()
        auths_idx = [unique_auths.index(prop.author) for prop in prop_group]
        return [colours[i % 10] for i in auths_idx]
    elif colour_by == "isotope":
        list_of_iso = [prop.isotope for prop in prop_group]
        unique_iso = np.unique(list_of_iso).tolist()
        iso_idx = [unique_iso.index(prop.isotope) for prop in prop_group]
        return [colours[i % 10] for i in iso_idx]


def make_graph_diffusivities(diffusivities, colour_by="property"):
    """Creates a graph for visualising diffusivities.

    Args:
        diffusivities (list): list of htm.ArrheniusProperty
        colour_by (str, optional): "property", "material", "isotope", "author". Defaults to "property".

    Returns:
        go.Figure: the diffusivity graph
    """
    fig = go.Figure()
    colour_list = list_of_colours(diffusivities, colour_by)
    for i, D in enumerate(diffusivities):
        label = "{} {} ({})".format(D.isotope, D.author.capitalize(), D.year)
        range = D.range
        if D.range is None:
            if D.data_T is not None:
                range = (D.data_T.min(), D.data_T.max())
            else:
                range = (300, 1200)
        T = np.linspace(range[0], range[1], num=500)
        fig.add_trace(
            go.Scatter(
                x=1 / T,
                y=D.value(T),
                name=label,
                mode="lines",
                line=dict(color=colour_list[i]),
                text=[label] * len(T),
                customdata=T,
                hovertemplate="<b>%{text}</b><br><br>"
                + D.material
                + "<br>"
                + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
                + "T: %{customdata:.0f} K<br>"
                + "D: %{y:,.2e} m<sup>2</sup>/s <br>"
                + "D_0: {:.2e} m<sup>2</sup>/s <br>".format(D.pre_exp)
                + "E_D : {:.2f} eV".format(D.act_energy)
                + "<extra></extra>",
            )
        )
        if D.data_T is not None:
            fig.add_trace(
                go.Scatter(
                    x=1 / D.data_T,
                    y=D.data_y,
                    name=label,
                    mode="markers",
                    marker=dict(color=fig.data[-1].line.color),
                )
            )

    fig.update_yaxes(type="log", tickformat=".0e", ticksuffix=" m<sup>2</sup>/s")
    fig.update_xaxes(title_text="1/T", tickformat=".2e", ticksuffix=" K<sup>-1</sup>")
    fig.update_yaxes(title_text="Diffusivity")
    # fig.write_html("out.html")
    return fig


def make_solubilities(materials=[], authors=[], isotopes=[], years=[]):
    if len(materials) * len(authors) * len(isotopes) * len(years) == 0:
        solubilities = []
    else:
        solubilities = (
            all_solubilities.filter(material=materials)
            .filter(author=[author.lower() for author in authors])
            .filter(isotope=[isotope.lower() for isotope in isotopes])
            .filter(year=np.arange(years[0], years[1], step=1).tolist())
        )

    return solubilities


def make_graph_solubilities(solubilities, colour_by="property"):
    fig = go.Figure()
    colour_list = list_of_colours(solubilities, colour_by)
    for i, S in enumerate(solubilities):
        label = "{} {} ({})".format(S.isotope, S.author.capitalize(), S.year)
        range = S.range
        if S.range is None:
            if S.data_T is not None:
                range = (S.data_T.min(), S.data_T.max())
            else:
                range = (300, 1200)
        T = np.linspace(range[0], range[1], num=500)
        fig.add_trace(
            go.Scatter(
                x=1 / T,
                y=S.value(T),
                name=label,
                mode="lines",
                line=dict(color=colour_list[i]),
                text=[label] * len(T),
                customdata=T,
                hovertemplate="<b>%{text}</b><br><br>"
                + S.material
                + "<br>"
                + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
                + "T: %{customdata:.0f} K<br>"
                + "S: %{y:,.2e}"
                + f" {S.units}<br>"
                + f"S_0: {S.pre_exp:.2e} {S.units} <br>"
                + f"E_S : {S.act_energy:.2f} eV"
                + "<extra></extra>",
            )
        )
        if S.data_T is not None:
            fig.add_trace(
                go.Scatter(
                    x=1 / S.data_T,
                    y=S.data_y,
                    name=label,
                    mode="markers",
                    marker=dict(color=fig.data[-1].line.color),
                )
            )

    all_units = np.unique([S.units for S in solubilities]).tolist()
    if len(all_units) == 1:
        if all_units == ["m-3 Pa-1/2"]:
            y_suffix = "m<sup>-3</sup> Pa<sup>-1/2</sup>"
        elif all_units == ["m-3 Pa-1"]:
            y_suffix = "m<sup>-3</sup> Pa<sup>-1</sup>"
        title_units = f"({y_suffix})"
    else:
        # if the group contains mixed units, display nothing
        title_units = "(mixed units)"
        y_suffix = ""

    fig.update_yaxes(type="log", tickformat=".0e", ticksuffix=y_suffix)
    fig.update_xaxes(title_text="1/T", tickformat=".2e", ticksuffix=" K<sup>-1</sup>")
    fig.update_yaxes(title_text=f"Solubility {title_units}")
    # fig.write_html("out.html")
    return fig


def make_figure_prop_per_year(group, step, selected_years=[1950, 2022]):
    years = [prop.year for prop in group]
    year_min, year_max = 1950, 2022

    years = np.arange(year_min, year_max, step=step)
    if years[-1] != 2022:
        years = np.append(years, [2022])

    nb_props_per_year = []
    for year1, year2 in zip(years[:-1], years[1:]):
        count = 0
        for prop in group:
            if year1 <= prop.year < year2:
                count += 1

        nb_props_per_year.append(count)

    average_years = years[:-1] - (years[:-1] - years[1:]) / 2
    selected = [
        i
        for i, year in enumerate(average_years)
        if selected_years[0] <= year <= selected_years[1]
    ]
    fig = go.Figure(
        [go.Bar(x=average_years, y=nb_props_per_year, selectedpoints=selected)]
    )
    fig.update_yaxes(title_text="Nb of properties")
    return fig


def make_citations_graph(group: htm.PropertiesGroup, per_year: bool = True):
    references = []
    nb_citations = []
    for prop in group:
        author = prop.author
        year = prop.year

        label = "{} ({})".format(author.capitalize(), year)

        if label not in references:

            references.append(label)
            if per_year:
                nb_citations.append(prop.nb_citations / (2022 - year))
            else:
                nb_citations.append(prop.nb_citations)

    # sort values
    references = [val_y for _, val_y in sorted(zip(nb_citations, references))]
    nb_citations = sorted(nb_citations)

    bar = go.Bar(x=nb_citations, y=references, orientation="h")
    fig = go.Figure(bar)
    if per_year:
        x_label = "Average number of citations per year"
    else:
        x_label = "Number of citations"
    fig.update_xaxes(title=x_label)
    return fig


def make_piechart_materials(prop_group):
    list_of_mats = [prop.material for prop in prop_group]
    labels = np.unique(list_of_mats).tolist()

    values = [list_of_mats.count(mat) for mat in labels]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
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

    values = [list_of_authors.count(isotope) for isotope in labels]

    labels = [lab.capitalize() for lab in labels]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return fig
