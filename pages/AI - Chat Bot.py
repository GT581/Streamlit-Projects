import streamlit as st
from App.AI.chat import AI_Chat


st.set_page_config(
    page_title="AI - Chat Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "https://github.com/GT581/Streamlit-Projects/blob/main/pages/AI%20-%20Chat%20Bot.py"
    }
)


st.title("AI Chat Bot")


AI_Chat()


with st.expander('Message Chat Log JSON'):
    st.session_state.messages