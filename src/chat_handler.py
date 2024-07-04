
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from config import CHAT_MODEL, TEMPERATURE


def create_chain(vector_store):
    model = ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        temperature=TEMPERATURE
    )

    prompt = ChatPromptTemplate.from_template(
        """
        Answer the user's question:
        context: {context}
        chat_history: {chat_history}
        Question: {input}
        """
    )

    chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt,
        output_parser=StrOutputParser()
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    retrieval_chain = create_retrieval_chain(
        retriever,
        chain
    )

    return retrieval_chain

def process_chat(chain, question, chat_history):
    response = chain.invoke({
        "input": question,
        "chat_history": chat_history
    })

    return response['answer']
