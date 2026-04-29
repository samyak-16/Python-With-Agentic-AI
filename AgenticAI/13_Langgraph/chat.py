from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

gpt_5_nano = init_chat_model("gpt-5-nano")


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Coding nodes
def chat(state: State):
    response = gpt_5_nano.invoke(state.get("messages"))
    return {"messages": [response]}


def sample_node(state: State):

    print("\n\nInside sample_node state: ", state)
    return {"messages": ["Hi, this is the message from Sample  Node"]}


graph_builder = StateGraph(State)
graph_builder.add_node("chat", chat)
graph_builder.add_node("sample_node", sample_node)

graph_builder.add_edge(START, "chat")
graph_builder.add_edge("chat", "sample_node")
graph_builder.add_edge("sample_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi, My name is Samyak Raj Subedi"]}))

print("\n\nFinal Updated state : ", updated_state)
