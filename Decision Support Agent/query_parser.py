# import os
# import re
# import yfinance as yf
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv

# load_dotenv()

# # Initialize LLM
# llm = ChatGroq(model="lllama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
# parser = StrOutputParser()

# # Prompt template to extract company names
# extract_prompt = ChatPromptTemplate.from_template(
#     """Extract the names of public companies from this query:
#     Query: {query}
#     Return the names as a comma-separated list."""
# )

# # Prompt template to generate investment strategy
# strategy_prompt = ChatPromptTemplate.from_template(
#     """You are a financial agent. Given the following company data, provide a brief investment strategy.

#     Company Information:
#     {company_data}

#     Respond professionally and concisely."""
# )

# def get_company_names(user_query):
#     chain = extract_prompt | llm | parser
#     raw_output = chain.invoke({"query": user_query})
#     return [name.strip() for name in raw_output.split(',') if name.strip()]

# def is_valid_ticker(company):
#     ticker = yf.Ticker(company)
#     info = ticker.info
#     return 'shortName' in info

# def fetch_company_data(company):
#     ticker = yf.Ticker(company)
#     info = ticker.info
#     return {
#         "name": info.get("shortName", "N/A"),
#         "sector": info.get("sector", "N/A"),
#         "marketCap": info.get("marketCap", "N/A"),
#         "currentPrice": info.get("currentPrice", "N/A")
#     }

# def generate_strategy(company_infos):
#     formatted_info = "\n\n".join([f"Name: {c['name']}\nSector: {c['sector']}\nMarket Cap: {c['marketCap']}\nCurrent Price: {c['currentPrice']}" for c in company_infos])
#     chain = strategy_prompt | llm | parser
#     return chain.invoke({"company_data": formatted_info})

# def handle_user_query(user_query):
#     try:
#         company_names = get_company_names(user_query)
#         if not company_names:
#             return "I am an investment strategy agent. Please ask which companies you'd like to compare."

#         valid_companies = []
#         invalid_companies = []

#         for name in company_names:
#             ticker = yf.Ticker(name)
#             if is_valid_ticker(name):
#                 valid_companies.append(fetch_company_data(name))
#             else:
#                 invalid_companies.append(name)

#         if invalid_companies:
#             return f"These are not valid public companies: {', '.join(invalid_companies)}. Please enter valid company names."

#         return generate_strategy(valid_companies)

#     except Exception as e:
#         return f"Something went wrong. I am an investment strategy agent. My job is to help you with smart investment decisions.\nError: {str(e)}"

# # Example usage
# if __name__ == "__main__":
#     query = input("Ask your investment question: ")
#     response = handle_user_query(query)
#     print("\nResponse:\n", response)




# from langchain.output_parsers import StructuredOutputParser, ResponseSchema
# from langchain_google_genai import GoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from dotenv import load_dotenv

# load_dotenv()

# # Define model
# model = GoogleGenerativeAI(model="gemini-2.0-flash")

# query = input("Enter compnay names to compare the stock price: ")

# # Prompt template
# template = PromptTemplate(
#     template="""Your work is to find out the valid company name form the query : {query}

#     If any invalid company name you found from the query {query} 
#     Response like : Invalid company name. Plese provide a valid company name
#     eg : 'Apple', 'Google', 'Microsoft', 'Tesla' or a big well kown company name

#     If found valid company names then provide the list of company names 
#     like : [Apple, Google, Reliance]

#     If user query will out of the box 
#     like : Latest song released
#     something like that then response
#     like : Tell your work that you are an agent to that compare the stock price between 2 or more than 2 company

#     If user in user query there will be only one company name found the response
#     like : Please enter at leaset 2 company names to compare the stock price

#     Every response should be user friendly
#     Do not helucinate
#     """,
#     input_variables=[query]
# )

# chain = template | model

# result = chain.invoke(query)

# print(result)




# from langchain_google_genai import GoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from dotenv import load_dotenv

# load_dotenv()

# # Define model
# model = GoogleGenerativeAI(model="gemini-2.0-flash")

# query = input("Enter company names to compare the stock price: ")

# # Correct PromptTemplate
# template = PromptTemplate(
#     template="""Your work is to find out the valid company name from the query: {query}

# If any invalid company name is found from the query {query}, respond like:
# Invalid company name. Please provide a valid company name
# eg: 'Apple', 'Google', 'Microsoft', 'Tesla' or another well-known company name.

# If valid company names are found, provide the list like: [Apple, Google, Reliance]

# If the user query is out of context
# (e.g., 'Latest song released'), respond:
# I am an agent to compare the stock price between 2 or more companies.

# If only one company name is found, respond:
# Please enter at least 2 company names to compare the stock price.

# Every response should be user-friendly.
# Do not hallucinate.
# """, 
#     input_variables=["query"]
# )

# # Format the prompt
# prompt = template.format(query=query)

# # Invoke the model
# result = model.invoke(prompt)

# print(f"\nResponse:\n", result)





# # from langchain_google_genai import GoogleGenerativeAI
# # from langchain.prompts import PromptTemplate
# # from dotenv import load_dotenv

# # load_dotenv()

# # # Define model
# # model = GoogleGenerativeAI(model="gemini-2.0-flash")

# # query = input("Enter company names to compare the stock price: ")

# # template = PromptTemplate(
# #     template="""You are a helpful assistant that extracts valid public company names from a user's query and determines if the query is related to comparing stock prices.

# # User Query: {query}

# # Instructions:
# # - If the query contains at least 2 valid, well-known company names, respond with just a list like: [Apple, Google]
# # - If it contains only 1 company name, respond with: "Please enter at least 2 company names to compare their stock prices."
# # - If it contains no valid company names, respond with: "Invalid company name. Please provide valid company names such as 'Apple', 'Google', 'Microsoft', 'Tesla'."
# # - If the query is unrelated to stock comparison (like music, jokes, movies, etc), respond with: "I'm an agent that compares stock prices between companies. Please enter valid company names."
# # - If even a single invalid company names found then where Invalid is written place the invalid company name and, respond with: "Plese enter valid company name. Invalid Company is not a valid company." 

# # Respond only with the appropriate message. Do not explain what you're doing.
# # """,
# #     input_variables=["query"]
# # )

# # prompt = template.format(query=query)
# # response = model.invoke(prompt)

# # print("\nResponse:\n", response)



# from langchain_google_genai import GoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from dotenv import load_dotenv
# import ast

# from tools.ticker_lookup import TickerLookupTool


# load_dotenv()

# # Initialize Gemini model
# model = GoogleGenerativeAI(model="gemini-2.0-flash")

# def extract_valid_companies(user_query: str) -> list | None:
#     """
#     Given a user query, use the Gemini model to extract a list of valid company names.
#     Returns:
#         - List of company names if model returns a proper list like [Apple, Tesla]
#         - None if the response is an error message or explanation
#     """
#     template = PromptTemplate(
#         template="""You are a helpful assistant that extracts valid public company names from a user's query and determines if the query is related to comparing stock prices.

# User Query: {query}

# Instructions:
# - If the query contains at least 2 valid, well-known company names, respond with just a list like: ["Apple", "Coca Cola"]
# - If it contains only 1 company name, respond with: "Please enter at least 2 company names to compare their stock prices."
# - If it contains no valid company names, respond with: "Invalid company name. Please provide valid company names such as 'Apple', 'Google', 'Microsoft', 'Tesla'."
# - If the query is unrelated to stock comparison (like music, jokes, movies, etc), respond with: "I'm an agent that compares stock prices between companies. Please enter valid company names."
# - If even a single invalid company name is found then where Invalid is written place the invalid company name and respond with: "Please enter valid company name. Invalid Company is not a valid company." 

# Respond only with the appropriate message. Do not explain what you're doing.
# """,
#         input_variables=["query"]
#     )
#     prompt = template.format(query=user_query)
#     response = model.invoke(prompt).strip()
#     # try:
#     #     prompt = template.format(query=user_query)
#     #     response = model.invoke(prompt).strip()

#     #     # Safely try to parse the response as a Python list
#     #     if response.startswith("[") and response.endswith("]"):
#     #         company_list = ast.literal_eval(response)
#     #         if isinstance(company_list, list):
#     #             print(company_list)
#     #             return [c.strip() for c in company_list]
#     # except Exception as e:
#     #     print(f"[QueryParser Error] {e}")

#     return response

# # Optional direct run example
# # if __name__ == "__main__":
# #     query = input("Enter company names to compare the stock price: ")
# #     result = extract_valid_companies(query)
# #     if result:
#     #     print("\n✅ Valid Company List:", result)
#     # else:
#     #     # print("\n❌ Could not extract a valid list of companies.")
#         # print(result)








import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM
model = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)


def extract_valid_companies(user_query: str) -> list | None:
    """
    Given a user query, use the Gemini model to extract a list of valid company names.
    Returns:
        - List of company names if model returns a proper list like [Apple, Tesla]
        - None if the response is an error message or explanation
    """
    template = PromptTemplate(
        template="""You are a helpful assistant that extracts valid public company names from a user's query and determines if the query is related to comparing stock prices.

User Query: {query}

Instructions:
- If the query contains at least 2 valid, well-known company names, respond with just a list like: ["Apple", "Coca Cola"]
- If it contains only 1 company name, respond with: "Please enter at least 2 company names to compare their stock prices."
- If it contains no valid company names, respond with: "Invalid company name. Please provide valid company names such as 'Apple', 'Google', 'Microsoft', 'Tesla'."
- If the query is unrelated to stock comparison (like music, jokes, movies, etc), respond with: "I'm an agent that compares stock prices between companies. Please enter valid company names."
- If even a single invalid company name is found then where Invalid is written place the invalid company name and respond with: "Please enter valid company name. Invalid Company is not a valid company." 

Respond only with the appropriate message. Do not explain what you're doing.
""",
        input_variables=["query"]
    )

    prompt = template.format(query=user_query)
    response = model.invoke(prompt)


    return response.content


# query = input("Query : ")
# result = extract_valid_companies(query)
# print(result.content)
