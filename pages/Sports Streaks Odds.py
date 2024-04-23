import streamlit as st
from App.streaks.streaks import sportsStreaksOdds


st.set_page_config(
    page_title="Sports Streaks Odds",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title("Sports Streaks Odds")


sportsStreaksOdds()