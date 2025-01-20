import streamlit as st
from App.AI import common, chat
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def loadPDF():
    '''
    Accepts user's PDF file when uploaded and loads the text

    Returns:
        pdf_text: text in the PDF file
    '''

    uploadedPdf = st.file_uploader("Upload a PDF file to ask AI about:", type=["pdf"])

    if uploadedPdf:
        with st.spinner("Processing the PDF..."):
            pdf_text = extract_text_from_pdf(uploadedPdf)
        return pdf_text
    else:
        st.stop()


def extract_text_from_pdf(uploadedPdf):
    '''
    Extracts text from PDF file

    Args:
        uploadedPDF: uploaded PDF file

    Returns:
        text: all text from PDF file
    '''

    pdf_reader = PdfReader(uploadedPdf)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    return text


def chunkText(pdf_text):
    '''
    Recursively splits PDF text into chunks for embeddings

    Args:
        pdf_text: text in the PDF file

    Returns:
        chunks: text chunks for embeddings
    '''

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) #Add option for user to specify chunk size and overlap
    chunks = text_splitter.split_text(pdf_text)

    return chunks


def createEmbeddings(chunks, apiKey):
    '''
    Creates embeddings from text chunks and creates the local vector store

    Args:
        chunks: text chunks for embeddings
        apiKey: string of API Key for selected platform

    Returns:
        vector_store: local vector store of embeddings
    '''

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=apiKey)
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

    return vector_store


def searchVectorDb(llm, vector_store, user_query):
    '''
    Executes search in vector store to answer user's question

    Args:
        llm: langchain model instance
        vector_store: local vector store of embeddings
        user_query: string of user's question
    
    Returns:
        response: llm response
    '''
    qa_chain = load_qa_chain(llm, chain_type="stuff")
    docs = vector_store.similarity_search(user_query, k=3)
    response = qa_chain.run(input_documents=docs, question=user_query)

    return response


def checkStartPdfChatSession(modelVersion, apiKey, pdf_text, apiSelection):
    '''
    Check if there is a current pdf chat session, and if not starts a session for the selected platform

    Args:
        modelVersion: string of selected model key
        apiKey: string of API Key for selected platform
        pdf_text: text of uploaded pdf file
        apiSelection: string of API platform selected

    '''

    if "pdfmessages" not in st.session_state and "pdfchat" not in st.session_state:
        st.session_state.pdf = pdf_text

        st.session_state.model = modelVersion
        st.write('Model in use:', modelVersion)

        startPdfChat(modelVersion, apiKey, apiSelection)


def startPdfChat(modelVersion, apiKey, apiSelection):
    '''
    Start a pdf chat session

    Args:
        modelVersion: string of selected model key
        apiKey: string of API Key for selected platform
        apiSelection: string of API platform selected
    '''

    pdf_text = st.session_state.pdf
    llm = common.createLangchainModel(modelVersion, apiKey, apiSelection)
    chunks = chunkText(pdf_text)
    vector_store = createEmbeddings(chunks, apiKey)

    st.session_state.pdfmessages = []
    st.session_state.llm = llm
    st.session_state.vectordb = vector_store


def checkPdfChange(modelVersion, apiKey, pdf_text, apiSelection):
    '''
    Checks if there was a change in uploaded pdf file, and if so, updates the streamlit session state
    and starts a new pdf chat with the new file

    Args:
        modelVersion: string of selected model key
        apiKey: string of API Key for selected platform
        pdf_text: text of uploaded pdf file
        apiSelection: string of API platform selected
    '''

    pdfState = st.session_state.pdf

    if pdf_text == pdfState:
        pass
    else:
        st.session_state.pdf = pdf_text
        startPdfChat(modelVersion, apiKey, apiSelection)


def writePdfChat():
    '''
    Write each user and AI message in a pdf chat
    '''

    for message in st.session_state.pdfmessages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def userPromptPdfChat():
    '''
    Takes each prompt from user and answer from AI and updates the chat instance for history 
    and streamlit session state
    '''

    if prompt := st.chat_input("Type question..."):
        llm = st.session_state.llm
        vector_store = st.session_state.vectordb
        answer = searchVectorDb(llm, vector_store, prompt)

        st.session_state.pdfmessages.append({"role": "You", "content": prompt})
        st.session_state.pdfmessages.append({"role": "AI", "content": answer})

        with st.chat_message("You"):
            st.markdown(prompt)
        
        with st.chat_message("AI"):
            st.markdown(answer)


def AI_Gemini_Pdf_Chat(apiSelection):
    '''
    Execute a pdf chat session for a Gemini model

    Args:
        apiSelection: string of API platform selected to use as a param in common functions
    '''

    apiKey = common.apiKeyInput(apiSelection)
    genai = common.configAI(apiKey, apiSelection)

    modelDict = common.listModels(genai, apiSelection)
    options = chat.filterGeminiChatModels(modelDict)
    modelVersion = common.selectedGeminiModel(options, modelDict)

    pdf_text = loadPDF()

    checkStartPdfChatSession(modelVersion, apiKey, pdf_text, apiSelection)
    checkPdfChange(modelVersion, apiKey, pdf_text, apiSelection)

    if common.checkModelChange(modelVersion):
        st.session_state.pdf = pdf_text
        startPdfChat(modelVersion, apiKey, apiSelection)

    writePdfChat()
    userPromptPdfChat()