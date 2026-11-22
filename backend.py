from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, BaseMessage
#from langchain_ollama import ChatOllama
#from langchain_openai import ChatOpenAI
import os
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import add_messages
class ChatBot(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

#llm = ChatOllama(
  #  model="llama3.2",
   # temperature=0.7
#)
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# Streamlit Cloud fallback
if not api_key:
    api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing!")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
    api_key=api_key
)
#llm = ChatOpenAI
def chat_node(state:ChatBot):
    #take user query from the state
    messages = state['messages']
    #send to llm
    response =llm.invoke(messages)

    #response store state
    return{'messages':[response]}
checkPointer= MemorySaver()
graph = StateGraph(ChatBot)

#node
graph.add_node('chat_node',chat_node)

#edgees
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node',END)
workflow =graph.compile(checkpointer=checkPointer)
