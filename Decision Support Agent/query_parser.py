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

