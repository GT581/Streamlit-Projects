import streamlit as st
from App.AI.pdfchat import AI_Gemini_Pdf_Chat


st.set_page_config(
    page_title="AI - PDF Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': ""
    }
)


st.title("AI PDF Chat")


AI_Gemini_Pdf_Chat(apiSelection='Gemini')


with st.expander('Message Chat Log JSON'):
    st.session_state.pdfmessages