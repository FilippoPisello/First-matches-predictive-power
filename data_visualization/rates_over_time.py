"""Contains function to plot similarity rates over the course of the seasons."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import pandas as pd

from . import tools


def visualize_rates_over_time(
    rates_df: pd.DataFrame,
    league_label: str,
    min_season: int,
    max_season: int,
    rounds_list: list[int] = [1, 9, 19, 27, 37],
    tolerance: int = 1,
) -> None:
    """Create a line plot for the trend of similarity rates at fixed rounds
    across multiple seasons"""
    _, ax = tools.initialize_plot(1)

    # Adding title and subtitle
    ttl = f"Leaderboard similarity rate with tolerance of {tolerance} over different seasons for a sample of rounds"
    plt.suptitle(ttl, y=0.94, ha="center", fontsize=18, weight=700)
    sub = tools.league_seasons_string(league_label, min_season, max_season)
    plt.title(sub, y=1, x=0.5, fontsize=14, ha="center")

    # Customizing y axis style
    ax.set_yticks([x / 10 for x in range(1, 11)])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    # Adding axes titles
    tools.set_y_label(ax, "Similarity rate compared with season's final leaderboard")
    tools.set_x_label(ax, "Season starting year")

    # Adding grid
    tools.set_grid(ax)

    for round_ in rounds_list:
        filt = (rates_df["Tolerance"] == tolerance) & (rates_df["Round"] == round_)
        season = rates_df.loc[filt, "Season"]
        rate = rates_df.loc[filt, "Rate"]
        ax.plot(season, rate, label=round_, marker=".", markersize=15, linewidth=1)

    # Adding legend
    tools.add_legend("Rounds")

    file_name = f"Similarity Rate over time_{league_label}_{tolerance}.png"
    tools.save_file(file_name)
