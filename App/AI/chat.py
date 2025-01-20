import streamlit as st
from App.AI import common


def filterGeminiChatModels(modelDict):
    '''
    Filter Gemini models for those with chat capability

    Args:
        modelDict: dict of Gemini models and their metadata

    Returns:
        chatOptions: list of Gemini models with chat capability
    '''

    chatModels = [
        'gemini-1.0-pro-001',
        'gemini-1.0-pro-latest',
        'gemini-1.5-pro-latest',
        'gemini-pro'
    ]

    chatOptions = [option for option in modelDict.keys() if modelDict[option] in chatModels]

    return chatOptions


def startGeminiChat(modelVersion, genai):
    '''
    Start a chat session with a Gemini model and update streamlit session state

    Args:
        modelVersion: string of selected Gemini model key
        genai: LLM instance for Gemini
    '''

    safe = common.configChatSafety()
    gllm = genai.GenerativeModel(modelVersion, safe)
    chat = gllm.start_chat(history = [])
    st.session_state.chat = chat


def checkStartChatSession(modelVersion, genai, apiSelection):
    '''
    Check if there is a current chat session, and if not starts a session for the selected platform

    Args:
        modelVersion: string of selected model key
        genai: LLM instance for selected platform
        apiSelection: string of API platform selected
    '''

    if "messages" not in st.session_state:
        st.session_state.model = modelVersion
        st.write('Model in use:', modelVersion)

        if apiSelection == 'Gemini' and "chat" not in st.session_state:
            st.session_state.messages = []
            startGeminiChat(modelVersion, genai)
        
        if apiSelection == 'Groq':
            st.session_state.messages = []


def writeChat():
    '''
    Write each user and AI message in a chat
    '''

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


def userPromptGeminiChat():
    '''
    Takes each prompt from user and answer from AI and updates the Gemini chat instance for history 
    and streamlit session state
    '''

    if prompt := st.chat_input("Type message...", key='geminiPrompt'):
        chat = st.session_state.chat
        response = chat.send_message(prompt)
        answer = response.text

        st.session_state.chat = chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            st.write(answer)


def groqChat(modelVersion, genai):
    '''
    Takes each prompt from user and answer from AI and updates the Groq chat instance for history 
    and streamlit session state
    '''

    if prompt := st.chat_input("Type message...", key='groqPrompt'):
        st.session_state.messages.append({"role": "user", "content": prompt})

        completion = genai.chat.completions.create(
        model = modelVersion, 
        messages=[
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ]
        )

        answer = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            st.write(answer)


def AI_Gemini_Chat(apiSelection):
    '''
    Execute a chat session for a Gemini model

    Args:
        apiSelection: string of API platform selected to use as a param in common functions
    '''

    apiKey = common.apiKeyInput(apiSelection)
    genai = common.configAI(apiKey, apiSelection)

    modelDict = common.listModels(genai, apiSelection)
    options = filterGeminiChatModels(modelDict)
    modelVersion = common.selectedGeminiModel(options, modelDict)

    checkStartChatSession(modelVersion, genai, apiSelection)

    if common.checkModelChange(modelVersion):
        startGeminiChat(modelVersion, genai)
    
    writeChat()
    userPromptGeminiChat()


def AI_Groq_Chat(apiSelection):
    '''
    Execute a chat session for a Groq model

    Args:
        apiSelection: string of API platform selected to use as a param in common functions
    '''

    apiKey = common.apiKeyInput(apiSelection)
    groq = common.configAI(apiKey, apiSelection)

    modelDict = common.listModels(groq, apiSelection)
    modelVersion = common.selectedGroqModel(modelDict)

    checkStartChatSession(modelVersion, groq, apiSelection)

    if common.checkModelChange(modelVersion):
        st.session_state.messages = []
    
    writeChat()
    groqChat(modelVersion, groq)


def AI_Chat():
    '''
    Execute a chat session
    '''

    apiSelection = common.selectApi()

    if apiSelection == 'Gemini':
        AI_Gemini_Chat(apiSelection)
    
    if apiSelection == 'Groq':
        AI_Groq_Chat(apiSelection)