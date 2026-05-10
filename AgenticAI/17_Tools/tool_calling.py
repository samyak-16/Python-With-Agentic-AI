from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from rich import print

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")


@tool
def get_text_length(text: str) -> int:
    """Returns the number of character in a given text"""
    return len(text)


#  Tool Binding
llm_with_tools = llm.bind_tools([get_text_length])

# result = llm.invoke(
#     "Returns the number of character in a given text : Hello How Are You ?"
# )
# print(result)  # ---> Less token used
# result2 = llm_with_tools.invoke(
#     "Returns the number of character in a given text : Hello How Are You ?"
# )
# print(result2.tool_calls[0])  # ---> More token used

# if result2.tool_calls:
#     tool_call = result2.tool_calls[0]

#     tool_name = tool_call["name"]
#     tool_args = tool_call["args"]

#     tool_result = get_text_length.invoke(tool_args)
#     final_response = llm_with_tools.invoke(f"The length of the text is {tool_result}")
#     print(final_response)

text = input("> ")
messages = []
query = HumanMessage(f"Return the characters in the given text : {text}")
messages.append(query)
# print(messages)
result = llm_with_tools.invoke(messages)
messages.append(result)

tools = {"get_text_length": get_text_length}


if result.tool_calls:
    # print(result.tool_calls[0])
    tool_name = result.tool_calls[0]["name"]
    tool_args = result.tool_calls[0]["args"]
    tool_result = tools[tool_name].invoke(result.tool_calls[0])
    messages.append(tool_result)

final_result = llm_with_tools.invoke(messages)
print(final_result)
