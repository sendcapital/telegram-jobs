import pandas as pd
from serpapi import GoogleSearch
import datetime
from google.cloud import bigquery
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from wordcloud import WordCloud
from dotenv import load_dotenv

load_dotenv() 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
API_KEY = os.getenv("API_KEY")


def fetch_data(search_term = "data analyst", search_location = "Singapore"):
      
  for i in range(45):
    start = i * 10
    params = {
      "api_key": API_KEY,
      "engine": "google_jobs",
      "google_domain": "google.com.sg",
      "q": search_term,
      "hl": "en",
      "gl": "sg",
      "location": search_location,
      "start": start
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    # check if the last search page (i.e., no results)
    try:
        if results['error'] == "Google hasn't returned any results for this query.":
            break
    except KeyError:
        print(f"Getting SerpAPI data for page: {start}")
    else:
        continue
      
    jobs = results['jobs_results']
    jobs = pd.DataFrame(jobs)
    jobs = pd.concat([pd.DataFrame(jobs), 
                    pd.json_normalize(jobs['detected_extensions'])], 
                    axis=1).drop('detected_extensions', axis=1)
    jobs['date_time'] = datetime.datetime.utcnow()

    # concat dataframe
    if start == 0:
        jobs_all = jobs
    else:
        jobs_all = pd.concat([jobs_all, jobs])

    jobs_all['search_term'] = search_term
    jobs_all['search_location'] = search_location
  return jobs_all


