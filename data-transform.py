#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
## Transforms the season by season records into individual team win/loss records
## We code wins as 1, losses as -1, the games that were not played are coded as
## 0 ("draws").
##

import numpy as np
import pandas as pd

# list of the years we are interested in
# list only the beginning year of the seasons
years=np.arange(1995,2018,1)

# setup templates to get and store the data
inputTemplate="data/full-scores-{:d}.csv"
outputFile="data/team-results.csv"

# dictionary of team name -> abbr
# note that older team names should be also included or be resolved in some way
# in the data-getter.py
teamAbbr={
    "Atlanta Hawks": "ATL",
    "Brooklyn Nets": "BKN",
    "Boston Celtics": "BOS",
    "Charlotte Hornets": "CHA",
    "Charlotte Bobcats": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Jersey Nets": "BKN",
    "New Orleans Hornets": "NOP",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia Sixers": "PHI",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Seattle Supersonics": "OKC",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Vancouver Grizzlies": "MEM",
    "Washington Bullets": "WAS",
    "Washington Wizards": "WAS",
}

# it is easier to track team records via dictionary
rez={t:[] for t in np.unique(list(teamAbbr.values()))}

# loop through the years
for y in years:
    # load the season data
    df=pd.read_csv(inputTemplate.format(y),index_col=0)

    del df["OT"] # we are not interested in overtimes

    # we are not interested in exact score, but only in the game winner
    df["homeTeam"]=df["homeTeam"].map(teamAbbr)
    df["awayTeam"]=df["awayTeam"].map(teamAbbr)
    df["diff"]=df["homeScore"]-df["awayScore"]
    del df["homeScore"], df["awayScore"]
    
    # estimate total number of games in a season based on the Utah Jazz record
    # note that not all season had 82 games (e.g., 1999-2000 season had only 50
    # games)
    totalGames=2*np.sum(df["homeTeam"]=="UTA")

    # for each team
    for team in rez.keys():
        # get the games in which they have played as home or away team
        gameIndex=df.index.map(lambda x: (df.loc[x]["homeTeam"]==team or df.loc[x]["awayTeam"]==team))
        # assuming that team played all the games or no games in the season
        # produce win/loss record
        if(np.sum(list(gameIndex))>0):
            homeWin=(df[gameIndex]["diff"]>0)
            teamHome=(df[gameIndex]["homeTeam"]==team)
            teamWin=np.array(homeWin==teamHome).astype(int)
            teamWin=2*teamWin-1
            rez[team]+=list(teamWin)
        else:
            rez[team]+=list(np.zeros(totalGames))
    del team, gameIndex, homeWin, teamHome, teamWin
del y, df, totalGames

odf=pd.DataFrame(rez)
odf.to_csv(outputFile,float_format="%.0f",index=False)
