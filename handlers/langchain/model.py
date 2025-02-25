from .openai_api import GPTModel
from .tools import tool_list

from typing import Annotated
from typing_extensions import TypedDict
from typing import Literal

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from .tools import tool_list, tool_node

class State(TypedDict):
    messages: Annotated[list, add_messages]

GPTModel = GPTModel.bind_tools(tools = tool_list)

graph_builder = StateGraph(State) 

def chatbot(state: State):
    return {"messages": [GPTModel.invoke(state["messages"])]}

def router(state: list[BaseMessage]) -> Literal["calendar", "__end__"]:
    tool_calls = state["messages"][-1].additional_kwargs.get("tool_calls", [])
    if len(tool_calls):
        return "calendar"
    else:
        return END

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_conditional_edges("chatbot", router)
graph_builder.add_node("calendar", tool_node)

graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")

graph = graph_builder.compile()

def model_invoke(user_input: str):
    output = list(graph.stream({"messages": [{"role": "user", "content": user_input}]}))
    last_message =  list(output[-1].values())[0]

    print(output)
    
    return last_message["messages"][-1].content