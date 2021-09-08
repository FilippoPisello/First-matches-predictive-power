from collections import namedtuple
from statistics import mean

import pandas as pd

from data_elaboration.leaderboard import Leaderboard


def rate_df_from_results(
    df_results: pd.DataFrame, start_season: int, end_season: int, league_label: str
) -> pd.DataFrame:
    Rate_Record = namedtuple("Rate", ["Serie", "Season", "Round", "Tolerance", "Rate"])

    rates = []
    for season in range(start_season, end_season + 1):
        final_leaderboard = Leaderboard(df_results, season, 38)
        for round_ in range(1, 38):
            partial_leaderboard = Leaderboard(df_results, season, round_)
            for numb in range(0, 3):
                rate = leaderboard_similarity_rate(
                    partial_leaderboard, final_leaderboard, tolerance=numb
                )
                rates.append(Rate_Record(league_label, season, round_, numb, rate))

    df = pd.DataFrame.from_records(rates, columns=Rate_Record._fields)
    return df


def leaderboard_similarity_rate(
    leaderboard1: Leaderboard, leaderboard2: Leaderboard, tolerance: int = 0
) -> float:
    """Return a float that represents the percentage of similarity between
    two leaderboards.

    A team has a similar rank across the two leaderboards if the absolute
    difference in ranks is less than or equal the tolerance. The similarity rate
    is the number of teams having a similar rank over the total number of teams
    considered."""
    is_similar_list = []

    for team in leaderboard1.teams_list:
        rank_initial = leaderboard1.get_rank_from_team(team)
        rank_final = leaderboard2.get_rank_from_team(team)

        is_similar_list.append(are_ranks_similar(rank_initial, rank_final, tolerance))

    return mean(is_similar_list)


def are_ranks_similar(rank1: int, rank2: int, tolerance: int) -> bool:
    return abs(rank2 - rank1) <= tolerance


def save_rate_df_to_excel(df: pd.DataFrame, league_label: str) -> None:
    filename = f"saved_dataframes/Similarity Rates_{league_label}.xlsx"
    df.to_excel(filename, index=False)
