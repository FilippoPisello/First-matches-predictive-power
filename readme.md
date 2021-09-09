[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
# Project Goal
It happened to many football fans. With a lot of games still to be played, looking at the standings and wondering "how much are the things going to change by the end of the season?". This question formulates more generally as "how similar should I expect to be the rankings after _n_ games and the ones at the end of the season?".

In this project, I used match results from season 2004/2005 to season 2020/2021 for Serie A, Premier League and Ligue 1 in the attempt of answering the above question.

# Usage
## How to run the code
To run the analysis on your machine you should download the entire content of the project and run the following command within the directory where you have placed the files:
```console
python first_game_power.py
```
The data scraping will immediately start and at the end of the process you will find some plots in the folder "saved_plots" and some spreadsheets in the folder "saved_spreadsheets".
## Required packages
The project requires the following packages:
- beautifulsoup
- matplotlib
- pandas
- regex
- requests