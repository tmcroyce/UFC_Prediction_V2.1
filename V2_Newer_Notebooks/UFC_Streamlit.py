

# THIS IS NOW APP.PY IN MAIN FOLDER



# # The following pages are involved with this page:
# # - Scraping Tapology.ipynb (scrapes tapology.com for fighter info and saves)
# # - Scrape_UFC_Upcoming_Events.ipynb (scrapes ufc.com for upcoming events and saves)

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mtick
# import seaborn as sns
# from matplotlib.pyplot import figure
# from bs4 import BeautifulSoup
# import time
# import requests     
# import shutil       
# import datetime
# from scipy.stats import norm
# import warnings
# warnings.filterwarnings('ignore')
# from random import randint
# import  random
# import os
# from cmath import nan
# from bs4 import BeautifulSoup
# import streamlit as st
# import pickle
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from PIL import Image

# st.set_page_config(page_title='UFC Prediction', page_icon=None, layout="wide", initial_sidebar_state="auto" )

# home = '/Users/travisroyce/Library/CloudStorage/OneDrive-Personal/Data Science/Personal_Projects/Sports/UFC_Prediction_V2/data'
# home2 = '/Users/travisroyce/Library/CloudStorage/OneDrive-Personal/Data Science/Personal_Projects/Sports/UFC_Prediction_V2'
# os.chdir(home)




# #------------------------------  Define Functions -----------------------------------------------------------------
# # function to return the next 3 UFC events using BeautifulSoup (BS)
# def get_next_events(url):
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     # get events
#     event1 = soup.find('div', class_='c-card-event--result__info')
#     event1_txt = soup.find('div', class_='c-card-event--result__info').text
#     event1_url = event1.find('a')['href']
#     event1_url = 'https://www.ufc.com' + event1_url
#     event1_title = event1_txt.split('\n')[1]
#     event1_time = event1_txt.split('/')[1]

#     data = pd.DataFrame({'event_title': [event1_title], 'event_url': [event1_url], 'event_date': [event1_time]})

#     event2 = soup.find('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info')
#     event2_txt = soup.find('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info').text
#     event2_url = event2.find('a')['href']
#     event2_url = 'https://www.ufc.com' + event2_url
#     event2_title = event2_txt.split('\n')[1]
#     event2_time = event2_txt.split('/')[1]


#     data = data.append({'event_title': event2_title, 'event_url': event2_url, 'event_date': event2_time}, ignore_index=True)
    
#     event3 = soup.find('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info')
#     event3_txt = soup.find('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info').find_next('div', class_='c-card-event--result__info').text
#     event3_url = event3.find('a')['href']
#     event3_url = 'https://www.ufc.com' + event3_url
#     event3_title = event3_txt.split('\n')[1]
#     event3_time = event3_txt.split('/')[1]

#     data = data.append({'event_title': event3_title, 'event_url': event3_url, 'event_date': event3_time}, ignore_index=True)
    
#     return data

# # Function to get the fight card for a given event using BS
# def get_event_fights(event_url):
#     page = requests.get(event_url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     # get main card, fight 1

#     mcn = soup.find_all('li', class_='l-listing__item')
#     # get num of mc
#     num_mc = len(mcn)
#     # for each mc, do the following
#     data = pd.DataFrame()
#     n = 0
#     for i in mcn:
#         mc = mcn[n]
#         # fight 1
#         fighter1= mc.find('div', class_ ='c-listing-fight__corner-name c-listing-fight__corner-name--red').text
#         fighter1 = fighter1.replace('\n', ' ')
#         fighter1 = fighter1.strip()
#         fighter2 = mc.find('div', class_ ='c-listing-fight__corner-name c-listing-fight__corner-name--blue').text
#         fighter2 = fighter2.replace('\n', ' ')
#         fighter2 = fighter2.strip()
#         weightclass = mc.find('div', class_='c-listing-fight__class-text').text
#         fighter1_odds = mc.find('span', class_='c-listing-fight__odds').text
#         fighter2_odds = mc.find('span', class_='c-listing-fight__odds').find_next('span', class_='c-listing-fight__odds').text
#         fighter1_odds = fighter1_odds.replace('\n', '')
#         fighter2_odds = fighter2_odds.replace('\n', '')
#         # fighter odds to float
#         if (fighter1_odds == '-') :
#             fighter1_odds = nan
#         if (fighter2_odds == '-') :
#             fighter2_odds = nan

#         data = data.append({'fighter1': fighter1, 'fighter2': fighter2, 'weightclass': weightclass, 
#                             'fighter1_odds': fighter1_odds, 'fighter2_odds': fighter2_odds}, ignore_index=True)
#         n = n + 1
#     return data

# # get next events if event fighter data is not na
# def get_next_events2(url):
#     data = get_next_events(url)
#     for i in range(0, len(data)):
#         event_url = data['event_url'][i]
#         event_fights = get_event_fights(event_url)
#         if (len(event_fights) == 0):
#             data = data.drop(i)
#     return data

# # get next events from UFCStats.com using BS
# def get_next_event_ufcstats():
#     url = 'http://www.ufcstats.com/statistics/events/upcoming'
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     # get events
#     event1 = soup.find('td', class_='b-statistics__table-col')
#     event1_txt = soup.find('td', class_='b-statistics__table-col').text
#     event_txt = event1_txt.replace('   ', '').replace('\n', '').strip()
#     event_title = event_txt.split('  ')[0]
#     event_date = event_txt.split('  ')[1]
#     event1_url = event1.find('a')['href']
#     data = pd.DataFrame({'event_title': [event_title], 'event_url': [event1_url], 'event_date': [event_date]})
#     return data

# # get fighter urls from UFCStats.com using BS
# def get_fighter_urls(event_details_url):
#     page = requests.get(event_details_url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     # get events
#     events = soup.find_all('tr', class_='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click')
#     n = 0
#     next_event_data = pd.DataFrame()

#     for event in events:
#         fighters = events[n].find_all('p', class_='b-fight-details__table-text')
#         fighter1 = fighters[0].text
#         fighter1 = fighter1.replace('  ', '').replace('\n', '').strip()
#         fighter2 = fighters[1].text
#         fighter2 = fighter2.replace('  ', '').replace('\n', '').strip()
#         fighter1_url = fighters[0].find('a')['href']
#         fighter2_url = fighters[1].find('a')['href']
#         next_event_data = next_event_data.append({'fighter1' :fighter1, 'fighter2:' : fighter2, 'fighter1_url': fighter1_url, 'fighter2_url':fighter2_url, 'fight#' : n+1}, ignore_index = True)
#         n += 1

#     return next_event_data


# # check if it is a saturday
# def is_saturday():
#     today = str(datetime.today().weekday())
#     if today == '5':
#         return True
#     else:
#         return False











# # Get next event from ufcstats.com
# next_eventz = get_next_event_ufcstats()


# # load primary dataframe
# data = pd.read_csv(home + '/final/aggregates/Double_Fights_DF_V14.csv')


# # make sure events have fight info. If not, disregard that event
# next = get_next_events('https://www.ufc.com/events')
# next_event_title = next['event_title'][0]

# # load next event data, if it exists. If it does not exist, run Scrape_UFC_Upcoming_Events
# try:
#     next_event_data = pd.read_csv(home + '/final/next_fights/'+ next_event_title+ '_.csv')
# except:
#     st.write('No data for ' + next_event_title)










# ########           Select Next Event    ################

# event = next_event_title
# selected_event = event

# fight = st.sidebar.selectbox('Select Fight', next_event_data['fighter1'] + ' vs. ' + next_event_data['fighter2'])

# ufc_data = next_event_data[next_event_data['fighter1'] + ' vs. ' + next_event_data['fighter2'] == fight]

# ## Get Names ##
# selected_fighter_1 = fight.split(' vs. ')[0]
# selected_fighter_2 = fight.split(' vs. ')[1].strip()

# # get last names
# selected_fighter_1_last_name = selected_fighter_1.split(' ')[-1]
# selected_fighter_2_last_name = selected_fighter_2.split(' ')[-1]

# #st.dataframe(next_event_data)


# selected_matchup_url = next_event_data[next_event_data['fighter1'] == selected_fighter_1]['matchup_url'].values[0]

# # Grab fighter pictures, download to disk. If already downloaded, load. 
# def get_fighter_pic_url(selected_matchup_url, fighter_choice):
#     # Split the selected fighter names into first and last names
#     fighter_last_name1 = selected_fighter_1.split(' ')[-1]
#     fighter_last_name1 = fighter_last_name1.upper()
#     # drop any ' in the name
#     fighter_last_name1 = fighter_last_name1.replace("'", '')
#     fighter_first_name1 = selected_fighter_1.split(' ')[0]
#     fighter_first_name1 = fighter_first_name1.upper()

#     fighter_last_name2 = selected_fighter_2.split(' ')[-1]
#     fighter_last_name2 = fighter_last_name2.upper()
#     # drop any ' in the name
#     fighter_last_name2 = fighter_last_name2.replace("'", '')
#     fighter_first_name2 = selected_fighter_2.split(' ')[0]
#     fighter_first_name2 = fighter_first_name2.upper()

#     # Call 
#     driver = None
#     if driver == None:
#         # Set up the Selenium WebDriver
#         driver = webdriver.Chrome(home2 + '/chromedriver')
#     driver.get(selected_matchup_url)
#     time.sleep(2)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     h = soup.find_all('img')
#     imgs = []
#     for i in h:
#         # Retrieve the URLs of all images on the page
#         imgs.append(i['src'])

#     # Keep only the images with 'full_body' in the URL
#     imgs = [i for i in imgs if 'full_body' in i]

#     # Get the URL of the first fighter's image
#     fighter_img1 = [i for i in imgs if fighter_last_name1 in i][0]
#     fighter_img1 = fighter_img1.replace('athlete_detail_stance_thumbnail_full_body', 'athlete_matchup_stats_full_body')
#     # Only keep the part of the URL before '.png'
#     fighter_img1 = fighter_img1[:fighter_img1.find('.png') + 4]

#     # Get the URL of the second fighter's image
#     fighter_img2 = [i for i in imgs if fighter_last_name2 in i][0]
#     fighter_img2 = fighter_img2.replace('athlete_detail_stance_thumbnail_full_body', 'athlete_matchup_stats_full_body')
#     # Only keep the part of the URL before '.png'
#     fighter_img2 = fighter_img2[:fighter_img2.find('.png') + 4]

#     if fighter_choice == 1:
#         # Download and save the first fighter's image to a file
#         fighter1_img = requests.get(fighter_img1)
#         with open(home + '/fighter_images/' + selected_fighter_1 + '.png', 'wb') as f:
#             f.write(fighter1_img.content)

#         # Return the URL of the first fighter's image
#         return fighter_img1
#     else:
#         # Download and save the second fighter's image to a file
#         fighter2_img = requests.get(fighter_img2)
#         with open(home + '/fighter_images/' + selected_fighter_2 + '.png', 'wb') as f:
#             f.write(fighter2_img.content)

#         # Return the URL of the second fighter's image
#         return fighter_img2



# # try loading fighter images. If fail, call function

# # Check and open the first fighter image
# try:
#     fighter1_img = home + '/fighter_images/' + str(selected_fighter_1) + '.png'
#     fighter1_final_image = Image.open(fighter1_img)
#     st.write('fighter 1 image found')
# except FileNotFoundError:
#     st.write('fighter 1 image not found. Calling function')
#     get_fighter_pic_url(selected_matchup_url, 1)
#     fighter1_img = home + '/fighter_images/' + str(selected_fighter_1) + '.png'

# # Check and open the second fighter image
# try:
#     fighter2_img = home + '/fighter_images/' + str(selected_fighter_2) + '.png'
#     fighter2_final_image = Image.open(fighter2_img)
#     st.write('fighter 2 image found')
# except FileNotFoundError:
#     st.write('fighter 2 image not found. Calling function')
#     get_fighter_pic_url(selected_matchup_url, 2)
#     fighter2_img = home + '/fighter_images/' + str(selected_fighter_2) + '.png'










# ################ FIGHTER INFO ####################

# from PIL import Image

# try:
#     fighter1_img = home + '/fighter_images/' + str(selected_fighter_1) + '.png'
#     fighter1_final_image = Image.open(fighter1_img)
# except:
#     fighter1_final_image = Image.open(home + '/fighter_images/unknown_fighter.png')
# try:
#     fighter2_img = home + '/fighter_images/' + str(selected_fighter_2) + '.png'
#     fighter2_final_image = Image.open(fighter2_img)
# except:
#     fighter2_final_image = Image.open(home + '/fighter_images/unknown_fighter.png')


# col0,  col1, col2, col4, col5= st.columns([.1, .2, .4, .2, .1])

# col1.header(selected_fighter_1)
# col4.header(selected_fighter_2)
# col1.image(fighter1_final_image, use_column_width=True)
# col4.image(fighter2_final_image, use_column_width=True)

# player1_height = ufc_data['red_height'].values[0]
# player1_reach = ufc_data['red_reach'].values[0]
# player1_leg_reach = ufc_data['red_legreach'].values[0]
# player1_winby_ko = ufc_data['red_win_by_ko_percent'].values[0]
# player1_winby_sub = ufc_data['red_win_by_sub_percent'].values[0]
# player1_winby_dec = ufc_data['red_win_by_dec_percent'].values[0]
# player1_avg_fighttime = ufc_data['red_avg_fight_time'].values[0]
# player1_knockdowns_per_15 = ufc_data['red_knockdowns_per_15_min'].values[0]
# player1_take_downs_per_15 = ufc_data['red_takedowns_landed_per_15_min'].values[0]
# player1_takedown_accuracy = ufc_data['red_takedown_accuracy'].values[0]
# player1_takedown_defense = ufc_data['red_takedown_defense'].values[0]
# player1_sub_attempts_per_15 = ufc_data['red_submissions_attempts_per_15_min'].values[0]
# player1_sig_strike_attempts_per_min = ufc_data['red_sig_strikes_landed_per_min'].values[0]
# player1_strike_accuracy = ufc_data['red_sig_strikes_percent'].values[0]
# player1_strike_defense = ufc_data['red_sig_strikes_absorbed_percent'].values[0]

# player2_height = ufc_data['blue_height'].values[0]
# player2_reach = ufc_data['blue_reach'].values[0]
# player2_leg_reach = ufc_data['blue_legreach'].values[0]
# player2_winby_ko = ufc_data['blue_win_by_ko_percent'].values[0]
# player2_winby_sub = ufc_data['blue_win_by_sub_percent'].values[0]
# player2_winby_dec = ufc_data['blue_win_by_dec_percent'].values[0]
# player2_avg_fighttime = ufc_data['blue_avg_fight_time'].values[0]
# player2_knockdowns_per_15 = ufc_data['blue_knockdowns_per_15_min'].values[0]
# player2_take_downs_per_15 = ufc_data['blue_takedowns_landed_per_15_min'].values[0]
# player2_takedown_accuracy = ufc_data['blue_takedown_accuracy'].values[0]
# player2_takedown_defense = ufc_data['blue_takedown_defense'].values[0]
# player2_sub_attempts_per_15 = ufc_data['blue_submissions_attempts_per_15_min'].values[0]
# player2_sig_strike_attempts_per_min = ufc_data['blue_sig_strikes_landed_per_min'].values[0]
# player2_strike_accuracy = ufc_data['red_sig_strikes_percent'].values[0]
# player2_strike_defense = ufc_data['blue_sig_strikes_absorbed_percent'].values[0]

# def height_to_inches(height):
#     height = height.split("'")
#     # drop the " from the inches
#     height[1] = height[1].replace('"', '')
#     feet = int(height[0])
#     inches = int(height[1])
#     total_inches = feet*12 + inches
#     return total_inches




# # calculate body size as height - leg_reach
# # height to inches
# player1_height_inches = height_to_inches(player1_height)
# # col2.metric('Height (Inches)', player1_height_inches)
# player1_height = float(player1_height_inches)
# # drop ' in' from leg reach
# player1_leg_reach = player1_leg_reach.replace(' in', '')
# player1_leg_reach = float(player1_leg_reach)
# player1_body_size = player1_height - player1_leg_reach

# # fix reach by dropping ' in' and converting to float
# player1_reach = player1_reach.replace(' in', '')
# player1_reach = float(player1_reach)

# # Make sure Takedowns per 15 is numeric
# player1_take_downs_per_15 = float(player1_take_downs_per_15)

# # calculate body size as height - leg_reach
# # height to inches
# player2_height_inches = height_to_inches(player2_height)
# # col3.metric('Height (Inches)', player2_height_inches)
# player2_height = float(player2_height_inches)
# # drop ' in' from leg reach
# player2_leg_reach = player2_leg_reach.replace(' in', '')
# player2_leg_reach = float(player2_leg_reach)
# player2_body_size = player2_height - player2_leg_reach

# # fix reach by dropping ' in' and converting to float
# player2_reach = player2_reach.replace(' in', '')
# player2_reach = float(player2_reach)

# # make sure takedowns per 15 is numeric
# player2_take_downs_per_15 = float(player2_take_downs_per_15)

# # make sure sig strike attempts per min is numeric
# player1_sig_strike_attempts_per_min = float(player1_sig_strike_attempts_per_min)
# player2_sig_strike_attempts_per_min = float(player2_sig_strike_attempts_per_min)


# fighter_metrics = pd.DataFrame({
#     'metric': ['Height', 'Reach (Inches)', 'Leg Reach (Inches)', 'Height (Inches)', 
#                'Upper Body Length (Inches)', 'Win by KO (%)', 'Win by Sub(%)', 'Win by Dec(%)', 
#                'Avg Fight Time', 'Knockdowns per 15', 'Takedowns per 15', 'Takedown Accuracy (%)', 
#                'Takedown Defense (%)', 'Sub Attempts per 15', 'Strike Attempts per Min',
#                'Strike Accuracy (%)', 'Strike Defense (%)'],
#     'fighter1': [player1_height, player1_reach, player1_leg_reach, player1_height_inches, 
#                  player1_body_size, player1_winby_ko, player1_winby_sub, player1_winby_dec, 
#                  player1_avg_fighttime, player1_knockdowns_per_15, player1_take_downs_per_15, 
#                  player1_takedown_accuracy, player1_takedown_defense, player1_sub_attempts_per_15,
#                  player1_sig_strike_attempts_per_min, player1_strike_accuracy, player1_strike_defense],
#     'fighter2': [player2_height, player2_reach, player2_leg_reach, player2_height_inches, 
#                  player2_body_size, player2_winby_ko, player2_winby_sub, player2_winby_dec, 
#                  player2_avg_fighttime, player2_knockdowns_per_15, player2_take_downs_per_15, 
#                  player2_takedown_accuracy, player2_takedown_defense, player2_sub_attempts_per_15,
#                  player2_sig_strike_attempts_per_min, player2_strike_accuracy, player2_strike_defense]
# })
# fighter_metrics = fighter_metrics.set_index('metric')

# # make sure each column is a float
# def time_to_float(time_str):
#     # convert time to float
#     minutes, seconds = time_str.split(':')
#     return float(minutes) + float(seconds) / 60

# def str_to_float(x):
#     if type(x) is str:
#         if ':' in x:
#             return time_to_float(x)
#         if '%' in x:
#             return float(x.replace('%', ''))
#     else:
#         return float(x)

# fighter_metrics['fighter1'] = fighter_metrics['fighter1'].apply(str_to_float)
# fighter_metrics['fighter2'] = fighter_metrics['fighter2'].apply(str_to_float)
# # rename fighter1 and fighter2 columns to actual names
# fighter_metrics = fighter_metrics.rename(columns={'fighter1': selected_fighter_1, 'fighter2': selected_fighter_2})

# # Add fighter differences to fighter metrics
# fighter_metrics['dif'] = fighter_metrics[selected_fighter_1] - fighter_metrics[selected_fighter_2]

# # round all values in fighter metrics to 2 decimal places
# fighter_metrics = fighter_metrics.round(2)

# # drop height in inches
# if 'Height (Inches)' in fighter_metrics.index:
#     fighter_metrics = fighter_metrics.drop(['Height (Inches)'], axis=0)

# # rearraange columns so dif in middle
# fighter_metrics = fighter_metrics[[selected_fighter_1, 'dif', selected_fighter_2]]

# # drop metric row 
# #fighter_metrics = fighter_metrics.drop(['metric'], axis=0)

# def highlight_larger(s, props):
#     is_max = s == s.max()
#     return [props if v else '' for v in is_max]

# # Apply highlight and formatting
# styled_fighter_metrics = (fighter_metrics.style
#                           .apply(highlight_larger, props='background-color: lightgreen;', 
#                                  subset=[selected_fighter_1, selected_fighter_2], axis=1)
#                           .format("{:.2f}", subset=[selected_fighter_1, selected_fighter_2, 'dif']))

# # Convert the styled dataframe to HTML and set a custom height
# html = styled_fighter_metrics.render()
# custom_height = 1000  # adjust this as needed
# html_with_custom_height = f'<div style="height: {custom_height}px; overflow:auto;">{html}</div>'

# col2.markdown(html_with_custom_height, unsafe_allow_html=True)








# ##      TAPOLOGY     ##
# st.write('---')

# st.subheader('Fights by Promotion')

# tapology_files = os.listdir(home + '/tapology/fighters')

# # load fighter 1 tapology
# fighter_1_files = [i for i in tapology_files if selected_fighter_1 in i]
# fighter_2_files = [i for i in tapology_files if selected_fighter_2 in i]

# # display available files if button is clicked
# if st.button('Show Available Files'):
#     st.write(fighter_1_files)
#     st.write(fighter_2_files)

# # Load Record by Promotion for both fighters
# fighter_1_promo_file = [i for i in fighter_1_files if 'record_by_promotion' in i][0]
# fighter_2_promo_file = [i for i in fighter_2_files if 'record_by_promotion' in i][0]

# # load and display
# fighter_1_promo = pd.read_csv(home + '/tapology/fighters/' + fighter_1_promo_file)
# fighter_2_promo = pd.read_csv(home + '/tapology/fighters/' + fighter_2_promo_file)

# # transpose and make first row the header
# fighter_1_promo = fighter_1_promo.T
# fighter_1_promo.columns = fighter_1_promo.iloc[0]
# fighter_1_promo = fighter_1_promo[1:]

# fighter_2_promo = fighter_2_promo.T
# fighter_2_promo.columns = fighter_2_promo.iloc[0]
# fighter_2_promo = fighter_2_promo[1:]

# # drop any rows with 'No Contests' in index
# fighter_1_promo = fighter_1_promo[~fighter_1_promo.index.str.contains('No Contests')]
# fighter_2_promo = fighter_2_promo[~fighter_2_promo.index.str.contains('No Contests')]
# # drop any rows with 'Draws' in index
# fighter_1_promo = fighter_1_promo[~fighter_1_promo.index.str.contains('Draws')]
# fighter_2_promo = fighter_2_promo[~fighter_2_promo.index.str.contains('Draws')]
# # drop any rows with 'DQ' in index
# fighter_1_promo = fighter_1_promo[~fighter_1_promo.index.str.contains('DQ')]
# fighter_2_promo = fighter_2_promo[~fighter_2_promo.index.str.contains('DQ')]
# # Replace all 'Percent' in the index values with '%'
# fighter_1_promo.index = fighter_1_promo.index.str.replace('Percent', '%')
# fighter_2_promo.index = fighter_2_promo.index.str.replace('Percent', '%')

# # Columns should only keep the first word of the column name
# fighter_1_promo.columns = fighter_1_promo.columns.str.split(' ').str[0]
# fighter_2_promo.columns = fighter_2_promo.columns.str.split(' ').str[0]

# # Rows should be sorted like this: Years Active, Wins, Losses, rows with 'Win %' in them, rows with 'Loss %' in them, then the rest
# fighter_1_promo = fighter_1_promo.loc[['Wins', 'Losses'] + [i for i in fighter_1_promo.index if 'Win %' in i] + [i for i in fighter_1_promo.index if 'Loss %' in i] + [i for i in fighter_1_promo.index if i not in ['Years', 'Wins', 'Losses'] and 'Win %' not in i and 'Loss %' not in i]]
# fighter_2_promo = fighter_2_promo.loc[['Wins', 'Losses'] + [i for i in fighter_2_promo.index if 'Win %' in i] + [i for i in fighter_2_promo.index if 'Loss %' in i] + [i for i in fighter_2_promo.index if i not in ['Years', 'Wins', 'Losses'] and 'Win %' not in i and 'Loss %' not in i]]


# #display in 2 columns
# col1, col2 = st.columns(2)
# col1.table(fighter_1_promo)
# col2.table(fighter_2_promo)


# # Load and Display Fight Results
# fighter_1_fight_results_file = [i for i in fighter_1_files if 'fight_results' in i][0]
# fighter_2_fight_results_file = [i for i in fighter_2_files if 'fight_results' in i][0]

# # load and display
# fighter_1_fight_results = pd.read_csv(home + '/tapology/fighters/' + fighter_1_fight_results_file)
# fighter_2_fight_results = pd.read_csv(home + '/tapology/fighters/' + fighter_2_fight_results_file)

# # # drop if cancelled bout
# # fighter_1_fight_results = fighter_1_fight_results[~fighter_1_fight_results['Fight Summary'].str.contains('Cancelled')]
# # fighter_2_fight_results = fighter_2_fight_results[~fighter_2_fight_results['Fight Summary'].str.contains('Cancelled')]

# # Re-arrange columns to be Opponent Name, Fight Date, Fight Summary, Event, and then the rest
# fighter_1_fight_results = fighter_1_fight_results[['Opponent Name', 'Fight Date', 'Fight Summary', 'Event'] + [col for col in fighter_1_fight_results.columns if col not in ['Opponent Name', 'Fight Date', 'Fight Summary', 'Event']]]
# fighter_2_fight_results = fighter_2_fight_results[['Opponent Name', 'Fight Date', 'Fight Summary', 'Event'] + [col for col in fighter_2_fight_results.columns if col not in ['Opponent Name', 'Fight Date', 'Fight Summary', 'Event']]]

# # add line
# st.write('---')

# st.subheader('Fight Results')

# # display in 2 columns
# col1, col2 = st.columns(2)
# col1.write(fighter_1_fight_results)
# col2.write(fighter_2_fight_results)












# ##    SCRAPE ODDS       ## 
# st.subheader('DraftKings Odds')
# st.write('---')

# # add button to request odds
# if st.button('Scrape Odds'):


#     # add button to scrape odds
#     url = 'https://sportsbook.draftkings.com/leagues/mma/ufc'

#     # load driver
#     driver_path = '/Users/travisroyce/Library/CloudStorage/OneDrive-Personal/Data Science/Personal_Projects/Sports/UFC_Prediction_V2/chromedriver'
#     driver = webdriver.Chrome(executable_path=driver_path)
#     driver.get(url)
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')

#     # get all tables
#     tables = soup.find_all('table')
#     # open first table
#     t1 = pd.read_html(str(tables[0]))[0]

#     # grab all links from table 1
#     links = []
#     for link in tables[0].find_all('a'):
#         links.append(link.get('href'))

#     # drop all items in list with sgpmode in it
#     links = [x for x in links if 'sgpmode' not in x]
#     #links to df
#     links_df = pd.DataFrame(links, columns=['links'])
#     # reindex
#     links_df.reset_index(drop=True, inplace=True)

#     # add links from links_df to the main df by index
#     merged_df = pd.merge(t1, links_df, left_index=True, right_index=True)
#     # get first column name
#     col_name = merged_df.columns[0]
#     # change it to 'Date - Fighter'
#     merged_df.rename(columns={col_name:'Date - Fighter'}, inplace=True)

#     # Split the 'Date - Fighter' column into two columns at 'PM' OR 'AM'
#     merged_df[['Time', 'Fighter']] = merged_df['Date - Fighter'].str.split('PM|AM', expand=True)
#     # Drop the 'Date - Fighter' column
#     merged_df.drop(columns=['Date - Fighter'], inplace=True)
#     # drop the Point Spread column
#     merged_df.drop(columns=['Point Spread'], inplace=True)
#     # New column for Rounds
#     merged_df['Rounds'] = merged_df['Total Rounds'].str[0:5]
#     # New column for Round Odds
#     merged_df['Round Odds'] = merged_df['Total Rounds'].str[5:]
#     # drop the Total Rounds column
#     merged_df.drop(columns=['Total Rounds'], inplace=True)
#     # Move Moneyline and links to right side of df
#     cols_at_end = ['Moneyline', 'links']
#     merged_df = merged_df[[c for c in merged_df if c not in cols_at_end]
#             + [c for c in cols_at_end if c in merged_df]]

#     # add the 'https://www.sportsbook.draftkings.com' to the links
#     merged_df['links'] = 'https://www.sportsbook.draftkings.com' + merged_df['links']

#     #st.table(merged_df)

#     # TO Get the specific odds, add:
#     # Popular:  ?category=odds&subcategory=popular to the end of the url
#     # Fight Lines: ?category=odds&subcategory=fight-lines
#     # Winning Method: ?category=odds&subcategory=winning-method
#     # Parlays: ?category=odds&subcategory=fight-parlays
#     # Fight Props: ?category=odds&subcategory=fight-props
#     # Round Props: ?category=odds&subcategory=round-props

#     # filter merged_df to only show selected fight
#     selected_fight = merged_df[merged_df['Fighter'].str.contains(selected_fighter_1_last_name) | merged_df['Fighter'].str.contains(selected_fighter_2_last_name)]
#     st.table(selected_fight)

#     # get top link in selected fight
#     selected_fight_link = selected_fight['links'].values[0]
#     selected_fight_popular_link = selected_fight_link + '?category=odds&subcategory=popular'
#     selected_fight_fight_lines_link = selected_fight_link + '?category=odds&subcategory=fight-lines'
#     selected_fight_winning_method_link = selected_fight_link + '?category=odds&subcategory=winning-method'
#     selected_fight_fight_parlays_link = selected_fight_link + '?category=odds&subcategory=fight-parlays'
#     selected_fight_fight_props_link = selected_fight_link + '?category=odds&subcategory=fight-props'
#     selected_fight_round_props_link = selected_fight_link + '?category=odds&subcategory=round-props'

#     # drop www from links
#     selected_fight_popular_link = selected_fight_popular_link.replace('www.', '')
#     selected_fight_fight_lines_link = selected_fight_fight_lines_link.replace('www.', '')
#     selected_fight_winning_method_link = selected_fight_winning_method_link.replace('www.', '')
#     selected_fight_fight_parlays_link = selected_fight_fight_parlays_link.replace('www.', '')
#     selected_fight_fight_props_link = selected_fight_fight_props_link.replace('www.', '')
#     selected_fight_round_props_link = selected_fight_round_props_link.replace('www.', '')

#     # scrape popular
#     driver.get(selected_fight_fight_lines_link)
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
#     # find div class sportsbook-responsive-card-container__body
#     div = soup.find('div', {'class': 'sportsbook-responsive-card-container__body'})
#     # print all text in div
#     # for each div in div, print the text
#     for div in div.find_all('div', {'class': 'sportsbook-event-accordion__wrapper expanded'}):
#         st.write(div.text)


#     # function to convert vegas odds to implied probability
#     def odds_to_prob(odds):
#         odds = float(odds)
#         if (odds > 0):
#             prob = round(1/(odds/100 + 1),3) * 100
#             prob = str(round(prob, 3)) + '%'
#             return prob
#         else:
#             prob = round(1 - 1/(-odds/100 + 1),3)*100
#             prob = str(round(prob, 3)) + '%'
#             return prob











# # # Assign Height and Length Values
# # try:
# #     dif = a_height - b_height
# #     dif2 = a_reach - b_reach
# #     dif3 = a_leg - b_leg


# #     col1, col2 = st.columns(2)
# #     with col1:
# #         st.subheader(selected_fighter_1)
# #         st.image(fighter1_img, height = 500, use_column_width=True)
# #         st.metric(label = 'Vegas Odds', value=next_event['fighter1_odds'][next_event['fighter1'] == selected_fighter_1].values[0])
# #         st.metric(label = 'Odds-Implied Probability', 
# #                     value=odds_to_prob(next_event['fighter1_odds'][next_event['fighter1'] == selected_fighter_1].values[0]))
# #         st.metric(label = 'Height', value=a_height, delta = dif)
# #         st.metric(label = 'Reach', value=a_reach, delta = dif2)
# #         st.metric(label = 'Leg Reach', value=a_leg, delta = dif3)

# #     with col2:
# #         st.subheader(selected_fighter_2)
# #         st.image(fighter2_img, height = 500, use_column_width=True)
# #         st.metric(label = 'Vegas Odds', value=next_event['fighter2_odds'][next_event['fighter2'] == selected_fighter_2].values[0])
# #         st.metric(label = 'Odds-Implied Probability', 
# #                     value=odds_to_prob(next_event['fighter2_odds'][next_event['fighter2'] == selected_fighter_2].values[0]))
# #         st.metric(label = 'Height', value=b_height, delta = -dif)
# #         st.metric(label = 'Reach', value=b_reach, delta = -dif2)
# #         st.metric(label = 'Leg Reach', value=b_leg, delta = -dif3)
# # except: 
# #     st.markdown('THERES A PROBLEM WITH ONE OF THE FIGHTERS GIVEN METRICS... CALL CUSTOMER SUPPORT OR SOMETHING')


# # st.write(next_eventz)

# # next_eventz['event_date'] = pd.to_datetime(next_eventz['event_date']).dt.date
# # d_o_e = next_eventz['event_date'].values[0]
# # doe = d_o_e.strftime('%Y-%m-%d')
# # # if fight is today
# # today = datetime.today().strftime('%Y-%m-%d')

# # fighter_urls = get_fighter_urls(next_eventz['event_url'].values[0])

# # #
# # nfd = pd.read_csv(home + 'final/next_fights/'+ doe + '.csv')
# # #replace na with 0
# # nfd.fillna(0, inplace=True)



# # next_fight_df = nfd
# # next_fight_df = next_fight_df.fillna(0)
# # this_fight_df= next_fight_df[next_fight_df['Fighter_A'] == selected_fighter_1]


# # put columns in proper order
# proper_order = ['Fighter_A_Odds',
#  'Fighter_B_Odds',
#  'Fighter_A_Odds_Change',
#  'Fighter_B_Odds_Change',
#  'Dif_Odds',
#  'A_Rolling_Kd_mean',
#  'B_Rolling_Kd_mean',
#  'A_Rolling_Kd_std',
#  'B_Rolling_Kd_std',
#  'A_Rolling_Kd_median',
#  'B_Rolling_Kd_median',
#  'A_Rolling_Sig_strike_land_mean',
#  'B_Rolling_Sig_strike_land_mean',
#  'A_Rolling_Sig_strike_land_std',
#  'B_Rolling_Sig_strike_land_std',
#  'A_Rolling_Sig_strike_land_median',
#  'B_Rolling_Sig_strike_land_median',
#  'A_Rolling_Sig_strike_att_mean',
#  'B_Rolling_Sig_strike_att_mean',
#  'A_Rolling_Sig_strike_att_std',
#  'B_Rolling_Sig_strike_att_std',
#  'A_Rolling_Sig_strike_att_median',
#  'B_Rolling_Sig_strike_att_median',
#  'A_Rolling_Sig_strike_percent_mean',
#  'B_Rolling_Sig_strike_percent_mean',
#  'A_Rolling_Sig_strike_percent_std',
#  'B_Rolling_Sig_strike_percent_std',
#  'A_Rolling_Sig_strike_percent_median',
#  'B_Rolling_Sig_strike_percent_median',
#  'A_Rolling_Total_Strikes_land_mean',
#  'B_Rolling_Total_Strikes_land_mean',
#  'A_Rolling_Total_Strikes_land_std',
#  'B_Rolling_Total_Strikes_land_std',
#  'A_Rolling_Total_Strikes_land_median',
#  'B_Rolling_Total_Strikes_land_median',
#  'A_Rolling_Total_Strikes_att_mean',
#  'B_Rolling_Total_Strikes_att_mean',
#  'A_Rolling_Total_Strikes_att_std',
#  'B_Rolling_Total_Strikes_att_std',
#  'A_Rolling_Total_Strikes_att_median',
#  'B_Rolling_Total_Strikes_att_median',
#  'A_Rolling_Total_Strikes_percent_mean',
#  'B_Rolling_Total_Strikes_percent_mean',
#  'A_Rolling_Total_Strikes_percent_std',
#  'B_Rolling_Total_Strikes_percent_std',
#  'A_Rolling_Total_Strikes_percent_median',
#  'B_Rolling_Total_Strikes_percent_median',
#  'A_Rolling_Takedowns_land_mean',
#  'B_Rolling_Takedowns_land_mean',
#  'A_Rolling_Takedowns_land_std',
#  'B_Rolling_Takedowns_land_std',
#  'A_Rolling_Takedowns_land_median',
#  'B_Rolling_Takedowns_land_median',
#  'A_Rolling_Takedowns_att_mean',
#  'B_Rolling_Takedowns_att_mean',
#  'A_Rolling_Takedowns_att_std',
#  'B_Rolling_Takedowns_att_std',
#  'A_Rolling_Takedowns_att_median',
#  'B_Rolling_Takedowns_att_median',
#  'A_Rolling_Takedown_percent_mean',
#  'B_Rolling_Takedown_percent_mean',
#  'A_Rolling_Takedown_percent_std',
#  'B_Rolling_Takedown_percent_std',
#  'A_Rolling_Takedown_percent_median',
#  'B_Rolling_Takedown_percent_median',
#  'A_Rolling_Sub_Attempts_land_mean',
#  'B_Rolling_Sub_Attempts_land_mean',
#  'A_Rolling_Sub_Attempts_land_std',
#  'B_Rolling_Sub_Attempts_land_std',
#  'A_Rolling_Sub_Attempts_land_median',
#  'B_Rolling_Sub_Attempts_land_median',
#  'A_Rolling_Sub_Attempts_att_mean',
#  'B_Rolling_Sub_Attempts_att_mean',
#  'A_Rolling_Sub_Attempts_att_std',
#  'B_Rolling_Sub_Attempts_att_std',
#  'A_Rolling_Sub_Attempts_att_median',
#  'B_Rolling_Sub_Attempts_att_median',
#  'A_Rolling_Rev_mean',
#  'B_Rolling_Rev_mean',
#  'A_Rolling_Rev_std',
#  'B_Rolling_Rev_std',
#  'A_Rolling_Rev_median',
#  'B_Rolling_Rev_median',
#  'A_Rolling_Ctrl_time_min_mean',
#  'B_Rolling_Ctrl_time_min_mean',
#  'A_Rolling_Ctrl_time_min_std',
#  'B_Rolling_Ctrl_time_min_std',
#  'A_Rolling_Ctrl_time_min_median',
#  'B_Rolling_Ctrl_time_min_median',
#  'A_Rolling_Ctrl_time_sec_mean',
#  'B_Rolling_Ctrl_time_sec_mean',
#  'A_Rolling_Ctrl_time_sec_std',
#  'B_Rolling_Ctrl_time_sec_std',
#  'A_Rolling_Ctrl_time_sec_median',
#  'B_Rolling_Ctrl_time_sec_median',
#  'A_Rolling_Ctrl_time_tot_mean',
#  'B_Rolling_Ctrl_time_tot_mean',
#  'A_Rolling_Ctrl_time_tot_std',
#  'B_Rolling_Ctrl_time_tot_std',
#  'A_Rolling_Ctrl_time_tot_median',
#  'B_Rolling_Ctrl_time_tot_median',
#  'A_Rolling_Head_Strikes_land_mean',
#  'B_Rolling_Head_Strikes_land_mean',
#  'A_Rolling_Head_Strikes_land_std',
#  'B_Rolling_Head_Strikes_land_std',
#  'A_Rolling_Head_Strikes_land_median',
#  'B_Rolling_Head_Strikes_land_median',
#  'A_Rolling_Head_Strikes_att_mean',
#  'B_Rolling_Head_Strikes_att_mean',
#  'A_Rolling_Head_Strikes_att_std',
#  'B_Rolling_Head_Strikes_att_std',
#  'A_Rolling_Head_Strikes_att_median',
#  'B_Rolling_Head_Strikes_att_median',
#  'A_Rolling_Head_Strikes_percent_mean',
#  'B_Rolling_Head_Strikes_percent_mean',
#  'A_Rolling_Head_Strikes_percent_std',
#  'B_Rolling_Head_Strikes_percent_std',
#  'A_Rolling_Head_Strikes_percent_median',
#  'B_Rolling_Head_Strikes_percent_median',
#  'A_Rolling_Body_Strikes_land_mean',
#  'B_Rolling_Body_Strikes_land_mean',
#  'A_Rolling_Body_Strikes_land_std',
#  'B_Rolling_Body_Strikes_land_std',
#  'A_Rolling_Body_Strikes_land_median',
#  'B_Rolling_Body_Strikes_land_median',
#  'A_Rolling_Body_Strikes_att_mean',
#  'B_Rolling_Body_Strikes_att_mean',
#  'A_Rolling_Body_Strikes_att_std',
#  'B_Rolling_Body_Strikes_att_std',
#  'A_Rolling_Body_Strikes_att_median',
#  'B_Rolling_Body_Strikes_att_median',
#  'A_Rolling_Body_Strikes_percent_mean',
#  'B_Rolling_Body_Strikes_percent_mean',
#  'A_Rolling_Body_Strikes_percent_std',
#  'B_Rolling_Body_Strikes_percent_std',
#  'A_Rolling_Body_Strikes_percent_median',
#  'B_Rolling_Body_Strikes_percent_median',
#  'A_Rolling_Leg_Strikes_land_mean',
#  'B_Rolling_Leg_Strikes_land_mean',
#  'A_Rolling_Leg_Strikes_land_std',
#  'B_Rolling_Leg_Strikes_land_std',
#  'A_Rolling_Leg_Strikes_land_median',
#  'B_Rolling_Leg_Strikes_land_median',
#  'A_Rolling_Leg_Strikes_att_mean',
#  'B_Rolling_Leg_Strikes_att_mean',
#  'A_Rolling_Leg_Strikes_att_std',
#  'B_Rolling_Leg_Strikes_att_std',
#  'A_Rolling_Leg_Strikes_att_median',
#  'B_Rolling_Leg_Strikes_att_median',
#  'A_Rolling_Leg_Strikes_percent_mean',
#  'B_Rolling_Leg_Strikes_percent_mean',
#  'A_Rolling_Leg_Strikes_percent_std',
#  'B_Rolling_Leg_Strikes_percent_std',
#  'A_Rolling_Leg_Strikes_percent_median',
#  'B_Rolling_Leg_Strikes_percent_median',
#  'A_Rolling_Distance_Strikes_land_mean',
#  'B_Rolling_Distance_Strikes_land_mean',
#  'A_Rolling_Distance_Strikes_land_std',
#  'B_Rolling_Distance_Strikes_land_std',
#  'A_Rolling_Distance_Strikes_land_median',
#  'B_Rolling_Distance_Strikes_land_median',
#  'A_Rolling_Distance_Strikes_att_mean',
#  'B_Rolling_Distance_Strikes_att_mean',
#  'A_Rolling_Distance_Strikes_att_std',
#  'B_Rolling_Distance_Strikes_att_std',
#  'A_Rolling_Distance_Strikes_att_median',
#  'B_Rolling_Distance_Strikes_att_median',
#  'A_Rolling_Distance_Strikes_percent_mean',
#  'B_Rolling_Distance_Strikes_percent_mean',
#  'A_Rolling_Distance_Strikes_percent_std',
#  'B_Rolling_Distance_Strikes_percent_std',
#  'A_Rolling_Distance_Strikes_percent_median',
#  'B_Rolling_Distance_Strikes_percent_median',
#  'A_Rolling_Clinch_Strikes_land_mean',
#  'B_Rolling_Clinch_Strikes_land_mean',
#  'A_Rolling_Clinch_Strikes_land_std',
#  'B_Rolling_Clinch_Strikes_land_std',
#  'A_Rolling_Clinch_Strikes_land_median',
#  'B_Rolling_Clinch_Strikes_land_median',
#  'A_Rolling_Clinch_Strikes_att_mean',
#  'B_Rolling_Clinch_Strikes_att_mean',
#  'A_Rolling_Clinch_Strikes_att_std',
#  'B_Rolling_Clinch_Strikes_att_std',
#  'A_Rolling_Clinch_Strikes_att_median',
#  'B_Rolling_Clinch_Strikes_att_median',
#  'A_Rolling_Clinch_Strikes_percent_mean',
#  'B_Rolling_Clinch_Strikes_percent_mean',
#  'A_Rolling_Clinch_Strikes_percent_std',
#  'B_Rolling_Clinch_Strikes_percent_std',
#  'A_Rolling_Clinch_Strikes_percent_median',
#  'B_Rolling_Clinch_Strikes_percent_median',
#  'A_Rolling_Ground_Strikes_land_mean',
#  'B_Rolling_Ground_Strikes_land_mean',
#  'A_Rolling_Ground_Strikes_land_std',
#  'B_Rolling_Ground_Strikes_land_std',
#  'A_Rolling_Ground_Strikes_land_median',
#  'B_Rolling_Ground_Strikes_land_median',
#  'A_Rolling_Ground_Strikes_att_mean',
#  'B_Rolling_Ground_Strikes_att_mean',
#  'A_Rolling_Ground_Strikes_att_std',
#  'B_Rolling_Ground_Strikes_att_std',
#  'A_Rolling_Ground_Strikes_att_median',
#  'B_Rolling_Ground_Strikes_att_median',
#  'A_Rolling_Ground_Strikes_percent_mean',
#  'B_Rolling_Ground_Strikes_percent_mean',
#  'A_Rolling_Ground_Strikes_percent_std',
#  'B_Rolling_Ground_Strikes_percent_std',
#  'A_Rolling_Ground_Strikes_percent_median',
#  'B_Rolling_Ground_Strikes_percent_median',
#  'A_topdown_Avg_Kd',
#  'B_topdown_Avg_Kd',
#  'A_topdown_Avg_Sig_strike_land',
#  'B_topdown_Avg_Sig_strike_land',
#  'A_topdown_Avg_Sig_strike_att',
#  'B_topdown_Avg_Sig_strike_att',
#  'A_topdown_Avg_Sig_strike_percent',
#  'B_topdown_Avg_Sig_strike_percent',
#  'A_topdown_Avg_Total_Strikes_land',
#  'B_topdown_Avg_Total_Strikes_land',
#  'A_topdown_Avg_Total_Strikes_att',
#  'B_topdown_Avg_Total_Strikes_att',
#  'A_topdown_Avg_Total_Strikes_percent',
#  'B_topdown_Avg_Total_Strikes_percent',
#  'A_topdown_Avg_Takedowns_land',
#  'B_topdown_Avg_Takedowns_land',
#  'A_topdown_Avg_Takedowns_att',
#  'B_topdown_Avg_Takedowns_att',
#  'A_topdown_Avg_Takedown_percent',
#  'B_topdown_Avg_Takedown_percent',
#  'A_topdown_Avg_Sub_Attempts_land',
#  'B_topdown_Avg_Sub_Attempts_land',
#  'A_topdown_Avg_Sub_Attempts_att',
#  'B_topdown_Avg_Sub_Attempts_att',
#  'A_topdown_Avg_Rev',
#  'B_topdown_Avg_Rev',
#  'A_topdown_Avg_Ctrl_time_min',
#  'B_topdown_Avg_Ctrl_time_min',
#  'A_topdown_Avg_Ctrl_time_sec',
#  'B_topdown_Avg_Ctrl_time_sec',
#  'A_topdown_Avg_Ctrl_time_tot',
#  'B_topdown_Avg_Ctrl_time_tot',
#  'A_topdown_Avg_Head_Strikes_land',
#  'B_topdown_Avg_Head_Strikes_land',
#  'A_topdown_Avg_Head_Strikes_att',
#  'B_topdown_Avg_Head_Strikes_att',
#  'A_topdown_Avg_Head_Strikes_percent',
#  'B_topdown_Avg_Head_Strikes_percent',
#  'A_topdown_Avg_Body_Strikes_land',
#  'B_topdown_Avg_Body_Strikes_land',
#  'A_topdown_Avg_Body_Strikes_att',
#  'B_topdown_Avg_Body_Strikes_att',
#  'A_topdown_Avg_Body_Strikes_percent',
#  'B_topdown_Avg_Body_Strikes_percent',
#  'A_topdown_Avg_Leg_Strikes_land',
#  'B_topdown_Avg_Leg_Strikes_land',
#  'A_topdown_Avg_Leg_Strikes_att',
#  'B_topdown_Avg_Leg_Strikes_att',
#  'A_topdown_Avg_Leg_Strikes_percent',
#  'B_topdown_Avg_Leg_Strikes_percent',
#  'A_topdown_Avg_Distance_Strikes_land',
#  'B_topdown_Avg_Distance_Strikes_land',
#  'A_topdown_Avg_Distance_Strikes_att',
#  'B_topdown_Avg_Distance_Strikes_att',
#  'A_topdown_Avg_Distance_Strikes_percent',
#  'B_topdown_Avg_Distance_Strikes_percent',
#  'A_topdown_Avg_Clinch_Strikes_land',
#  'B_topdown_Avg_Clinch_Strikes_land',
#  'A_topdown_Avg_Clinch_Strikes_att',
#  'B_topdown_Avg_Clinch_Strikes_att',
#  'A_topdown_Avg_Clinch_Strikes_percent',
#  'B_topdown_Avg_Clinch_Strikes_percent',
#  'A_topdown_Avg_Ground_Strikes_land',
#  'B_topdown_Avg_Ground_Strikes_land',
#  'A_topdown_Avg_Ground_Strikes_att',
#  'B_topdown_Avg_Ground_Strikes_att',
#  'A_topdown_Avg_Ground_Strikes_percent',
#  'B_topdown_Avg_Ground_Strikes_percent',
#  'A_Opp_Avg_Kd',
#  'B_Opp_Avg_Kd',
#  'A_Opp_Avg_Sig_strike_land',
#  'B_Opp_Avg_Sig_strike_land',
#  'A_Opp_Avg_Sig_strike_att',
#  'B_Opp_Avg_Sig_strike_att',
#  'A_Opp_Avg_Sig_strike_percent',
#  'B_Opp_Avg_Sig_strike_percent',
#  'A_Opp_Avg_Total_Strikes_land',
#  'B_Opp_Avg_Total_Strikes_land',
#  'A_Opp_Avg_Total_Strikes_att',
#  'B_Opp_Avg_Total_Strikes_att',
#  'A_Opp_Avg_Total_Strikes_percent',
#  'B_Opp_Avg_Total_Strikes_percent',
#  'A_Opp_Avg_Takedowns_land',
#  'B_Opp_Avg_Takedowns_land',
#  'A_Opp_Avg_Takedowns_att',
#  'B_Opp_Avg_Takedowns_att',
#  'A_Opp_Avg_Takedown_percent',
#  'B_Opp_Avg_Takedown_percent',
#  'A_Opp_Avg_Sub_Attempts_land',
#  'B_Opp_Avg_Sub_Attempts_land',
#  'A_Opp_Avg_Sub_Attempts_att',
#  'B_Opp_Avg_Sub_Attempts_att',
#  'A_Opp_Avg_Rev',
#  'B_Opp_Avg_Rev',
#  'A_Opp_Avg_Ctrl_time_min',
#  'B_Opp_Avg_Ctrl_time_min',
#  'A_Opp_Avg_Ctrl_time_sec',
#  'B_Opp_Avg_Ctrl_time_sec',
#  'A_Opp_Avg_Ctrl_time_tot',
#  'B_Opp_Avg_Ctrl_time_tot',
#  'A_Opp_Avg_Head_Strikes_land',
#  'B_Opp_Avg_Head_Strikes_land',
#  'A_Opp_Avg_Head_Strikes_att',
#  'B_Opp_Avg_Head_Strikes_att',
#  'A_Opp_Avg_Head_Strikes_percent',
#  'B_Opp_Avg_Head_Strikes_percent',
#  'A_Opp_Avg_Body_Strikes_land',
#  'B_Opp_Avg_Body_Strikes_land',
#  'A_Opp_Avg_Body_Strikes_att',
#  'B_Opp_Avg_Body_Strikes_att',
#  'A_Opp_Avg_Body_Strikes_percent',
#  'B_Opp_Avg_Body_Strikes_percent',
#  'A_Opp_Avg_Leg_Strikes_land',
#  'B_Opp_Avg_Leg_Strikes_land',
#  'A_Opp_Avg_Leg_Strikes_att',
#  'B_Opp_Avg_Leg_Strikes_att',
#  'A_Opp_Avg_Leg_Strikes_percent',
#  'B_Opp_Avg_Leg_Strikes_percent',
#  'A_Opp_Avg_Distance_Strikes_land',
#  'B_Opp_Avg_Distance_Strikes_land',
#  'A_Opp_Avg_Distance_Strikes_att',
#  'B_Opp_Avg_Distance_Strikes_att',
#  'A_Opp_Avg_Distance_Strikes_percent',
#  'B_Opp_Avg_Distance_Strikes_percent',
#  'A_Opp_Avg_Clinch_Strikes_land',
#  'B_Opp_Avg_Clinch_Strikes_land',
#  'A_Opp_Avg_Clinch_Strikes_att',
#  'B_Opp_Avg_Clinch_Strikes_att',
#  'A_Opp_Avg_Clinch_Strikes_percent',
#  'B_Opp_Avg_Clinch_Strikes_percent',
#  'A_Opp_Avg_Ground_Strikes_land',
#  'B_Opp_Avg_Ground_Strikes_land',
#  'A_Opp_Avg_Ground_Strikes_att',
#  'B_Opp_Avg_Ground_Strikes_att',
#  'A_Opp_Avg_Ground_Strikes_percent',
#  'B_Opp_Avg_Ground_Strikes_percent',
#  'Dif_Rolling_Kd_mean',
#  'Dif_Rolling_Sig_strike_land_mean',
#  'Dif_Rolling_Sig_strike_att_mean',
#  'Dif_Rolling_Sig_strike_percent_mean',
#  'Dif_Rolling_Total_Strikes_land_mean',
#  'Dif_Rolling_Total_Strikes_att_mean',
#  'Dif_Rolling_Total_Strikes_percent_mean',
#  'Dif_Rolling_Takedowns_land_mean',
#  'Dif_Rolling_Takedowns_att_mean',
#  'Dif_Rolling_Takedown_percent_mean',
#  'Dif_Rolling_Sub_Attempts_land_mean',
#  'Dif_Rolling_Sub_Attempts_att_mean',
#  'Dif_Rolling_Rev_mean',
#  'Dif_Rolling_Ctrl_time_min_mean',
#  'Dif_Rolling_Ctrl_time_sec_mean',
#  'Dif_Rolling_Ctrl_time_tot_mean',
#  'Dif_Rolling_Head_Strikes_land_mean',
#  'Dif_Rolling_Head_Strikes_att_mean',
#  'Dif_Rolling_Head_Strikes_percent_mean',
#  'Dif_Rolling_Body_Strikes_land_mean',
#  'Dif_Rolling_Body_Strikes_att_mean',
#  'Dif_Rolling_Body_Strikes_percent_mean',
#  'Dif_Rolling_Leg_Strikes_land_mean',
#  'Dif_Rolling_Leg_Strikes_att_mean',
#  'Dif_Rolling_Leg_Strikes_percent_mean',
#  'Dif_Rolling_Distance_Strikes_land_mean',
#  'Dif_Rolling_Distance_Strikes_att_mean',
#  'Dif_Rolling_Distance_Strikes_percent_mean',
#  'Dif_Rolling_Clinch_Strikes_land_mean',
#  'Dif_Rolling_Clinch_Strikes_att_mean',
#  'Dif_Rolling_Clinch_Strikes_percent_mean',
#  'Dif_Rolling_Ground_Strikes_land_mean',
#  'Dif_Rolling_Ground_Strikes_att_mean',
#  'Dif_Rolling_Ground_Strikes_percent_mean',
#  'Dif_Rolling_Kd_median',
#  'Dif_Rolling_Sig_strike_land_median',
#  'Dif_Rolling_Sig_strike_att_median',
#  'Dif_Rolling_Sig_strike_percent_median',
#  'Dif_Rolling_Total_Strikes_land_median',
#  'Dif_Rolling_Total_Strikes_att_median',
#  'Dif_Rolling_Total_Strikes_percent_median',
#  'Dif_Rolling_Takedowns_land_median',
#  'Dif_Rolling_Takedowns_att_median',
#  'Dif_Rolling_Takedown_percent_median',
#  'Dif_Rolling_Sub_Attempts_land_median',
#  'Dif_Rolling_Sub_Attempts_att_median',
#  'Dif_Rolling_Rev_median',
#  'Dif_Rolling_Ctrl_time_min_median',
#  'Dif_Rolling_Ctrl_time_sec_median',
#  'Dif_Rolling_Ctrl_time_tot_median',
#  'Dif_Rolling_Head_Strikes_land_median',
#  'Dif_Rolling_Head_Strikes_att_median',
#  'Dif_Rolling_Head_Strikes_percent_median',
#  'Dif_Rolling_Body_Strikes_land_median',
#  'Dif_Rolling_Body_Strikes_att_median',
#  'Dif_Rolling_Body_Strikes_percent_median',
#  'Dif_Rolling_Leg_Strikes_land_median',
#  'Dif_Rolling_Leg_Strikes_att_median',
#  'Dif_Rolling_Leg_Strikes_percent_median',
#  'Dif_Rolling_Distance_Strikes_land_median',
#  'Dif_Rolling_Distance_Strikes_att_median',
#  'Dif_Rolling_Distance_Strikes_percent_median',
#  'Dif_Rolling_Clinch_Strikes_land_median',
#  'Dif_Rolling_Clinch_Strikes_att_median',
#  'Dif_Rolling_Clinch_Strikes_percent_median',
#  'Dif_Rolling_Ground_Strikes_land_median',
#  'Dif_Rolling_Ground_Strikes_att_median',
#  'Dif_Rolling_Ground_Strikes_percent_median',
#  'Dif_Rolling_Kd_std',
#  'Dif_Rolling_Sig_strike_land_std',
#  'Dif_Rolling_Sig_strike_att_std',
#  'Dif_Rolling_Sig_strike_percent_std',
#  'Dif_Rolling_Total_Strikes_land_std',
#  'Dif_Rolling_Total_Strikes_att_std',
#  'Dif_Rolling_Total_Strikes_percent_std',
#  'Dif_Rolling_Takedowns_land_std',
#  'Dif_Rolling_Takedowns_att_std',
#  'Dif_Rolling_Takedown_percent_std',
#  'Dif_Rolling_Sub_Attempts_land_std',
#  'Dif_Rolling_Sub_Attempts_att_std',
#  'Dif_Rolling_Rev_std',
#  'Dif_Rolling_Ctrl_time_min_std',
#  'Dif_Rolling_Ctrl_time_sec_std',
#  'Dif_Rolling_Ctrl_time_tot_std',
#  'Dif_Rolling_Head_Strikes_land_std',
#  'Dif_Rolling_Head_Strikes_att_std',
#  'Dif_Rolling_Head_Strikes_percent_std',
#  'Dif_Rolling_Body_Strikes_land_std',
#  'Dif_Rolling_Body_Strikes_att_std',
#  'Dif_Rolling_Body_Strikes_percent_std',
#  'Dif_Rolling_Leg_Strikes_land_std',
#  'Dif_Rolling_Leg_Strikes_att_std',
#  'Dif_Rolling_Leg_Strikes_percent_std',
#  'Dif_Rolling_Distance_Strikes_land_std',
#  'Dif_Rolling_Distance_Strikes_att_std',
#  'Dif_Rolling_Distance_Strikes_percent_std',
#  'Dif_Rolling_Clinch_Strikes_land_std',
#  'Dif_Rolling_Clinch_Strikes_att_std',
#  'Dif_Rolling_Clinch_Strikes_percent_std',
#  'Dif_Rolling_Ground_Strikes_land_std',
#  'Dif_Rolling_Ground_Strikes_att_std',
#  'Dif_Rolling_Ground_Strikes_percent_std',
#  'A_Height',
#  'B_Height',
#  'Dif_Height',
#  'A_Reach',
#  'B_Reach',
#  'Dif_Reach',
#  'A_Leg_Reach',
#  'B_Leg_Reach',
#  'Dif_Leg_Reach',
#  'A_Reach_NA',
#  'B_Reach_NA',
#  'Reach_NA',
#  'A_Leg_Reach_NA',
#  'B_Leg_Reach_NA',
#  'Leg_Reach_NA',
#  'fight_weightclass',
#  'A_Fight_in_Typical_Weightclass',
#  'B_Fight_in_Typical_Weightclass',
#  'Leg_Reach_Dif',
#  'Reach_Dif',
#  'A_Ape_Index',
#  'B_Ape_Index',
#  'A_Leg_Index',
#  'B_Leg_Index',
#  'A_Leg_to_Wing_Index',
#  'B_Leg_to_Wing_Index',
#  'favorite?',
#  'A_Total_UFC_Fights',
#  'B_Total_UFC_Fights',
#  'Dif_Total_UFC_Fights',
#  'A_UFC_Wins',
#  'B_UFC_Wins',
#  'Dif_UFC_Wins',
#  'A_UFC_Losses',
#  'B_UFC_Losses',
#  'Dif_UFC_Losses',
#  'A_UFC_Win_Percentage',
#  'B_UFC_Win_Percentage',
#  'Dif_UFC_Win_Percentage',
#  'A_Last5_Win_Percentage',
#  'B_Last5_Win_Percentage',
#  'Dif_Last5_Win_Percentage',
#  'A_Last3_Win_Percentage',
#  'B_Last3_Win_Percentage',
#  'Dif_Last3_Win_Percentage',
#  'A_Win_By_KO_Percentage',
#  'B_Win_By_KO_Percentage',
#  'Dif_Win_By_KO_Percentage',
#  'A_Loss_By_KO_Percentage',
#  'B_Loss_By_KO_Percentage',
#  'Dif_Loss_By_KO_Percentage',
#  'A_Win_By_Decision_Percentage',
#  'B_Win_By_Decision_Percentage',
#  'Dif_Win_By_Decision_Percentage',
#  'A_Loss_By_Decision_Percentage',
#  'B_Loss_By_Decision_Percentage',
#  'Dif_Loss_By_Decision_Percentage',
#  'A_UFC_Fight_Time_Seconds',
#  'B_UFC_Fight_Time_Seconds',
#  'Dif_UFC_Fight_Time_Seconds',
#  'A_UFC_Fight_Rounds',
#  'B_UFC_Fight_Rounds',
#  'A_topdown_Avg_Kd_per_round',
#  'A_topdown_Avg_Sig_strike_land_per_round',
#  'A_topdown_Avg_Sig_strike_att_per_round',
#  'A_topdown_Avg_Total_Strikes_land_per_round',
#  'A_topdown_Avg_Total_Strikes_att_per_round',
#  'A_topdown_Avg_Takedowns_land_per_round',
#  'A_topdown_Avg_Takedowns_att_per_round',
#  'A_topdown_Avg_Sub_Attempts_land_per_round',
#  'A_topdown_Avg_Sub_Attempts_att_per_round',
#  'A_topdown_Avg_Rev_per_round',
#  'A_topdown_Avg_Ctrl_time_min_per_round',
#  'A_topdown_Avg_Ctrl_time_sec_per_round',
#  'A_topdown_Avg_Ctrl_time_tot_per_round',
#  'A_topdown_Avg_Head_Strikes_land_per_round',
#  'A_topdown_Avg_Head_Strikes_att_per_round',
#  'A_topdown_Avg_Body_Strikes_land_per_round',
#  'A_topdown_Avg_Body_Strikes_att_per_round',
#  'A_topdown_Avg_Leg_Strikes_land_per_round',
#  'A_topdown_Avg_Leg_Strikes_att_per_round',
#  'A_topdown_Avg_Distance_Strikes_land_per_round',
#  'A_topdown_Avg_Distance_Strikes_att_per_round',
#  'A_topdown_Avg_Clinch_Strikes_land_per_round',
#  'A_topdown_Avg_Clinch_Strikes_att_per_round',
#  'A_topdown_Avg_Ground_Strikes_land_per_round',
#  'A_topdown_Avg_Ground_Strikes_att_per_round',
#  'B_topdown_Avg_Kd_per_round',
#  'B_topdown_Avg_Sig_strike_land_per_round',
#  'B_topdown_Avg_Sig_strike_att_per_round',
#  'B_topdown_Avg_Total_Strikes_land_per_round',
#  'B_topdown_Avg_Total_Strikes_att_per_round',
#  'B_topdown_Avg_Takedowns_land_per_round',
#  'B_topdown_Avg_Takedowns_att_per_round',
#  'B_topdown_Avg_Sub_Attempts_land_per_round',
#  'B_topdown_Avg_Sub_Attempts_att_per_round',
#  'B_topdown_Avg_Rev_per_round',
#  'B_topdown_Avg_Ctrl_time_min_per_round',
#  'B_topdown_Avg_Ctrl_time_sec_per_round',
#  'B_topdown_Avg_Ctrl_time_tot_per_round',
#  'B_topdown_Avg_Head_Strikes_land_per_round',
#  'B_topdown_Avg_Head_Strikes_att_per_round',
#  'B_topdown_Avg_Body_Strikes_land_per_round',
#  'B_topdown_Avg_Body_Strikes_att_per_round',
#  'B_topdown_Avg_Leg_Strikes_land_per_round',
#  'B_topdown_Avg_Leg_Strikes_att_per_round',
#  'B_topdown_Avg_Distance_Strikes_land_per_round',
#  'B_topdown_Avg_Distance_Strikes_att_per_round',
#  'B_topdown_Avg_Clinch_Strikes_land_per_round',
#  'B_topdown_Avg_Clinch_Strikes_att_per_round',
#  'B_topdown_Avg_Ground_Strikes_land_per_round',
#  'B_topdown_Avg_Ground_Strikes_att_per_round',
#  'A_Opp_Avg_Kd_per_round',
#  'A_Opp_Avg_Sig_strike_land_per_round',
#  'A_Opp_Avg_Sig_strike_att_per_round',
#  'A_Opp_Avg_Total_Strikes_land_per_round',
#  'A_Opp_Avg_Total_Strikes_att_per_round',
#  'A_Opp_Avg_Takedowns_land_per_round',
#  'A_Opp_Avg_Takedowns_att_per_round',
#  'A_Opp_Avg_Sub_Attempts_land_per_round',
#  'A_Opp_Avg_Sub_Attempts_att_per_round',
#  'A_Opp_Avg_Rev_per_round',
#  'A_Opp_Avg_Ctrl_time_min_per_round',
#  'A_Opp_Avg_Ctrl_time_sec_per_round',
#  'A_Opp_Avg_Ctrl_time_tot_per_round',
#  'A_Opp_Avg_Head_Strikes_land_per_round',
#  'A_Opp_Avg_Head_Strikes_att_per_round',
#  'A_Opp_Avg_Body_Strikes_land_per_round',
#  'A_Opp_Avg_Body_Strikes_att_per_round',
#  'A_Opp_Avg_Leg_Strikes_land_per_round',
#  'A_Opp_Avg_Leg_Strikes_att_per_round',
#  'A_Opp_Avg_Distance_Strikes_land_per_round',
#  'A_Opp_Avg_Distance_Strikes_att_per_round',
#  'A_Opp_Avg_Clinch_Strikes_land_per_round',
#  'A_Opp_Avg_Clinch_Strikes_att_per_round',
#  'A_Opp_Avg_Ground_Strikes_land_per_round',
#  'A_Opp_Avg_Ground_Strikes_att_per_round',
#  'B_Opp_Avg_Kd_per_round',
#  'B_Opp_Avg_Sig_strike_land_per_round',
#  'B_Opp_Avg_Sig_strike_att_per_round',
#  'B_Opp_Avg_Total_Strikes_land_per_round',
#  'B_Opp_Avg_Total_Strikes_att_per_round',
#  'B_Opp_Avg_Takedowns_land_per_round',
#  'B_Opp_Avg_Takedowns_att_per_round',
#  'B_Opp_Avg_Sub_Attempts_land_per_round',
#  'B_Opp_Avg_Sub_Attempts_att_per_round',
#  'B_Opp_Avg_Rev_per_round',
#  'B_Opp_Avg_Ctrl_time_min_per_round',
#  'B_Opp_Avg_Ctrl_time_sec_per_round',
#  'B_Opp_Avg_Ctrl_time_tot_per_round',
#  'B_Opp_Avg_Head_Strikes_land_per_round',
#  'B_Opp_Avg_Head_Strikes_att_per_round',
#  'B_Opp_Avg_Body_Strikes_land_per_round',
#  'B_Opp_Avg_Body_Strikes_att_per_round',
#  'B_Opp_Avg_Leg_Strikes_land_per_round',
#  'B_Opp_Avg_Leg_Strikes_att_per_round',
#  'B_Opp_Avg_Distance_Strikes_land_per_round',
#  'B_Opp_Avg_Distance_Strikes_att_per_round',
#  'B_Opp_Avg_Clinch_Strikes_land_per_round',
#  'B_Opp_Avg_Clinch_Strikes_att_per_round',
#  'B_Opp_Avg_Ground_Strikes_land_per_round',
#  'B_Opp_Avg_Ground_Strikes_att_per_round',
#  'Dif_topdown_Avg_Kd_per_round',
#  'Dif_topdown_Avg_Sig_strike_land_per_round',
#  'Dif_topdown_Avg_Sig_strike_att_per_round',
#  'Dif_topdown_Avg_Total_Strikes_land_per_round',
#  'Dif_topdown_Avg_Total_Strikes_att_per_round',
#  'Dif_topdown_Avg_Takedowns_land_per_round',
#  'Dif_topdown_Avg_Takedowns_att_per_round',
#  'Dif_topdown_Avg_Sub_Attempts_land_per_round',
#  'Dif_topdown_Avg_Sub_Attempts_att_per_round',
#  'Dif_topdown_Avg_Rev_per_round',
#  'Dif_topdown_Avg_Ctrl_time_min_per_round',
#  'Dif_topdown_Avg_Ctrl_time_sec_per_round',
#  'Dif_topdown_Avg_Ctrl_time_tot_per_round',
#  'Dif_topdown_Avg_Head_Strikes_land_per_round',
#  'Dif_topdown_Avg_Head_Strikes_att_per_round',
#  'Dif_topdown_Avg_Body_Strikes_land_per_round',
#  'Dif_topdown_Avg_Body_Strikes_att_per_round',
#  'Dif_topdown_Avg_Leg_Strikes_land_per_round',
#  'Dif_topdown_Avg_Leg_Strikes_att_per_round',
#  'Dif_topdown_Avg_Distance_Strikes_land_per_round',
#  'Dif_topdown_Avg_Distance_Strikes_att_per_round',
#  'Dif_topdown_Avg_Clinch_Strikes_land_per_round',
#  'Dif_topdown_Avg_Clinch_Strikes_att_per_round',
#  'Dif_topdown_Avg_Ground_Strikes_land_per_round',
#  'Dif_topdown_Avg_Ground_Strikes_att_per_round',
#  'Dif_Opp_Avg_Kd_per_round',
#  'Dif_Opp_Avg_Sig_strike_land_per_round',
#  'Dif_Opp_Avg_Sig_strike_att_per_round',
#  'Dif_Opp_Avg_Total_Strikes_land_per_round',
#  'Dif_Opp_Avg_Total_Strikes_att_per_round',
#  'Dif_Opp_Avg_Takedowns_land_per_round',
#  'Dif_Opp_Avg_Takedowns_att_per_round',
#  'Dif_Opp_Avg_Sub_Attempts_land_per_round',
#  'Dif_Opp_Avg_Sub_Attempts_att_per_round',
#  'Dif_Opp_Avg_Rev_per_round',
#  'Dif_Opp_Avg_Ctrl_time_min_per_round',
#  'Dif_Opp_Avg_Ctrl_time_sec_per_round',
#  'Dif_Opp_Avg_Ctrl_time_tot_per_round',
#  'Dif_Opp_Avg_Head_Strikes_land_per_round',
#  'Dif_Opp_Avg_Head_Strikes_att_per_round',
#  'Dif_Opp_Avg_Body_Strikes_land_per_round',
#  'Dif_Opp_Avg_Body_Strikes_att_per_round',
#  'Dif_Opp_Avg_Leg_Strikes_land_per_round',
#  'Dif_Opp_Avg_Leg_Strikes_att_per_round',
#  'Dif_Opp_Avg_Distance_Strikes_land_per_round',
#  'Dif_Opp_Avg_Distance_Strikes_att_per_round',
#  'Dif_Opp_Avg_Clinch_Strikes_land_per_round',
#  'Dif_Opp_Avg_Clinch_Strikes_att_per_round',
#  'Dif_Opp_Avg_Ground_Strikes_land_per_round',
#  'Dif_Opp_Avg_Ground_Strikes_att_per_round']

# # this_fight_df['Dif_Odds'] = this_fight_df['Fighter_A_Odds'] - this_fight_df['Fighter_B_Odds']

# # final_vect = this_fight_df[proper_order]


# # # load model
# # extra_trees = pickle.load(open('C:\\Users\\Travis\\OneDrive\\Data Science\\Personal_Projects\\Sports\\UFC_Prediction_V2\\models\\SVC.pkl', 'rb'))

# # # Predict
# # prediction = pd.DataFrame(extra_trees.predict(final_vect))
# # prediction = prediction[0].values[0]

# # if prediction == 1:
# #     st.sidebar.header("Predicted Winner: " + selected_fighter_1)
# # if prediction == 0:
# #     st.sidebar.header("Predicted Winner: " + selected_fighter_2)

# # probabilities = extra_trees.predict_proba(final_vect)
# # prob_win = probabilities[0][1]
# # prob_win = round(prob_win * 100,1)
# # prob_lose = probabilities[0][0]
# # prob_lose = round(prob_lose * 100,1)

# # # Display sidebar probabilities
# # st.sidebar.write("")
# # st.sidebar.subheader("Model Predicted Win Probabilities:")
# # st.sidebar.write(selected_fighter_1 + " : " + str(prob_win) + "%")
# # st.sidebar.write(selected_fighter_2 + " : " + str(prob_lose)+ "%")
# # st.sidebar.write("")

# # st.sidebar.subheader('Expected Value of $10:')

# # def american_odds_to_payout(odds):
# #     # make sure odds are numerical
# #     odds = float(odds)
# #     if odds > 0:
# #         return odds/100 + 1
# #     else:
# #         return 100/abs(odds) + 1

# # vegas_odds_1 = next_event['fighter1_odds'][next_event['fighter1'] == selected_fighter_1].values[0]
# # vegas_odds_2 = next_event['fighter2_odds'][next_event['fighter2'] == selected_fighter_2].values[0]

# # american_payout1 = american_odds_to_payout(vegas_odds_1)
# # american_payout2 = american_odds_to_payout(vegas_odds_2)

# # # Expected Value
# # ev1 = (american_payout1 * (prob_win/100 * 10)) - ((prob_lose/100) * 10 * american_payout2)
# # st.sidebar.write(f' {selected_fighter_1} EV: {ev1.round()}')


# # ev2 = ((prob_lose/100) * 10 * american_payout2) - (american_payout1 * (prob_win/100 * 10))
# # st.sidebar.write("")
# # st.sidebar.write(f' {selected_fighter_2} EV: {ev2.round()}')

# # if ev1 > ev2:
# #     st.sidebar.subheader("A Bet on " + selected_fighter_1 + " is positive EV")
# # else:
# #     st.sidebar.subheader("A Bet on " + selected_fighter_2+ " is positive EV")



# # ###########        MATCHUPS      ###############


# # st.sidebar.header('Selected UFC Event: '+ selected_event)

# # ne = next_event.rename(columns={'fighter1': 'Fighter #1', 'fighter2': 'Fighter #2', 
# #                                 'weightclass': 'Weightclass', 'fighter1_odds': 'Fighter #1 Odds', 
# #                                 'fighter2_odds': 'Fighter #2 Odds'})
# # colz = ['Fighter #1', 'Fighter #2', ]
# # ne = ne[colz]
# # st.sidebar.table(ne.style.format({'Fighter #1 Odds': '{:.2f}', 'Fighter #2 Odds': '{:.2f}'}))

# # st.header('Important Features')
# # st.write('Peruse the model features below')


# # num_cols = final_vect.select_dtypes(include=['float64', 'int64']).columns
# # # round all float columns to 2 decimal places
# # final_vect_t = final_vect.copy()
# # final_vect_t[num_cols] = final_vect_t[num_cols].round(2)
# # final_vect_t = final_vect_t.T
# # final_vect_t.columns = ['Value']

# # st.dataframe(final_vect_t)

# # ############   ALL FEATURES  ############


# # #cols = []

# # #a_cols = [n for n in cols if n.startswith('A')]
# # #b_cols = [n for n in cols if n.startswith('B')]

# # #a_cols_df = final_vect[a_cols]
# # #b_cols_df = final_vect[b_cols]
# # # Make new df with a cols as rows in one column and b cols as rows in the other
# # #df = pd.DataFrame(columns=[selected_fighter_1, selected_fighter_2])
# # # make column values the values from a_cols_df and b_cols_df
# # #df[selected_fighter_1] = a_cols_df.values[0]
# # #df[selected_fighter_2] = b_cols_df.values[0]
# # # round to 1
# # #df = df.round(1)
# # # rows are the index of a_cols_df
# # #df.index = a_cols
# # # rename indexes
# # #df.index = ['Total Strikes (Average)', 'Total Significant Strikes (Average)', 'Distance Strikes (Average)', 'Head Strikes (Average)', 'Ground Strikes Percent (Median)',
# # #            'Ground Strikes Percent (Minimum)', 'Leg Reach (inches)', 'Control Time (Average)']

# # # only display one decimal place
# # #st.table(df.style.highlight_max(axis = 1, color = 'darkgreen').format("{:.1f}"))


# st.sidebar.header('Links for More Fighter Information:')
# st.sidebar.subheader('Wikipedia')
# st.sidebar.write('Follow links for fighter Wikipedia pages')

# first_name1 = selected_fighter_1.split()[0]
# last_name1 = selected_fighter_1.split()[1]
# wiki_link1 = f'https://en.wikipedia.org/wiki/{first_name1}_{last_name1}'
# st.sidebar.markdown(f"[{first_name1} {last_name1} Wikipedia]({wiki_link1})")

# first_name2 = selected_fighter_2.split()[0]
# last_name2 = selected_fighter_2.split()[1]
# wiki_link2 = f'https://en.wikipedia.org/wiki/{first_name2}_{last_name2}'
# st.sidebar.markdown(f"[{first_name2} {last_name2} Wikipedia]({wiki_link2})")

# st.sidebar.subheader('UFC.COM')
# ufc_link1 = f'https://www.ufc.com/search?query={first_name1}+{last_name1}'
# st.sidebar.markdown(f"[{first_name1} {last_name1} UFC.COM]({ufc_link1})")

# ufc_link2 = f'https://www.ufc.com/search?query={first_name2}+{last_name2}'
# st.sidebar.markdown(f"[{first_name2} {last_name2} UFC.COM]({ufc_link2})")


# st.sidebar.subheader('Tapology')
# tapology_link1 = f'https://www.tapology.com/search?term={first_name1}+{last_name1}&search=Submit&mainSearchFilter=fighters'
# st.sidebar.markdown(f"[{first_name1} {last_name1} Tapology]({tapology_link1})")

# tapology_link2 = f'https://www.tapology.com/search?term={first_name2}+{last_name2}&search=Submit&mainSearchFilter=fighters'
# st.sidebar.markdown(f"[{first_name2} {last_name2} Tapology]({tapology_link2})")

# st.sidebar.subheader('BestFightOdds')
# bfo_link = f'https://www.bestfightodds.com/search?query={first_name1}+{last_name1}'
# st.sidebar.markdown(f"[{first_name1} {last_name1} BestFightOdds]({bfo_link})")

# bfo_link = f'https://www.bestfightodds.com/search?query={first_name2}+{last_name2}'
# st.sidebar.markdown(f"[{first_name2} {last_name2} BestFightOdds]({bfo_link})")

# st.sidebar.subheader('UFC FightPass')
# ufc_fp_link = f'https://www.ufc.tv/search?term={first_name1}+{last_name1}'
# st.sidebar.markdown(f"[{first_name1} {last_name1} UFC FightPass]({ufc_fp_link})")

# ufc_fp_link = f'https://www.ufc.tv/search?term={first_name2}+{last_name2}'
# st.sidebar.markdown(f"[{first_name2} {last_name2} UFC FightPass]({ufc_fp_link})")

# st.sidebar.subheader('DraftKings Odds')
# dk_link = f'https://sportsbook.draftkings.com/leagues/mma/ufc'
# st.sidebar.markdown(f"[DraftKings Odds]({dk_link})")

