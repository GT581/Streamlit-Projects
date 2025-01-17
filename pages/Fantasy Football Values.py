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

st.markdown("""
*Notes:*
- When choosing player result size, pick according to the expected draft pool (ex: 12 person league, 16 normal roster size, at least ~200 drafted players)
- QB stats are best to be looked at alone unless playing in 2QB / superflex leagues

---

*Page is currently suspended until 2025 season when the new endpoint on ESPN will be available

""")


#espnAdpValues()
