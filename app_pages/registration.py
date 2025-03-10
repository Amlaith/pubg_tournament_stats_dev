import streamlit as st

from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
st.write(conn)
# st.help(conn)

df = conn.read(worksheet='Sheet1')
st.table(df)

# conn.create()