from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict, Optional, Literal

load_dotenv()

gpt_5_nano = init_chat_model("gpt-5-nano")
gemini_2_dot_5_flash = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai"
)


class State(TypedDict):
    # messages: Annotated[list[AnyMessage], add_messages]
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


def opeanai_chatbot(state: State):
    response = gpt_5_nano.invoke(state.get("user_query"))
    state["llm_output"] = response
    return state


def route_based_on_response(
    state: State,
) -> Literal["end_node", "gemini_chatbot"]:  # Routing function
    if False:  # Change to True if you want openAI ans else gemini : This is a router , for now i did a manual routing based on True and False
        return "end_node"
    return "gemini_chatbot"


def gemini_chatbot(state: State):
    print("\n\nRouter choosed gemini as the response was not good\n\n")
    response = gemini_2_dot_5_flash.invoke(state.get("user_query"))
    state["llm_output"] = response
    return state


def end_node(state: State):
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("openai_chatbot", opeanai_chatbot)
graph_builder.add_node("gemini_chatbot", gemini_chatbot)
graph_builder.add_node("end_node", end_node)


graph_builder.add_edge(START, "openai_chatbot")
graph_builder.add_conditional_edges("openai_chatbot", route_based_on_response)
graph_builder.add_edge("gemini_chatbot", "end_node")
graph_builder.add_edge("end_node", END)

graph = graph_builder.compile()
final_state = graph.invoke(State({"user_query": "What is an LLM  ? Explain in short"}))
print(final_state.get("llm_output").content)
