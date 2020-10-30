#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 18:46:15 2020

@author: yangzhang
"""

import pandas as pd
import matplotlib.pyplot as plt

jobs = pd.read_csv('./data/data_scientist_jobs_indeed.csv')
jobs = jobs.drop('Unnamed: 0', axis = 1)
jobs.drop_duplicates(keep=False,inplace=True)
#jobs.shape

jobs['State'] = jobs['location'].apply(lambda x: x.split(',')[1] if ',' in x else x)
jobs.drop(jobs[jobs.State == 'United States'].index, inplace=True)
jobs.drop(jobs[jobs.State == 'Remote'].index, inplace=True)

jobs['State'] = jobs['State'].apply(lambda x: x.replace('California', 'CA').replace('Massachusetts', 'MA')
                                    .replace('Florida', 'FL').replace('Washington State', 'WA')
                                    .replace('Indiana', 'IN').replace('New York State', 'NY'))
jobs['State'] = jobs['State'].str.strip()

jobs['City'] = jobs['location'].apply(lambda x: x.split(',')[0] if ',' in x else x)
jobs = jobs.drop('location', axis = 1)

jobs.to_csv('./data/data_scientist_jobs_indeed_cleaned.csv', index=False)
jobs.State.value_counts()

from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

words = " ".join(jobs['summary'])

def punctuation_stop(text):
    """remove punctuation and stop words"""
    filtered = []
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    for w in word_tokens:
        if w not in stop_words and w.isalpha():
            filtered.append(w.lower())
    return filtered


words_filtered = punctuation_stop(words)

text = " ".join([ele for ele in words_filtered])

wc= WordCloud(background_color="white", random_state=1,stopwords=STOPWORDS, max_words = 2000, width =800, height = 1500)
wc.generate(text)

plt.figure(figsize=[10,10])
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.show()