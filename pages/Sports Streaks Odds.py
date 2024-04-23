import streamlit as st
from App.streaks.streaks import sportsStreaksOdds


st.set_page_config(
    page_title="Sports Streaks Odds",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "https://github.com/GT581/Streamlit-Projects/blob/main/pages/Sports%20Streaks%20Odds.py"
    }
)


st.title("Sports Streaks Odds")


sportsStreaksOdds()