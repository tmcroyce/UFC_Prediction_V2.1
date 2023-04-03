# cd OneDrive/Data Science/Personal_Projects/Sports/UFC_Prediction/notebooks/final_notebooks
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
#os.chdir('C:/Users/tmcro/OneDrive/Data Science/Personal_Projects/Sports/UFC_Prediction')
from cmath import nan
from bs4 import BeautifulSoup
import streamlit as st
import pickle
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


home = 'C:/Users/Travis/OneDrive/Data Science/Personal_Projects/Sports/UFC_Prediction_V2/data/'
home2 = 'C:/Users/Travis/OneDrive/Data Science/Personal_Projects/Sports/UFC_Prediction_V2/'
os.chdir(home)

#------------------------------  Define Functions -----------------------------------------------------------------
# function to return the next 3 UFC events using BeautifulSoup
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


# check if it is a saturday
def is_saturday():
    today = str(datetime.today().weekday())
    if today == '5':
        return True
    else:
        return False

# if it is a saturday, get the current event, otherwise, get the next event

# Get next event from ufcstats.com
next_eventz = get_next_event_ufcstats()


##########           DATA        ################

data = pd.read_csv(home + '/final/aggregates/Double_Fights_DF_V14.csv')

##########           GET EVENTS       ################

# make sure events have fight info. If not, disregard that event
next = get_next_events2('https://www.ufc.com/events')

########           Select Next Event    ################

event = st.sidebar.selectbox('Select Event', next['event_title'])
selected_event = event
event_url =  next['event_url'][next['event_title'] == selected_event].values[0]
selected_event_secret_number = secret_number(event_url)

next_event = get_event_fights(event_url)
fight = st.sidebar.selectbox('Select Fight', next_event['fighter1'] + ' vs. ' + next_event['fighter2'])

## Get Names ##

selected_fighter_1 = fight.split(' vs. ')[0]
selected_fighter_2 = fight.split(' vs. ')[1].strip()


########          Scrape UFC.com Data    ################

# get the matchup fight numbers

page = requests.get(event_url)
soup = BeautifulSoup(page.content, 'html.parser')
h = soup.find_all('div', class_='c-listing-fight')

data_fmid = []
for i in h:
    data_fmid.append(i['data-fmid'])

next_event['fight_number'] = data_fmid[:len(next_event)]
next_event['matchup_url'] = event_url +'#' + next_event['fight_number'].astype(str)
selected_matchup_url = next_event['matchup_url'][next_event['fighter1'] == selected_fighter_1].values[0]

st.write(' FOR EDIT -- selected_matchup_url: ' + selected_matchup_url)

# Function to scrape UFC fight data
def grab_matchup_data(matchup_url):
    response = requests.get(matchup_url)
    soup = BeautifulSoup(response.text, 'html.parser').text
    soup = soup.replace('   ', '').replace('\n', '')

    od = soup.find('Odds')
    rec = soup.find('Record')
    a_record = soup[od + 5 : rec - 2]
    last_fight = soup.find("Last Fight")
    b_record = soup[rec + 7 : last_fight - 5]

    hite = soup.find('Height')
    f = soup.find("' ")
    a_height = soup[f -1 : hite - 2]
    # find second occurance of f
    f2 = soup.find("' ", f + 1)
    b_height = soup[hite + 7 : f2+5]

    # Find reach
    reach = soup.find('Reach')
    # find second occurance of "LB"
    lb = soup.find('LB')
    lb2 = soup.find('LB', lb + 1)
    a_reach = soup[lb2 +5 : reach ]
    inn = soup.find("in ")
    # get the word after reach
    big_space = soup.find('  ', reach + 1)
    b_reach = soup[reach + 6 : big_space]

    # Find Leg Reach
    leg = soup.find('Leg Reach')
    big_space2 = soup.find('  ', big_space + 1)
    a_leg = soup[big_space2 + 2 : leg]
    big_space4 = soup.find('  ', big_space2 + 2)
    b_leg = soup[leg + 10 : leg + 17]

    a_record = a_record.strip()
    b_record = b_record.strip()

    a_height_ft = float(a_height[:1])
    a_height_in = float(a_height[3:].replace("'", "").replace('"', ''))
    a_height = (a_height_ft * 12) + a_height_in 


    b_height_ft = float(b_height[:1])
    b_height_in = float(b_height[3:].replace("'", "").replace('"', ''))
    b_height = (b_height_ft * 12) + b_height_in

    a_reach = float(a_reach.replace(' in', '').strip())
    b_reach = float(b_reach.replace(' in', '').strip())

    a_leg = float(a_leg.replace(' in', '').strip())
    b_leg = float(b_leg.replace(' in', '').strip())

    
    return a_record, b_record, a_height, b_height, a_reach, b_reach, a_leg, b_leg

url = 'https://www.ufc.com/matchup/' + str(selected_event_secret_number) + '/' + next_event[next_event['fighter1'] == selected_fighter_1]['fight_number'].values[0]

st.write('ufc_matchup_url_xtra: ' + url)

a_record, b_record, a_height, b_height, a_reach, b_reach, a_leg, b_leg = grab_matchup_data(url)


##########     Get Fighter Info      ############# 

# GET PICTURE URLS
# fighter1_pic_url = "ufc.com/athlete/" + selected_fighter_1.replace(' ', '-').lower()
# fighter2_pic_url = "ufc.com/athlete/" + selected_fighter_2.replace(' ', '-').lower()


# # SCRAPE PICTURES FROM UFC.COM
# def get_info(url):
#     page = requests.get(url)
#     return page.text

# pagedata = get_info('https://' + fighter1_pic_url)
# soup = BeautifulSoup(pagedata, 'html.parser')
# fighter1_pic_url = soup.find('img', class_='hero-profile__image')['src']

# page2data = get_info('https://' + fighter2_pic_url)
# soup2 = BeautifulSoup(page2data, 'html.parser')
# fighter2_pic_url = soup2.find('img', class_='hero-profile__image')['src']



def get_fighter_pic_url(selected_matchup_url, fighter_choice):
    fighter_last_name1 = selected_fighter_1.split(' ')[1]
    fighter_last_name1 = fighter_last_name1.upper()

    fighter_last_name2 = selected_fighter_2.split(' ')[1]
    fighter_last_name2 = fighter_last_name2.upper()
    driver = None
    if driver == None:
        driver = webdriver.Chrome('C:\\Users\\Travis\\OneDrive\\Data Science\\Personal_Projects\\Sports\\UFC_Prediction_V2\\chromedriver.exe')
    driver.get(selected_matchup_url)
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    h = soup.find_all('img')
    imgs = []
    for i in h:
        imgs.append(i['src'])

    # keep imgs with full_body
    imgs = [i for i in imgs if 'full_body' in i]

    fighter_img1 = [i for i in imgs if fighter_last_name1 in i][0]
    fighter_img1 = fighter_img1.replace('athlete_detail_stance_thumbnail_full_body', 'athlete_matchup_stats_full_body')
    # end fighter_img at .png
    fighter_img1 = fighter_img1[:fighter_img1.find('.png') + 4]

    fighter_img2 = [i for i in imgs if fighter_last_name2 in i][0]
    fighter_img2 = fighter_img2.replace('athlete_detail_stance_thumbnail_full_body', 'athlete_matchup_stats_full_body')
    # end fighter_img at .png
    fighter_img2 = fighter_img2[:fighter_img2.find('.png') + 4]
    if fighter_choice == 1:
        return fighter_img1
    else:
        return fighter_img2

fighter1_img = get_fighter_pic_url(selected_matchup_url, fighter_choice=1)
fighter2_img = get_fighter_pic_url(selected_matchup_url, fighter_choice=2)

################ FIGHTER INFO ####################


st.header('UFC Fight Prediction')
st.write('Choose a fight from the sidebar to see the prediction.')

f1 = data[data['Fighter_A'] == selected_fighter_1]
f2 = data[data['Fighter_A'] == selected_fighter_2]

# transpose f1
cols = ['Fighter_A', 'A_Height', 'A_Reach', 'A_Leg_Reach']
f11 = f1[cols].reset_index().drop(['index'], axis=1)
# rename columns
f11.columns = ['Fighter', 'Height', 'Reach', 'Leg_Reach']
f22 = f2[cols].reset_index().drop(['index'], axis=1)
f22.columns = ['Fighter', 'Height', 'Reach', 'Leg_Reach']


# function to convert vegas odds to implied probability
def odds_to_prob(odds):
    odds = float(odds)
    if (odds > 0):
        prob = round(1/(odds/100 + 1),3) * 100
        prob = str(round(prob, 3)) + '%'
        return prob
    else:
        prob = round(1 - 1/(-odds/100 + 1),3)*100
        prob = str(round(prob, 3)) + '%'
        return prob

# Assign Height and Length Values
try:
    dif = a_height - b_height
    dif2 = a_reach - b_reach
    dif3 = a_leg - b_leg


    col1, col2 = st.columns(2)
    with col1:
        st.subheader(selected_fighter_1)
        st.image(fighter1_img, height = 500, use_column_width=True)
        st.metric(label = 'Vegas Odds', value=next_event['fighter1_odds'][next_event['fighter1'] == selected_fighter_1].values[0])
        st.metric(label = 'Odds-Implied Probability', 
                    value=odds_to_prob(next_event['fighter1_odds'][next_event['fighter1'] == selected_fighter_1].values[0]))
        st.metric(label = 'Height', value=a_height, delta = dif)
        st.metric(label = 'Reach', value=a_reach, delta = dif2)
        st.metric(label = 'Leg Reach', value=a_leg, delta = dif3)

    with col2:
        st.subheader(selected_fighter_2)
        st.image(fighter2_img, height = 500, use_column_width=True)
        st.metric(label = 'Vegas Odds', value=next_event['fighter2_odds'][next_event['fighter2'] == selected_fighter_2].values[0])
        st.metric(label = 'Odds-Implied Probability', 
                    value=odds_to_prob(next_event['fighter2_odds'][next_event['fighter2'] == selected_fighter_2].values[0]))
        st.metric(label = 'Height', value=b_height, delta = -dif)
        st.metric(label = 'Reach', value=b_reach, delta = -dif2)
        st.metric(label = 'Leg Reach', value=b_leg, delta = -dif3)
except: 
    st.markdown('THERES A PROBLEM WITH ONE OF THE FIGHTERS GIVEN METRICS... CALL CUSTOMER SUPPORT OR SOMETHING')


st.write(next_eventz)

next_eventz['event_date'] = pd.to_datetime(next_eventz['event_date']).dt.date
d_o_e = next_eventz['event_date'].values[0]
doe = d_o_e.strftime('%Y-%m-%d')
# if fight is today
today = datetime.today().strftime('%Y-%m-%d')

fighter_urls = get_fighter_urls(next_eventz['event_url'].values[0])

#
nfd = pd.read_csv(home + 'final/next_fights/'+ doe + '.csv')
#replace na with 0
nfd.fillna(0, inplace=True)



next_fight_df = nfd
next_fight_df = next_fight_df.fillna(0)
this_fight_df= next_fight_df[next_fight_df['Fighter_A'] == selected_fighter_1]


# put columns in proper order
proper_order = ['Fighter_A_Odds',
 'Fighter_B_Odds',
 'Fighter_A_Odds_Change',
 'Fighter_B_Odds_Change',
 'Dif_Odds',
 'A_Rolling_Kd_mean',
 'B_Rolling_Kd_mean',
 'A_Rolling_Kd_std',
 'B_Rolling_Kd_std',
 'A_Rolling_Kd_median',
 'B_Rolling_Kd_median',
 'A_Rolling_Sig_strike_land_mean',
 'B_Rolling_Sig_strike_land_mean',
 'A_Rolling_Sig_strike_land_std',
 'B_Rolling_Sig_strike_land_std',
 'A_Rolling_Sig_strike_land_median',
 'B_Rolling_Sig_strike_land_median',
 'A_Rolling_Sig_strike_att_mean',
 'B_Rolling_Sig_strike_att_mean',
 'A_Rolling_Sig_strike_att_std',
 'B_Rolling_Sig_strike_att_std',
 'A_Rolling_Sig_strike_att_median',
 'B_Rolling_Sig_strike_att_median',
 'A_Rolling_Sig_strike_percent_mean',
 'B_Rolling_Sig_strike_percent_mean',
 'A_Rolling_Sig_strike_percent_std',
 'B_Rolling_Sig_strike_percent_std',
 'A_Rolling_Sig_strike_percent_median',
 'B_Rolling_Sig_strike_percent_median',
 'A_Rolling_Total_Strikes_land_mean',
 'B_Rolling_Total_Strikes_land_mean',
 'A_Rolling_Total_Strikes_land_std',
 'B_Rolling_Total_Strikes_land_std',
 'A_Rolling_Total_Strikes_land_median',
 'B_Rolling_Total_Strikes_land_median',
 'A_Rolling_Total_Strikes_att_mean',
 'B_Rolling_Total_Strikes_att_mean',
 'A_Rolling_Total_Strikes_att_std',
 'B_Rolling_Total_Strikes_att_std',
 'A_Rolling_Total_Strikes_att_median',
 'B_Rolling_Total_Strikes_att_median',
 'A_Rolling_Total_Strikes_percent_mean',
 'B_Rolling_Total_Strikes_percent_mean',
 'A_Rolling_Total_Strikes_percent_std',
 'B_Rolling_Total_Strikes_percent_std',
 'A_Rolling_Total_Strikes_percent_median',
 'B_Rolling_Total_Strikes_percent_median',
 'A_Rolling_Takedowns_land_mean',
 'B_Rolling_Takedowns_land_mean',
 'A_Rolling_Takedowns_land_std',
 'B_Rolling_Takedowns_land_std',
 'A_Rolling_Takedowns_land_median',
 'B_Rolling_Takedowns_land_median',
 'A_Rolling_Takedowns_att_mean',
 'B_Rolling_Takedowns_att_mean',
 'A_Rolling_Takedowns_att_std',
 'B_Rolling_Takedowns_att_std',
 'A_Rolling_Takedowns_att_median',
 'B_Rolling_Takedowns_att_median',
 'A_Rolling_Takedown_percent_mean',
 'B_Rolling_Takedown_percent_mean',
 'A_Rolling_Takedown_percent_std',
 'B_Rolling_Takedown_percent_std',
 'A_Rolling_Takedown_percent_median',
 'B_Rolling_Takedown_percent_median',
 'A_Rolling_Sub_Attempts_land_mean',
 'B_Rolling_Sub_Attempts_land_mean',
 'A_Rolling_Sub_Attempts_land_std',
 'B_Rolling_Sub_Attempts_land_std',
 'A_Rolling_Sub_Attempts_land_median',
 'B_Rolling_Sub_Attempts_land_median',
 'A_Rolling_Sub_Attempts_att_mean',
 'B_Rolling_Sub_Attempts_att_mean',
 'A_Rolling_Sub_Attempts_att_std',
 'B_Rolling_Sub_Attempts_att_std',
 'A_Rolling_Sub_Attempts_att_median',
 'B_Rolling_Sub_Attempts_att_median',
 'A_Rolling_Rev_mean',
 'B_Rolling_Rev_mean',
 'A_Rolling_Rev_std',
 'B_Rolling_Rev_std',
 'A_Rolling_Rev_median',
 'B_Rolling_Rev_median',
 'A_Rolling_Ctrl_time_min_mean',
 'B_Rolling_Ctrl_time_min_mean',
 'A_Rolling_Ctrl_time_min_std',
 'B_Rolling_Ctrl_time_min_std',
 'A_Rolling_Ctrl_time_min_median',
 'B_Rolling_Ctrl_time_min_median',
 'A_Rolling_Ctrl_time_sec_mean',
 'B_Rolling_Ctrl_time_sec_mean',
 'A_Rolling_Ctrl_time_sec_std',
 'B_Rolling_Ctrl_time_sec_std',
 'A_Rolling_Ctrl_time_sec_median',
 'B_Rolling_Ctrl_time_sec_median',
 'A_Rolling_Ctrl_time_tot_mean',
 'B_Rolling_Ctrl_time_tot_mean',
 'A_Rolling_Ctrl_time_tot_std',
 'B_Rolling_Ctrl_time_tot_std',
 'A_Rolling_Ctrl_time_tot_median',
 'B_Rolling_Ctrl_time_tot_median',
 'A_Rolling_Head_Strikes_land_mean',
 'B_Rolling_Head_Strikes_land_mean',
 'A_Rolling_Head_Strikes_land_std',
 'B_Rolling_Head_Strikes_land_std',
 'A_Rolling_Head_Strikes_land_median',
 'B_Rolling_Head_Strikes_land_median',
 'A_Rolling_Head_Strikes_att_mean',
 'B_Rolling_Head_Strikes_att_mean',
 'A_Rolling_Head_Strikes_att_std',
 'B_Rolling_Head_Strikes_att_std',
 'A_Rolling_Head_Strikes_att_median',
 'B_Rolling_Head_Strikes_att_median',
 'A_Rolling_Head_Strikes_percent_mean',
 'B_Rolling_Head_Strikes_percent_mean',
 'A_Rolling_Head_Strikes_percent_std',
 'B_Rolling_Head_Strikes_percent_std',
 'A_Rolling_Head_Strikes_percent_median',
 'B_Rolling_Head_Strikes_percent_median',
 'A_Rolling_Body_Strikes_land_mean',
 'B_Rolling_Body_Strikes_land_mean',
 'A_Rolling_Body_Strikes_land_std',
 'B_Rolling_Body_Strikes_land_std',
 'A_Rolling_Body_Strikes_land_median',
 'B_Rolling_Body_Strikes_land_median',
 'A_Rolling_Body_Strikes_att_mean',
 'B_Rolling_Body_Strikes_att_mean',
 'A_Rolling_Body_Strikes_att_std',
 'B_Rolling_Body_Strikes_att_std',
 'A_Rolling_Body_Strikes_att_median',
 'B_Rolling_Body_Strikes_att_median',
 'A_Rolling_Body_Strikes_percent_mean',
 'B_Rolling_Body_Strikes_percent_mean',
 'A_Rolling_Body_Strikes_percent_std',
 'B_Rolling_Body_Strikes_percent_std',
 'A_Rolling_Body_Strikes_percent_median',
 'B_Rolling_Body_Strikes_percent_median',
 'A_Rolling_Leg_Strikes_land_mean',
 'B_Rolling_Leg_Strikes_land_mean',
 'A_Rolling_Leg_Strikes_land_std',
 'B_Rolling_Leg_Strikes_land_std',
 'A_Rolling_Leg_Strikes_land_median',
 'B_Rolling_Leg_Strikes_land_median',
 'A_Rolling_Leg_Strikes_att_mean',
 'B_Rolling_Leg_Strikes_att_mean',
 'A_Rolling_Leg_Strikes_att_std',
 'B_Rolling_Leg_Strikes_att_std',
 'A_Rolling_Leg_Strikes_att_median',
 'B_Rolling_Leg_Strikes_att_median',
 'A_Rolling_Leg_Strikes_percent_mean',
 'B_Rolling_Leg_Strikes_percent_mean',
 'A_Rolling_Leg_Strikes_percent_std',
 'B_Rolling_Leg_Strikes_percent_std',
 'A_Rolling_Leg_Strikes_percent_median',
 'B_Rolling_Leg_Strikes_percent_median',
 'A_Rolling_Distance_Strikes_land_mean',
 'B_Rolling_Distance_Strikes_land_mean',
 'A_Rolling_Distance_Strikes_land_std',
 'B_Rolling_Distance_Strikes_land_std',
 'A_Rolling_Distance_Strikes_land_median',
 'B_Rolling_Distance_Strikes_land_median',
 'A_Rolling_Distance_Strikes_att_mean',
 'B_Rolling_Distance_Strikes_att_mean',
 'A_Rolling_Distance_Strikes_att_std',
 'B_Rolling_Distance_Strikes_att_std',
 'A_Rolling_Distance_Strikes_att_median',
 'B_Rolling_Distance_Strikes_att_median',
 'A_Rolling_Distance_Strikes_percent_mean',
 'B_Rolling_Distance_Strikes_percent_mean',
 'A_Rolling_Distance_Strikes_percent_std',
 'B_Rolling_Distance_Strikes_percent_std',
 'A_Rolling_Distance_Strikes_percent_median',
 'B_Rolling_Distance_Strikes_percent_median',
 'A_Rolling_Clinch_Strikes_land_mean',
 'B_Rolling_Clinch_Strikes_land_mean',
 'A_Rolling_Clinch_Strikes_land_std',
 'B_Rolling_Clinch_Strikes_land_std',
 'A_Rolling_Clinch_Strikes_land_median',
 'B_Rolling_Clinch_Strikes_land_median',
 'A_Rolling_Clinch_Strikes_att_mean',
 'B_Rolling_Clinch_Strikes_att_mean',
 'A_Rolling_Clinch_Strikes_att_std',
 'B_Rolling_Clinch_Strikes_att_std',
 'A_Rolling_Clinch_Strikes_att_median',
 'B_Rolling_Clinch_Strikes_att_median',
 'A_Rolling_Clinch_Strikes_percent_mean',
 'B_Rolling_Clinch_Strikes_percent_mean',
 'A_Rolling_Clinch_Strikes_percent_std',
 'B_Rolling_Clinch_Strikes_percent_std',
 'A_Rolling_Clinch_Strikes_percent_median',
 'B_Rolling_Clinch_Strikes_percent_median',
 'A_Rolling_Ground_Strikes_land_mean',
 'B_Rolling_Ground_Strikes_land_mean',
 'A_Rolling_Ground_Strikes_land_std',
 'B_Rolling_Ground_Strikes_land_std',
 'A_Rolling_Ground_Strikes_land_median',
 'B_Rolling_Ground_Strikes_land_median',
 'A_Rolling_Ground_Strikes_att_mean',
 'B_Rolling_Ground_Strikes_att_mean',
 'A_Rolling_Ground_Strikes_att_std',
 'B_Rolling_Ground_Strikes_att_std',
 'A_Rolling_Ground_Strikes_att_median',
 'B_Rolling_Ground_Strikes_att_median',
 'A_Rolling_Ground_Strikes_percent_mean',
 'B_Rolling_Ground_Strikes_percent_mean',
 'A_Rolling_Ground_Strikes_percent_std',
 'B_Rolling_Ground_Strikes_percent_std',
 'A_Rolling_Ground_Strikes_percent_median',
 'B_Rolling_Ground_Strikes_percent_median',
 'A_topdown_Avg_Kd',
 'B_topdown_Avg_Kd',
 'A_topdown_Avg_Sig_strike_land',
 'B_topdown_Avg_Sig_strike_land',
 'A_topdown_Avg_Sig_strike_att',
 'B_topdown_Avg_Sig_strike_att',
 'A_topdown_Avg_Sig_strike_percent',
 'B_topdown_Avg_Sig_strike_percent',
 'A_topdown_Avg_Total_Strikes_land',
 'B_topdown_Avg_Total_Strikes_land',
 'A_topdown_Avg_Total_Strikes_att',
 'B_topdown_Avg_Total_Strikes_att',
 'A_topdown_Avg_Total_Strikes_percent',
 'B_topdown_Avg_Total_Strikes_percent',
 'A_topdown_Avg_Takedowns_land',
 'B_topdown_Avg_Takedowns_land',
 'A_topdown_Avg_Takedowns_att',
 'B_topdown_Avg_Takedowns_att',
 'A_topdown_Avg_Takedown_percent',
 'B_topdown_Avg_Takedown_percent',
 'A_topdown_Avg_Sub_Attempts_land',
 'B_topdown_Avg_Sub_Attempts_land',
 'A_topdown_Avg_Sub_Attempts_att',
 'B_topdown_Avg_Sub_Attempts_att',
 'A_topdown_Avg_Rev',
 'B_topdown_Avg_Rev',
 'A_topdown_Avg_Ctrl_time_min',
 'B_topdown_Avg_Ctrl_time_min',
 'A_topdown_Avg_Ctrl_time_sec',
 'B_topdown_Avg_Ctrl_time_sec',
 'A_topdown_Avg_Ctrl_time_tot',
 'B_topdown_Avg_Ctrl_time_tot',
 'A_topdown_Avg_Head_Strikes_land',
 'B_topdown_Avg_Head_Strikes_land',
 'A_topdown_Avg_Head_Strikes_att',
 'B_topdown_Avg_Head_Strikes_att',
 'A_topdown_Avg_Head_Strikes_percent',
 'B_topdown_Avg_Head_Strikes_percent',
 'A_topdown_Avg_Body_Strikes_land',
 'B_topdown_Avg_Body_Strikes_land',
 'A_topdown_Avg_Body_Strikes_att',
 'B_topdown_Avg_Body_Strikes_att',
 'A_topdown_Avg_Body_Strikes_percent',
 'B_topdown_Avg_Body_Strikes_percent',
 'A_topdown_Avg_Leg_Strikes_land',
 'B_topdown_Avg_Leg_Strikes_land',
 'A_topdown_Avg_Leg_Strikes_att',
 'B_topdown_Avg_Leg_Strikes_att',
 'A_topdown_Avg_Leg_Strikes_percent',
 'B_topdown_Avg_Leg_Strikes_percent',
 'A_topdown_Avg_Distance_Strikes_land',
 'B_topdown_Avg_Distance_Strikes_land',
 'A_topdown_Avg_Distance_Strikes_att',
 'B_topdown_Avg_Distance_Strikes_att',
 'A_topdown_Avg_Distance_Strikes_percent',
 'B_topdown_Avg_Distance_Strikes_percent',
 'A_topdown_Avg_Clinch_Strikes_land',
 'B_topdown_Avg_Clinch_Strikes_land',
 'A_topdown_Avg_Clinch_Strikes_att',
 'B_topdown_Avg_Clinch_Strikes_att',
 'A_topdown_Avg_Clinch_Strikes_percent',
 'B_topdown_Avg_Clinch_Strikes_percent',
 'A_topdown_Avg_Ground_Strikes_land',
 'B_topdown_Avg_Ground_Strikes_land',
 'A_topdown_Avg_Ground_Strikes_att',
 'B_topdown_Avg_Ground_Strikes_att',
 'A_topdown_Avg_Ground_Strikes_percent',
 'B_topdown_Avg_Ground_Strikes_percent',
 'A_Opp_Avg_Kd',
 'B_Opp_Avg_Kd',
 'A_Opp_Avg_Sig_strike_land',
 'B_Opp_Avg_Sig_strike_land',
 'A_Opp_Avg_Sig_strike_att',
 'B_Opp_Avg_Sig_strike_att',
 'A_Opp_Avg_Sig_strike_percent',
 'B_Opp_Avg_Sig_strike_percent',
 'A_Opp_Avg_Total_Strikes_land',
 'B_Opp_Avg_Total_Strikes_land',
 'A_Opp_Avg_Total_Strikes_att',
 'B_Opp_Avg_Total_Strikes_att',
 'A_Opp_Avg_Total_Strikes_percent',
 'B_Opp_Avg_Total_Strikes_percent',
 'A_Opp_Avg_Takedowns_land',
 'B_Opp_Avg_Takedowns_land',
 'A_Opp_Avg_Takedowns_att',
 'B_Opp_Avg_Takedowns_att',
 'A_Opp_Avg_Takedown_percent',
 'B_Opp_Avg_Takedown_percent',
 'A_Opp_Avg_Sub_Attempts_land',
 'B_Opp_Avg_Sub_Attempts_land',
 'A_Opp_Avg_Sub_Attempts_att',
 'B_Opp_Avg_Sub_Attempts_att',
 'A_Opp_Avg_Rev',
 'B_Opp_Avg_Rev',
 'A_Opp_Avg_Ctrl_time_min',
 'B_Opp_Avg_Ctrl_time_min',
 'A_Opp_Avg_Ctrl_time_sec',
 'B_Opp_Avg_Ctrl_time_sec',
 'A_Opp_Avg_Ctrl_time_tot',
 'B_Opp_Avg_Ctrl_time_tot',
 'A_Opp_Avg_Head_Strikes_land',
 'B_Opp_Avg_Head_Strikes_land',
 'A_Opp_Avg_Head_Strikes_att',
 'B_Opp_Avg_Head_Strikes_att',
 'A_Opp_Avg_Head_Strikes_percent',
 'B_Opp_Avg_Head_Strikes_percent',
 'A_Opp_Avg_Body_Strikes_land',
 'B_Opp_Avg_Body_Strikes_land',
 'A_Opp_Avg_Body_Strikes_att',
 'B_Opp_Avg_Body_Strikes_att',
 'A_Opp_Avg_Body_Strikes_percent',
 'B_Opp_Avg_Body_Strikes_percent',
 'A_Opp_Avg_Leg_Strikes_land',
 'B_Opp_Avg_Leg_Strikes_land',
 'A_Opp_Avg_Leg_Strikes_att',
 'B_Opp_Avg_Leg_Strikes_att',
 'A_Opp_Avg_Leg_Strikes_percent',
 'B_Opp_Avg_Leg_Strikes_percent',
 'A_Opp_Avg_Distance_Strikes_land',
 'B_Opp_Avg_Distance_Strikes_land',
 'A_Opp_Avg_Distance_Strikes_att',
 'B_Opp_Avg_Distance_Strikes_att',
 'A_Opp_Avg_Distance_Strikes_percent',
 'B_Opp_Avg_Distance_Strikes_percent',
 'A_Opp_Avg_Clinch_Strikes_land',
 'B_Opp_Avg_Clinch_Strikes_land',
 'A_Opp_Avg_Clinch_Strikes_att',
 'B_Opp_Avg_Clinch_Strikes_att',
 'A_Opp_Avg_Clinch_Strikes_percent',
 'B_Opp_Avg_Clinch_Strikes_percent',
 'A_Opp_Avg_Ground_Strikes_land',
 'B_Opp_Avg_Ground_Strikes_land',
 'A_Opp_Avg_Ground_Strikes_att',
 'B_Opp_Avg_Ground_Strikes_att',
 'A_Opp_Avg_Ground_Strikes_percent',
 'B_Opp_Avg_Ground_Strikes_percent',
 'Dif_Rolling_Kd_mean',
 'Dif_Rolling_Sig_strike_land_mean',
 'Dif_Rolling_Sig_strike_att_mean',
 'Dif_Rolling_Sig_strike_percent_mean',
 'Dif_Rolling_Total_Strikes_land_mean',
 'Dif_Rolling_Total_Strikes_att_mean',
 'Dif_Rolling_Total_Strikes_percent_mean',
 'Dif_Rolling_Takedowns_land_mean',
 'Dif_Rolling_Takedowns_att_mean',
 'Dif_Rolling_Takedown_percent_mean',
 'Dif_Rolling_Sub_Attempts_land_mean',
 'Dif_Rolling_Sub_Attempts_att_mean',
 'Dif_Rolling_Rev_mean',
 'Dif_Rolling_Ctrl_time_min_mean',
 'Dif_Rolling_Ctrl_time_sec_mean',
 'Dif_Rolling_Ctrl_time_tot_mean',
 'Dif_Rolling_Head_Strikes_land_mean',
 'Dif_Rolling_Head_Strikes_att_mean',
 'Dif_Rolling_Head_Strikes_percent_mean',
 'Dif_Rolling_Body_Strikes_land_mean',
 'Dif_Rolling_Body_Strikes_att_mean',
 'Dif_Rolling_Body_Strikes_percent_mean',
 'Dif_Rolling_Leg_Strikes_land_mean',
 'Dif_Rolling_Leg_Strikes_att_mean',
 'Dif_Rolling_Leg_Strikes_percent_mean',
 'Dif_Rolling_Distance_Strikes_land_mean',
 'Dif_Rolling_Distance_Strikes_att_mean',
 'Dif_Rolling_Distance_Strikes_percent_mean',
 'Dif_Rolling_Clinch_Strikes_land_mean',
 'Dif_Rolling_Clinch_Strikes_att_mean',
 'Dif_Rolling_Clinch_Strikes_percent_mean',
 'Dif_Rolling_Ground_Strikes_land_mean',
 'Dif_Rolling_Ground_Strikes_att_mean',
 'Dif_Rolling_Ground_Strikes_percent_mean',
 'Dif_Rolling_Kd_median',
 'Dif_Rolling_Sig_strike_land_median',
 'Dif_Rolling_Sig_strike_att_median',
 'Dif_Rolling_Sig_strike_percent_median',
 'Dif_Rolling_Total_Strikes_land_median',
 'Dif_Rolling_Total_Strikes_att_median',
 'Dif_Rolling_Total_Strikes_percent_median',
 'Dif_Rolling_Takedowns_land_median',
 'Dif_Rolling_Takedowns_att_median',
 'Dif_Rolling_Takedown_percent_median',
 'Dif_Rolling_Sub_Attempts_land_median',
 'Dif_Rolling_Sub_Attempts_att_median',
 'Dif_Rolling_Rev_median',
 'Dif_Rolling_Ctrl_time_min_median',
 'Dif_Rolling_Ctrl_time_sec_median',
 'Dif_Rolling_Ctrl_time_tot_median',
 'Dif_Rolling_Head_Strikes_land_median',
 'Dif_Rolling_Head_Strikes_att_median',
 'Dif_Rolling_Head_Strikes_percent_median',
 'Dif_Rolling_Body_Strikes_land_median',
 'Dif_Rolling_Body_Strikes_att_median',
 'Dif_Rolling_Body_Strikes_percent_median',
 'Dif_Rolling_Leg_Strikes_land_median',
 'Dif_Rolling_Leg_Strikes_att_median',
 'Dif_Rolling_Leg_Strikes_percent_median',
 'Dif_Rolling_Distance_Strikes_land_median',
 'Dif_Rolling_Distance_Strikes_att_median',
 'Dif_Rolling_Distance_Strikes_percent_median',
 'Dif_Rolling_Clinch_Strikes_land_median',
 'Dif_Rolling_Clinch_Strikes_att_median',
 'Dif_Rolling_Clinch_Strikes_percent_median',
 'Dif_Rolling_Ground_Strikes_land_median',
 'Dif_Rolling_Ground_Strikes_att_median',
 'Dif_Rolling_Ground_Strikes_percent_median',
 'Dif_Rolling_Kd_std',
 'Dif_Rolling_Sig_strike_land_std',
 'Dif_Rolling_Sig_strike_att_std',
 'Dif_Rolling_Sig_strike_percent_std',
 'Dif_Rolling_Total_Strikes_land_std',
 'Dif_Rolling_Total_Strikes_att_std',
 'Dif_Rolling_Total_Strikes_percent_std',
 'Dif_Rolling_Takedowns_land_std',
 'Dif_Rolling_Takedowns_att_std',
 'Dif_Rolling_Takedown_percent_std',
 'Dif_Rolling_Sub_Attempts_land_std',
 'Dif_Rolling_Sub_Attempts_att_std',
 'Dif_Rolling_Rev_std',
 'Dif_Rolling_Ctrl_time_min_std',
 'Dif_Rolling_Ctrl_time_sec_std',
 'Dif_Rolling_Ctrl_time_tot_std',
 'Dif_Rolling_Head_Strikes_land_std',
 'Dif_Rolling_Head_Strikes_att_std',
 'Dif_Rolling_Head_Strikes_percent_std',
 'Dif_Rolling_Body_Strikes_land_std',
 'Dif_Rolling_Body_Strikes_att_std',
 'Dif_Rolling_Body_Strikes_percent_std',
 'Dif_Rolling_Leg_Strikes_land_std',
 'Dif_Rolling_Leg_Strikes_att_std',
 'Dif_Rolling_Leg_Strikes_percent_std',
 'Dif_Rolling_Distance_Strikes_land_std',
 'Dif_Rolling_Distance_Strikes_att_std',
 'Dif_Rolling_Distance_Strikes_percent_std',
 'Dif_Rolling_Clinch_Strikes_land_std',
 'Dif_Rolling_Clinch_Strikes_att_std',
 'Dif_Rolling_Clinch_Strikes_percent_std',
 'Dif_Rolling_Ground_Strikes_land_std',
 'Dif_Rolling_Ground_Strikes_att_std',
 'Dif_Rolling_Ground_Strikes_percent_std',
 'A_Height',
 'B_Height',
 'Dif_Height',
 'A_Reach',
 'B_Reach',
 'Dif_Reach',
 'A_Leg_Reach',
 'B_Leg_Reach',
 'Dif_Leg_Reach',
 'A_Reach_NA',
 'B_Reach_NA',
 'Reach_NA',
 'A_Leg_Reach_NA',
 'B_Leg_Reach_NA',
 'Leg_Reach_NA',
 'fight_weightclass',
 'A_Fight_in_Typical_Weightclass',
 'B_Fight_in_Typical_Weightclass',
 'Leg_Reach_Dif',
 'Reach_Dif',
 'A_Ape_Index',
 'B_Ape_Index',
 'A_Leg_Index',
 'B_Leg_Index',
 'A_Leg_to_Wing_Index',
 'B_Leg_to_Wing_Index',
 'favorite?',
 'A_Total_UFC_Fights',
 'B_Total_UFC_Fights',
 'Dif_Total_UFC_Fights',
 'A_UFC_Wins',
 'B_UFC_Wins',
 'Dif_UFC_Wins',
 'A_UFC_Losses',
 'B_UFC_Losses',
 'Dif_UFC_Losses',
 'A_UFC_Win_Percentage',
 'B_UFC_Win_Percentage',
 'Dif_UFC_Win_Percentage',
 'A_Last5_Win_Percentage',
 'B_Last5_Win_Percentage',
 'Dif_Last5_Win_Percentage',
 'A_Last3_Win_Percentage',
 'B_Last3_Win_Percentage',
 'Dif_Last3_Win_Percentage',
 'A_Win_By_KO_Percentage',
 'B_Win_By_KO_Percentage',
 'Dif_Win_By_KO_Percentage',
 'A_Loss_By_KO_Percentage',
 'B_Loss_By_KO_Percentage',
 'Dif_Loss_By_KO_Percentage',
 'A_Win_By_Decision_Percentage',
 'B_Win_By_Decision_Percentage',
 'Dif_Win_By_Decision_Percentage',
 'A_Loss_By_Decision_Percentage',
 'B_Loss_By_Decision_Percentage',
 'Dif_Loss_By_Decision_Percentage',
 'A_UFC_Fight_Time_Seconds',
 'B_UFC_Fight_Time_Seconds',
 'Dif_UFC_Fight_Time_Seconds',
 'A_UFC_Fight_Rounds',
 'B_UFC_Fight_Rounds',
 'A_topdown_Avg_Kd_per_round',
 'A_topdown_Avg_Sig_strike_land_per_round',
 'A_topdown_Avg_Sig_strike_att_per_round',
 'A_topdown_Avg_Total_Strikes_land_per_round',
 'A_topdown_Avg_Total_Strikes_att_per_round',
 'A_topdown_Avg_Takedowns_land_per_round',
 'A_topdown_Avg_Takedowns_att_per_round',
 'A_topdown_Avg_Sub_Attempts_land_per_round',
 'A_topdown_Avg_Sub_Attempts_att_per_round',
 'A_topdown_Avg_Rev_per_round',
 'A_topdown_Avg_Ctrl_time_min_per_round',
 'A_topdown_Avg_Ctrl_time_sec_per_round',
 'A_topdown_Avg_Ctrl_time_tot_per_round',
 'A_topdown_Avg_Head_Strikes_land_per_round',
 'A_topdown_Avg_Head_Strikes_att_per_round',
 'A_topdown_Avg_Body_Strikes_land_per_round',
 'A_topdown_Avg_Body_Strikes_att_per_round',
 'A_topdown_Avg_Leg_Strikes_land_per_round',
 'A_topdown_Avg_Leg_Strikes_att_per_round',
 'A_topdown_Avg_Distance_Strikes_land_per_round',
 'A_topdown_Avg_Distance_Strikes_att_per_round',
 'A_topdown_Avg_Clinch_Strikes_land_per_round',
 'A_topdown_Avg_Clinch_Strikes_att_per_round',
 'A_topdown_Avg_Ground_Strikes_land_per_round',
 'A_topdown_Avg_Ground_Strikes_att_per_round',
 'B_topdown_Avg_Kd_per_round',
 'B_topdown_Avg_Sig_strike_land_per_round',
 'B_topdown_Avg_Sig_strike_att_per_round',
 'B_topdown_Avg_Total_Strikes_land_per_round',
 'B_topdown_Avg_Total_Strikes_att_per_round',
 'B_topdown_Avg_Takedowns_land_per_round',
 'B_topdown_Avg_Takedowns_att_per_round',
 'B_topdown_Avg_Sub_Attempts_land_per_round',
 'B_topdown_Avg_Sub_Attempts_att_per_round',
 'B_topdown_Avg_Rev_per_round',
 'B_topdown_Avg_Ctrl_time_min_per_round',
 'B_topdown_Avg_Ctrl_time_sec_per_round',
 'B_topdown_Avg_Ctrl_time_tot_per_round',
 'B_topdown_Avg_Head_Strikes_land_per_round',
 'B_topdown_Avg_Head_Strikes_att_per_round',
 'B_topdown_Avg_Body_Strikes_land_per_round',
 'B_topdown_Avg_Body_Strikes_att_per_round',
 'B_topdown_Avg_Leg_Strikes_land_per_round',
 'B_topdown_Avg_Leg_Strikes_att_per_round',
 'B_topdown_Avg_Distance_Strikes_land_per_round',
 'B_topdown_Avg_Distance_Strikes_att_per_round',
 'B_topdown_Avg_Clinch_Strikes_land_per_round',
 'B_topdown_Avg_Clinch_Strikes_att_per_round',
 'B_topdown_Avg_Ground_Strikes_land_per_round',
 'B_topdown_Avg_Ground_Strikes_att_per_round',
 'A_Opp_Avg_Kd_per_round',
 'A_Opp_Avg_Sig_strike_land_per_round',
 'A_Opp_Avg_Sig_strike_att_per_round',
 'A_Opp_Avg_Total_Strikes_land_per_round',
 'A_Opp_Avg_Total_Strikes_att_per_round',
 'A_Opp_Avg_Takedowns_land_per_round',
 'A_Opp_Avg_Takedowns_att_per_round',
 'A_Opp_Avg_Sub_Attempts_land_per_round',
 'A_Opp_Avg_Sub_Attempts_att_per_round',
 'A_Opp_Avg_Rev_per_round',
 'A_Opp_Avg_Ctrl_time_min_per_round',
 'A_Opp_Avg_Ctrl_time_sec_per_round',
 'A_Opp_Avg_Ctrl_time_tot_per_round',
 'A_Opp_Avg_Head_Strikes_land_per_round',
 'A_Opp_Avg_Head_Strikes_att_per_round',
 'A_Opp_Avg_Body_Strikes_land_per_round',
 'A_Opp_Avg_Body_Strikes_att_per_round',
 'A_Opp_Avg_Leg_Strikes_land_per_round',
 'A_Opp_Avg_Leg_Strikes_att_per_round',
 'A_Opp_Avg_Distance_Strikes_land_per_round',
 'A_Opp_Avg_Distance_Strikes_att_per_round',
 'A_Opp_Avg_Clinch_Strikes_land_per_round',
 'A_Opp_Avg_Clinch_Strikes_att_per_round',
 'A_Opp_Avg_Ground_Strikes_land_per_round',
 'A_Opp_Avg_Ground_Strikes_att_per_round',
 'B_Opp_Avg_Kd_per_round',
 'B_Opp_Avg_Sig_strike_land_per_round',
 'B_Opp_Avg_Sig_strike_att_per_round',
 'B_Opp_Avg_Total_Strikes_land_per_round',
 'B_Opp_Avg_Total_Strikes_att_per_round',
 'B_Opp_Avg_Takedowns_land_per_round',
 'B_Opp_Avg_Takedowns_att_per_round',
 'B_Opp_Avg_Sub_Attempts_land_per_round',
 'B_Opp_Avg_Sub_Attempts_att_per_round',
 'B_Opp_Avg_Rev_per_round',
 'B_Opp_Avg_Ctrl_time_min_per_round',
 'B_Opp_Avg_Ctrl_time_sec_per_round',
 'B_Opp_Avg_Ctrl_time_tot_per_round',
 'B_Opp_Avg_Head_Strikes_land_per_round',
 'B_Opp_Avg_Head_Strikes_att_per_round',
 'B_Opp_Avg_Body_Strikes_land_per_round',
 'B_Opp_Avg_Body_Strikes_att_per_round',
 'B_Opp_Avg_Leg_Strikes_land_per_round',
 'B_Opp_Avg_Leg_Strikes_att_per_round',
 'B_Opp_Avg_Distance_Strikes_land_per_round',
 'B_Opp_Avg_Distance_Strikes_att_per_round',
 'B_Opp_Avg_Clinch_Strikes_land_per_round',
 'B_Opp_Avg_Clinch_Strikes_att_per_round',
 'B_Opp_Avg_Ground_Strikes_land_per_round',
 'B_Opp_Avg_Ground_Strikes_att_per_round',
 'Dif_topdown_Avg_Kd_per_round',
 'Dif_topdown_Avg_Sig_strike_land_per_round',
 'Dif_topdown_Avg_Sig_strike_att_per_round',
 'Dif_topdown_Avg_Total_Strikes_land_per_round',
 'Dif_topdown_Avg_Total_Strikes_att_per_round',
 'Dif_topdown_Avg_Takedowns_land_per_round',
 'Dif_topdown_Avg_Takedowns_att_per_round',
 'Dif_topdown_Avg_Sub_Attempts_land_per_round',
 'Dif_topdown_Avg_Sub_Attempts_att_per_round',
 'Dif_topdown_Avg_Rev_per_round',
 'Dif_topdown_Avg_Ctrl_time_min_per_round',
 'Dif_topdown_Avg_Ctrl_time_sec_per_round',
 'Dif_topdown_Avg_Ctrl_time_tot_per_round',
 'Dif_topdown_Avg_Head_Strikes_land_per_round',
 'Dif_topdown_Avg_Head_Strikes_att_per_round',
 'Dif_topdown_Avg_Body_Strikes_land_per_round',
 'Dif_topdown_Avg_Body_Strikes_att_per_round',
 'Dif_topdown_Avg_Leg_Strikes_land_per_round',
 'Dif_topdown_Avg_Leg_Strikes_att_per_round',
 'Dif_topdown_Avg_Distance_Strikes_land_per_round',
 'Dif_topdown_Avg_Distance_Strikes_att_per_round',
 'Dif_topdown_Avg_Clinch_Strikes_land_per_round',
 'Dif_topdown_Avg_Clinch_Strikes_att_per_round',
 'Dif_topdown_Avg_Ground_Strikes_land_per_round',
 'Dif_topdown_Avg_Ground_Strikes_att_per_round',
 'Dif_Opp_Avg_Kd_per_round',
 'Dif_Opp_Avg_Sig_strike_land_per_round',
 'Dif_Opp_Avg_Sig_strike_att_per_round',
 'Dif_Opp_Avg_Total_Strikes_land_per_round',
 'Dif_Opp_Avg_Total_Strikes_att_per_round',
 'Dif_Opp_Avg_Takedowns_land_per_round',
 'Dif_Opp_Avg_Takedowns_att_per_round',
 'Dif_Opp_Avg_Sub_Attempts_land_per_round',
 'Dif_Opp_Avg_Sub_Attempts_att_per_round',
 'Dif_Opp_Avg_Rev_per_round',
 'Dif_Opp_Avg_Ctrl_time_min_per_round',
 'Dif_Opp_Avg_Ctrl_time_sec_per_round',
 'Dif_Opp_Avg_Ctrl_time_tot_per_round',
 'Dif_Opp_Avg_Head_Strikes_land_per_round',
 'Dif_Opp_Avg_Head_Strikes_att_per_round',
 'Dif_Opp_Avg_Body_Strikes_land_per_round',
 'Dif_Opp_Avg_Body_Strikes_att_per_round',
 'Dif_Opp_Avg_Leg_Strikes_land_per_round',
 'Dif_Opp_Avg_Leg_Strikes_att_per_round',
 'Dif_Opp_Avg_Distance_Strikes_land_per_round',
 'Dif_Opp_Avg_Distance_Strikes_att_per_round',
 'Dif_Opp_Avg_Clinch_Strikes_land_per_round',
 'Dif_Opp_Avg_Clinch_Strikes_att_per_round',
 'Dif_Opp_Avg_Ground_Strikes_land_per_round',
 'Dif_Opp_Avg_Ground_Strikes_att_per_round']

this_fight_df['Dif_Odds'] = this_fight_df['Fighter_A_Odds'] - this_fight_df['Fighter_B_Odds']

final_vect = this_fight_df[proper_order]


# load model
extra_trees = pickle.load(open('C:\\Users\\Travis\\OneDrive\\Data Science\\Personal_Projects\\Sports\\UFC_Prediction_V2\\models\\SVC.pkl', 'rb'))

# Predict
prediction = pd.DataFrame(extra_trees.predict(final_vect))
prediction = prediction[0].values[0]

if prediction == 1:
    st.sidebar.header("Predicted Winner: " + selected_fighter_1)
if prediction == 0:
    st.sidebar.header("Predicted Winner: " + selected_fighter_2)

probabilities = extra_trees.predict_proba(final_vect)
prob_win = probabilities[0][1]
prob_win = round(prob_win * 100,1)
prob_lose = probabilities[0][0]
prob_lose = round(prob_lose * 100,1)

# Display sidebar probabilities
st.sidebar.write("")
st.sidebar.subheader("Model Predicted Win Probabilities:")
st.sidebar.write(selected_fighter_1 + " : " + str(prob_win) + "%")
st.sidebar.write(selected_fighter_2 + " : " + str(prob_lose)+ "%")
st.sidebar.write("")

st.sidebar.subheader('Expected Value of $10:')

def american_odds_to_payout(odds):
    # make sure odds are numerical
    odds = float(odds)
    if odds > 0:
        return odds/100 + 1
    else:
        return 100/abs(odds) + 1

vegas_odds_1 = next_event['fighter1_odds'][next_event['fighter1'] == selected_fighter_1].values[0]
vegas_odds_2 = next_event['fighter2_odds'][next_event['fighter2'] == selected_fighter_2].values[0]

american_payout1 = american_odds_to_payout(vegas_odds_1)
american_payout2 = american_odds_to_payout(vegas_odds_2)

# Expected Value
ev1 = (american_payout1 * (prob_win/100 * 10)) - ((prob_lose/100) * 10 * american_payout2)
st.sidebar.write(f' {selected_fighter_1} EV: {ev1.round()}')


ev2 = ((prob_lose/100) * 10 * american_payout2) - (american_payout1 * (prob_win/100 * 10))
st.sidebar.write("")
st.sidebar.write(f' {selected_fighter_2} EV: {ev2.round()}')

if ev1 > ev2:
    st.sidebar.subheader("A Bet on " + selected_fighter_1 + " is positive EV")
else:
    st.sidebar.subheader("A Bet on " + selected_fighter_2+ " is positive EV")



###########        MATCHUPS      ###############


st.sidebar.header('Selected UFC Event: '+ selected_event)

ne = next_event.rename(columns={'fighter1': 'Fighter #1', 'fighter2': 'Fighter #2', 
                                'weightclass': 'Weightclass', 'fighter1_odds': 'Fighter #1 Odds', 
                                'fighter2_odds': 'Fighter #2 Odds'})
colz = ['Fighter #1', 'Fighter #2', ]
ne = ne[colz]
st.sidebar.table(ne.style.format({'Fighter #1 Odds': '{:.2f}', 'Fighter #2 Odds': '{:.2f}'}))

st.header('Important Features')
st.write('Peruse the model features below')


num_cols = final_vect.select_dtypes(include=['float64', 'int64']).columns
# round all float columns to 2 decimal places
final_vect_t = final_vect.copy()
final_vect_t[num_cols] = final_vect_t[num_cols].round(2)
final_vect_t = final_vect_t.T
final_vect_t.columns = ['Value']

st.dataframe(final_vect_t)

############   ALL FEATURES  ############


#cols = []

#a_cols = [n for n in cols if n.startswith('A')]
#b_cols = [n for n in cols if n.startswith('B')]

#a_cols_df = final_vect[a_cols]
#b_cols_df = final_vect[b_cols]
# Make new df with a cols as rows in one column and b cols as rows in the other
#df = pd.DataFrame(columns=[selected_fighter_1, selected_fighter_2])
# make column values the values from a_cols_df and b_cols_df
#df[selected_fighter_1] = a_cols_df.values[0]
#df[selected_fighter_2] = b_cols_df.values[0]
# round to 1
#df = df.round(1)
# rows are the index of a_cols_df
#df.index = a_cols
# rename indexes
#df.index = ['Total Strikes (Average)', 'Total Significant Strikes (Average)', 'Distance Strikes (Average)', 'Head Strikes (Average)', 'Ground Strikes Percent (Median)',
#            'Ground Strikes Percent (Minimum)', 'Leg Reach (inches)', 'Control Time (Average)']

# only display one decimal place
#st.table(df.style.highlight_max(axis = 1, color = 'darkgreen').format("{:.1f}"))


st.header('Links for More Fighter Information:')
st.subheader('Wikipedia')
st.write('Follow links for fighter Wikipedia pages')

first_name1 = selected_fighter_1.split()[0]
last_name1 = selected_fighter_1.split()[1]
st.write('https://en.wikipedia.org/wiki/' + first_name1 + '_' + last_name1)

first_name2 = selected_fighter_2.split()[0]
last_name2 = selected_fighter_2.split()[1]
st.write('https://en.wikipedia.org/wiki/' + first_name2 + '_' + last_name2)

st.subheader('UFC.COM')
st.write('https://www.ufc.com/search?query=' + first_name1 + '+' + last_name1)
st.write('https://www.ufc.com/search?query=' + first_name2 + '+' + last_name2)

st.subheader('Sherdog Stats')
st.write('https://www.sherdog.com/search.php?q=' + first_name1 + '+' + last_name1)
st.write('https://www.sherdog.com/search.php?q=' + first_name2 + '+' + last_name2)





