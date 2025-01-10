import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama

def get_vectorstore(db_path):
    """
    Initializes and returns the Chroma vector store.
    """
    embedding = OllamaEmbeddings(model="llama3.2:1b")
    vectorstore = Chroma(
        embedding_function=embedding, persist_directory=db_path
    )

    return vectorstore

def get_conversation_chain(vectorstore):
    """
    Creates and returns a conversational retrieval chain.
    """
    llm = Ollama(model="llama3.2:1b")
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
    )

    return conversation_chain