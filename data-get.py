#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
## Gets the full regular season records from the landofbasketball.com website
## and stores the records to csv file.
##

## NOTE: Do not forget to manually add the games which were not played
## such as Celtics - Pacers game cancelled to the Boston marathon bombings.
## In these cases we have simply set the score to 0:0. We have added the
## aforementioned games as 1213rd game in 2012 season.

import numpy as np
import pandas as pd
import re
import urllib
from bs4 import BeautifulSoup

# list of the years we are interested in
# list only the beginning year of the seasons
years=np.arange(1995,2018,1)

# setup templates to get and store the data
urlTemplate="http://www.landofbasketball.com/results/{:d}_{:d}_scores_full.htm"
outputTemplate="data/full-scores-{:d}.csv"

# precompile regex
multiSpace=re.compile(r"\s+") # will be used to remove multiple spaces
special=re.compile(r"(\\t|\\n)") # will be used to remove tab and newline markers
teamScore=re.compile(r"\s?([A-Za-z\s]+) (\d+)") # extract team name and score
location=re.compile(r"at ([A-Za-z\s]+)") # extract location where the game was played
overtime=re.compile("OT") # check whether the game went to overtime
playoffs=re.compile("Playoffs") # check whether the line contains Playoffs marker
# loop through the years
for y in years:
    scores=[]
    # fetch HTML
    page=urllib.request.urlopen(urlTemplate.format(y,y+1)).read()
    # interpret HTML
    soup=BeautifulSoup(page,"html5lib")
    # find the table
    table=soup.find("table")
    # loop through the rows of the table while looking for lines
    # with valid game records
    # terminate on "Playoffs" marker
    for tr in table.findAll("tr"):
        line=tr.text.replace("76ers","Sixers").strip() # might mess up our score detection regex
        # remove whitespaces and special markers
        line=special.sub("",line)
        line=multiSpace.sub(" ",line)
        line=line.strip()
        # find team names and scores
        score=teamScore.findall(line)
        if(len(score)==0): # does not contain score or date
            if(playoffs.search(line) is not None):# contains "Playoffs"
                break
        elif(len(score)>=2): # contains score
            # more than two instances are found in case there were multiple OT's
            ot=(overtime.search(line) is not None)
            loc=location.findall(line)
            if(y in [2005,2006]):
                score[0]=[score[0][0].replace("Oklahoma City","New Orleans")
                                     .replace("New Orleans/New Orleans","New Orleans"),
                          score[0][1]]
                score[1]=[score[1][0].replace("Oklahoma City","New Orleans")
                                     .replace("New Orleans/New Orleans","New Orleans"),
                          score[1][1]]
                loc[0]=loc[0].replace("Oklahoma City","New Orleans")
                             .replace("New Orleans/New Orleans","New Orleans")
            # try sorting so that the first team would be the home team and the
            # second team would be away team (impossible for LAL and LAC as both
            # play in LA).
            if(score[0][0].find(loc[0])>-1):# first team is home team
                scores+=[[score[0][0],score[1][0],score[0][1],score[1][1],int(ot),loc[0]],]
            elif(score[1][0].find(loc[0])>-1):# second team is home team
                scores+=[[score[1][0],score[0][0],score[1][1],score[0][1],int(ot),loc[0]],]
            else:# these will have to be resolved by hand
                scores+=[[score[0][0],score[1][0],score[0][1],score[1][1],int(ot),loc[0]],]
                print(y,scores[-1]) # hence print these cases
    del line, score, ot, loc, tr, table
    scores=np.array(scores)
            
    df=pd.DataFrame(scores[:,:5],columns=["homeTeam","awayTeam","homeScore","awayScore","OT"])
    df["homeScore"]=pd.to_numeric(df["homeScore"])
    df["awayScore"]=pd.to_numeric(df["awayScore"])
    df["OT"]=pd.to_numeric(df["OT"])
    
    df.to_csv(outputTemplate.format(y))
