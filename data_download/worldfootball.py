"""Download matches data connecting to worldfootball.net."""

from concurrent.futures import ThreadPoolExecutor
from typing import Any
from dataclasses import dataclass

import pandas as pd
import regex as re
import requests
from bs4 import BeautifulSoup

################################################################################
# Download of matches data from different leagues
################################################################################
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


################################################################################
# Construction of the download process
################################################################################
def download_from_worldfootball(
    league_url_tag: str, starting_season: int, ending_season: int
) -> pd.DataFrame:
    output_df = None

    seasons = [f"{x}-{x+1}" for x in range(starting_season, ending_season + 1)]

    web_data = []
    for season in seasons:
        season_data = multithread_round_data(league_url_tag, season)
        web_data.extend(season_data)

    for page in web_data:
        table_info = get_matches_table_from_page(page.page_response)

        df = table_to_dataframe(table_info)
        df = score_in_two_columns(df)
        df = add_season_round_info_to_df(df, page.season_int, page.round_)

        if output_df is None:
            output_df = df
        else:
            output_df = output_df.append(df)

    output_df.sort_values(by=["Season", "Round"], ascending=[True, True], inplace=True)
    print("Data download completed!\n")
    return output_df


# ---------------------------------
# Connect to the web and request data
# ---------------------------------
@dataclass
class MatchPageResponse:
    season_label: str
    round_: int
    page_response: requests.Response

    @property
    def season_int(self):
        return int(self.season_label.split("-")[0])


def multithread_round_data(league_tag: str, season: Any) -> list[MatchPageResponse]:
    output = []
    # Execute our get_data in multiple threads each having a different page number
    with ThreadPoolExecutor(max_workers=38) as executor:
        [
            executor.submit(get_season_round_page, league_tag, season, round_, output)
            for round_ in range(1, 39)
        ]
    return output


def get_season_round_page(
    league_tag: str, season: Any, round_: Any, req_list: list
) -> None:
    """Get the page for a round in a given season"""
    url = f"https://www.worldfootball.net/schedule/{league_tag}-{season}-spieltag/{round_}/"
    response = requests.get(url)
    req_list.append(MatchPageResponse(season, round_, response))
    print(f"Requesting data from season {season}, round {round_}...")


# ---------------------------------
# Elaborate the data downloaded from the web
# ---------------------------------
def get_matches_table_from_page(page: requests.Response) -> list:
    """Retrive desired table info from target page"""
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", class_="standard_tabelle")
    return table.find_all("td")


def table_to_dataframe(page_table: list) -> pd.DataFrame:
    """Turn table from list to data frame"""
    elements_as_text = [i.text.replace("\n", "") for i in page_table]

    scores_info, teams_info = [], []
    for element in elements_as_text:
        if text_is_score(element):
            if element == " abor." or element == " dnp":
                element = "0:0 fix."
            scores_info.append(element)
            continue
        if text_is_team(element):
            teams_info.append(element)

    team1 = teams_info[::2]
    team2 = teams_info[1::2]

    return pd.DataFrame({"Team 1": team1, "Team 2": team2, "Score": scores_info})


def text_is_team(input_text):
    """Return true if text matches a team name"""
    # This excludes specifically the special case dec. of score
    return bool(re.search("[a-z]", input_text))


def text_is_score(input_text):
    """Return true if match score in the form '3:4 (0:3) '"""
    match1 = bool(re.match("(\d+:\d+ \(\d:\d\) )", input_text))
    match2 = bool(re.match("(\d:\d dec.)", input_text))
    match3 = input_text == " abor." or input_text == " dnp"
    return match1 or match2 or match3


# Not in use at the moment
def too_many_null_games(scores_list: list[str], invalid_token: str) -> bool:
    return scores_list.count(invalid_token) >= 4


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
