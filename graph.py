import plotly.graph_objects as go
import h_transport_materials as htm
import numpy as np


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


def make_diffusivities(materials=[], authors=[], isotopes=[], years=[]):
    fig = go.Figure()
    diffusivities = htm.diffusivities.filter(material="tungsten")

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

    add_mean_value(diffusivities, fig)

    fig.update_yaxes(type="log", tickformat=".0e", ticksuffix=" m<sup>2</sup>/s")
    fig.update_xaxes(title_text="1/T", tickformat=".2e", ticksuffix=" K<sup>-1</sup>")
    fig.update_yaxes(title_text="Diffusivity")
    # fig.write_html("out.html")
    return fig
