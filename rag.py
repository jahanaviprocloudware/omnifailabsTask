from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

def create_chunks(document_text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_text(
        document_text
    )

    return chunks

def create_vector_store(chunks, api_key):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )


    vector_store = FAISS.from_texts(
        chunks,
        embedding=embeddings
    )


    return vector_store

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

def ask_question(vector_store, question, api_key):

    docs = vector_store.similarity_search(
        question,
        k=3
    )

    context = ""

    for doc in docs:
        context += doc.page_content + "\n"


    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key
    )


    prompt = f"""
    Answer the question using only the given document information.

    Document:
    {context}

    Question:
    {question}
    """


    response = llm.invoke(prompt)


    return response.content