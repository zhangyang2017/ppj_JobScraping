#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 18:46:15 2020

@author: yangzhang
"""

import pandas as pd

jobs = pd.read_csv('bioinformatics_jobs_indeed.csv')
jobs = jobs.drop('Unnamed: 0', axis = 1)
jobs.drop_duplicates(keep=False,inplace=True)
#jobs.shape

jobs['State'] = jobs['location'].apply(lambda x: x.split(',')[1] if ',' in x else x)

jobs['State'] = jobs['State'].apply(lambda x: x.replace('California', 'CA').replace('Wisconsin', 'WI')
                                    .replace('Florida', 'FL').replace('Delaware', 'DE')
                                    .replace('Illinois', 'IL').replace('Connecticut', 'CT')
                                    .replace('Hawaii', 'HI').replace('New York State', 'NY'))
jobs['State'] = jobs['State'].str.strip()
jobs.drop(jobs[jobs.State == 'United States'].index, inplace=True)
jobs.drop(jobs[jobs.State == 'Remote'].index, inplace=True)
jobs['City'] = jobs['location'].apply(lambda x: x.split(',')[0] if ',' in x else x)




df = jobs[['State', 'City']].groupby(['State']).agg(['count'])
df.sort_values('City count', ascending=False)