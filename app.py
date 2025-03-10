import streamlit as st

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.write("# GAZ CUP")

    col1, col2 = st.columns(2, gap='large')

    # You can also use "with" notation:
    with col1:
        st.subheader('Главное правило')
        st.markdown("""
                    **Смурфинг или стримснайпинг – дисквалификация и бан на будущих турнирах**  
                    *Решение о дисквалификации выносится по усмотрению организатора*
                    """)

    with col2:
        st.subheader('Призовой фонд')
        st.markdown("""
                    - 1 место – 5 000 р.
                    - 2 место – 3 000 р.
                    - 3 место – 2 000 р.
                    """)
            
    col3, col4 = st.columns(2, gap='large')
    with col3:
        st.subheader('Игровой процесс')
        st.markdown("""
                    Лобби создаются на европейском сервере в режиме "киберспорт".

                    Название лобби и пароль присылаются в группу капитанов непосредственно перед началом каждого матча.

                    Время ожидания команд в лобби – 5 минут после оповещения капитанов.
                    """)
        
    with col4:
        st.subheader('Контакты')
        st.markdown("""
                    [Telegram](https://t.me/gazcupPUBG)  
                    [Discord](https://discord.gg/gSUJckTg)  
                    [Twitch](https://www.twitch.tv/gazbro27)  
                    """)



    st.subheader('Подсчет баллов')
    st.markdown("""
                Итоговые баллы = сумма баллов команды за все матчи турнира  
                Баллы за матч = баллы за место в матче + баллы за киллы в матче  

                Баллы за место в матче:  
                - 1 место = 12 баллов  
                - 2 место = 9 баллов  
                - 3 место = 7 баллов  
                - 4 место = 5 баллов  
                - 5 - 6 места = 4 балла  
                - 7 - 8 места = 3 балла  
                - 9 - 12 места = 2 балла  	
                - 13 - 16 места = 1 балл  
                - 17 - 20 места = 0 баллов  

                Баллы за киллы в матче:  		
                - 1 килл = 1 балл  

                Распределение итоговых мест при равенстве баллов у нескольких команд:  
                - Сначала учитывается сумма баллов за места в матчах 
                - Затем учитывается сумма баллов за последний матч  
                - Затем учитывается место, занятое в последнем матче  
                """)
    # st.subheader('Личный рейтинг')
    # st.markdown("""
    #             5 игроков с наибольшим количеством киллов выигрывают бесплатное участие в следующем турнире  

    #             В случае равного количества киллов у нескольких игроков, выбирается игрок с наименьшим уровнем аккаунта		
    #             """)
    
    


homepage = st.Page(main, title="О турнирах", icon=":material/trophy:")
gazcup_1 = st.Page("app_pages/3_GazCup_1.py", title="GAZ CUP #1", icon=":material/history:")
gazcup_2a = st.Page("app_pages/1_GazCup_2a.py", title="GAZ CUP #2, лобби A", icon=":material/table:")
gazcup_2b = st.Page("app_pages/2_GazCup_2b.py", title="GAZ CUP #2, лобби B", icon=":material/table:")
ratings = st.Page("app_pages/ratings.py", title="Таблица рейтинга", icon=":material/table:")
sandbox = st.Page("app_pages/sandbox.py", title="peep", icon=":material/help:")
team_registration = st.Page("app_pages/team_registration.py", title="Зарегистрировать команду", icon=":material/group_add:")
player_registration = st.Page("app_pages/player_registration.py", title="Подбор команды", icon=":material/person_add:")


pg = st.navigation(
        {
            "GAZ CUP": [homepage, ratings, sandbox, team_registration, player_registration],
            "Актуальные турниры": [gazcup_2a, gazcup_2b],
            "Архив": [gazcup_1],
        }
    )

pg.run()