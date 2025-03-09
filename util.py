from config import PUBG_KEY
import os
import requests
import pandas as pd


MAP_NAME = {
  "Baltic_Main": "Erangel",
  "Chimera_Main": "Paramo",
  "Desert_Main": "Miramar",
  "DihorOtok_Main": "Vikendi",
  "Erangel_Main": "Erangel_old",
  "Heaven_Main": "Haven",
  "Kiki_Main": "Deston",
  "Range_Main": "Camp Jackal",
  "Savage_Main": "Sanhok",
  "Summerland_Main": "Karakin",
  "Tiger_Main": "Taego",
  "Neon_Main": "Rondo"
}

def get_player(player_name: str | list) -> dict:
    players_url = "https://api.pubg.com/shards/steam/players/"
    header = {
    "Authorization": "Bearer " + PUBG_KEY,
    "Accept": "application/vnd.api+json"
    }
    params = {
        "filter[playerNames]": player_name if type(player_name) == str else ','.join(player_name)
    }

    r = requests.get(players_url, headers=header, params=params)
    return r.json()

def get_match(match_id: str = 'b9a2659b-c099-4fc4-bd5e-9c1b69ce567b') -> dict:
    matches_url = "https://api.pubg.com/shards/steam/matches/"

    header = {
    # "Authorization": "Bearer " + PUBG_KEY,
    "Accept": "application/vnd.api+json"
    }

    match_r = requests.get(matches_url + match_id, headers=header)
    return match_r.json()

def get_players_last_matches(player_name: str, n_matches:int = 20) -> pd.DataFrame:
    player_json = get_player(player_name)
    matches = [match['id'] for match in player_json['data'][0]['relationships']['matches']['data'][:n_matches]]
    
    attrs_to_save = ['gameMode', 'mapName', 'isCustomMatch', 'matchType', 'createdAt']
    attrs_dict = {'matchId': []} | {attr: [] for attr in attrs_to_save}

    for match_id in matches:
        match_json = get_match(match_id)

        attrs_dict['matchId'].append(match_id)
        for attr in attrs_to_save:
            attrs_dict[attr].append(match_json['data']['attributes'][attr])
    
    return pd.DataFrame(attrs_dict).replace({'mapName': MAP_NAME})

def add_tournament(
        tournament_id:int = 1,
        tournament_name:str = 'GAZCUP #1',
        date:str = '2025-02-15',
        rules:str = 'lvl < 1500'
) -> None:
    tournaments_path = 'data/tournaments.csv'
    tournaments_exists = os.path.isfile(tournaments_path)

    tournament_row = pd.DataFrame({
        'tournamentId': tournament_id,
        'tournamentName': tournament_name,
        'date': pd.to_datetime(date),
        'rules': rules,
    }, index=[0])

    tournament_row.to_csv(tournaments_path, mode='a', index=False, header=not tournaments_exists)

def add_teams(
        tournament_id:int = 1,
        teams_names:list[tuple] = [(1, 'Панцерфауст'), (2, 'Пончики')]
) -> None:
    teams_path = 'data/teams.csv'
    teams_exists = os.path.isfile(teams_path)

    teams_dict = {
        'tournamentId': [],
        'teamId': [],
        'teamName': [],
    }
    for team_id, team_name in teams_names:
        teams_dict['tournamentId'].append(tournament_id)
        teams_dict['teamId'].append(team_id)
        teams_dict['teamName'].append(team_name)

    teams_df = pd.DataFrame(teams_dict)

    teams_df.to_csv(teams_path, mode='a', index=False, header=not teams_exists)

def add_match(tournament_id:int, match_num:int, match_id:str) -> None:
    def save_match(tournament_id:int, match_num:int, match_id:str, map_name:str) -> None:
        matches_path = 'data/matches.csv'
        matches_exists = os.path.isfile(matches_path)

        match_df = pd.DataFrame({
            'tournamentId': tournament_id,
            'matchNum': match_num,
            'matchId': match_id,
            'mapName': map_name
        }, index=[0])
        match_df.to_csv(matches_path, mode='a', index=False, header=not matches_exists)

    def save_teams_results(teams_results_dict:dict) -> None:
        teams_results_path = 'data/teamsResults.csv'
        teams_results_exists = os.path.isfile(teams_results_path)

        teams_results_df = pd.DataFrame(teams_results_dict)
        teams_results_df.to_csv(teams_results_path, mode='a', index=False, header=not teams_results_exists)

    def save_players_results(players_results_dict:dict) -> None:
        players_results_path = 'data/playersResults.csv'
        players_results_exists = os.path.isfile(players_results_path)

        players_results_df = pd.DataFrame(players_results_dict)
        players_results_df.to_csv(players_results_path, mode='a', index=False, header=not players_results_exists)
    
    
    match_json = get_match(match_id)
    
    # add match to matches table [DONE]
    save_match(
        tournament_id=tournament_id,
        match_num=match_num,
        match_id=match_id,
        map_name=MAP_NAME[match_json['data']['attributes']['mapName']],
    )

    # add team place to teamsResults table [DONE]
    teams_results_dict = {
        'tournamentId': [],
        'matchNum': [],
        'teamId': [],
        'rank': []
    }
    rosters = dict()
    for roster in match_json['included']:
        if roster['type'] != 'roster':
            continue

        team_id = roster['attributes']['stats']['teamId']

        for player in roster['relationships']['participants']['data']:
            rosters[player['id']] = team_id

        teams_results_dict['tournamentId'].append(tournament_id)
        teams_results_dict['matchNum'].append(match_num)
        teams_results_dict['teamId'].append(team_id)
        teams_results_dict['rank'].append(roster['attributes']['stats']['rank'])

    save_teams_results(teams_results_dict)  # write to teamsResults table

    # add players stats to playersResults table
    players_results_dict = {
        'tournamentId': [],
        'matchNum': [],
        'teamId': [],
        'playerName': [],
        'DBNOs': [],
        'assists': [],
        'damageDealt': [],
        'kills': [],
        'longestKill': [],
        'revives': [],
        'timeSurvived': [],
    }
    
    for player in match_json['included']:
        if player['type'] != 'participant':
            continue

        players_results_dict['tournamentId'].append(tournament_id)
        players_results_dict['matchNum'].append(match_num)
        players_results_dict['teamId'].append(rosters[player['id']])
        players_results_dict['playerName'].append(player['attributes']['stats']['name'])
        players_results_dict['DBNOs'].append(player['attributes']['stats']['DBNOs'])
        players_results_dict['assists'].append(player['attributes']['stats']['assists'])
        players_results_dict['damageDealt'].append(player['attributes']['stats']['damageDealt'])
        players_results_dict['kills'].append(player['attributes']['stats']['kills'])
        players_results_dict['longestKill'].append(player['attributes']['stats']['longestKill'])
        players_results_dict['revives'].append(player['attributes']['stats']['revives'])
        players_results_dict['timeSurvived'].append(player['attributes']['stats']['timeSurvived'])

    save_players_results(players_results_dict)  # write to playersResults table

# def match_json_to_pandas(match_json: dict) -> pd.DataFrame:
#     # assert match_json['data']['attributes']['isCustomMatch'] == True

#     stats_to_save = [
#         "DBNOs",
#         "assists",
#         "damageDealt",
#         "kills",
#         "longestKill",
#         "name",
#         "revives",
#         "timeSurvived",
#         "winPlace"
#     ]
#     players_stats = {stat: [] for stat in stats_to_save}

#     for player in match_json['included']:
#         if player['type'] != 'participant':
#             continue
#         for stat in stats_to_save:
#             players_stats[stat].append(player['attributes']['stats'][stat])

#     players_stats['matchId'] = [match_json['data']['id']] * len(players_stats['name'])

#     return pd.DataFrame(players_stats).rename(columns={'name': 'playerName'})

# def add_rosters(rosters:list[tuple] = [(1, 'Пять озёр', 'Amlaith', 737)]) -> None:
#     rosters_dict = {
#         'tournamentId': [],
#         'teamName': [],
#         'playerName': [],
#         'playerLevel': [],
#     }
#     for tournament_id, team_name, player_name, player_level in rosters:
#         rosters_dict['tournamentId'].append(tournament_id)
#         rosters_dict['teamName'].append(team_name)
#         rosters_dict['playerName'].append(player_name)
#         rosters_dict['playerLevel'].append(player_level)

    
#     rosters_df = pd.DataFrame(rosters_dict)

#     rosters_path = 'data/rosters.csv'
#     rosters_exists = os.path.isfile(rosters_path)
#     rosters_df.to_csv(rosters_path, mode='a', index=False, header=not rosters_exists)