from utils.env import get_env
from langchain_openai import ChatOpenAI
from config import Config

OPENAI_API_KEY =get_env("OPENAI_API_KEY")

# ChatModelの作成
llm = ChatOpenAI(model = Config.llm_model)
