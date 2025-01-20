import streamlit as st
from App.AI import common, chat
import pandas as pd
from pandasai import Agent
from pandasai.responses.streamlit_response import StreamlitResponse


def loadCsv():
    '''
    Accepts user's CSV file when uploaded and loads it into a dataframe

    Returns:
        df: dataframe of uploaded CSV file
    '''

    uploadedCsv = st.file_uploader('Upload a CSV file to ask AI about:')

    if uploadedCsv:
        df = loadDf(uploadedCsv)
        return df
    else:
        st.stop()


def loadDf(uploadedCsv):
    '''
    Attempts to load uploaded CSV file with different encodings into a dataframe.
    Stops with encoding error, previews data if loaded.

    Args:
        uploadedCSV: user's uploaded CSV file

    Returns:
        df: encoded dataframe of uploaded CSV file
    '''

    try:
        df = readCsvEncoded(uploadedCsv)
    except UnicodeDecodeError as e:
        st.error(e)
        st.stop()
    
    with st.expander('File Preview:'):
        st.dataframe(df.head(10), use_container_width = True, hide_index = True)
    
    return df


def readCsvEncoded(uploadedCsv):
    '''
    Reads uploaded CSV with different encodings, if needed, and returns a dataframe.
    If reading is unsuccessful, raise decoding error.

    Args:
        uploadedCSV: user's uploaded CSV file
    
    Returns:
        df: encoded dataframe of uploaded CSV file
    '''

    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']

    for encoding in encodings:
        try:
            df = pd.read_csv(uploadedCsv, encoding=encoding)
            return df
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("Unable to read CSV file with any encoding")


def createPandasAgent(df, llm):
    '''
    Create PandasAI agent with dataframe and langchain model instance configured for streamlit outputs

    Args:
        df: dataframe of uploaded CSV file
        llm: langchain model instance

    Returns:
        dfAgent: PandasAI agent

    '''

    dfAgent = Agent(df, config={"llm": llm, "response_parser": StreamlitResponse}, memory_size=25)

    return dfAgent


def startDataChat(modelVersion, apiKey, apiSelection):
    '''
    Start a data chat session

    Args:
        modelVersion: string of selected model key
        apiKey: string of API Key for selected platform
        apiSelection: string of API platform selected
    '''

    df = st.session_state.csv
    llm = common.createLangchainModel(modelVersion, apiKey, apiSelection)
    dfAgent = createPandasAgent(df, llm)

    st.session_state.datachat = dfAgent
    st.session_state.datamessages = []
    st.session_state.llm = llm


def checkStartDataChatSession(modelVersion, apiKey, df, apiSelection):
    '''
    Check if there is a current data chat session, and if not starts a session for the selected platform

    Args:
        modelVersion: string of selected model key
        apiKey: string of API Key for selected platform
        df: dataframe of uploaded CSV file
        apiSelection: string of API platform selected

    '''

    if "datamessages" not in st.session_state and "datachat" not in st.session_state:
        st.session_state.csv = df

        st.session_state.model = modelVersion
        st.write('Model in use:', modelVersion)

        startDataChat(modelVersion, apiKey, apiSelection)


def checkDataChange(modelVersion, apiKey, df, apiSelection):
    '''
    Checks if there was a change in uploaded data, and if so, updates the streamlit session state
    and starts a new data chat with the new file

    Args:
        modelVersion: string of selected model key
        apiKey: string of API Key for selected platform
        df: dataframe of uploaded CSV file
        apiSelection: string of API platform selected
    '''

    dfState = st.session_state.csv

    if df.equals(dfState):
        pass
    else:
        st.session_state.csv = df
        startDataChat(modelVersion, apiKey, apiSelection)


def writeDataChat():
    '''
    Write each user and AI message in a data chat
    '''

    for message in st.session_state.datamessages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def userPromptDataChat():
    '''
    Takes each prompt from user and answer from AI and updates the agent chat instance for history 
    and streamlit session state
    '''

    if prompt := st.chat_input("Type question..."):
        dfAgent = st.session_state.datachat
        answer = dfAgent.chat(prompt)
        st.session_state.datachat = dfAgent

        st.session_state.datamessages.append({"role": "You", "content": prompt})
        st.session_state.datamessages.append({"role": "AI", "content": answer})

        with st.chat_message("You"):
            st.markdown(prompt)
        
        with st.chat_message("AI"):
            st.markdown(answer)


def AI_Gemini_Data_Chat(apiSelection):
    '''
    Execute a data chat session for a Gemini model

    Args:
        apiSelection: string of API platform selected to use as a param in common functions
    '''

    apiKey = common.apiKeyInput(apiSelection)
    genai = common.configAI(apiKey, apiSelection)

    modelDict = common.listModels(genai, apiSelection)
    options = chat.filterGeminiChatModels(modelDict)
    modelVersion = common.selectedGeminiModel(options, modelDict)

    df = loadCsv()

    checkStartDataChatSession(modelVersion, apiKey, df, apiSelection)
    checkDataChange(modelVersion, apiKey, df, apiSelection)

    if common.checkModelChange(modelVersion):
        st.session_state.csv = df
        startDataChat(modelVersion, apiKey, apiSelection)
    
    writeDataChat()
    userPromptDataChat()


def AI_Groq_Data_Chat(apiSelection):
    '''
    Execute a data chat session for a Groq model

    Args:
        apiSelection: string of API platform selected to use as a param in common functions

    '''

    apiKey = common.apiKeyInput(apiSelection)

    modelDict = common.listModels(None, apiSelection)
    modelVersion = common.selectedGroqModel(modelDict)

    df = loadCsv()

    checkStartDataChatSession(modelVersion, apiKey, df, apiSelection)
    checkDataChange(modelVersion, apiKey, df, apiSelection)

    if common.checkModelChange(modelVersion):
        st.session_state.csv = df
        startDataChat(modelVersion, apiKey, apiSelection)
    
    writeDataChat()
    userPromptDataChat()


def AI_Data_Chat():
    '''
    Execute a data chat session
    '''

    apiSelection = common.selectApi()

    if apiSelection == 'Gemini':
        AI_Gemini_Data_Chat(apiSelection)
    
    if apiSelection == 'Groq':
        AI_Groq_Data_Chat(apiSelection)