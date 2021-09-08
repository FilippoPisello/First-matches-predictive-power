from typing import Union
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def initialize_plot(number_of_subplots: int) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(number_of_subplots)
    fig.set_size_inches(20, 10)
    fig.set_dpi(200)
    return fig, ax


def set_y_label(axes_object: Axes, label: str) -> None:
    axes_object.set_ylabel(label, fontsize=13, fontstyle="italic")


def set_x_label(axes_object: Axes, label: str) -> None:
    axes_object.set_xlabel(label, fontsize=13, fontstyle="italic")


def league_seasons_string(league_label: str, min_season: int, max_season: int) -> str:
    s1, s2 = season_label(min_season), season_label(max_season)
    return f"League: {league_label}, Considered seasons: from {s1} to {s2}"


def season_label(season_starting_year: int) -> str:
    return f"{season_starting_year}/{season_starting_year+1}"


def set_grid(axes_object: Axes) -> None:
    axes_object.grid(True, linestyle="--")


def add_legend(title: Union[str, None]) -> None:
    plt.legend(title=title, fontsize=13)


def save_file(file_name: str) -> None:
    plt.savefig("saved_plots/" + file_name)
    print(f"File {file_name} saved correctly")
