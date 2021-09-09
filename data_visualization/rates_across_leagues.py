"""Contains function to plot the similarity rate across different leagues"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

from . import tools


def visualize_rates_per_round_across_leagues(
    rates_data: dict[str, pd.DataFrame],
    min_season: int,
    max_season: int,
    tolerance: int = 1,
    rounds: list = range(1, 38),
):
    """Create a line plot comparing median similarity rates at given rounds for
    multiple leagues."""
    _, ax = tools.initialize_plot(1)
    league_labels = ", ".join(list(rates_data.keys()))

    # Adding title and subtitle
    ttl = f"Median leaderboard similarity rate per championship round with tolerance of {tolerance}"
    plt.suptitle(ttl, y=0.94, ha="center", fontsize=18, weight=700)
    sub = tools.league_seasons_string(league_labels, min_season, max_season)
    plt.title(sub, y=1, x=0.5, fontsize=14, ha="center")

    # Adding axes titles
    tools.set_y_label(
        ax, "Median similarity rate compared with season's final leaderboard"
    )
    tools.set_x_label(ax, "Championship round")

    # Customizing axes
    ax.set_xticks(rounds)
    ax.set_xlim(min(rounds) - 1, max(rounds) + 1)
    ax.set_ylim(0.1, 1)
    ax.set_yticks([x / 10 for x in range(1, 11)])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    data = {
        league: median_per_round(rates_data[league], tolerance, rounds)
        for league in rates_data
    }
    for league in data:
        ax.plot(
            rounds, data[league], label=league, marker=".", markersize=15, linewidth=1
        )

    tools.set_grid(ax)
    tools.add_legend("League")

    filename = f"Median similarity rate per round across leagues_{league_labels}_{tolerance}.png"
    tools.save_file(filename)


def median_per_round(df: pd.DataFrame, tolerance: int, rounds: list) -> list[float]:
    filt = df["Tolerance"] == tolerance
    return [df.loc[(df["Round"] == round) & filt, "Rate"].median() for round in rounds]
