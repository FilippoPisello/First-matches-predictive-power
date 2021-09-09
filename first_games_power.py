"""Run the complete similarity rate analysis"""
from data_download.worldfootball import (
    seriea_download,
    premierleague_download,
    ligue1_download,
)
from data_elaboration.leaderboard_comparison import rate_df_from_results
from data_elaboration.leaderboard_comparison import save_rate_df_to_excel
from data_elaboration.results import results_df_from_matches
from data_visualization.rates_over_time import visualize_rates_over_time
from data_visualization.rates_per_round import visualize_rates_per_round
from data_visualization.rates_across_leagues import (
    visualize_rates_per_round_across_leagues,
)

start_season = 2004
end_season = 2020

df_matches_seriea = seriea_download()
df_matches_premier = premierleague_download()
df_matches_ligue1 = ligue1_download()

matches_data = {
    "Serie A": df_matches_seriea,
    "Premier League": df_matches_premier,
    "Ligue 1": df_matches_ligue1,
}

rates_data = {}
for league in matches_data:
    df_results = results_df_from_matches(matches_data[league])
    df_rates = rate_df_from_results(df_results, start_season, end_season, league)
    rates_data[league] = df_rates
    save_rate_df_to_excel(df_rates, league_label=league)

    visualize_rates_per_round(df_rates, league, start_season, end_season)
    visualize_rates_over_time(df_rates, league, 2004, 2020)

for tolerance_level in range(0, 3):
    visualize_rates_per_round_across_leagues(
        rates_data, start_season, end_season, tolerance_level
    )
