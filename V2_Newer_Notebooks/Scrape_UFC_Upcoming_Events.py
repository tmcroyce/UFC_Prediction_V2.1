# Load Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sqlite3
import seaborn as sns
from matplotlib.pyplot import figure
from bs4 import BeautifulSoup
import time
import requests     # to get images
import shutil       # to save files locally
import datetime
from scipy.stats import norm
import warnings
warnings.filterwarnings('ignore')
from random import randint
import  random
import os
os.chdir('/Users/travisroyce/Library/CloudStorage/OneDrive-Personal/Data Science/Personal_Projects/Sports/UFC_Prediction_V2/')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cmath import nan
import urllib
import urllib.request
import re
import time


def get_next_events(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # get events
    event1 = soup.find('div', class_='c-card-event--result__info')
    event1_txt = soup.find('div', class_='c-card-event--result__info').text
    event1_url = event1.find('a')['href']
    event1_url = 'https://www.ufc.com' + event1_url
    event1_title = event1_txt.split('\n')[1]
    event1_time = event1_txt.split('/')[1]

    data = pd.DataFrame({'event_title': [event1_title], 'event_url': [event1_url], 'event_date': [event1_time]})

    event2 = soup.find('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info')
    event2_txt = soup.find('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info').text
    event2_url = event2.find('a')['href']
    event2_url = 'https://www.ufc.com' + event2_url
    event2_title = event2_txt.split('\n')[1]
    event2_time = event2_txt.split('/')[1]


    data = data.append({'event_title': event2_title, 'event_url': event2_url, 'event_date': event2_time}, ignore_index=True)
    
    event3 = soup.find('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info')
    event3_txt = soup.find('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info').text
    event3_url = event3.find('a')['href']
    event3_url = 'https://www.ufc.com' + event3_url
    event3_title = event3_txt.split('\n')[1]
    event3_time = event3_txt.split('/')[1]

    data = data.append({'event_title': event3_title, 'event_url': event3_url, 'event_date': event3_time}, ignore_index=True)
    
    return data

# Function to get the fight card for a given event using BeautifulSoup
def get_event_fights(event_url):
    page = requests.get(event_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # get main card, fight 1

    mcn = soup.find_all('li', class_='l-listing__item')
    # get num of mc
    num_mc = len(mcn)
    # for each mc, do the following
    data = pd.DataFrame()
    n = 0
    for i in mcn:
        mc = mcn[n]
        # fight 1
        fighter1= mc.find('div', class_ ='c-listing-fight__corner-name c-listing-fight__corner-name--red').text
        fighter1 = fighter1.replace('\n', ' ')
        fighter1 = fighter1.strip()
        fighter2 = mc.find('div', class_ ='c-listing-fight__corner-name c-listing-fight__corner-name--blue').text
        fighter2 = fighter2.replace('\n', ' ')
        fighter2 = fighter2.strip()
        weightclass = mc.find('div', class_='c-listing-fight__class-text').text
        fighter1_odds = mc.find('span', class_='c-listing-fight__odds').text
        fighter2_odds = mc.find('span', class_='c-listing-fight__odds').find_next('span', class_='c-listing-fight__odds').text
        fighter1_odds = fighter1_odds.replace('\n', '')
        fighter2_odds = fighter2_odds.replace('\n', '')
        # fighter odds to float
        if (fighter1_odds == '-') :
            fighter1_odds = nan
        if (fighter2_odds == '-') :
            fighter2_odds = nan

        data = data.append({'fighter1': fighter1, 'fighter2': fighter2, 'weightclass': weightclass, 
                            'fighter1_odds': fighter1_odds, 'fighter2_odds': fighter2_odds}, ignore_index=True)
        n = n + 1
    return data

# Find secret number in ufc events using BS & Selenium
def secret_number(event_url):
    # if no driver open, open one
    driver = None
    if (driver == None):
        driver = webdriver.Chrome('C:\\Users\\Travis\\OneDrive\\Data Science\\Personal_Projects\\Sports\\UFC_Prediction_V2\\chromedriver.exe')
    else:
        driver = driver
    
    driver.get(event_url)
    time.sleep(3)
    # click the first matchup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pretty = soup.prettify()
    # find first data-fmid to get first matchup
    fmid_start = pretty.find('data-fmid')
    fmid = pretty[fmid_start+11:fmid_start+16]
    driver.get(event_url +'#' + fmid)
    time.sleep(6)
    # find all links within page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # find all iframe src
    iframe = soup.find_all('iframe')
    # find all links
    iframe_text = str(iframe)
    matchup = iframe_text.find('matchup')
    matchup_url = iframe_text[matchup+8:matchup+12]
    print('matchup_url: ' + matchup_url)
    secret_number = matchup_url
    return matchup

# get next events if event fighter data is not na
def get_next_events2(url):
    data = get_next_events(url)
    for i in range(0, len(data)):
        event_url = data['event_url'][i]
        event_fights = get_event_fights(event_url)
        if (len(event_fights) == 0):
            data = data.drop(i)
    return data

# get next events from UFCStats.com using BS
def get_next_event_ufcstats():
    url = 'http://www.ufcstats.com/statistics/events/upcoming'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # get events
    event1 = soup.find('td', class_='b-statistics__table-col')
    event1_txt = soup.find('td', class_='b-statistics__table-col').text
    event_txt = event1_txt.replace('   ', '').replace('\n', '').strip()
    event_title = event_txt.split('  ')[0]
    event_date = event_txt.split('  ')[1]
    event1_url = event1.find('a')['href']
    data = pd.DataFrame({'event_title': [event_title], 'event_url': [event1_url], 'event_date': [event_date]})
    return data


# get fighter urls from UFCStats.com using BS
def get_fighter_urls(event_details_url):
    page = requests.get(event_details_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # get events
    events = soup.find_all('tr', class_='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click')
    n = 0
    next_event_data = pd.DataFrame()

    for event in events:
        fighters = events[n].find_all('p', class_='b-fight-details__table-text')
        fighter1 = fighters[0].text
        fighter1 = fighter1.replace('  ', '').replace('\n', '').strip()
        fighter2 = fighters[1].text
        fighter2 = fighter2.replace('  ', '').replace('\n', '').strip()
        fighter1_url = fighters[0].find('a')['href']
        fighter2_url = fighters[1].find('a')['href']
        next_event_data = next_event_data.append({'fighter1' :fighter1, 'fighter2:' : fighter2, 'fighter1_url': fighter1_url, 'fighter2_url':fighter2_url, 'fight#' : n+1}, ignore_index = True)
        n += 1

    return next_event_data

next_events = get_next_events2('https://www.ufc.com/events')

event_url =  next_events['event_url'][0]
next_event_title = next_events['event_title'][0]
next_event = get_event_fights(event_url)

page = requests.get(event_url)
soup = BeautifulSoup(page.content, 'html.parser')
h = soup.find_all('div', class_='c-listing-fight')

data_fmid = []
for i in h:
    data_fmid.append(i['data-fmid'])

next_event['fight_number'] = data_fmid[:len(next_event)]
next_event['matchup_url'] = event_url +'#' + next_event['fight_number'].astype(str)


def find_all_iframe_sources(matchup_url):
    try:
        driver = webdriver.Chrome('/Users/travisroyce/Library/CloudStorage/OneDrive-Personal/Data Science/Personal_Projects/Sports/UFC_Prediction_V2/V2_Newer_Notebooks/chromedriver')
        driver.get(matchup_url)
        time.sleep(3)
        # get innerhtml
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pretty = soup.prettify()
        # find all links within page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # find all iframe src
        iframe = soup.find_all('iframe')
        # list all links
        iframe_text = str(iframe)
        # separate links
        iframe_text = iframe_text.split('src="')
        iframe_text = iframe_text[1:]
        iframe_text = [i.split('"')[0] for i in iframe_text]
        # only keep links that contain matchup
        iframe_text = [i for i in iframe_text if 'matchup' in i]
        # only keep top link
        iframe_text = iframe_text[0]
        
        return iframe_text
    except:
        return 'error'


# add iframe sources to df  with itterrows and apply
next_event['iframe_src'] = next_event.apply(lambda x: find_all_iframe_sources(x['matchup_url']), axis=1)

next_event['full_iframe_src'] = 'https://www.ufc.com' + next_event['iframe_src']

def get_iframe_src_data_2(iframe_src):
    iframe_response = requests.get(iframe_src)
    iframe_soup = BeautifulSoup(iframe_response.content, 'html.parser')
    # get all c-stat-compare__group-1 red
    red = iframe_soup.find_all('div', class_='c-stat-compare__group-1 red')
    # return all red texts
    red_text = [i.text for i in red]
    # assign to variables
    red_record = red_text[0]
    red_last_fight = red_text[1]
    red_country = red_text[2]
    red_height = red_text[3]
    red_weight = red_text[4]
    red_reach = red_text[5]
    red_legreach = red_text[6]
    red_win_by_ko_percent = red_text[7]
    red_win_by_sub_percent = red_text[8]
    red_win_by_dec_percent = red_text[9]
    red_avg_fight_time = red_text[10]
    red_knockdowns_per_15_min = red_text[11]
    # sig strikes
    red_sig_strikes_landed_per_min = red_text[12]
    red_sig_strikes_percent = red_text[13]
    red_sig_strikes_absorbed_per_min = red_text[14]
    red_sig_strikes_absorbed_percent = red_text[15]
    # grappling
    red_takedowns_landed_per_15_min = red_text[16]
    red_takedown_accuracy = red_text[17]
    red_takedown_defense = red_text[18]
    red_submissions_attempts_per_15_min = red_text[19]
    # odds
    red_moneyline = red_text[20]


    # make df for red
    red_df = pd.DataFrame({'red_record': red_record, 'red_last_fight': red_last_fight, 
                            'red_country': red_country, 'red_height': red_height, 'red_weight': red_weight, 
                            'red_reach': red_reach, 'red_legreach': red_legreach, 
                            'red_win_by_ko_percent': red_win_by_ko_percent, 
                            'red_win_by_sub_percent': red_win_by_sub_percent, 'red_win_by_dec_percent': red_win_by_dec_percent, 
                            'red_avg_fight_time': red_avg_fight_time, 'red_knockdowns_per_15_min': red_knockdowns_per_15_min, 
                            'red_sig_strikes_landed_per_min': red_sig_strikes_landed_per_min, 
                            'red_sig_strikes_percent': red_sig_strikes_percent, 
                            'red_sig_strikes_absorbed_per_min': red_sig_strikes_absorbed_per_min, 
                            'red_sig_strikes_absorbed_percent': red_sig_strikes_absorbed_percent, 
                            'red_takedowns_landed_per_15_min': red_takedowns_landed_per_15_min, 
                            'red_takedown_accuracy': red_takedown_accuracy, 'red_takedown_defense': red_takedown_defense, 
                            'red_submissions_attempts_per_15_min': red_submissions_attempts_per_15_min, 
                            'red_moneyline': red_moneyline}, index=[0])

    # clean all values in red_df, removing all \n 
    red_df = red_df.applymap(lambda x: x.replace('\n', ''))
    # strip all values in red_df
    red_df = red_df.applymap(lambda x: x.strip())

    # get all c-stat-compare__group-1 blue
    blue = iframe_soup.find_all('div', class_='c-stat-compare__group-2 blue')
    # return all blue texts
    blue_text = [i.text for i in blue]
    # assign to variables
    blue_record = blue_text[0]
    blue_last_fight = blue_text[1]
    blue_country = blue_text[2]
    blue_height = blue_text[3]
    blue_weight = blue_text[4]
    blue_reach = blue_text[5]
    blue_legreach = blue_text[6]
    blue_win_by_ko_percent = blue_text[7]
    blue_win_by_sub_percent = blue_text[8]
    blue_win_by_dec_percent = blue_text[9]
    blue_avg_fight_time = blue_text[10]
    blue_knockdowns_per_15_min = blue_text[11]
    # sig strikes
    blue_sig_strikes_landed_per_min = blue_text[12]
    blue_sig_strikes_percent = blue_text[13]
    blue_sig_strikes_absorbed_per_min = blue_text[14]
    blue_sig_strikes_absorbed_percent = blue_text[15]
    # grappling
    blue_takedowns_landed_per_15_min = blue_text[16]
    blue_takedown_accuracy = blue_text[17]
    blue_takedown_defense = blue_text[18]
    blue_submissions_attempts_per_15_min = blue_text[19]
    # odds
    blue_moneyline = blue_text[20]


    # make df for blue
    blue_df = pd.DataFrame({'blue_record': blue_record, 'blue_last_fight': blue_last_fight,
                            'blue_country': blue_country, 'blue_height': blue_height, 'blue_weight': blue_weight,
                            'blue_reach': blue_reach, 'blue_legreach': blue_legreach,
                            'blue_win_by_ko_percent': blue_win_by_ko_percent,
                            'blue_win_by_sub_percent': blue_win_by_sub_percent, 'blue_win_by_dec_percent': blue_win_by_dec_percent,
                            'blue_avg_fight_time': blue_avg_fight_time, 'blue_knockdowns_per_15_min': blue_knockdowns_per_15_min,
                            'blue_sig_strikes_landed_per_min': blue_sig_strikes_landed_per_min,
                            'blue_sig_strikes_percent': blue_sig_strikes_percent,
                            'blue_sig_strikes_absorbed_per_min': blue_sig_strikes_absorbed_per_min,
                            'blue_sig_strikes_absorbed_percent': blue_sig_strikes_absorbed_percent,
                            'blue_takedowns_landed_per_15_min': blue_takedowns_landed_per_15_min,
                            'blue_takedown_accuracy': blue_takedown_accuracy, 'blue_takedown_defense': blue_takedown_defense,
                            'blue_submissions_attempts_per_15_min': blue_submissions_attempts_per_15_min,
                            'blue_moneyline': blue_moneyline}, index=[0])

    # clean all values in blue_df, removing all \n
    blue_df = blue_df.applymap(lambda x: x.replace('\n', ''))
    # strip all values in blue_df
    blue_df = blue_df.applymap(lambda x: x.strip())


    # append blue_df to red_df by axis=1
    dfs = pd.concat([red_df, blue_df], axis=1)

    # return df
    return dfs


rand_iframe_src = next_event['full_iframe_src'][1]

# get iframe src data for all events

event_data = []

for i in range(len(next_event['full_iframe_src'])):
    try:
        event_data.append(get_iframe_src_data_2(next_event['full_iframe_src'][i]))
    except:
        event_data.append(pd.DataFrame([{'error': 'error'}]))

# make df from event_data
event_data_df = pd.concat(event_data, axis=0)

# reindex both
next_event = next_event.reset_index(drop=True)
event_data_df = event_data_df.reset_index(drop=True)

# Append event_data_df to next_event
next_event = pd.concat([next_event, event_data_df], axis=1)

next_event.to_csv('data/final/next_fights/'+ next_event_title +'_.csv', index=False)
