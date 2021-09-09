# How much do football leaderboards change throughout a season?
_It happened to many football fans. With a lot of games still to be played, looking at the standings and wondering "how much are the things going to change by the end of the season?". This question formulates more generally as "how similar should I expect to be the rankings after n games and the ones at the end of the season?". In this artiscle, I describe my attempt to answer this question._

## The dataset
My analysis started from the Serie A league. I downloaded the matches results from season 2004/2005 to season 2020/2021. The data was scraped through Python from the website https://www.worldfootball.net/. The data scraping process is contained into [this module](data_download/worldfootball.py).

You can view the resulting dataset in this [excel file](saved_dataframes/Matches%20Data_Serie%20A.xlsx).

## From matches to standings
By aggregating the relevant matches results, I could compute the league's standings at a given round in a given season.

The process happened in two steps. I first transformed matches into results ([here](data_elaboration/results.py)) and then results into leaderboards ([here](data_elaboration/leaderboard.py)).

## Creating the leaderboard similarity rate
For my purpose, I needed to identify a way of measuring how similar two leaderboards are. I came up with an index that I labelled "leaderboard similarity rate". Given two leaderboards (L1, L2) and a tolerance rate (T), the leaderboard similarity rate is the percentage of teams whose distance - absolute value of the difference - in ranking across L1 and L2 is less than or equal to T.

An index of 60% with a tolerance of 0 means that six teams out of ten have the same ranking in the two leaderboards.

Note the implication of tolerance being applied to the absolute value of the difference in ranking. If T=2, a team at rank 6 in L1 would be considered in a "similar" position in L2 if it is in any of the following spots: 4, 5, 6, 7, 8.

## Computing the similarity rates
With the data downloaded and the index defined, I computed the similarity rates for the observed period. In practice, for every round R in [1, 37] and every season S in [2004/2005, 2020/2021], I derived the similarity rate between the leaderboard at round R in season S and the one at round 38, the last one, and season S. The process was iterated for three tolerance levels: 0, 1 and 2.

The records in my dataset ended up looking like what you see in this [excel file](saved_dataframes/Similarity%20Rates_Serie%20A.xlsx).

## Similarity rates along the season
Moving to the visualization, I first plotted the leaderboard similarity rates per season round for the three levels of tolerance. Given the low number of observations per round - one per season for 17 seasons - I used violin plots to capture the sample variability.
![](saved_plots/Similarity%20Rate%20per%20round_Serie%20A.png)
For every violin, the top, middle and bottom bars represent respectively the maximum, the median and the minimum. As expected, the median similarity rate increases with the rounds, meaning that the leaderboard consolidates over time. Similarly, higher tolerance implies higher similarity rates.

Looking at the top plot, you can see that in half of the observed seasons the similarity rate was less than or equal to 50% when R=35. With only two games left, half of the teams still were not in the sport where they would end up the season in. The 50% mark was instead reached by the median respectively at game 18 with T=1 and game 8 with T=2.

It is interesting to look at round 19, when the first half of the season is over. With T=0, the median rate is ~30%, with T=1 is ~55% and with T=2 is ~70%. It follows that most of the teams used to conclude their seasons not too far from where they were after the first half of it.

## Is Serie A getting more boring?
Higher similarity rates at earlier rounds imply that a good number of teams stick to their ranking for long periods of time. This might lead to less interesting matches and an overall more boring season. To check if Serie A is getting more boring, I arbitrary chose a subset of rounds and plotted the similarity rate - still compared to the final leaderboard - across different seasons.
![](saved_plots/Similarity%20Rate%20over%20time_Serie%20A_1.png)

Each line corresponds to a given round and each dot represents an observation of the similarity rate at round R of season S. Commenting at a qualitative level, I see no unequivocal trend: to my eye, the rates seem to be scattered around a rather consistent average.

## What about the other European Leagues?
The next thing I wanted to check is how Serie A compared with some other European leagues. I went back to https://www.worldfootball.net/ and repeated the same process of the Serie A data with the Premier League and Ligue 1.

I then plotted the median leaderboard similarity rate with tolerance of 1 of the 17 observed seasons across the first 37 rounds for the three leagues, obtaining the following:
![](saved_plots/Median%20similarity%20rate%20per%20round%20across%20leagues_Serie%20A,%20Premier%20League,%20Ligue%201_1.png)

Each line represents a league and each dot represents the median value of the observations for the similarity rate at a given round R for the seasons in the interval [2004/2005, 2020/2021]. You can see that Serie A's leaderboard similarity rates seem to be consistently higher than the ones of the other league from match 12 on. In other words, Serie A's leaderboard has been more stable than the one of Premier League and Ligue 1 in the central part of the season. The same result is observed with tolerance of 0 and 2, even if less pronounced.

## Conclusion
So what do I take from home from this analysis? How much do football leaderboards change? My answer is an underwhelming "quite a bit but not too much". On the one hand, in Serie A considering the last 17 seasons, at minimum 40% of the teams saw a change in their ranking in the last two games. On the other hand, at least 50% of the teams did not change their ranking of more than two positions throughout all the 19 games of the second half of the season.

What is your thought? Do you agree with my interpretation?

## Limitations and ideas for further research
I should point out one flaw of my analysis. When constructing the leaderboards at a given round of a given season, I simplified the ranking computation for teams having the same amount of points. While in real life there is a list of criteria considered so that an order is always established, in my leaderboards both teams get the minimum ranking. This means that, for example, if two teams have the maximum number of points, they will both be at rank 1 on the leaderboard. I believe however that this shortcoming has no significant impact on the aggregated results.

While conducting this analysis, more research ideas came to my mind. How does the study change by observing only the top or the bottom of the leaderboard? How much predictive power over the similarity rate would a simple regression model have using the round and the league information?