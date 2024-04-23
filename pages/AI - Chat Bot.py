import streamlit as st
from App.AI.chat import AI_Chat


st.set_page_config(
    page_title="AI - Chat Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title("AI Chat Bot")


AI_Chat()


with st.expander('Message Chat Log JSON'):
    st.session_state.messages