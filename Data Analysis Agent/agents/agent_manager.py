"""Agent initialization and management."""

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from core.llm import get_llm
from tools.analysis_tool import smart_analysis_tool
from tools.visualization_tool import visualization_tool
from tools.suggestion_tool import suggestion_tool

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def create_agent():
    """Create and initialize the conversational agent."""
    # Initialize tools
    tools = [smart_analysis_tool, visualization_tool, suggestion_tool]
    
    # Initialize memory
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True
    )
    
    # Get LLM instance
    llm = get_llm()
    
    # Initialize agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=False,
        handle_parsing_errors=True
    )
    
    return agent

def get_available_tools():
    """Get list of available tools."""
    return [smart_analysis_tool, visualization_tool, suggestion_tool]