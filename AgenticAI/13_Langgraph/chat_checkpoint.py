from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict, Optional, Literal
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

gpt_5_nano = init_chat_model("gpt-5-nano")
gemini_2_dot_5_flash = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai"
)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_query: str
    final_output: AIMessage


def opeanai_chatbot(state: State):
    user_query = state.get("user_query")
    state["messages"].append(HumanMessage(user_query))
    response = gpt_5_nano.invoke(state["messages"])
    state["messages"].append(response)
    state["final_output"] = response
    return state


def route_based_on_response(
    state: State,
) -> Literal["end_node", "gemini_chatbot"]:  # Routing function
    if True:  # Change to True if you want openAI ans else gemini : This is a router , for now i did a manual routing based on True and False
        return "end_node"
    return "gemini_chatbot"


def gemini_chatbot(state: State):
    print("\n\nRouter choosed gemini as the response was not good\n\n")
    response = gemini_2_dot_5_flash.invoke(state["messages"])
    state["messages"].append(response)
    state["final_output"] = response
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

# graph = graph_builder.compile()


def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


DB_URI = "mongodb://localhost:27017/"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph = compile_graph_with_checkpointer(checkpointer)

    config_samyak = {"configurable": {"thread_id": "samyak"}}

    config_simran = {"configurable": {"thread_id": "simran"}}

    final_state_1 = graph.invoke(
        # State({"user_query": "Hey , My name is Samyak Raj "}),
        State({"user_query": "Hey , what is my name ?"}),
        config=config_samyak,
    )
    final_state_2 = graph.invoke(
        # State({"user_query": "Hey my name is Simran"}),
        State({"user_query": "What is my name ?"}),
        config=config_simran,
    )

    print(final_state_1.get("final_output").content)
    print(final_state_2.get("final_output").content)
