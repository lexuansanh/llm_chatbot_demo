from src.config import SEARCH_INTERNET_PROMT
from src.llm.llm import llm_manager
from src.utils.logger import logger


def search_internet(state):
    """
    Searches the internet using LLM based on the response message from the current state.

    Args:
        state (dict): The current state containing context information.

    Returns:
        dict: Updated state with search results and next step set to "END".
    """
    logger.info(f"AgentSearchInternet ### with state {state['response_message']}")

    prompt = SEARCH_INTERNET_PROMT  # Fetch predefined search prompt

    # Construct message list for LLM processing
    messages = [
        ("system", prompt["parts"]["text"]),
        ("human", state["response_message"]),
    ]

    return {
        "next_step": "END",  # Mark the process as completed
        "messages": llm_manager.search_internet(messages),  # Fetch search results
        "length_cache_response": state["length_cache_response"]
        + 1,  # Increment cache length
    }
