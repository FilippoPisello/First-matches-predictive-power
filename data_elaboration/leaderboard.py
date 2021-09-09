"""Class to represent a leaderboard for a given season at a given round."""
from typing import Union
import pandas as pd


class Leaderboard:
    def __init__(
        self,
        results: pd.DataFrame,
        season: int,
        round: int = 38,
        ranks_range: tuple[Union[None, int], Union[None, int]] = (None, None),
    ) -> None:
        """Represent a leaderboard for a given season at a given round.

        Parameters
        ----------
        results : pd.DataFrame
            Pandas data frame with columns for team, season, round and points.
        season : int
            The starting year of the season the leaderboard should be constructed
            for.
        round : int, optional
            The round the leaderboard should be constructed for, by default 38.
        ranks_range : tuple[Union[None, int], Union[None, int]], optional
            If not (None, None), it restricts the leaderboard only to include
            the ranks in the provided range. The range is inclusive on both
            sides. Use a single None for a one-sided interval.
        """
        self.season = season
        self.round = round
        self.table_as_df = self.make_leaderboard(results, ranks_range)
        self.table_as_dict = self.make_dictionary()

    @property
    def teams_list(self) -> list[str]:
        """Return the list of teams in the leaderboard"""
        return list(self.table_as_dict.keys())

    @property
    def ranks_list(self) -> list[int]:
        """Return the list of ranks in the leaderboard"""
        return list(self.table_as_dict.values())

    def make_leaderboard(self, df: pd.DataFrame, ranks_range: tuple) -> pd.DataFrame:
        """Create data frame with columns ["Team", "Points Earned", "Rank"]"""
        df = self.relevant_season_rounds_only(df)

        df = df.groupby(["Team"], as_index=False).agg({"Points earned": "sum"})
        df["Rank"] = df["Points earned"].rank(method="min", ascending=False)

        df = self.desired_ranks_only(df, ranks_range)

        df = df.sort_values(by=["Rank"], ascending=True)
        return df

    def relevant_season_rounds_only(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filters out from the df the results relevant for the leaderboard"""
        filter_ = (df["Season"] == self.season) & (df["Round"] <= self.round)
        return df.loc[filter_, :]

    @staticmethod
    def desired_ranks_only(df: pd.DataFrame, ranks_range: tuple):
        min_rank, max_rank = ranks_range
        if min_rank is not None:
            df = df.loc[df["Ranks"] >= min_rank, :].copy()
        if max_rank is not None:
            df = df.loc[df["Ranks"] <= max_rank, :].copy()
        return df

    def make_dictionary(self) -> dict[str:int]:
        """Return a dict of the form {team : rank}"""
        return {
            team: score
            for team, score in zip(self.table_as_df["Team"], self.table_as_df["Rank"])
        }

    def get_rank_from_team(self, team: str) -> int:
        """Return the rank of a given team provided its name"""
        return self.table_as_dict[team]
