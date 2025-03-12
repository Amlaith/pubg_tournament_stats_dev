import streamlit as st
import pandas as pd

from streamlit_gsheets import GSheetsConnection

st.title('Подбор команды')

st.write('Заполните эту форму, если в вашей команде меньше четырех человек. Мы свяжемся с вами и поможем найти команду.')

# st.write(conn)
# st.help(conn)

# st.table(current_df)

with st.form(key='my_form'):
    team_name = st.text_input('Название команды')

    tab1, tab2, tab3 = st.tabs(['Игрок №1', 'Игрок №2', 'Игрок №3'])
    with tab1:
        tg_name_1 = st.text_input('Никнейм игрока №1 в Telegram', placeholder='@your_username', )
        player_name_1 = st.text_input('Никнейм игрока №1 в PUBG', placeholder='Внимательно проверьте написание')
        steam_link_1 = st.text_input('Ссылка на профиль игрока №1 в Steam', placeholder='https://steamcommunity.com/profiles/99999999999999999/')
    with tab2:
        st.write('Заполнять необязательно')
        tg_name_2 = st.text_input('Никнейм игрока №2 в Telegram', placeholder='@your_username', )
        player_name_2 = st.text_input('Никнейм игрока №2 в PUBG', placeholder='Внимательно проверьте написание')
        steam_link_2 = st.text_input('Ссылка на профиль игрока №2 в Steam', placeholder='https://steamcommunity.com/profiles/99999999999999999/')
    with tab3:
        st.write('Заполнять необязательно')
        tg_name_3 = st.text_input('Никнейм игрока №3 в Telegram', placeholder='@your_username', )
        player_name_3 = st.text_input('Никнейм игрока №3 в PUBG', placeholder='Внимательно проверьте написание')
        steam_link_3 = st.text_input('Ссылка на профиль игрока №3 в Steam', placeholder='https://steamcommunity.com/profiles/99999999999999999/')
    
    st.write('-----------------------------------------')

    # agreed = st.checkbox('Все игроки прочитали правила регистрации и обязуются их соблюдать')
    
    submitted = st.form_submit_button("Отправить заявку", )
    if submitted:
        new_data = pd.DataFrame({
            'teamName' : team_name,
            'playerName' : [
                player_name_1,
            ] + (
                [player_name_2] if player_name_2 else []
            ) + (
                [player_name_3] if player_name_3 else []
            ),
            'tgName' : [
                tg_name_1,
            ] + (
                [tg_name_2] if player_name_2 else []
            ) + (
                [tg_name_3] if player_name_3 else []
            ),
            'steamLink' : [
                steam_link_1,
            ] + (
                [steam_link_2] if player_name_2 else []
            ) + (
                [steam_link_2] if player_name_3 else []
            ),
        })
        conn = st.connection("gsheets", type=GSheetsConnection)
        player_registration_worksheet = 'people_to_match'
        current_df = conn.read(worksheet=player_registration_worksheet)
        df_to_write = pd.concat([current_df, new_data])
        # st.dataframe(df_to_write)
        df = conn.update(worksheet=player_registration_worksheet, data=df_to_write)
        st.cache_data.clear()
        st.success('Спасибо за регистрацию! Мы рассмотрим вашу заявку и свяжемся с вами.')
        # st.rerun()



# df = conn.read(worksheet='Sheet1')
# st.table(df)