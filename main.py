import uuid

from src.utils.logger import logger
from src.workflows.graph import graph

thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

user_messages = str(input(">>"))
output = graph.invoke(
    {"messages": [user_messages], "intent": None, "length_cache_response": 0}, config
)
print(output["messages"][0])

print(output["messages"][1].content)
while True:
    if output:
        for e in output["messages"]:
            e.pretty_print()
            output = None
    user_messages = str(input(">>"))
    output = graph.invoke({"messages": [user_messages]}, config)
