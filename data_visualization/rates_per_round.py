import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

from . import tools


def visualize_rates_per_round(
    rates_df: pd.DataFrame, league_label: str, min_season: int, max_season: int
) -> None:
    _, ax = tools.initialize_plot(3)

    # Adding title and subtitle
    ttl = "Leaderboard similarity rate per championship round with different levels of tolerance"
    plt.text(s=ttl, y=3.6, x=18, fontsize=16, ha="center", weight=700)
    sub = tools.league_seasons_string(league_label, min_season, max_season)
    plt.text(s=sub, y=3.5, x=18, fontsize=14, ha="center")

    # Adding axes titles
    tools.set_y_label(ax[1], "Similarity rate compared with season's final leaderboard")
    tools.set_x_label(ax[2], "Championship round")

    for number in range(0, 3):
        # Plotting data
        data = data_per_round(rates_df, tolerance=number)
        ax[number].violinplot(data, showmedians=True)

        # Customizing the axis
        ax[number].set_xlim(0, 38)
        ax[number].set_xticks(range(1, 38))
        ax[number].set_ylim(0, 1)
        ax[number].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

        # Adding individual titles
        ax[number].set_title(f"Tolerance = {number}", y=0.87)

        # Adding grid
        tools.set_grid(ax[number])

    tools.save_file(f"Similarity Rate per round_{league_label}.png")


def data_per_round(df: pd.DataFrame, tolerance: int) -> list[list[float]]:
    return [
        df.loc[(df["Round"] == round) & (df["Tolerance"] == tolerance), "Rate"].tolist()
        for round in range(1, 38)
    ]
