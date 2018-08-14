#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
## This program fully shuffles the original team win/loss record data
## (namely it destroys season-to-season and game-to-game correlations)
## and estimates 95% CIs for H after preset number of shuffles
##

import numpy as np
import pandas as pd
from stats.mfdfa import dfa
import scipy.optimize as spo

# desired amount of shuffles
shuffles=10000

# setup input/output files
inputFile="data/team-results.csv"
outputFile="data/team-shuffle-total.csv"

# read the original data
df=pd.read_csv(inputFile)

# it is easier to tracks teams using dictionary
rez={t:[] for t in df.columns}

# estimate s in the desired range
qs=np.unique(np.logspace(0.7,1.8,num=50).astype(int))
logQs=np.log10(qs)

for _ in range(shuffles):
    sdf=df.copy() # copy the original data
    sdf.apply(np.random.shuffle,axis=0) # perform shuffling
    sProfileDf=sdf.subtract(sdf.mean()).cumsum() # obtain profile
    for team in df.columns: # for each team
        fqs=dfa(list(sProfileDf[team].values),2,qs) # estimate F(s)
        params,_=spo.curve_fit(lambda x,a,b: a*x+b,logQs,np.log10(fqs)) # fit F(s)
        rez[team]+=[params[0],] # store the obtained H
del sdf, sProfileDf, team, qs, logQs, fqs, params

# estimate 95% CIs
bounds=[]
for team in df.columns:
    bounds+=[[
            team,
            np.percentile(rez[team],2.5),
            np.percentile(rez[team],97.5),
        ],]

boundDf=pd.DataFrame(bounds,columns=["team","H25","H975"])
boundDf.to_csv(outputFile,float_format="%.5f")
