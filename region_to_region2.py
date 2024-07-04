import pandas as pd
import requests
import time

API_KEY = 'RGAPI-19c4b0fd-1e03-45e4-b833-7e4ea0c8a648'

REGIONS_CODES = {'BR1', 'EUN1', 'EUW1', 'JP1', 'KR', 'LA1', 'LA2', 'ME1', 'NA1', 'OC1', 'PH2', 'RU', 'SG2', 'TH2',
                 'TR1', 'TW2', 'VN2'}
REGIONS_CODES_2 = {'AMERICAS', 'ASIA', 'EUROPE', 'SEA'}

df = pd.read_csv('summonerid.csv')
for region in REGIONS_CODES:
    row = df[df['region'] == region].head(1)
    summonerId = row['summonerId'].values[0]
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}?api_key={API_KEY}"
    data = requests.get(url).json()
    print(data)
    time.sleep(1.2)
    puuid = data['puuid']
    for region2 in REGIONS_CODES_2:
        url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}'
        data = requests.get(url).json()
        time.sleep(1.2)
        print(f'Region: {region}. Region2: {region2}. Response length: {len(data)}')
