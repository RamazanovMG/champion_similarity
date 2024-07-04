import pandas as pd
import csv
import time
import requests

# METRICS:
# 1 Kills/min
# 2 Deaths/min
# 3 Assists/min
# 4 totalDamageDealtToChampions/min
# 5 damageSelfMitigated/totalDamageTaken
# 6 damageDealtToObjectives/min
# 7 timeEnemySpentControlled/min
# 8 Split score (avg euc dist to teammates) mins 10-end
# 9 Companion score (avg euc dist to the closest teammate) mins 1-end
# 10 goldEarned/min
# 11 effectiveHealAndShielding/min

with open('data.csv', 'w') as file:
    file.write("champion,role,kills,deaths,assists,damage,mitigatedDamage,objectivesDamage,crowdControl,splitpushScore,companionScore,goldGeneration,healsAndShields\n")


API_KEY = 'RGAPI-1057a2e8-b295-49c5-8103-1a2dc6215ef0'

SUMMONERS_RIFT = (420, 440, 400, 430)


#  Checks for afk, remakes, no junglers
def check_game_validity(data: dict) -> bool:
    # if data
    def has_three_consecutive_identical_tuples(position_dict):
        for key, values in position_dict.items():
            for i in range(len(values) - 2):
                if values[i] == values[i + 1] == values[i + 2]:
                    return True
        return False
    frames = data['info']['frames']
    if len(frames) < 6:
        return False  # Remake
    position = {str(i): [] for i in range(1, 11)}
    for frame in frames:
        p_frames = frame['participantFrames']
        for p_id, local_p_frames in p_frames.items():
            position[p_id].append((local_p_frames['position']['x'], local_p_frames['position']['y']))
    if has_three_consecutive_identical_tuples(position):
        return False  # Found afk player
    teams = (('1', '2', '3', '4', '5'), ('6', '7', '8', '9', '10'))
    for team in teams:
        jungleMinionsKilled = 0
        for player in team:
            jungleMinionsKilled += frames[5]['participantFrames'][player]['jungleMinionsKilled']
        if jungleMinionsKilled < 5:
            return False  # Less than 5 total jungle kills by 6 minutes => no jungler
    return True

df = pd.read_csv('matchid.csv').reset_index().drop_duplicates()
for _, row in df.iterrows():
    matchid = row['matchId']
    region = row['region']
    url2 = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={API_KEY}'
    response = requests.get(url2)
    time.sleep(1.2)
    if response.status_code != 200:
        print(f'status code {response.status_code} for url {url2}')
        continue  # Bad matchid response
    data = response.json()
    if data['info']['queueId'] not in SUMMONERS_RIFT:
        continue  # non-Summoners Rift game
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{matchid}/timeline?api_key={API_KEY}'
    timeline_response = requests.get(url)
    time.sleep(1.2)
    if timeline_response.status_code != 200:
        print(f'status code {timeline_response.status_code} for url {url}')
        continue  # Bad matchid timeline response
    timeline_data = timeline_response.json()
    if not check_game_validity(timeline_data):
        continue  # invalid game
    #  Magic happens here
    print('success')
    break

# url = f'https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_6992716062/timeline?api_key=RGAPI-1057a2e8-b295-49c5-8103-1a2dc6215ef0'
# data = requests.get(url).json()
# print(check_game_validity(data))