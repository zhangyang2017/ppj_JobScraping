#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:16:36 2020

@author: yangzhang
"""

import glassdoor_scraper as gs

path = '/Users/yangzhang/document/ds_projs/ppj_JobScraping/chromedriver'

df = gs.get_jobs('data scientist', 1241, True, path, 10)
df.to_csv('./data/glassdoor_raw_dataScientist.csv', index=False)