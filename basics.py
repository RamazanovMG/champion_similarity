import requests
import json

# queueIds:
# Ranked Solo/Duo: 420
# Ranked Flex: 440
# Normal Draft Pick: 400
# Normal Blind Pick: 430
# ARAM: 450
# Clash: 700
# Ranked Teamfight Tactics: 1100
SUMMONERS_RIFT = [420, 440, 400, 430]

API_KEY = 'RGAPI-46344c19-4e39-43c9-b907-f2c2fb4e38f7'
start_id = 6983374886
matches_to_parse = 5000
end_id = start_id + 1 - matches_to_parse  # 100 matches
match_id = 'EUW1_6983374886'
url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}'
response = requests.get(url)
data = response.json()
pretty_data = json.dumps(data, indent=4, separators=('\t', ': '))
print(pretty_data)
print(len(data['info']['participants']))

# count_success = 0
# count_failure = 0
# count_summoners_rift = 0
# count_others = 0
#
# for i in range(start_id, end_id - 1, -1):
#     j = start_id - i
#     if j % (matches_to_parse / 100) == 0:
#         print(f'{j / (matches_to_parse / 100)}% completed')
#     match_id = 'EUW1_' + str(i)
#     url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         count_success += 1
#         data = response.json()
#         queue_id = data['info']['queueId']
#         if queue_id in SUMMONERS_RIFT:
#             #  Analyze stats here
#             #  Choose metrics. Divide by game length?
#             count_summoners_rift += 1
#         else:
#             count_others += 1
#     else:
#         count_failure += 1
# print(f'fraction of successful responses: {round(count_success / (count_success + count_failure), 2)}')
# print(f'fraction of SR games: {round(count_summoners_rift / (count_summoners_rift + count_others), 2)}')
