import pandas as pd


def results_df_from_matches(df: pd.DataFrame) -> pd.DataFrame:
    df = add_result_column(df)
    df = add_points_per_team_columns(df)

    df1 = df.loc[:, ["Team 1", "Season", "Round", "Points team 1"]].copy()
    df2 = df.loc[:, ["Team 2", "Season", "Round", "Points team 2"]].copy()

    df1.columns = ["Team", "Season", "Round", "Points earned"]
    df2.columns = ["Team", "Season", "Round", "Points earned"]

    df1 = df1.append(df2)
    return df1


def add_result_column(df: pd.DataFrame) -> pd.DataFrame:
    score_difference = df["Score Team 1"] - df["Score Team 2"]
    df["Result"] = score_difference.apply(score_diff_to_result_sign)
    return df


def score_diff_to_result_sign(score_diff: int) -> str:
    if score_diff > 0:
        return "1"
    if score_diff < 0:
        return "2"
    return "X"


def add_points_per_team_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["Points team 1"] = df["Result"].map({"1": 3, "2": 0, "X": 1})
    df["Points team 2"] = df["Result"].map({"1": 0, "2": 3, "X": 1})
    return df
