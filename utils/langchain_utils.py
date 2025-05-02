# utils/langchain_utils.py
import os
from typing import List
import streamlit as st
import logging

# app.py (ou utils/langchain_utils.py)
import os
from dotenv import load_dotenv

load_dotenv()  # carrega .env para as variáveis de ambiente



from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Configuração de logging para auxiliar na depuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente com valores padrão
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

def _get_embeddings() -> OpenAIEmbeddings:
    """Instancia o modelo de embeddings da OpenAI."""
    return OpenAIEmbeddings()

@st.cache_resource
def criar_vector_store(chunks: List[str]) -> FAISS:
    """
    Cria e retorna um FAISS vector store a partir de uma lista de chunks de texto.
    Este recurso é cacheado para não ser recriado a cada rerun. 
    """
    embeddings = _get_embeddings()  # st.cache_resource garante singleton do modelo :contentReference[oaicite:7]{index=7}
    logger.info("Criando vector store com %d chunks", len(chunks))
    return FAISS.from_texts(texts=chunks, embedding=embeddings)

def criar_conversation_chain(
    vectorstore: FAISS,
    model_name: str = OPENAI_MODEL,
    temperature: float = TEMPERATURE,
    memory_key: str = "chat_history",
    return_source_documents: bool = True
) -> ConversationalRetrievalChain:
    """
    Configura e retorna uma ConversationalRetrievalChain pronta para uso.
    """
    llm = ChatOpenAI(model=model_name, temperature=temperature)
    memory = ConversationBufferMemory(
        memory_key=memory_key,
        return_messages=True,
        output_key="answer"
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=return_source_documents,
        output_key="answer"
    )
    logger.info(
        "Cadeia de conversação criada (model=%s, temp=%.2f)",
        model_name, temperature
    )
    return chain
