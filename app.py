from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from graphs.router import create_router_graph

app = create_router_graph()

state = {
    "messages": [HumanMessage(content="O que é LangGraph?")],
    "route": None,
    "steps": 0,
}

result = app.invoke(state)

print(result["messages"][-1].content)
