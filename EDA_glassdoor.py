#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:03:01 2020

@author: yangzhang
"""

import pandas as pd

df = pd.read_csv('./data/glassdoor_raw_dataScientist.csv')

##drop rows with no salary info
df = df[df.SalaryEstimate != '-1']

##split location into state and city
df['State'] = df['Location'].apply(lambda x: x.split(',')[1] if ',' in x else x)
df['State'] = df['State'].str.strip()
df['State'] = df['State'].apply(lambda x: x.replace('California', 'CA').replace('Maryland', 'MD')
                                    .replace('North Carolina', 'NC').replace('Virginia', 'VA')
                                    .replace('New Jersey', 'NJ').replace('Tennessee', 'TN'))

df.drop(df[df.State == 'Bristol'].index, inplace=True)
df.drop(df[df.State == 'United States'].index, inplace=True)

df['City'] = df['Location'].apply(lambda x: x.split(',')[0] if ',' in x else x)
df = df.drop('Location', axis = 1)
