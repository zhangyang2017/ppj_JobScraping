# -*- coding: utf-8 -*-
"""
Spyder Editor
"""
from datetime import datetime #to get the current date
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import numpy as np

def extract(job_title, location):
    inquiry = 'https://www.indeed.com/jobs?q={}&l={}&filter=0'
    job_title = job_title.replace(' ', '+')
    location = location.replace(' ', '+')
    url = inquiry.format(job_title, location)
    return url

def transform(card):
    title = card.h2.a.get('title')
    job_link = 'https://www.indeed.com' + card.h2.a.get('href')
    company = card.find('span', class_ = 'company').text.strip()
    try:
        rating = card.find('span', class_ = 'ratingsContent').text.strip()
    except AttributeError:
        rating = ''
    location = card.find('div', class_ = 'recJobLoc').get('data-rc-loc')
    try:
        salary = card.find('span', 'salaryText').text.strip()
    except AttributeError:
        salary = ''
    summary = card.find('div', 'summary').text.strip()
    post_date = card.find('span', 'date').text
    today = datetime.today().strftime('%Y-%m-%d')
        
    job = {'title': title,
           'company': company,
           'rating': rating,
           'location': location,
           'salary': salary,
           'summary': summary,
           'post_date': post_date,
           'record obtained': today,
           'job_url': job_link
        }
    return job

def get_jobs(job_title, location):
    joblist = []
    url = extract(job_title, location)
    
    while True:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
        delays = [7, 4, 6, 2, 10, 19]
        delay = np.random.choice(delays)
        r = requests.get(url, headers)
        time.sleep(delay)
        soup = bs(r.content, 'html.parser')
        cards = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')
        for index, card in enumerate(cards):
            job = transform(card)
            joblist.append(job)
            print('moving along', index)
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

    data = pd.DataFrame(joblist)
    data.to_csv(job_title + '_jobs_indeed.csv')
    print('JOB FINISHED!')
    

#####
#get_jobs('data scientist', 'united states')