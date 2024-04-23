import streamlit as st
from App.fantasyfootball.values import espnAdpValues


st.set_page_config(
    page_title="Fantasy Football Values",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "https://github.com/GT581/Streamlit-Projects/blob/main/pages/Fantasy%20Football%20Values.py"
    }
)


st.title("Fantasy Football Values")


espnAdpValues()