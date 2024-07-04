import pandas as pd
import requests
import time
import csv

API_KEY = 'RGAPI-19c4b0fd-1e03-45e4-b833-7e4ea0c8a648'

MATCHID_PATH = 'matchid.csv'

df = pd.read_csv('puuid.csv').drop_duplicates()

with open(MATCHID_PATH, 'w') as file:
    file.write("matchId\n")

REGION_DICT = {'BR1': 'AMERICAS', 'EUN1': 'EUROPE', 'PH2': 'SEA', 'RU': 'EUROPE', 'SG2': 'SEA', 'VN2': 'SEA',
               'JP1': 'ASIA', 'LA1': 'AMERICAS', 'NA1': 'AMERICAS', 'TH2': 'SEA', 'TW2': 'SEA', 'OC1': 'SEA',
               'LA2': 'AMERICAS', 'TR1': 'EUROPE', 'ME1': 'EUROPE', 'EUW1': 'EUROPE', 'KR': 'ASIA'}

to_skip = None
counter = 0

for index, row in df.iterrows():
    print(f'{counter}')
    counter += 1
    # if counter < to_skip:
    #     continue
    puuid = row['puuid']
    region = row['region']
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime=1712113877&start=0&count=100&api_key={API_KEY}'
    response = requests.get(url)
    time.sleep(1.2)
    if response.status_code != 200:
        print(f'status_code {response.status_code} for url {url}')
        continue
    data = response.json()
    with open(MATCHID_PATH, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for item in data:
            r = item.split('_')[0]
            csvwriter.writerow([item, REGION_DICT[r]])
