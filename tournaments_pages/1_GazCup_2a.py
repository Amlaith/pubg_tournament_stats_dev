import streamlit as st
import numpy as np
import pandas as pd


matches = pd.read_csv('data/matches.csv')
teams = pd.read_csv('data/teams.csv')
players_results = pd.read_csv('data/playersResults.csv')
teams_results = pd.read_csv('data/teamsResults.csv')

tournament_id = 2
matches = matches[matches['tournamentId'] == tournament_id].drop('tournamentId', axis=1)
teams = teams[teams['tournamentId'] == tournament_id].drop('tournamentId', axis=1)
players_results = players_results[players_results['tournamentId'] == tournament_id].drop('tournamentId', axis=1)
teams_results = teams_results[teams_results['tournamentId'] == tournament_id].drop('tournamentId', axis=1)

rank_to_points = [0, 12, 9, 7, 5, 4, 4, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,]
column_names = {
    'teamName': 'Команда',
    'points': 'Баллы за места',
    'kills': 'Баллы за киллы',
    'total': 'Всего баллов',
    'rank': 'Место в матче',
}

st.title("GAZ CUP #2, лобби A")
st.subheader(":grey[1 марта 2025]")

results_tab, matches_tab, players_tab = st.tabs(["Турнирная таблица", "Результаты матчей", "Статистика игроков"])

# Турнирная таблица
with results_tab:
    # Место / Команда / Очки за места / Очки за килы / Сумма очков

    teams_results['points'] = teams_results['rank'].apply(lambda rank: rank_to_points[rank])
    rank_points = teams_results.groupby('teamId')['points'].sum()

    kill_points = players_results.groupby('teamId')['kills'].sum()

    res = pd.concat([rank_points, kill_points], axis=1)
    res['total'] = res['points'] + res['kills']
    res = teams.join(res, on='teamId').drop('teamId', axis=1)
    res = res.sort_values(['total', 'points'], ascending=False)
    res = res.set_index(np.arange(1, res.shape[0] + 1))
    res = res.fillna(0)
    res = res.astype({
        'kills': 'int32',
        'points': 'int32',
        'total': 'int32',
    })
    res = res.rename(columns=column_names)

    st.table(res)

# Результаты матчей
with matches_tab:
    match_num = int(st.selectbox(
            label='Выберите матч:',
            options=[str(row[1]['matchNum']) + ' – ' + row[1]['mapName'] for row in matches.iterrows()],
            label_visibility='collapsed'
        ).split()[0]) if matches.shape[0] > 0 else 0
    
    placement_in_match = teams_results[teams_results['matchNum'] == match_num][['teamId', 'rank', 'points']]
    kills_in_match = players_results[players_results['matchNum'] == match_num].groupby('teamId')['kills'].sum()

    team_res_in_match = teams.set_index('teamId').join(placement_in_match.set_index('teamId').join(kills_in_match))
    team_res_in_match['total'] = team_res_in_match['points'] + team_res_in_match['kills']
    team_res_in_match = team_res_in_match.fillna(0)
    team_res_in_match = team_res_in_match.astype({
        'rank': 'int32',
        'kills': 'int32',
        'points': 'int32',
        'total': 'int32',
    })
    team_res_in_match = team_res_in_match.rename(columns=column_names)
    team_res_in_match.index.name = None

    st.table(team_res_in_match)

# Статистика игроков
with players_tab:
    players_results_agg = players_results.groupby('playerName').agg({
            'teamId': pd.Series.mode,
            'matchNum': pd.Series.count,
            'DBNOs': pd.Series.sum,
            'assists': pd.Series.sum,
            'damageDealt': pd.Series.sum,
            'kills': pd.Series.sum,
            'longestKill': pd.Series.max,
            'revives': pd.Series.sum,
            'timeSurvived': pd.Series.sum,        
        })

    for col in ['DBNOs', 'assists', 'damageDealt', 'kills', 'revives', 'timeSurvived']:
        players_results_agg[col + '_per_match'] = players_results_agg[col] / players_results_agg['matchNum']

    players_results_agg = players_results_agg.join(teams.set_index('teamId'), on='teamId')

    column_config = {
            'playerName': st.column_config.TextColumn('Игровой ник', pinned=True),
            'teamName': st.column_config.TextColumn('Команда', pinned=True),
            # 'playerName': 'Игровой ник',
            'kills': 'Киллы', 
            'kills_per_match': st.column_config.NumberColumn("Киллы/матч", format="%.2f"),
            'assists': 'Ассисты',
            'assists_per_match': st.column_config.NumberColumn("Ассисты/матч", format="%.2f"),
            'DBNOs': 'DBNOs',
            'DBNOs_per_match': st.column_config.NumberColumn("DBNOs/матч", format="%.2f"),
            'revives': 'Оживления',
            'revives_per_match': st.column_config.NumberColumn("Оживления/матч", format="%.2f"),
            'damageDealt': 'Урон',
            'damageDealt_per_match': st.column_config.NumberColumn("Урон/матч", format="%.2f"),
            'timeSurvived': 'Время выживания',
            'timeSurvived_per_match': st.column_config.NumberColumn("Время выживания/матч", format="%.2f"),
            'longestKill': 'Самый далекий килл',
            'matchNum': 'Кол-во сыгранных матчей',
    }

    column_order = [
        'playerName',
        'teamName',
        'kills',
        'kills_per_match',
        'assists',
        'assists_per_match',
        'DBNOs',
        'DBNOs_per_match',
        'revives',
        'revives_per_match',
        'damageDealt',
        'damageDealt_per_match',
        'timeSurvived',
        'timeSurvived_per_match',
        'longestKill',
        'matchNum',
    ]
    
    st.dataframe(players_results_agg, column_config=column_config, column_order=column_order)