import streamlit as st
import numpy as np
import pandas as pd

pub_stats = pd.read_csv('data\pub_stats.csv')[[
        'playerId',
        'isPro',
        'level',
        'damageDealt_normal',
        'damageDealt_ranked',
        'roundsPlayed_normal',
        'roundsPlayed_ranked',
    ]]
players = pd.read_csv('data\players.csv')
players_results = pd.read_csv('data/playersResults.csv')[['tournamentId', 'teamId','playerName']].drop_duplicates()
teams = pd.read_csv('data/teams.csv')

ranked_coef = st.slider('кеф ранкеда', 1., 2., step=.1)
adr_coef = st.slider('отношение килы/лвл', 1, 50)
show_pros = st.checkbox('показать нонеймов')

players_df = pub_stats.join(players.set_index('playerId'), on='playerId')
players_df['totalRoundsPlayed'] = players_df['roundsPlayed_normal'] + players_df['roundsPlayed_ranked']
players_df = players_df.replace({'totalRoundsPlayed': {0: 999}})
players_df['rating'] = (players_df['damageDealt_normal'] * players_df['roundsPlayed_normal'] + players_df['damageDealt_ranked'] * players_df['roundsPlayed_ranked'] * ranked_coef) / (players_df['totalRoundsPlayed']) * (adr_coef / (adr_coef + 1)) + players_df['level'] * (1 / (adr_coef + 1))
players_df = players_results.join(players_df.set_index(['playerName']), on='playerName')
players_df = players_df.join(teams.set_index(['tournamentId', 'teamId']), on=['tournamentId', 'teamId'])


players_column_config = {
    'playerName': 'Игровой ник', 
    'teamName': 'team',
    'rating': 'rating', 
    'isPro': 'нонейм',
    'damageDealt_normal': 'ADR normal',
    'damageDealt_ranked': 'ADR ranked',
    'level': 'lvl',
}

players_column_order = (
    'playerName',
    'teamName',
    'rating',
    'isPro',
    'level',
    'damageDealt_normal',
    'damageDealt_ranked',
)
st.write('asd')
st.dataframe(
    players_df if show_pros else players_df[~players_df['isPro']],
    column_config=players_column_config,
    column_order=players_column_order,
)


players_results = players_results.join(players_df[['playerId', 'playerName', 'rating']].set_index('playerName'), on='playerName')
players_results = players_results.groupby(['tournamentId', 'teamId']).agg({'rating': lambda x: (sum(x ** 2)) ** (1/2) })
players_results = players_results.join(teams.set_index(['tournamentId', 'teamId']), on=['tournamentId', 'teamId']).reset_index()

teams_column_order = (
    'tournamentId',
    'teamName',
    'rating',
)

st.dataframe(players_results, column_order=teams_column_order)


