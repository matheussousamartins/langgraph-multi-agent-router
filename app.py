from langgraph.checkpoint.memory import MemorySaver
from graphs.router import create_router_graph

if __name__ == "__main__":
    graph = create_router_graph()

    # MemorySaver
    app = graph.with_config(
        {"checkpointer": MemorySaver()}
    )

    from langchain_core.messages import HumanMessage

    state = {
        "messages": [HumanMessage(content="O que é LangGraph?")],
        "route": None,
        "steps": 0,
    }

    result = app.invoke(state)
    print(result["messages"][-1].content)
