from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import csv
import rankings_scrape as rs
from rankings_scrape import rankings_scraper, overview_scraper
import rankings_scrape as rs
import seaborn as sns

top_100 = rankings_scraper()

overview_df = overview_scraper(top_100['Website'])

###Collating stats for Nadal

url = 'https://www.atptour.com/en/players/rafael-nadal/n409/overview'
url = re.sub('overview',''.url)

