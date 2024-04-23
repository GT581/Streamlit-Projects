import streamlit as st
from App.fantasyfootball.values import espnAdpValues


st.set_page_config(
    page_title="Fantasy Football Values",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title("Fantasy Football Values")


espnAdpValues()