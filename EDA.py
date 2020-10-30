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

def punctuation_stop(text):
    """remove punctuation and stop words"""
    filtered = []
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    for w in word_tokens:
        if w not in stop_words and w.isalpha():
            filtered.append(w.lower())
    return filtered

words_DS = " ".join(jobs['summary'])
words_filtered = punctuation_stop(words_DS)
text_DS = " ".join([ele for ele in words_filtered])
wc_DS= WordCloud(background_color="white", random_state=1,stopwords=STOPWORDS, max_words = 2000, width =800, height = 1500)
wc_DS.generate(text_DS)

words_bio = " ".join(bio['summary'])
words_filtered = punctuation_stop(words_bio)
text_bio = " ".join([ele for ele in words_filtered])

wc_bio= WordCloud(background_color="white", random_state=1,stopwords=STOPWORDS, max_words = 2000, width =800, height = 1500)
wc_bio.generate(text_bio)


f = plt.figure(figsize=(20,20))
ax1 = f.add_subplot(1, 2, 1)
f.suptitle("Most Wanted Skills", fontsize=22, fontweight='bold', color='chocolate')
plt.imshow(wc_DS, interpolation="bilinear")
ax1.set_title('Data Scientist from 1,269 Job Posts', fontsize=16, fontweight='bold')
plt.axis('off')

#####
ax2 = f.add_subplot(1, 2, 2)
plt.imshow(wc_bio, interpolation="bilinear")
ax2.set_title('Bioinformatics from 1,286 Job Posts', fontsize=16, fontweight='bold')
plt.axis('off')
plt.subplots_adjust(hspace=0.2,wspace=0.2)
f.subplots_adjust(top=1.2)
plt.tight_layout()
plt.show()




plt.figure(figsize=[12,12])
plt.imshow(wc_DS, interpolation="bilinear")
plt.title('Most Wanted Skills for Data Scientist \n(2020-10-29 from Indeed.com)')
plt.axis('off')
plt.savefig('./figures/wordCloud_DS.png', bbox_inches = 'tight', dpi=300)
plt.show()

bio = pd.read_csv('./data/bioinformatics_jobs_indeed.csv')
bio = bio.drop('Unnamed: 0', axis = 1)
bio.drop_duplicates(keep=False,inplace=True)
bio.shape

bio['State'] = bio['location'].apply(lambda x: x.split(',')[1] if ',' in x else x)
bio.drop(bio[bio.State == 'United States'].index, inplace=True)
bio.drop(bio[bio.State == 'Remote'].index, inplace=True)

bio['State'] = bio['State'].apply(lambda x: x.replace('California', 'CA').replace('Massachusetts', 'MA')
                                  .replace('Florida', 'FL').replace('Wisconsin', 'WI')
                                  .replace('Connecticut', 'CT').replace('New York State', 'NY')
                                  .replace('Hawaii', 'HI').replace('Delaware', 'DE').replace('Illinois', 'IL'))
bio['State'] = bio['State'].str.strip()

bio['City'] = bio['location'].apply(lambda x: x.split(',')[0] if ',' in x else x)
bio = bio.drop('location', axis = 1)




plt.figure(figsize=[12,14])
plt.imshow(wc, interpolation="bilinear")
plt.title('Most Wanted Skills for Bioinformatician \n(1,286 Job Posts from Indeed.com 2020-10-29)')
plt.axis('off')
plt.savefig('./figures/wordCloud_BioInfo.png', bbox_inches = 'tight', dpi=300)
plt.show()