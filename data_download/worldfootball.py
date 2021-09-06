"""Download matches data connecting to worldfootball.net."""

from typing import Any
import pandas as pd
import regex as re
import requests
from bs4 import BeautifulSoup


def seriea_download(
    starting_season: int = 2004, ending_season: int = 2020, save_to_excel: bool = True
) -> pd.DataFrame:
    print("\nStarting the download of Serie A matches data...")
    df = download_from_worldfootball("ita-serie-a", starting_season, ending_season)
    if save_to_excel:
        save_dataframe_to_excel(df, "Serie A")
    return df


def premierleague_download(
    starting_season: int = 2004, ending_season: int = 2020, save_to_excel: bool = True
) -> pd.DataFrame:
    print("\nStarting the download of Premier League matches data...")
    df = download_from_worldfootball(
        "eng-premier-league", starting_season, ending_season
    )
    if save_to_excel:
        save_dataframe_to_excel(df, "Premier League")
    return df


def ligue1_download(
    starting_season: int = 2004, ending_season: int = 2020, save_to_excel: bool = True
) -> pd.DataFrame:
    print("\nStarting the download of Ligue 1 matches data...")
    df = download_from_worldfootball("fra-ligue-1", starting_season, ending_season)
    if save_to_excel:
        save_dataframe_to_excel(df, "Ligue 1")
    return df


def primieradivision_download(
    starting_season: int = 2004, ending_season: int = 2020, save_to_excel: bool = True
) -> pd.DataFrame:
    print("\nStarting the download of Primiera Division matches data...")
    df = download_from_worldfootball(
        "esp-primera-division", starting_season, ending_season
    )
    if save_to_excel:
        save_dataframe_to_excel(df, "Primiera Division")
    return df


def download_from_worldfootball(
    league_url_tag: str, starting_season: int, ending_season: int
) -> pd.DataFrame:
    output_df = None

    seasons = [f"{x}-{x+1}" for x in range(starting_season, ending_season + 1)]
    rounds = range(1, 39)

    for season in seasons:
        for round_ in rounds:
            print(f"Downloading data from season {season}, round {round_}...")
            page = get_season_round_page(league_url_tag, season, round_)
            table_info = get_info_table(page)

            df = table_to_dataframe(table_info)
            df = score_in_two_columns(df)
            season_as_int = int(season.split("-")[0])
            df = add_season_round_info_to_df(df, season_as_int, round_)

            if output_df is None:
                output_df = df
            else:
                output_df = output_df.append(df)

    print("Data download completed!\n")
    return output_df


def get_season_round_page(
    league_tag: str, season: Any, round: Any
) -> requests.Response:
    """Get page from the web"""
    url = f"https://www.worldfootball.net/schedule/{league_tag}-{season}-spieltag/{round}/"
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


def save_dataframe_to_excel(df: pd.DataFrame, league_tag: str) -> None:
    df.to_excel(f"saved_dataframes/Matches Data_{league_tag}.xlsx", index=False)
    print(f"{league_tag} matches data saved correctly")
