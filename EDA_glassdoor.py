#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:03:01 2020

@author: yangzhang
"""

import pandas as pd

df = pd.read_csv('./data/glassdoor_raw_dataScientist.csv')
df = df.drop('Headquarters', axis = 1) ##something seemed wrong during the scraping step; failed to grab this information.

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

##drop internship job posts
df.drop(df.loc[df['Title'].str.contains('Intern', regex=True)].index, inplace=True)

##clean up salary estimate column
df['Salary'] = df['SalaryEstimate'].apply(lambda x: x.split('(')[0] if '(' in x else x).apply(lambda x: x.replace('$', '')).apply(lambda x: x.replace('K', ''))
df['minSalary'] = df['Salary'].apply(lambda x: x.split('-')[0] if '-' in x else x)
df['maxSalary'] = df['Salary'].apply(lambda x: x.split('-')[1] if '-' in x else x)
df = df.drop(['SalaryEstimate', 'Salary'], axis = 1)

##clean up company column, remove numbers
df['Company'] = df['Company'].apply(lambda x: x.split('\n')[0] if '\n' in x else x)

##create new feature: company age
df['compHistory'] = df['Founded'].apply(lambda x: x if x < 1 else 2020-x)

##clean up revenue
df['Revenue'] = df['Revenue'].apply(lambda x: x.split('(')[0] if '(' in x else x)
df['Revenue'] = df['Revenue'].apply(lambda x: x.split('/')[0] if '/' in x else x).str.strip()
df['Revenue'] = df['Revenue'].apply(lambda x: x.replace('-1', 'Unknown'))

##clean up ownership
df['Ownership'] = df['Ownership'].apply(lambda x: x.replace('-1', 'Unknown'))

df.to_csv('./data/glassdoor_halfcleaned_dataScientist.csv', index=False)
##manually fill in some missing values if I can dig more information


##things to do
## split company size into groups
## fill in missing values
## entry level or senior, job level
## data analytics vs scientists, aka title simplifier
##tools mentioned in job description, like python, and R, etc.
##job description length