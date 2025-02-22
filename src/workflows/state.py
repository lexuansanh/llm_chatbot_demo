from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    """
    Represents the state of a chat session, including message history,
    processing status, intent detection, and response details.
    """

    messages: Annotated[list, add_messages]  # List of messages exchanged in the session
    tools: list  # List of tools available for processing the conversation
    status: str  # Current status of the chat session (e.g., "active", "completed")
    intent: str  # Detected intent of the conversation
    next_step: str  # Next step in the conversation flow
    is_end_flow: bool  # Indicates if the conversation flow has ended
    response_message: str  # The latest response message generated
    history: Annotated[list, add_messages]  # List of previous messages for context
    stand_alone_query: str  # Reformulated query if extracted from conversation
    length_cache_response: int  # Length of cached responses (if applicable)
    scope: (
        str  # Scope or domain of the conversation (e.g., "default", "customer_support")
    )
