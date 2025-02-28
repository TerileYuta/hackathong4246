from langchain.chat_models import init_chat_model
from utils.env import get_env
from langchain_openai import ChatOpenAI

OPENAI_API_KEY =get_env("OPENAI_API_KEY")

# ChatModelの作成
llm = ChatOpenAI(model = "gpt-4o")
