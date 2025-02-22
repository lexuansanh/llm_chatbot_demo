from src.config import DEFAULT_SYSTEM_PROMPT
from src.llm.llm import llm_manager
from src.utils.logger import logger


def greeting(state):
    """
    Handles the greeting interaction using LLM.

    Args:
        state (dict): The current state containing context information.

    Returns:
        dict: Updated state with the greeting response and next step set to "END".
    """
    logger.info(
        f"AgentGreeting ### with state {state['scope']} - {state['response_message']}"
    )

    prompt = DEFAULT_SYSTEM_PROMPT  # Fetch default system prompt

    # Construct message list for LLM processing
    messages = [
        ("system", prompt["parts"]["text"]),
        ("human", state["response_message"]),
    ]

    response = llm_manager.invoke(messages)  # Get response from LLM

    return {
        "next_step": "END",  # Mark the process as completed
        "messages": response,  # Store generated response
        "length_cache_response": state["length_cache_response"]
        + 1,  # Increment cache length
    }
