from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import csv
import rankings_scrape as rs
from rankings_scrape import rankings_scraper, overview_scraper
import seaborn as sns

top_100 = rankings_scraper()

top_100['Website'] = 'https://www.atptour.com/' + top_100['Website']

personal_sites = top_100['Website']

overview_df = overview_scraper(top_100['Website'])

####Making some plots

sns.distplot(top_100['Height'])
sns.distplot(top_100['Weight'])
sns.distplot(top_100['Turned_pro'])

sns.scatterplot(top_100['Height'],top_100['Ranking'])
sns.scatterplot(top_100['Age'],top_100['Ranking'])
sns.scatterplot(top_100['Height'],top_100['Weight'])    

