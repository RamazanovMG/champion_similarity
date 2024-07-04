import requests
import csv
import time

# Collecting summonerId for each region

API_KEY = 'RGAPI-033f7cf8-012e-43e4-b37b-f6f4b454f9c4'

# Rate limits
LIMIT_1_SEC = 20
LIMIT_2_MIN = 100

SUMMONER_ID_PATH = 'summonerid.csv'

# step 1: Fetch players

REGIONS_CODES = {'BR1', 'EUN1', 'EUW1', 'JP1', 'KR', 'LA1', 'LA2', 'ME1', 'NA1', 'OC1', 'PH2', 'RU', 'SG2', 'TH2',
                 'TR1', 'TW2', 'VN2'}
DIVISION = {'I', 'II', 'III', 'IV'}
TIER = {'DIAMOND', 'EMERALD', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON'}
# QUEUES = {'RANKED_SOLO_5x5', 'RANKED_FLEX_SR'}

# requests_made = 0
# start_time_1_sec = time.time()
# start_time_2_min = time.time()

with open('summonerid.csv', 'w') as file:
    file.write("summonerId,region\n")

TOTAL_COMBINATIONS = len(REGIONS_CODES) * len(DIVISION) * len(TIER)
count = 0

for region in REGIONS_CODES:
    for division in DIVISION:
        for tier in TIER:
            count += 1
            print(f'Parsing {tier} {division} {region} ({count}/{TOTAL_COMBINATIONS})')
            page = 1
            while True:
                time.sleep(1.2)
                url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}&api_key={API_KEY}'
                response = requests.get(url)
                data = response.json()
                page += 1
                if len(data) == 0 or page == 5:  # limited to 1025 players
                    break
                if response.status_code != 200:
                    print(f'status_code {response.status_code} for url {url}')
                    break
                with open(SUMMONER_ID_PATH, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    for i in range(len(data)):
                        csvwriter.writerow([data[i]['summonerId'], region])
