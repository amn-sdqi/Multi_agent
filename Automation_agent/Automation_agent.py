from langchain_community.agent_toolkits import GmailToolkit 
from langchain_community.tools.gmail.utils import (
	build_resource_service,
	get_gmail_credentials,
)
from dotenv import load_dotenv
load_dotenv()
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent,AgentType,initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.tools import BaseTool
from langchain_core.tools import Tool
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain 
from langchain_community.tools import DuckDuckGoSearchRun,WikipediaQueryRun 
from langchain_community.utilities import WikipediaAPIWrapper 
import json
import re

# Google Model API Use
#----------------------------------------------------------------------------------------------------------------------------------------------------------
model= ChatGoogleGenerativeAI(model="gemini-2.0-flash")
browser_search=DuckDuckGoSearchRun()
browser_search=DuckDuckGoSearchRun()
wiki_search=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


# Funtion For Clean The Report Generate Output
#--------------------------------------------------------------------------------------------------------------------------------------------------
def clean_report(text):
    
         text = re.sub(r'## ?', '', text)
         text = re.sub(r'\*\*', '', text)
         text = re.sub(r'^\*\s*', '', text, flags=re.MULTILINE)
         text = re.sub(r'^\*+', '', text, flags=re.MULTILINE)
         text = re.sub(r'\*+$', '', text, flags=re.MULTILINE)
         text = re.sub(r'^\*\s*', '', text, flags=re.MULTILINE)
         text = re.sub(r' +', ' ', text)
         return text.strip()

# Create Email Agent As a Tool
#----------------------------------------------------------------------------------------------------------------------------------------------------------
class email_agent(BaseTool):
	name: str = "email_assistance_tool"
	description: str = "A tool that uses a agent to to create draft email and send email "
	  
	  
	def _run(self, input, **kwargs):
		return self.report_agent(input)
	
	
	
	def report_agent(self, input):

		credentials = get_gmail_credentials(
			token_file="token.json",
			scopes=["https://mail.google.com/"],
			client_secrets_file="Credentials.json",
		)

		api_resource = build_resource_service(credentials=credentials)
		toolkit = GmailToolkit(api_resource=api_resource)
		tools = toolkit.get_tools()

		instructions = """You are an assistant in making report and email ."""
		base_prompt = hub.pull("langchain-ai/openai-functions-template")
		prompt = base_prompt.partial(instructions=instructions)

		agent = create_openai_functions_agent(model, tools, prompt)

		agent_executor = AgentExecutor(
			agent=agent,
			tools=toolkit.get_tools(),
			verbose=False, 
		)

		result = agent_executor.invoke({"input": input})
		return result


# Create Report Generater Agent As a Tool
#---------------------------------------------------------------------------------------------------------------------------------------------------
class report_agent(BaseTool):
	name: str = "report_generater_tool"
	description: str = "A tool that uses a agent to generate the report By user given topic"
	
	def _run(self, input, **kwargs):
		return self.report_agent(input)
	

	def report_agent(self, input):

		report_template = PromptTemplate(
			input_variables=["topic", "points"],
			template="""Write a professional report about the topic: "{topic}".Here are the main points:{points}
				Include:
				- Title
				- Introduction
				- Key Details
				- Conclusion"""
		)

		report_chain = LLMChain(llm=model, prompt=report_template)

		generate_report_tool = Tool(
			name="GenerateReport",
			func=lambda x: report_chain.run(**json.loads(x)),
			description="Generates a structured report. Input must be JSON with keys 'topic' and 'points'." 
		)

		tools = [generate_report_tool, wiki_search]

		agent = initialize_agent(
			tools=tools,
			llm=model,
			agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
			verbose=True
		)

		report = agent.invoke(input)
		# cleaned_report = clean_report(report["output"]) # its comment Becusce when its use its giving the error
		return report["output"]


# Combine The Agent Tool
#----------------------------------------------------------------------------------------------------------------------------------------------------------
report_generater_tool = report_agent()
email_assistance_tool = email_agent()
agent_tool = [report_generater_tool, email_assistance_tool]


#initialize The Agent And Provide The Agent tool
#----------------------------------------------------------------------------------------------------------------------------------------------------------
agent_executor = initialize_agent(
    tools=agent_tool, 
    llm=model,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)



# These are The Result so You can try and check by yourself
#----------------------------------------------------------------------------------------------------------------------------------------------------------

# drafting email Prompt------>>>>>>>>>

# report=agent_executor.invoke("darft an email to be sent by me (sheikh shakeel) to My Team (sheikhupdesk@gmail.com) The subject of the email is fifa final match and in the content write about fifa 2018 final match summary in detail and draf it")
# report["output"]


# drafting report genrator Prompt------>>>>>>>>>

# report=agent_executor.invoke("""Create a today report on 'india win t20 worldcup 2024'. Points are: unbeaten india , way of win jurny, final watch, history.""")
# report["output"]



# drafting email with report generater Prompt------>>>>>>>>>

# report=agent_executor.invoke("""Create a today report on 'india win t20 worldcup 2024'.
#                                 Points are: unbeaten india , way of win jurny, final watch, history.and then draf this report to
#                                 and then take this report as content and darft an email to be sent by me (sheikh shakeel) 
#                                 to My Team (sheikhupdesk@gmail.com) 
#                                 The subject of the email is report topic 
#                                 and draf it """)
# report["output"]

# report=agent_executor.invoke("""Create a report on 'final distinace movie'.
#                                 Points are: all parts , boxoffice colloction, overall rating, about.and then draf this report to
#                                 and then take this report as content and darft an email to be sent by me (sheikh shakeel) 
#                                 to My Team (sheikhupdesk@gmail.com) 
#                                 The subject of the email is report topic 
#                                 and draf it """)
# report["output"]