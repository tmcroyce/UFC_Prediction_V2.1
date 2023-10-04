# Load Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from bs4 import BeautifulSoup
import time
import requests
import shutil       
import datetime
from scipy.stats import norm
from random import randint
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cmath import nan
import urllib
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chromedriver = '/Users/travisroyce/Library/CloudStorage/OneDrive-Personal/Data Science/Personal_Projects/Sports/UFC_Prediction_V2/V2_Newer_Notebooks/chromedriver'

# set working directory
os.chdir('/Users/travisroyce/Library/CloudStorage/OneDrive-Personal/Data Science/Personal_Projects/Sports/UFC_Prediction_V2')
os.getcwd()

# Set options
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chromedriver, options=chrome_options)

# set up header for other
headerrr = {
                        "User-Agent": "Mozilla/6.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                        "X-Requested-With": "XMLHttpRequest"
        }

#Get Url of next fight from tapology

init_url = 'https://www.tapology.com/fightcenter?group=ufc'
driver.get(init_url)
# find class fightcenterEvents
fightcenterEvents = driver.find_element_by_class_name('fightcenterEvents')
# find all links
links = fightcenterEvents.find_elements_by_tag_name('a')
# get all links
links = [link.get_attribute('href') for link in links]
# return first link
links = links[0]
tap_url = links
# print(tap_url)

# Get all fighters Tapology Links
# Enter Event Here
tapology_event_url = tap_url


header = {
                        "User-Agent": "Mozilla/6.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                        "X-Requested-With": "XMLHttpRequest"
        }

response = requests.get(tapology_event_url, headers=header)
soup = BeautifulSoup(response.text, 'html.parser')
# to ul class fightCard
fight_card = soup.find('ul', {'class': 'fightCard'})
# get all links in fight card
fight_links = fight_card.find_all('a', href=True)
# return all links in fight card
fight_links = [fight_link['href'] for fight_link in fight_links]
fight_links = [fight_link for fight_link in fight_links if '/fightcenter/fighters/' in fight_link]
# add base url to links
fight_links = ['https://www.tapology.com' + fight_link for fight_link in fight_links]
fight_links


def get_fighter_tapology(url):
    # scrape with requests, using a header
    header = {
                        "User-Agent": "Mozilla/6.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                        "X-Requested-With": "XMLHttpRequest"
        }

    # scrape with requests
    r = requests.get(url, headers = header)
    soup = BeautifulSoup(r.text, 'html.parser')

    fighter_name = soup.find('div', {'class': 'fighterUpcomingHeader'})

    values = fighter_name.text
    values = values.split('\n')
    # delete empty strings
    values = list(filter(None, values))
    # only keep last item
    values = values[-1]
    fighter_name = values

    # get Fighter Details
    fighter_details = soup.find_all('div', {'class': 'details details_two_columns'})
    fighter_details_text = fighter_details[0].text
    # split on \n
    fighter_details_text = fighter_details_text.split('\n')
    # remove empty strings
    fighter_details_text = list(filter(None, fighter_details_text))
    # replace | with new line
    fighter_details_text = [x.replace('|', '\n') for x in fighter_details_text]
    # replace any '\n ' with ''
    fighter_details_text = [x.replace('\n ', '') for x in fighter_details_text]

    # Creating a dictionary from the list
    fighter_dict = {}
    for i in range(len(fighter_details_text)):
        # Check if the current element is a key (ends with a colon)
        if fighter_details_text[i][-1] == ':':
            # Check if the next element is also a key
            if i + 1 < len(fighter_details_text) and fighter_details_text[i + 1][-1] != ':':
                # If not, add the current element as a key and the next as a value
                fighter_dict[fighter_details_text[i][:-1]] = fighter_details_text[i + 1]
            else:
                # If the next element is a key, add the current one with a placeholder value
                fighter_dict[fighter_details_text[i][:-1]] = "N/A"

    # Converting the dictionary into a DataFrame
    fighter_details = pd.DataFrame(fighter_dict, index=[0])

    # add fighter name
    fighter_details['Fighter Name'] = fighter_name

    # move fighter_name to first column
    cols = fighter_details.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    fighter_details = fighter_details[cols]


    # FIGHTER RECORD

    soup = BeautifulSoup(r.text, 'html.parser')

    # Get the fighter record stats
    fighter_record_stats = soup.find_all('ul', {'class': 'fighterRecordStats'})

    # Assuming fighter_record_stats[0] is the BeautifulSoup object containing the ul
    ul = fighter_record_stats[0]

    # Find all li tags - each li corresponds to a different record type
    lis = ul.find_all('li')

    records = []

    # Loop through the li tags
    for li in lis:
        # Get the record type (KO/TKO, Submission, Decision)
        record_type = li.find('div', class_='primary').text
        
        # Get the secondary data - number of wins and losses
        secondary = li.find('div', class_='secondary').text
        wins_losses = secondary.split(',')
        wins = wins_losses[0].strip()
        losses = wins_losses[1].strip() if len(wins_losses) > 1 else '0 losses'
        
        # Get the percentage of wins
        win_stats = li.find('div', class_='statRow', id=lambda id: id and id.endswith('Win'))
        percent_of_win = win_stats.find('div', class_='percentOf') if win_stats else None
        percent_wins = percent_of_win.text.strip() if percent_of_win else 'N/A'
        # replace any \ofwins with ''
        percent_wins = percent_wins.replace('\n', ' ')
        percent_wins = percent_wins.replace('of wins', '')
        
        # Get the percentage of losses
        loss_stats = li.find('div', class_='statRow', id=lambda id: id and id.endswith('Loss'))
        percent_of_loss = loss_stats.find('div', class_='percentOf') if loss_stats else None
        percent_losses = percent_of_loss.text.strip() if percent_of_loss else 'N/A'
        # replace any \oflosses with ''
        percent_losses = percent_losses.replace('\n', ' ')
        percent_losses = percent_losses.replace('of losses', '')
        
        # Add the data to the records list
        records.append([record_type, wins, losses, percent_wins, percent_losses])

    # Convert the list to a DataFrame
    records_df = pd.DataFrame(records, columns=['Type', 'Wins', 'Losses', 'Percentage of Wins', 'Percentage of Losses'])
    
    
    # PROMOTION RESULTS
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        # get mma record by promotion using ul class = 'fighterPromotions'
        fighter_promotions = soup.find_all('ul', {'class': 'fighterPromotions'})

        # Assuming fighter_promotions[0] is the BeautifulSoup object containing the ul
        ul = fighter_promotions[0]

        # Find all li tags - each li corresponds to a different promotion record
        lis = ul.find_all('li')

        promotion_records = []

        # Loop through the li tags
        for li in lis:
            # Get the promotion name
            promotion_name = li.find('img')['title']
            

            # Get the years of participation
            years_active = li.find('div', class_='yearsActive').get_text(separator=' ').strip()
            
            # Get the win-loss record
            wins = li.find('div', class_='wins').get_text(separator=' ').strip()
            losses = li.find('div', class_='losses').get_text(separator=' ').strip()
            draws = li.find('div', class_='draws').get_text(separator=' ').strip()
            no_contests = li.find('div', class_='no_contests').get_text(separator=' ').strip()
            
            # Get the method records
            method_labels = ["KO/TKO", "Sub", "Decision", "DQ"]
            method_wins = [div.get_text() if div.get_text() != '-' else 'N/A' for div in li.find_all('div', class_='methodRecordWins')[0].find_all('div', class_='methodRecordRow')]
            method_win_percents = [div.get_text() if div.get_text() != '-' else 'N/A' for div in li.find_all('div', class_='methodRecordWinPercent')[0].find_all('div', class_='methodRecordRow')]
            method_losses = [div.get_text() if div.get_text() != '-' else 'N/A' for div in li.find_all('div', class_='methodRecordLosses')[0].find_all('div', class_='methodRecordRow')]
            method_loss_percents = [div.get_text() if div.get_text() != '-' else 'N/A' for div in li.find_all('div', class_='methodRecordLossPercent')[0].find_all('div', class_='methodRecordRow')]
            
            # Convert method records into a dictionary for easy DataFrame creation
            method_records_dict = {f'{label} Wins': win for label, win in zip(method_labels, method_wins)}
            method_records_dict.update({f'{label} Win Percent': win_percent for label, win_percent in zip(method_labels, method_win_percents)})
            method_records_dict.update({f'{label} Losses': loss for label, loss in zip(method_labels, method_losses)})
            method_records_dict.update({f'{label} Loss Percent': loss_percent for label, loss_percent in zip(method_labels, method_loss_percents)})
            
            # Add the data to the promotion records list
            promotion_records.append([promotion_name, years_active, wins, losses, draws, no_contests, method_records_dict])

        # Convert the list to a DataFrame
        df = pd.DataFrame(promotion_records, columns=['Promotion', 'Years Active', 'Wins', 'Losses', 'Draws', 'No Contests', 'Method Records'])

        # Extract method records into separate columns
        df_method_records = pd.DataFrame(df['Method Records'].tolist())
        df = pd.concat([df.drop('Method Records', axis=1), df_method_records], axis=1)
        # drop any \n characters
        df = df.replace('\n','', regex=True)
        # drop any 'win' or 'loss' characters
        df = df.replace('win','', regex=True)
        df = df.replace('loss','', regex=True)
        df = df.replace('draw','', regex=True)
        df = df.replace('no contest','', regex=True)
        # change NA to 0
        df = df.replace('N/A',0, regex=True)

        record_by_promotion = df
    
    except:
        # if no record by promotion, set each column to 'N/A'
        record_by_promotion = pd.DataFrame(columns=['Promotion', 'Years Active', 'Wins', 'Losses', 'Draws', 'No Contests', 'Method Records'])
        record_by_promotion.loc[0] = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
        

    # GET FIGHT RESULTS
    soup = BeautifulSoup(r.text, 'html.parser')

    # scrape fighter fight results (class="fighterFightResults")
    fighter_fight_results = soup.find_all('section', {'class': 'fighterFightResults'})
    # count number of li tags
    len(fighter_fight_results[0].find_all('li'))

    # each li tag is a fight. each fight contains oppenent div, summary div, date div, and more div. 
    # grab all divs within each li tag
    fighter_fight_results_li = fighter_fight_results[0].find_all('li')


    # create an empty list to store the data
    data = []

    # loop through each li tag
    for li in fighter_fight_results_li:
        # create an empty dictionary to store the data for this fight
        fight = {}

        # extract the opponent name using CSS selectors
        name_tag = li.select_one('.opponent .name')
        fight['Opponent Name'] = name_tag.get_text(strip=True) if name_tag else 'N/A'

        # extract the opponent record using CSS selectors
        record_tags = li.select('.opponent .record span')  # this will return a list of span tags
        if record_tags:
            fight['Fighter Record Before Fight'] = record_tags[0].get_text(strip=True) if len(record_tags) > 0 else 'N/A'
            fight['Opponent Record Before Fight'] = record_tags[1].get_text(strip=True) if len(record_tags) > 1 else 'N/A'
        else:
            fight['Fighter Record Before Fight'] = 'N/A'
            fight['Opponent Record Before Fight'] = 'N/A'

        # extract the fight summary and event using CSS selectors
        summary_lead = li.select_one('.summary .lead a')
        if summary_lead is not None:
            fight['Fight Summary'] = summary_lead.get_text(strip=True)
        else:
            fight['Fight Summary'] = 'N/A'

        summary_notes = li.select_one('.summary .notes a')
        if summary_notes is not None:
            fight['Event'] = summary_notes.get_text(strip=True)
        else:
            fight['Event'] = 'N/A'

        # extract the fight date using CSS selectors
        date_tag = li.select_one('.date')
        fight['Fight Date'] = date_tag.get_text(strip=True) if date_tag else 'N/A'

        # add the fight details to the list
        data.append(fight)

    # create a DataFrame from the list of fight details
    fight_results = pd.DataFrame(data)

    # save each to CSV
    fighter_details.to_csv(f'data/tapology/fighters/{fighter_name}_details.csv', index=False)
    records_df.to_csv(f'data/tapology/fighters/{fighter_name}_records_by_finish.csv', index=False)
    record_by_promotion.to_csv(f'data/tapology/fighters/{fighter_name}_record_by_promotion.csv', index=False)
    fight_results.to_csv(f'data/tapology/fighters/{fighter_name}_fight_results.csv', index=False)
    
    
    return records_df,fighter_details, record_by_promotion, fight_results

# Download Tapology Data
for link in fight_links:
    try:
        get_fighter_tapology(link)
        print(link)
    except:
        print('error:', link)
        pass