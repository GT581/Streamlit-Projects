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

st.markdown("""
*Notes:*
- Past matches will result in an error warning as the app only pulls available odds
- The farther out a future match is the less likely it will have available odds
- If going back to change screener selections, "x" out of the selection prior to changing

---

*Page is currently suspended due to changes in the Draftkings API

""")


#sportsStreaksOdds()
