from dotenv import load_dotenv

from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")
parser = StrOutputParser(max_results=5)
prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant

summarize the following news into clear bullet points 

{news}
"""
)
search_tool = TavilySearch(max_results=5)

runnables = prompt | llm | parser
# results = search_tool.invoke({"query": "What happened at the last wimbledon"})
# print(results)
news = search_tool.run("Latesh AI news ")
# print(results)
results = runnables.invoke({"news": news})

print(results)
 