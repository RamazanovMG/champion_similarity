import requests
import time

# EUW1 block

API_KEY = 'RGAPI-033f7cf8-012e-43e4-b37b-f6f4b454f9c4'

# Rate limits
LIMIT_1_SEC = 20
LIMIT_2_MIN = 100

STARTING_PUUID = 'r9VODWD5H4fwGtSfGYCso7dkM1fQemzQUV9k8SzCaWGOCnhNgiIafJ7f3VGSAkbSkZ4Q6Pq6MMJW2g'
MATCHES_LIMIT = 1e6
TIMESTAMP_START = 1688131327  # 30 June 2023

def get_matches(puuid: str, region: str) -> list:
    global requests_made, start_time_1_sec, start_time_2_min
    start = 0
    output = []
    while True:
        url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={TIMESTAMP_START}&start={start}&count=100&api_key={API_KEY}'
        if requests_made >= LIMIT_1_SEC:
            elapsed_time = time.time() - start_time_1_sec
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)
            start_time_1_sec = time.time()
            requests_made = 0

        elapsed_time_2_min = time.time() - start_time_2_min
        if elapsed_time_2_min >= 120:
            start_time_2_min = time.time()
        elif requests_made >= LIMIT_2_MIN:
            time.sleep(120 - elapsed_time_2_min)
            start_time_2_min = time.time()

        response = requests.get(url)
        if response.status_code != 200:
            print(f'status_code {response.status_code} for url {url}')
        data = response.json()
        if len(data) == 0:
            break
        else:
            output.extend(data)
        start += 100

    return output

requests_made = 0
start_time_1_sec = time.time()
start_time_2_min = time.time()

puuids = set(STARTING_PUUID)
matchesIds = set()

while len(matchesIds) < MATCHES_LIMIT:
    matches = get_matches(STARTING_PUUID, 'europe')
