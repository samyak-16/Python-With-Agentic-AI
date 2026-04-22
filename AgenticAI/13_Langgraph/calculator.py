from langchain.tools import tool
from langchain.chat_models import init_chat_model

from langchain.messages import AnyMessage
from typing import TypedDict, Annotated
import operator
from langchain.messages import SystemMessage

from dotenv import load_dotenv

load_dotenv()

model = init_chat_model("gpt-4o")


# Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a / b


#! Augment the LLM with tools

tools = [multiply, add, divide]
tools_by_name = {
    tool.name: tool for tool in tools
}  # tool.name        # "multiply" - returns name of the function
# tools_by_name — It's a lookup dictionary :
# {
#     "multiply": <multiply tool object>,
#     "add":      <add tool object>,
#     "divide":   <divide tool object>
# }

model.bind_tools(tools=tools)


#!  2) Creating a global store which can be accessable to all nodes - (graph)
#
# type AnyMessage =
#   | { role: "human"; content: string }
#   | { role: "ai"; content: string }
#   | { role: "system"; content: string }
#   | { role: "tool"; content: string; tool_call_id: string };


class MessagesState(TypedDict):
    # Annotated[type, how_to_merge(old, new)] : Fn tells how will new mesage be merged to list of old messages : )
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


# 3. Define model node


def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""
