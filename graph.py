import plotly.graph_objects as go
import h_transport_materials as htm
import numpy as np
import plotly.express as px

all_diffusivities = htm.diffusivities
all_solubilities = htm.solubilities

all_authors_diffusivities = np.unique(
    [D.author.capitalize() for D in all_diffusivities]
).tolist()
all_authors_solubilities = np.unique(
    [S.author.capitalize() for S in all_solubilities]
).tolist()

all_years_solubilities = [S.year for S in all_solubilities]
min_year_solubilities = min(all_years_solubilities)
max_year_solubilities = max(all_years_solubilities)

all_years_diffusivities = [S.year for S in all_diffusivities]
min_year_diffusivities = min(all_years_diffusivities)
max_year_diffusivities = max(all_years_diffusivities)


colours = px.colors.qualitative.Plotly


def add_mean_value(group: htm.PropertiesGroup, fig: go.Figure):
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
            + "D: %{y:,.2e} m<sup>2</sup>/s"
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
            + "D: %{y:,.2e}"
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


def make_graph(diffusivities):
    fig = go.Figure()
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
                line=dict(color=colours[i % 10]),
                text=[label] * len(T),
                customdata=T,
                hovertemplate="<b>%{text}</b><br><br>"
                + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
                + "T: %{customdata:.0f} K<br>"
                + "D: %{y:,.2e} m<sup>2</sup>/s"
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


def make_graph_solubilities(solubilities):
    fig = go.Figure()
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
                line=dict(color=colours[i % 10]),
                text=[label] * len(T),
                customdata=T,
                hovertemplate="<b>%{text}</b><br><br>"
                + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
                + "T: %{customdata:.0f} K<br>"
                + "S: %{y:,.2e}"
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

    fig.update_yaxes(type="log", tickformat=".0e", ticksuffix=" ")
    fig.update_xaxes(title_text="1/T", tickformat=".2e", ticksuffix=" K<sup>-1</sup>")
    fig.update_yaxes(title_text="Solubility")
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
