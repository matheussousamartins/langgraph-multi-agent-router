from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

from state import AppState
from graphs.tools import generate_structured_plan


def create_task_graph():
    model = ChatOpenAI(model="gpt-5-nano").bind_tools(
        [generate_structured_plan]
    )

    tool_node = ToolNode([generate_structured_plan])

    def agent_node(state: AppState):
        response = model.invoke(state["messages"])
        return {
            "messages": [response],
            "steps": state.get("steps", 0) + 1,
        }

    def should_continue(state: AppState):
        last_message = state["messages"][-1]

        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "continue"

        return "end"

    graph = StateGraph(AppState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )

    graph.add_edge("tools", "agent")

    return graph.compile()
