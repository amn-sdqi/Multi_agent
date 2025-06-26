from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor,Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from langchain import hub
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title = "QnA_Agent")
@app.get("/QnA_Agent")
def QnA_Agent(input:str) -> dict :
    llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest" )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    search_tool = DuckDuckGoSearchRun()
    tool = Tool(
        name="Search",
        func=search_tool.run,
        description="Use this tool to look up information on the web ONLY when needed."
    )

    prompt = hub.pull("hwchase17/react-chat")

    agent = create_react_agent(
        llm=llm,
        tools = [tool],
        prompt = prompt
    )

    agent_executer = AgentExecutor(
        agent = agent,
        tools = [tool],
        memory = memory,
        verbose = True,
        handle_parsing_errors=True
    )

    response = agent_executer.invoke({"input":input})

    return{"response":response['output']}