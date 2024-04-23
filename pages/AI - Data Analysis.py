import streamlit as st
from App.AI.datachat import AI_Data_Chat


st.set_page_config(
    page_title="AI - Data Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title("AI Data Chat")


AI_Data_Chat()


with st.expander('Message Data Chat Log JSON'):
    st.session_state.datamessages