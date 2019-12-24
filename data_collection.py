from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import csv
import rankings_scrape as rs
from rankings_scrape import rankings_scraper, overview_scraper, str_to_num, stats_scraper
import seaborn as sns
import re
from datetime import datetime

top_100 = rankings_scraper()

overview_df = overview_scraper(top_100['Website'], display=True)

top_100 = pd.concat([top_100, overview_df], axis=1)

service_stats_df, returns_stats_df = stats_scraper(url, 2001)

service_stats = {}
returns_stats = {}

for index, player in top_100.iterrows():
    print(player[0])
    service_df_temp, returns_df_temp = stats_scraper(player[4], player[10], display = True)
    service_stats[player[3]] = service_df_temp
    returns_stats[player[3]] = returns_df_temp
    