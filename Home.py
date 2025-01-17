import streamlit as st


st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "https://github.com/GT581/Streamlit-Projects/blob/main/Home.py"
    }
)


st.title("Home")


st.markdown("""
---

## About This App

This Streamlit app is designed to showcase various Data Engineering and Data Science projects I created.

Current and future projects will be mainly focused around applying my data and software engineering skill set toward my interests of AI / ML, Sports Analytics, and Financial Analysis.

Each page on this app hosts a different project, which can be accessed in the sidebar. Below are the summaries of each project deployed so far.

All code for this app can be found on my Github: https://github.com/GT581/Streamlit-Projects/tree/main

*Note: for "AI" labeled projects, an API key must be provided. These were puposely designed around platforms that are currently offering free API keys to models, and you can get one at the corresponding links below:*
- Google: [https://ai.google.dev/pricing](https://ai.google.dev/pricing)
- Groq: [https://console.groq.com/login](https://console.groq.com/login)  *(Recommended)*

---

## AI - Chat Bot

The AI Chat Bot is a project that recreates your usual conversation interface with a LLM using an API.

It allows you to select a free API option from above, choose one of their model offerings, and have a conversation for your needs.

The whole chat history is stored for use in interacting with the model, displaying the conversation in the chat window, and providing the option to copy a JSON of your conversation.

The type of model can be changed at anytime to start a new conversation with a different model.

---

## AI - Data Analysis

The AI - Data Analysis project allows for you to ask a LLM questions about a CSV dataset you provide.

Using PandasAI, it will generate and execute code on a pandas dataframe of your provided data to provide an answer back in the chat window.

This is useful for understanding your data, calculating metrics, or even generating plots. 

The PandasAI docs can be found here: https://docs.pandas-ai.com/en/latest/

---

## Fantasy Football Values

This project is enabling real time accessibility to the data involved in a process I do every football season: finding values in my fantasy football drafts.

Using the ESPN API, we can pull the top X number of players, ordered by the "ESPN Rank" value. The final data can be viewed with one or more positions selected.

With this call, we also pull average draft position and projection data for each fantasy relevant position, which is parsed and loaded into a dataframe.

Calculations then add ranking values based on the ADP, projected points for a player's position, and projected points overall.

This data can be searched and filtered through in the UI, or downloaded to a CSV.

---

## Sports Streaks Odds

This project enables the analysis of a sports team's recent hot streaks and trends to the market price of that specific trend continuing in upcoming matches.

Using the Sofascore and Draftkings API, for a selected date we can choose between any matches occuring for configured sports and their leagues, pulling the data in real time.

Any streaks or trends that are available for the teams in a chosen match will be displayed, and selecting an assigned streak category will pull the corresponding odds.

Both of the Sofascore and Draftkings APIs were essentially reversed engingeered for this project. 

The API endpoints and parameters for the desired data on all sport / league / category levels were configured, in addition to mapping exercises between the two data sources on both the match and streak / bet level. 

*Note: 
This project originally started as a local web app, involving a local postgres database with designed schemas, DDL, and CDC scripts for each table and category, and FastAPI endpoints to connect to a React front end. 
JSON files from API calls that were parsed and SQL files for ETL are available in the GitHub repo for reference.

---

""")


st.write('*Disclaimer: This app is for demonstration purposes only and not intended to provide advice of any kind.')
