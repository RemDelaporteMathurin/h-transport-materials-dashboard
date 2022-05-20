import plotly.graph_objects as go
import h_transport_materials as htm
import numpy as np

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
    for D in diffusivities:
        label = "{} {} ({})".format(D.isotope, D.author.capitalize(), D.year)
        range = D.range
        if D.range is None:
            range = (300, 1200)
        T = np.linspace(range[0], range[1], num=500)
        fig.add_trace(
            go.Scatter(
                x=1 / T,
                y=D.value(T),
                name=label,
                mode="lines",
                text=[label] * len(T),
                customdata=T,
                hovertemplate="<b>%{text}</b><br><br>"
                + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
                + "T: %{customdata:.0f} K<br>"
                + "D: %{y:,.2e} m<sup>2</sup>/s"
                + "<extra></extra>",
            )
        )

    # add_mean_value(diffusivities, fig)

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
    for S in solubilities:
        label = "{} {} ({})".format(S.isotope, S.author.capitalize(), S.year)
        range = S.range
        if S.range is None:
            range = (300, 1200)
        T = np.linspace(range[0], range[1], num=500)
        fig.add_trace(
            go.Scatter(
                x=1 / T,
                y=S.value(T),
                name=label,
                mode="lines",
                text=[label] * len(T),
                customdata=T,
                hovertemplate="<b>%{text}</b><br><br>"
                + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
                + "T: %{customdata:.0f} K<br>"
                + "S: %{y:,.2e}"
                + "<extra></extra>",
            )
        )

    # add_mean_value(diffusivities, fig)

    fig.update_yaxes(type="log", tickformat=".0e", ticksuffix=" ")
    fig.update_xaxes(title_text="1/T", tickformat=".2e", ticksuffix=" K<sup>-1</sup>")
    fig.update_yaxes(title_text="Solubility")
    # fig.write_html("out.html")
    return fig
