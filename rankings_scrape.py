"""This module contains the functions required to scrape data from the ATP single rankings."""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def rankings_scraper(urlpage='https://www.atptour.com/en/rankings/singles'):
    
    """
    Scrapes data from the current top 100 ranked Men's Tennis players according to the ATP rankings site.
    
    Returns a Pandas DataFrame.
    
    Default website is: https://www.atptour.com/en/rankings/singles.
    
    Requires urllib, bs4, numpy and pandas to be installed.  
    
    """
    
    request = Request(urlpage,headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(request).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    table = soup.find('table',attrs={'class':'mega-table'})
    results = table.find_all('td')

    results_ll = []
    for i in np.arange(0,len(results)-1,9):
        result_l_temp = []
        for j in range(0,9):
            result_l_temp.append(results[i+j])
        results_ll.append(result_l_temp)

    rows = []
    rows.append(['Ranking','Move','Country','Name','Website','Age','Points','Tournaments Played','Points Dropping','Next Best'])

    for result in results_ll:
        rank = result[0].getText()
        move = result[1].getText()
        country = result[2].find('img').get('alt')
        name = result[3].getText()
        website = result[3].find_all('a', href=True)[0]['href']
        age = result[4].getText()
        points = result[5].getText()
        tournaments = result[6].getText()
        dropping = result[7].getText()
        nextbest = result[8].getText()

        row_temp = [rank,move,country,name,website,age,points,tournaments,dropping,nextbest]
        row_temp = [x.replace('\r','').replace('\n','').replace('\t','').replace(',','') for x in row_temp]

        if row_temp[1] == '':
            row_temp[1]=0

        rows.append(row_temp)

    ATP_df = pd.DataFrame.from_records(rows)
    ATP_df.columns = ATP_df.iloc[0]
    ATP_df = ATP_df.iloc[1:]
    
    #Converting some columns to integer
    ATP_df = ATP_df.astype({
        'Ranking':'int32',
        'Move':'int32',
        'Age':'int32',
        'Points':'int32',
        'Tournaments Played':'int32',
        'Points Dropping':'int32',
        'Next Best':'int32',
               })
    
    ATP_df['Website'] = 'https://www.atptour.com/' + ATP_df['Website']
    
    return (ATP_df)

def overview_scraper(sites):
    
    """
    Should be run in conjunction with with rankings_scraper,
    as it assumes that the sites given to it are from the ATP rankings.
    
    Outputs all information from the player overview page in a DataFrame
    Year turned pro, weight, height, brith place, current residence,
    right vs left hand, type of backhand used, and coach
    """
    
    turned_pro = []
    weights = []
    heights = []
    birth_places = []
    residences = []
    hands = []
    backhands = []
    coaches = []

    for site in sites: #Might be worthwhile finding a way to scrape multiple sites simultaneously
        
       
        urlpage= site
        request = Request(urlpage,headers={'User-Agent':'Mozilla/5.0'})
        webpage = urlopen(request).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        
        main = soup.find_all('div',attrs={'class':'inner-wrap'})[1]
        
        turned_pro_year = main.find_all('div', attrs={'class':'table-big-value'})[1].getText()    
        weight = main.find('span', attrs={'class':'table-weight-kg-wrapper'}).getText().strip('()kg')
        height = main.find('span', attrs={'class':'table-height-cm-wrapper'}).getText().strip('()cm')
        main_row_2 = main.find_all('div', attrs={'class':'table-value'})
        birth_place = main_row_2[0].getText().replace('\r','').replace('\n','').strip()
        residence = main_row_2[1].getText().replace('\r','').replace('\n','').strip()
        handedness, backhand = main_row_2[2].getText().replace('\r','').replace('\n','').strip().split(',')
        backhand = backhand.strip()
        coach = main_row_2[3].getText().replace('\r','').replace('\n','').strip()
        
        turned_pro.append(int(turned_pro_year))
        weights.append(int(weight))
        heights.append(int(height))
        birth_places.append(birth_place)
        residences.append(residence)
        hands.append(handedness)
        backhands.append(backhand)
        coaches.append(coach)
    
    overview_df = pd.DataFrame({
            'Turned_pro':turned_pro,
            'Weight':weights,
            'Height':heights,
            'Birth_place':birth_places,
            'Residences':residences,
            'Handedness':handedness,
            'Backhand':backhands,
            'Coach':coaches
            })
    
    return(overview_df)
