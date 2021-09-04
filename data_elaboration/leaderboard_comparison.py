from statistics import mean

from data_elaboration.leaderboard import Leaderboard


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
