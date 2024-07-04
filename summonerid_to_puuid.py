import pandas as pd
import csv
import requests
import time

API_KEY = 'RGAPI-19c4b0fd-1e03-45e4-b833-7e4ea0c8a648'
PUUID_PATH = 'puuid.csv'

REGION_DICT = {'BR1': 'AMERICAS', 'EUN1': 'EUROPE', 'PH2': 'SEA', 'RU': 'EUROPE', 'SG2': 'SEA', 'VN2': 'SEA',
               'JP1': 'ASIA', 'LA1': 'AMERICAS', 'NA1': 'AMERICAS', 'TH2': 'SEA', 'TW2': 'SEA', 'OC1': 'SEA',
               'LA2': 'AMERICAS', 'TR1': 'EUROPE', 'ME1': 'EUROPE', 'EUW1': 'EUROPE', 'KR': 'ASIA'}

sumid_df = pd.read_csv('summonerid.csv').drop_duplicates()
# with open(PUUID_PATH, 'w') as file:
#     file.write("puuid,region\n")

to_skip = 10210
counter = 0

df = sumid_df.sample(n=50000, random_state=69)
for index, row in df.iterrows():
    counter += 1
    if counter < to_skip:
        continue
    summonderId = row['summonerId']
    region = row['region']
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summonderId}?api_key={API_KEY}'
    response = requests.get(url)
    time.sleep(1.2)
    if response.status_code != 200:
        print(f'status_code {response.status_code} for url {url}')
        continue
    data = response.json()
    with open(PUUID_PATH, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([data['puuid'], REGION_DICT[region]])
