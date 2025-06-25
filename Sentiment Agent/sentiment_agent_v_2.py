"""## analysis tool"""

from langchain_core.tools import tool
from transformers import pipeline

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders.csv_loader import CSVLoader


# Load models once ------------------------------------------------------------------------------------------------------------------------------------------
sentiment_pipeline = pipeline("sentiment-analysis")
emotion_pipeline = pipeline("text-classification", model="boltuix/bert-emotion", top_k=1)

@tool(return_direct=True)
def analysis_tool(text: str) -> dict:
    """
    Analyze the input text and return sentiment + primary emotion.
    """
    sentiment = sentiment_pipeline(text)[0]
    emotion = emotion_pipeline(text)[0]

    return {
        "Sentiment": {
            "label": sentiment["label"],
            # "confidence": round(sentiment["score"], 2)
        },
        "Emotion": {
            "label": emotion[0]['label'],
            # "confidence": round(emotion[0]['score'])
        }
    }

# CSV Document Support ------------------------------------------------------------------------------------------------------------------------------------------


file_path = "Reviews.csv"

loader = CSVLoader(file_path=file_path)
data = loader.load()
CSV_reviews=[]
for record in data:
  CSV_reviews.append(record.page_content)


# JSON Document support

file_path = "Reviews.json"

json_Loader=JSONLoader(
    file_path=file_path,
    jq_schema='.messages[].review'
    )

json_data= json_Loader.load()

json_reviews=[]

for d in json_data:
  json_reviews.append(d.page_content)


# mock data ------------------------------------------------------------------------------------------------------------------------------------------
texts = [
        "The design is beautiful and intuitive!",
        "Ugh, app crashes constantly. Annoying.",
        "Customer support was helpful and fast.",
        "I hate the recent update. Terrible UX.",
        "Works well for my needs. No complaints."
    ]


# summerizing ------------------------------------------------------------------------------------------------------------------------------------------
from collections import Counter

def summarize_results(results: list[dict]) -> str:
    sentiments = [r['Sentiment']['label'] for r in results]
    emotions = [r['Emotion']['label'] for r in results]

    sentiment_counts = Counter(sentiments)
    emotion_counts = Counter(emotions)

    total = len(results)
    pos_pct = (sentiment_counts.get("POSITIVE", 0) / total) * 100
    neg_pct = (sentiment_counts.get("NEGATIVE", 0) / total) * 100
    common_emotion = emotion_counts.most_common(1)[0][0]

    summary = (
        f" {pos_pct:.0f}% of feedback is positive.\n"
        f" {neg_pct:.0f}% is negative.\n"
        f" Dominant emotion: {common_emotion}.\n"
    )
    return summary

# feedback ------------------------------------------------------------------------------------------------------------------------------------------

from google.colab import userdata
GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')



llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=GOOGLE_API_KEY)
agent = llm.bind_tools([analysis_tool])

from langchain_core.messages import HumanMessage, AIMessage

text=texts[0]
print(f"Text: {text}")

messages=[HumanMessage(text)]

result=agent.invoke(messages)

messages.append(result)

messages.append(analysis_tool.invoke(result.tool_calls[0]))

agent.invoke(messages)


# CSV Data Test ------------------------------------------------------------------------------------------------------------------------------------------
results = []
for review in reviews:
    print(f"review: {review}")
    result=analysis_tool.invoke(review)
    print(f"Result: {result}")
    results.append(result)

summary = summarize_results(results)

print(summary)

# JSON Data Test ------------------------------------------------------------------------------------------------------------------------------------------
json_results = []
for review in json_reviews:
    print(f"review: {review}")
    result=analysis_tool.invoke(review)
    print(f"Result: {result}")
    json_results.append(result)

json_data_summary = summarize_results(json_results)

print(json_data_summary)