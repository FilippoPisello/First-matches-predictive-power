from typing import Any
import pandas as pd
import regex as re
import requests
from bs4 import BeautifulSoup


def main():
    output_df = None
    seasons = [f"{x}-{x+1}" for x in range(2004, 2021)]
    rounds = range(1, 39)

    for season in seasons:
        for round in rounds:
            print(f"Downloading data from season {season}, round {round}")
            page = get_season_round_page(season, round)
            table_info = get_info_table(page)

            df = table_to_dataframe(table_info)
            df = score_in_two_columns(df)
            df = add_result_column(df)
            df = add_season_round_info_to_df(df, season, round)

            if output_df is None:
                output_df = df
            else:
                output_df = output_df.append(df)

    output_df.to_excel("Serie A Data.xlsx", index=False)


def get_season_round_page(season: Any, round: Any) -> requests.Response:
    """Get page from the web"""
    url = (
        f"https://www.worldfootball.net/schedule/ita-serie-a-{season}-spieltag/{round}/"
    )
    return requests.get(url)


def get_info_table(page: requests.Response) -> list:
    """Retrive desired table info from target page"""
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", class_="standard_tabelle")
    return table.find_all("td")


def table_to_dataframe(page_table: list) -> pd.DataFrame:
    """Turn table from list to data frame"""
    elements_as_text = [i.text.replace("\n", "") for i in page_table]

    teams_info = [i for i in elements_as_text if text_is_team(i)]
    scores_info = [i for i in elements_as_text if text_is_score(i)]

    team1 = teams_info[::2]
    team2 = teams_info[1::2]
    return pd.DataFrame({"Team 1": team1, "Team 2": team2, "Score": scores_info})


def text_is_team(input_text):
    """Return true if text matches a team name"""
    # This excludes specifically the special case dec. of score
    if bool(re.search("(dec.)", input_text)):
        return False
    return bool(re.search("[a-z]", input_text))


def text_is_score(input_text):
    """Return true if match score in the form '3:4 (0:3) '"""
    match1 = bool(re.match("(\d:\d \(\d:\d\) )", input_text))
    match2 = bool(re.match("(\d:\d dec.)", input_text))
    return match1 or match2


def add_season_round_info_to_df(
    dataframe: pd.DataFrame, season: Any, round: Any
) -> pd.DataFrame:
    """Add season and round column to existing data frame"""
    dataframe["Season"] = season
    dataframe["Round"] = round
    return dataframe


def score_in_two_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["Score"] = df["Score"].apply(lambda x: x.split(" ")[0])
    df["Score Team 1"] = df["Score"].apply(lambda x: int(x.split(":")[0]))
    df["Score Team 2"] = df["Score"].apply(lambda x: int(x.split(":")[1]))
    return df


def add_result_column(df: pd.DataFrame) -> pd.DataFrame:
    df["Result"] = df["Score Team 1"] - df["Score Team 2"]
    df["Result"] = df["Result"].apply(score_diff_to_result_sign)
    return df


def score_diff_to_result_sign(score_diff: int) -> str:
    if score_diff > 0:
        return "1"
    if score_diff < 0:
        return "2"
    return "X"


if __name__ == "__main__":
    main()
