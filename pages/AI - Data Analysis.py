import streamlit as st
from App.AI.datachat import AI_Data_Chat


st.set_page_config(
    page_title="AI - Data Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "https://github.com/GT581/Streamlit-Projects/blob/main/pages/AI%20-%20Data%20Analysis.py"
    }
)


st.title("AI Data Chat")


AI_Data_Chat()


with st.expander('Message Data Chat Log JSON'):
    st.session_state.datamessages