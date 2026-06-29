import os
import sys
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_classic.chains import conversational_retrieval
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

# add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def setup_conversational_chain():
    # 1. Initialize Embeddings and Vectore store
    encode_kwargs = {"prompt_name": "STS"}
    embeddings = HuggingFaceEmbeddings(
        model_name = config.EMBEDDING_MODEL,
        encode_kwargs = encode_kwargs
    )
    vectorestore = PGVector(
        embeddings=embeddings,
        collection_name=config.COLLECTION_NAME,
        connection= config.CONNECTION_STRING,
        use_jsonb=True
    )

    retriever = vectorestore.as_retriever(search_kwargs={"k": config.NUM_RETRIEVED_DOCS})

    # 2. Initialize LLM (Groq)
    llm= ChatGroq(
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        api_key= config.GROQ_API_KEY
    )

    # 3. Create History-Aware Retriever
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is." 
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # 4. Create the final Question-answering chain
    system_prompt = (
        "You are a helpful assistant for CamTech University."
        "Use the following pieces of retrieved context to answer the user's questioin."
        "If you don't know the answer based on the context, say that you don't know.\n\n"
        "Context: \n{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    question_anwer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever,question_anwer_chain)
    return rag_chain