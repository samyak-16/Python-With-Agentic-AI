from dotenv import load_dotenv
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from rich import print


load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

search_tool = TavilySearch(max_results=5)


@tool
def get_city_weather(city: str):
    """Get the latest weather data of the given city"""
    return "45 degree C"  # testing value


@tool
def get_city_news(city: str):
    """Get the latest news for the given city"""
    return search_tool.run(f"Latest news in {city}")


tools = {"get_city_weather": get_city_weather, "get_city_news": get_city_news}

llm_with_tools = llm.bind_tools([get_city_weather, get_city_news])

messages = []

user_query = input("> ")

messages.append(HumanMessage(user_query))
find_tool_llm_call = llm_with_tools.invoke(
    messages
)  # Call LLM with user query and registered tools to find the relative tool
print(find_tool_llm_call)
messages.append(find_tool_llm_call)

#  Invoke all the tools which AI suggested according to user query :
for _tool in find_tool_llm_call.tool_calls:
    tool_name = _tool["name"]
    tool_result = tools[tool_name].invoke(_tool)
    messages.append(tool_result)
final_result = llm_with_tools.invoke(messages)

print(final_result)
