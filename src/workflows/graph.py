from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from src.agents.active import active_agent
from src.agents.ask_again import ask_again
from src.agents.get_answer_from_context import get_answer_from_context
from src.agents.greeting import greeting
from src.agents.search_internet import search_internet
from src.workflows.router_edges import Router
from src.workflows.state import State

# Create a state graph for managing conversation flow
graph_builder = StateGraph(State)

# Adding nodes to the graph (Each node represents an agent handling a specific task)
graph_builder.add_node("active_agent", active_agent)  # Main agent to process user input
graph_builder.add_node(
    "ask_again_agent", ask_again
)  # Handles unclear queries by requesting clarification
graph_builder.add_node(
    "search_internet_agent", search_internet
)  # Searches the internet if needed
graph_builder.add_node(
    "get_answer_from_context_agent", get_answer_from_context
)  # Retrieves answers from internal knowledge base
graph_builder.add_node("greeting", greeting)  # Handles greeting messages

# Define the starting point of the conversation flow
graph_builder.add_edge(START, "active_agent")

# Define conditional transitions between agents based on the routing logic
graph_builder.add_conditional_edges(
    "active_agent",  # The node making the decision
    Router,  # Router function to determine the next step
    {
        "get_answer_from_context_agent": "get_answer_from_context_agent",  # Use internal knowledge base
        "ask_again_agent": "ask_again_agent",  # Ask the user for clarification
        "greeting": "greeting",  # Respond to greetings
        "search_internet_agent": "search_internet_agent",  # Perform internet search
        "end_flow": END,  # End the conversation
    },
)

# Initialize memory storage to keep track of conversation state
memory = MemorySaver()

# Compile the conversation graph with checkpointing enabled
graph = graph_builder.compile(checkpointer=memory)
