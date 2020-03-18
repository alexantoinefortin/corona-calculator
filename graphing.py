import pandas as pd
import plotly.express as px

TEMPLATE = "plotly_white"


def _set_legends(fig):
    fig.layout.update(legend=dict(x=-0.1, y=1.2))
    fig.layout.update(legend_orientation="h")


def plot_true_versus_confirmed(confirmed, predicted):
    df = pd.DataFrame(
        {
            "Status": ["Confirmed", "Predicted"],
            "Cases": [confirmed, predicted],
            "Color": ["b", "r"],
        }
    )
    fig = px.bar(df, x="Status", y="Cases", color="Color", template=TEMPLATE)
    fig.layout.update(showlegend=False)

    return fig


def infection_graph(df, y_max):
    # We cannot explicitly set graph width here, have to do it as injected css: see interface.css
    fig = px.line(df, x="Days", y="Forecast", color="Status", template=TEMPLATE)
    fig.update_yaxes(range=[0, y_max])
    _set_legends(fig)
    return fig


def age_segregated_hospitalization_and_mortality(df):
    colors = ['blue', 'pink', 'red', 'grey', ]
    fig = px.bar(df, x='Age group', y='Percentage', color='Outcome',
                 color_discrete_sequence=colors,
                 opacity=0.4,
                 template=TEMPLATE)
    return fig


def hospitalization_graph(df, number_of_beds, y_max):
    # Add in the number of beds and number of ventilators to the df
    days = list(df.Days.unique())
    n_days = len(days)

    bed_df = pd.DataFrame(
        {
            "Days": days,
            "Forecast": [number_of_beds] * n_days,
            "Status": ["Number of Beds"] * n_days,
        }
    )

    fig = px.line(df, x="Days", y="Forecast", color="Status", template=TEMPLATE)
    fig.add_scatter(
        x=bed_df.Days,
        y=bed_df.Forecast,
        name="Number of Beds",
        fill="tozeroy",
        opacity=0.1,
        fillcolor="rgba(50,255,140,.2)",
        line={"color": "rgba(50,255,140,.5)"},
    )
    fig.update_yaxes(range=[0, y_max])
    _set_legends(fig)
    return fig
