import streamlit as st
import pandas as pd
from time import sleep
from streamlit_gsheets import GSheetsConnection

st.title('Регистрация команды')

st.write('Заполните эту форму, если в вашей команде есть четыре человека.')
st.markdown("""Если в вашей команде меньше четырех человек, заполните форму во вкладке <a href="player_registration" target = "_self" rel="noopener noreferrer">Подбор команды</a>.""", unsafe_allow_html=True)
st.markdown("""Если в вашей команде меньше четырех человек, заполните форму во вкладке [Подбор команды](player_registration#daacee3d)""")

link_col1, link_col2, link_col3 = st.columns([16, 1, 3],)
with link_col1:
    st.write("Если в вашей команде меньше четырех человек, заполните форму во вкладке ")
with link_col2:
    st.page_link("app_pages\player_registration.py", label="Подбор команды")
with link_col3:
    pass

# st.write(conn)
# st.help(conn)

# st.table(current_df)

if "submitted" not in st.session_state:
   st.session_state.submitted = False

with st.form(key='my_form'):
    team_name = st.text_input('Название команды')

    tab1, tab2, tab3, tab4, tab5= st.tabs(['Игрок №1 (Капитан)', 'Игрок №2', 'Игрок №3', 'Игрок №4', 'Игрок №5 (Замена)'])
    with tab1:
        tg_name_1 = st.text_input('Никнейм капитана в Telegram', placeholder='@your_username', )
        player_name_1 = st.text_input('Никнейм капитана в PUBG', placeholder='Внимательно проверьте написание')
        steam_link_1 = st.text_input('Ссылка на профиль капитана в Steam', placeholder='https://steamcommunity.com/profiles/99999999999999999/')
    with tab2:
        tg_name_2 = st.text_input('Никнейм игрока №2 в Telegram', placeholder='@your_username', )
        player_name_2 = st.text_input('Никнейм игрока №2 в PUBG', placeholder='Внимательно проверьте написание')
        steam_link_2 = st.text_input('Ссылка на профиль игрока №2 в Steam', placeholder='https://steamcommunity.com/profiles/99999999999999999/')
    with tab3:
        tg_name_3 = st.text_input('Никнейм игрока №3 в Telegram', placeholder='@your_username', )
        player_name_3 = st.text_input('Никнейм игрока №3 в PUBG', placeholder='Внимательно проверьте написание')
        steam_link_3 = st.text_input('Ссылка на профиль игрока №3 в Steam', placeholder='https://steamcommunity.com/profiles/99999999999999999/')
    with tab4:
        tg_name_4 = st.text_input('Никнейм игрока №4 в Telegram', placeholder='@your_username', )
        player_name_4 = st.text_input('Никнейм игрока №4 в PUBG', placeholder='Внимательно проверьте написание')
        steam_link_4 = st.text_input('Ссылка на профиль игрока №4 в Steam', placeholder='https://steamcommunity.com/profiles/99999999999999999/')
    with tab5:
        st.write('Заполнять необязательно')
        tg_name_5 = st.text_input('Никнейм игрока замены в Telegram', placeholder='@your_username', )
        player_name_5 = st.text_input('Никнейм игрока замены в PUBG', placeholder='Внимательно проверьте написание')
        steam_link_5 = st.text_input('Ссылка на профиль игрока замены в Steam', placeholder='https://steamcommunity.com/profiles/99999999999999999/')
    
    st.write('-----------------------------------------')

    # agreed = st.checkbox('Все игроки команды прочитали правила регистрации и обязуются их соблюдать')
    
    submitted = st.form_submit_button("Отправить заявку", )
    if submitted:
        new_data = pd.DataFrame({
            'teamName' : team_name,
            'playerName' : [
                player_name_1,
                player_name_2,
                player_name_3,
                player_name_4,
            ] + ([player_name_5] if player_name_5 else []),
            'tgName' : [
                tg_name_1,
                tg_name_2,
                tg_name_3,
                tg_name_4,
            ] + ([tg_name_5] if player_name_5 else []),
            'steamLink' : [
                steam_link_1,
                steam_link_2,
                steam_link_3,
                steam_link_4,
            ] + ([steam_link_5] if player_name_5 else []), 
        })
        
        conn = st.connection("gsheets", type=GSheetsConnection)
        team_registration_worksheet = 'full_teams'
        current_df = conn.read(worksheet=team_registration_worksheet)
        df_to_write = pd.concat([current_df, new_data])
        df = conn.update(worksheet=team_registration_worksheet, data=df_to_write)
        st.cache_data.clear()
        st.success('Спасибо за регистрацию! Мы рассмотрим вашу заявку и свяжемся с капитаном.')



# df = conn.read(worksheet='Sheet1')
# st.table(df)