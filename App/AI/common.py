import streamlit as st
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from groq import Groq
from langchain_groq import ChatGroq


def selectApi():
    '''
    Selection of API platform by the user

    Returns:
        apiSelection: string of API platform selected
    '''

    apiOptions = ['Gemini', 'Groq']
    apiSelection = st.selectbox("Select API: ", apiOptions, index=None)

    if apiSelection is None:
        st.stop()

    return apiSelection


def apiKeyInput(apiSelection):
    '''
    Input of user's API key based on the platform selection

    Args:
        apiSelection: string of API platform selected

    Returns:
        apiKey: string of API Key for selected platform

    '''

    if apiSelection == 'Gemini':
        if apiKey := st.text_input("Input Gemini API Key: ", type='password'):
            return apiKey
        else:
            st.stop()

    if apiSelection == 'Groq':
        if apiKey := st.text_input("Input Groq API Key: ", type='password'):
            return apiKey
        else:
            st.stop()


def configAI(apiKey, apiSelection):
    '''
    Configure LLM client instance based on platform selection

    Args:
        apiKey: string of API Key for selected platform
        apiSelection: string of API platform selected
    
    Returns:
        genai: gemini LLM instance
        groq: groq LLM instance
    '''

    if apiSelection == 'Gemini':
        genai.configure(api_key=apiKey)
        return genai
    
    if apiSelection == 'Groq':
        groq = Groq(api_key=apiKey)
        return groq


def configChatSafety():
    '''
    List to remove Gemini safety configurations for Gemini chat

    Returns:
        safe: dict of Gemini safety configurations
    '''

    safe = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
        # {
        #     "category": "HARM_CATEGORY_DEROGATORY",
        #     "threshold": "BLOCK_NONE",
        # },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        # {
        #     "category": "HARM_CATEGORY_MEDICAL",
        #     "threshold": "BLOCK_NONE",
        # },
        {
            "category": "HARM_CATEGORY_SEXUAL",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        # {
        #     "category": "HARM_CATEGORY_TOXICITY",
        #     "threshold": "BLOCK_NONE",
        # },
        # {
        #     "category": "HARM_CATEGORY_UNSPECIFIED",
        #     "threshold": "BLOCK_NONE",
        # },
        # {
        #     "category": "HARM_CATEGORY_VIOLENCE",
        #     "threshold": "BLOCK_NONE",
        # },
    ]

    return safe


def configLangchainSafety():
    '''
    List to remove Gemini safety configurations in langchain

    Returns:
        safe: dict of Gemini safety configurations for langchain
    '''

    safe = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, 
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE, 
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    }

    return safe


def listModels(genai, apiSelection):
    '''
    Load dict of model options based on platform selection

    Args:
        genai: LLM instance for selected platform
        apiSelection: string of API platform selected
    
    Returns:
        modelDict: dict of models and their metadata for selected platform
    '''

    if apiSelection == 'Gemini':
        models = genai.list_models()
        modelDict = {
            ', '.join((model.display_name, model.description)): model.name.replace('models/', '') 
            for model in models
        }
    
    if apiSelection == 'Groq':
        modelDict = {
        "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
        "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
        "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
        "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
        "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
        }
    
    return modelDict


def selectedGeminiModel(options, modelDict):
    '''
    Selection of Gemini models by user

    Args:
        options: list of Gemini models with chat capability
        modelDict: dict of Gemini models and their metadata

    Returns:
        modelVersion: string of selected model key
    '''

    selection = st.selectbox("Select Gemini Model: ", options, index=None)

    if selection is None:
        st.stop()
    else:
        modelVersion = modelDict[selection]
    
    return modelVersion


def selectedGroqModel(modelDict):
    '''
    Selection of Groq models by user

    Args:
        modelDict: dict of Groq models and their metadata

    Returns:
        modelVersion: string of selected Groq model key
    '''

    modelVersion = st.selectbox("Select Groq Model: ", options=list(modelDict.keys()), format_func=lambda x: modelDict[x]["name"], index=None)

    if modelVersion is None:
        st.stop()
    
    return modelVersion


def checkModelChange(modelVersion):
    '''
    Check if user changed the selected model to use

    Args:
        modelVersion: string of selected model key

    Returns:
        bool: True if changed model, false if same model
    '''

    if st.session_state.model != modelVersion:
        st.write('Model changed from:', st.session_state.model)
        st.session_state.model = modelVersion
        st.write('Model in use:', modelVersion)
        return True
    else:
        return False
    

def createLangchainModel(modelVersion, apiKey, apiSelection):
    '''
    Creates langchain model instance based on selected platform

    Args:
        modelVersion: string of selected model key
        apiKey: string of API Key for selected platform
        apiSelection: string of API platform selected
    
    Returns:
        llm: langchain model instance
    '''

    if apiSelection == 'Gemini':
        safe = configLangchainSafety()
        llm = GoogleGenerativeAI(model=modelVersion, google_api_key=apiKey, safety_settings=safe)
    
    if apiSelection == 'Groq':
        llm = ChatGroq(temperature=1, groq_api_key=apiKey, model_name=modelVersion)
    
    return llm