from .tools import tool_list

from .openai_api import llm

from langchain_core.messages import ToolMessage
from langgraph.graph.message import add_messages
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver

tools_by_name = {tool.name: tool for tool in tool_list}
checkpointer = MemorySaver()

@task
def call_model(messages: str):
    """
    
    LLMモデルの推論を行う

    Parameters
    ----------
        messages(str) : ユーザークエリー

    Returns
    ----------
        AIレスポンス

    """

    response = llm.bind_tools(tool_list).invoke(messages)

    return response

@task
def call_tool(tool_call, line_id):
    """
    
    toolの呼び出しを行う

    Parameters
    ----------
        tool_call : 呼び出されたツールのリスト
        line_id : LINE ID

    Returns
    ----------
        Toolの実行結果

    """


    if("line_id" in tool_call["args"]):
        tool_call["args"]["line_id"] = line_id

    tool = tools_by_name[tool_call["name"]]
    success, result = tool.invoke(tool_call["args"])

    return ToolMessage(content = str(result), tool_call_id = tool_call["id"])

def model_invoke(messages, line_id):
    config = {"configurable": {"thread_id": "1"}}
    
    @entrypoint(checkpointer=checkpointer)
    def agent(messages):
        """
        


        """

        llm_response = call_model(messages).result()

        while True:
            if not llm_response.tool_calls:
                break

            tool_result_futures = [
                call_tool(tool_call, line_id) for tool_call in llm_response.tool_calls
            ]

            # TODO Google認証失敗時の挙動を設定する

            tool_results = [fut.result() for fut in tool_result_futures]

            # Append to message list
            messages = add_messages(messages, [llm_response, *tool_results])
            

            # Call model again
            llm_response = call_model(messages).result()
        
        return llm_response
    
    for step in agent.stream(messages, config):
        for task_name, message in step.items():
            if task_name == "agent":
                continue  # Just print task updates

            message.pretty_print()

    return message.content