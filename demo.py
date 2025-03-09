import streamlit as st
import pandas as pd

team_ratings = pd.read_csv('data/team_ratings.csv', encoding='utf-16')
stats_and_predicted_rating = pd.read_csv('data/stats_and_predicted_rating.csv').drop('Unnamed: 0', axis=1)


all_players, all_teams, one, two_a, two_b = st.tabs(["all_players", "all_teams", "1", "2a", "2b", ])
for tournament_id, tab in zip([-1, 0, 1, 2, 3], [all_players, all_teams, one, two_a, two_b]):
    with tab:
        if tournament_id == -1:
            st.dataframe(stats_and_predicted_rating, column_config={'playerName': {'pinned': True}},column_order=['playerName','damageDealt','kills','assists','dBNOs','revives','wins','roundsPlayed','level','predictedRating','17dmg_to_1lvl','5dmg_to_1lvl'])
        elif tournament_id:
            st.dataframe(team_ratings[team_ratings['tournamentId'] == tournament_id])
        else:
            st.dataframe(team_ratings.drop(['tournamentId'], axis=1).drop_duplicates())
