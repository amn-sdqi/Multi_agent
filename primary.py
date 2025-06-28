from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor       
from langchain.memory import ConversationBufferMemory
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
import requests
import os

from dotenv import load_dotenv
load_dotenv()

primary_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# prompt = PromptTemplate(
#     input_variables=["input"],
#     template="Choose tools wisely based on the input query: {input}"
# )
prompt = hub.pull("hwchase17/react-chat")
llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest") ##bhari wala

parser = StrOutputParser()


from Automation_agent.Automation_agent.automation_agent import email_agent,report_agent # Shakeel
from QnA_Agent.qna_agent import qna_agent_response 
from Sentiment_Agent.agent_core  import analysis_tool 




tools = [
    Tool(name="EmailAgent", func=email_agent(), description="draf and Send emails , also email asistince"),
    Tool(name="ReportAgent", func=report_agent(), description="Generate reports"),
    Tool(name="analysis_tool", func=analysis_tool, description="Analyze the input text and return sentiment + primary emotion."),
    Tool(name="QnA_Agent", func=qna_agent_response, description="Answer the input query and retain the context for future use")
    # Tool(name="NotifyAgent", func=notify_run, description="Send notifications"),
    # Tool(name="NotifyAgent", func=notify_run, description="Send notifications"),
    # Tool(name="NotifyAgent", func=notify_run, description="Send notifications"),
]




agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=primary_memory,
    verbose=True
)
query = input("Enter your demands: ")
result = agent_executor.invoke({"input": query})
print(result)