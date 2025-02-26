from utils.text import open_text_file
from .ReAct import agent

config = {"configurable": {"thread_id": "1"}}

system_prompt = open_text_file(r"C:\Users\YUTA\Desktop\Env\egh\hackathong4246\handlers\langgraph\prompts\test_prompt.txt")

def invoke(message: str):
    system_message = {"role": "system", "content" : system_prompt}
    user_message = {"role": "user", "content": message}

    for step in agent.stream([system_message ,user_message], config):
        for task_name, message in step.items():
            if task_name == "agent":
                continue  # Just print task updates

            print(f"\n{task_name}:")
            message.pretty_print()