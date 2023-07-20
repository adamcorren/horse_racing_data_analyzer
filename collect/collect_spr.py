import datetime
from datetime import timedelta
import requests
import pandas as pd
import io
import re
import warnings
from bs4 import BeautifulSoup
from functools import reduce
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

# DRIVER SET UP
def selenium_set_up():
    print('Setting up driver...')
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome("chromedriver_windows.exe", options=options)
    return driver


# GET NAMES OF DIFFERENT RACE MEETS
def get_meets(driver, url):
    # navigate to only UK and Ireland races
    driver.minimize_window()
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH,'//div[contains(@data-test-id, \
                                                                         "new-switch-button")]'))).click()
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    
    # get locations of race meets
    containers = page_content.select('span.NewGenericTabs__ActiveTab-mpmc8b-3.dFMNzR, \
                                      span.NewGenericTabs__Tab-mpmc8b-2.MfCLi')
    meets = list(set([container.text.lower().replace(" ", "-") for container in containers]))
    meets = [m for m in meets if m != 'all']
    return meets


# GET URL LINKS FOR EACH RACE TAKING PLACE ON DAY
def get_race__links(driver, meets, sporting_life_format):
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    links = set()
    for l in page_content.find_all('a'):
        url = l.get('href', '')
        if '/racing/results/' in url and sporting_life_format in url:
            if any(ext in url for ext in meets) and '#video-player' not in url:
                links.add('https://www.sportinglife.com' + url)
    print(f'Collecting data from {len(links)} races...')
    return list(links)

                
# GET RACE INFO
def get_race_info(driver, race):
    driver.get(race)
    raceinfo_container = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH,
            '//li[contains(@class, "RacingRacecardSummary__StyledAdditionalInfo-sc-1intsbr-2 gaIFRF")]'))).text

    # extract ages, class, distance, surfacem runners, ground 
    race_info = raceinfo_container.replace(' ', '').split('|')
    if len(race_info) == 6:
        race_info.insert(1, None)

    # extract race age range, calss from race_info
    race_ages = race_info[0].strip().replace('YO', '').replace(' plus', '+').replace(' only','') \
        .replace(' to', '-')
    try:
        race_class = race_info[1].strip().replace('Class ', '')
    except AttributeError:
        race_class = None

    # extract race distance from race_info and convert to yards
    race_distance = race_info[2].strip().replace('1m', '1760,').replace('2m','3520,') \
        .replace('3m', '5280,').replace('4m', '7040,').replace('1f', '220,').replace('2f','440,') \
        .replace('3f', '660,').replace('4f', '880,').replace('5f', '1100,').replace('6f','1320,') \
        .replace('7f', '1540,').replace('y', '').replace(' ', '').split(',')
    race_distance = [x for x in race_distance if x]
    race_distance = sum(int(x) for x in race_distance)

    # extract ground condition, runners, surface from race_info
    race_going = race_info[3].strip()
    race_runners = race_info[4].strip().replace(' Runners', '')
    race_surface = race_info[5].strip()

    # extract non runners in race
    try:
        nonrunner_containers = WebDriverWait(driver, 1).until(
            ec.visibility_of_all_elements_located((By.XPATH,
                '//div[contains(@class, "NonRunner__NonRunnerWrapper-sc-1hosg08-0 hhzBUF")]')))
        
        non_runners = [re.sub('[^a-zA-Z ]+', '', x.text).title().split('weight')[0] \
            .strip() for x in nonrunner_containers]
    except:
        non_runners = None

    race_info = list([race_surface, race_runners, race_going, race_distance,
                      race_class, race_ages, non_runners])
    return race_info


# GETTING RACECARD DATA
def get_racecard_data(driver):
    # navigate to race card
    WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, '//a[(text()= "Racecard")]'))).click()

    # extract horse names
    horse_names = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.XPATH,
            '//a[contains(@data-test-id, "horse-name-link")]')))
    
    # clean horse names
    names = [re.sub('[^a-zA-Z ]+', '', n.text).title() for n in horse_names]

    # get summary data
    all_info = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.XPATH,
            '//div[contains(@data-test-id, "horse-sub-info")]')))
    
    # split summary data into ages, weights, jockeys, trainers, ratings
    horse_info = [x.text.strip().split('| ') for x in all_info]

    # extract ages from summary data
    ages = [re.sub('[^0-9]', '', x[0]).title() for x in horse_info]

    # extract weights and convert to pounds from summary data
    weights = [re.sub('[^0-9-]', '', x[1]).title().split('-') for x in horse_info]
    weights = [(int(w[0]) * 14) + int(w[1]) for w in weights]

    #extract jockey and trainer names from summary data
    jockeys = [re.sub('[^a-zA-Z ]', '', x[2][3:]) for x in horse_info]
    trainers = [re.sub('[^a-zA-Z ]', '', x[3][3:]) for x in horse_info]

    # extract horse rating from summary dara
    ratings = []
    for x in horse_info:
        if len(x) >=5 and x[4].startswith('OR:'):
            ratings.append(re.sub('[^0-9-]', '', x[4]))
        else:
            ratings.append(None)

    # extract horse form
    horse_form = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.XPATH,
            '//div[contains(@class, "Runner__StyledFormKeyInfo-sc-4nkld7-11 ieAYok")]')))
    forms = [re.sub('[^0-9]', '', x.text) for x in horse_form]

    # add data to single df
    race_card_df = pd.DataFrame({'names': names, 'age': ages, 'weight': weights, 
        'jockey': jockeys, 'trainer': trainers, 'ratings': ratings, 'form': forms})
    return race_card_df


# GETTING RESULT DATA
def get_results_data(driver):
    # navigate to results page
    WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, '//*[(text()= "Result")]'))).click()
    
    # extract horse names
    result_names = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.XPATH,
            '//div[contains(@class, "ResultRunner__StyledHorseName-sc-58kifh-5 dXVlkd")]')))
    
    result_names = [re.sub('[^a-zA-Z ]+', '', n.text).title() for n in result_names]

    # extract distance behind horse infront 
    distance_behind = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.XPATH,
            '//div[contains(@class, "ResultRunner__StyledFinishDistance-sc-58kifh-2 fJvvMx")]')))

    distance_behind = [d.text.replace('½', '.5').replace('¾','.75').replace('¼', '.25') \
        .replace(' .', '.').strip() for d in distance_behind]

    # extract ISP odds
    isp = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.XPATH,
            '//span[contains(@class, "BetLink__BetLinkStyle-jgjcm-0 tlpHs")]')))

    isp = [re.sub('[^0-9/]', '', o.text).split('/') for o in isp]
    isp = [(int(o[0]) + int(o[1])) / int(o[1]) for o in isp if len(o)>1]
    
    # add data to single df
    results_df = pd.DataFrame({'names': result_names, 'distance_behind': distance_behind, 'isp': isp})
    results_df['position'] = results_df.index+1
    return results_df


def get_spr_data(day):
    print('Getting bookmaker data...')
    # convert date into format sportinglife uses
    sporting_life_format = day.strftime("%Y-%m-%d")
    url = f"https://www.sportinglife.com/racing/results/{sporting_life_format}"

    driver = selenium_set_up()
    meets = get_meets(driver, url)
    race_links = get_race__links(driver, meets, sporting_life_format)

    # create empty final data frame 
    spr_data = pd.DataFrame([])

    # Loops through all races and extracts data
    for count,race in enumerate(race_links):
        attempts = 0
        while attempts <5:
            try:
                surface, runners, going, distance, race_class, ages, non_runners = get_race_info(driver, race)
                race_card_data = get_racecard_data(driver)
                results_data = get_results_data(driver)
                final_df = pd.merge(race_card_data, results_data, on='names')
                
                final_df['race_surface'] = surface
                final_df['race_runners'] = runners
                final_df['race_going'] = going
                final_df['race_distance'] = distance
                final_df['race_class'] = race_class
                final_df['race_ages'] = ages
                final_df['non_runners'] = str(non_runners)

                # add race data to final data frame
                spr_data = pd.concat([spr_data, final_df])
                print(f'Collected data from {count+1} / {len(race_links)} races...')
                break
            except:
                print(f'ERROR collecting data from race {count+1}, trying again...')
                attempts +=1
        else:
            print(f'Unable to collect from race {count+1}')
    print('Bookmaker data collected!...')
    return spr_data
           
