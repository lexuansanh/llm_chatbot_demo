from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.schemas.schema import AskAgainSchema


@tool("greeting")
def greeting():
    """Check if message of user want to make greeting action"""
    return "greeting"


@tool("get_answer_from_context")
def get_answer_from_context():
    """Call tool when in context has answer and user want to get information from context"""
    return "get_answer_from_context"


@tool("search_internet")
def search_internet():
    """Call this tool when you can't find an answer based on the given context"""
    return "search_internet"


@tool("ask_again", args_schema=AskAgainSchema)
def ask_again():
    """Call tool when need more information to confirm what tool you need to call"""
    return "ask_again"
