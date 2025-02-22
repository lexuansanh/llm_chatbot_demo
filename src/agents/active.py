from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import create_react_agent

from src.config.prompts import DEFAULT_SYSTEM_PROMPT
from src.llm.llm import llm_manager
from src.tools.active_agent_tools import (
    ask_again,
    get_answer_from_context,
    greeting,
    search_internet,
)
from src.utils.logger import logger
from src.workflows.state import State


def active_agent(state: State):
    """
    Active Agent function to determine user intent and direct the workflow accordingly.

    Args:
        state (State): The current state containing user input messages and other relevant details.

    Returns:
        dict: Contains the next step in the workflow along with relevant response details.
    """
    logger.info(f"Active Agent ### Initializing intent detection.")

    # Define available tools
    greeting_tool = Tool(
        name=greeting.name, func=greeting, description=greeting.description
    )
    get_answer_from_context_tool = Tool(
        name=get_answer_from_context.name,
        func=get_answer_from_context,
        description=get_answer_from_context.description,
    )
    ask_again_tool = Tool(
        name=ask_again.name, func=ask_again, description=ask_again.description
    )
    search_internet_tool = Tool(
        name=search_internet.name,
        func=search_internet,
        description=search_internet.description,
    )

    tools = [
        greeting_tool,
        get_answer_from_context_tool,
        ask_again_tool,
        search_internet_tool,
    ]

    # Bind LLM with tools, allowing it to choose one tool per call
    llm_bind_tools = llm_manager.bind_tools(tools, tool_choice="any")

    # Extract user input
    user_input = str(state["messages"])
    logger.info(f"User Input: {user_input}")

    # Define system prompt
    prompt = DEFAULT_SYSTEM_PROMPT

    messages = [
        (
            "system",
            f"You are a smart virtual assistant. Your job is to determine the user's intent based on the provided context:\n {prompt}",
        ),
        ("human", user_input),
    ]

    # Invoke the LLM with tool binding
    response = llm_bind_tools.invoke(messages)
    logger.info(f"Active Agent Response: {response}")

    # Determine the next step based on tool calls
    if response.tool_calls:
        for tool_call in response.tool_calls:
            name_tool_called = tool_call["name"]
            match name_tool_called:
                case "ask_again":
                    logger.info("Redirecting to AskAgain Agent")
                    return {
                        "response_message": str(state["messages"][-1]),
                        "scope": state["scope"],
                        "next_step": "ask_again_agent",
                    }
                case "get_answer_from_context":
                    logger.info("Redirecting to GetAnswerFromContext Agent")
                    return {
                        "response_message": str(state["messages"][-1]),
                        "scope": state["scope"],
                        "next_step": "get_answer_from_context_agent",
                    }
                case "greeting":
                    logger.info("Redirecting to Greeting Agent")
                    return {
                        "response_message": str(state["messages"][-1]),
                        "scope": state["scope"],
                        "next_step": "greeting",
                    }
                case "search_internet":
                    logger.info("Redirecting to SearchInternet Agent")
                    return {
                        "response_message": str(state["messages"][-1]),
                        "scope": state["scope"],
                        "next_step": "search_internet_agent",
                    }
