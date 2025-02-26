from .tools import tool_list

from .openai_api import llm

from langchain_core.messages import ToolMessage
from langgraph.graph.message import add_messages
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver

tools_by_name = {tool.name: tool for tool in tool_list}

@task
def call_model(messages: str):
    """
    

    """

    response = llm.bind_tools(tool_list).invoke(messages)

    return response

@task
def call_tool(tool_call):
    """
    


    """

    tool = tools_by_name[tool_call["name"]]
    observation = tool.invoke(tool_call["args"])

    return ToolMessage(content = observation, tool_call_id = tool_call["id"])

checkpointer = MemorySaver()

@entrypoint(checkpointer=checkpointer)
def agent(messages):
    """
    


    """

    llm_response = call_model(messages).result()

    while True:
        if not llm_response.tool_calls:
            break

        tool_result_futures = [
            call_tool(tool_call) for tool_call in llm_response.tool_calls
        ]

        tool_results = [fut.result() for fut in tool_result_futures]

        # Append to message list
        messages = add_messages(messages, [llm_response, *tool_results])

        # Call model again
        llm_response = call_model(messages).result()

    return llm_response

