from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from config import(
    OPENAI_MODEL_NAME,
    OPENAI_MODEL_TEMPERATURE,    
)

from memory import get_session_history
from vectorstore import get_vectorstore
from prompts import contextualize_prompt, qa_prompt


def get_chain_rag():
    llm = ChatOpenAI(
        model=OPENAI_MODEL_NAME,
        temperature=OPENAI_MODEL_TEMPERATURE
    )

    retriver = get_vectorstore().as_retriever()
    history_aware_chain = create_history_aware_retriever(
        llm, retriver, contextualize_prompt)
    question_anwser_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=qa_prompt,
    )
    return create_retrieval_chain(history_aware_chain, question_anwser_chain)


def get_conversational_rag_chain():
    rag_chain = get_chain_rag()
    return RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=get_session_history,
        input_messages_key='input',
        history_messages_key='chat_history',
        output_messages_key='answer',
    )