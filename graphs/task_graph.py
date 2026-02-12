from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from state import AppState


def create_task_graph():
    model = ChatOpenAI(model="gpt-5-nano")

    def task_node(state: AppState):
        last_user_message = state["messages"][-1].content

        prompt = f"""
        Execute a tarefa solicitada pelo usuário.
        Seja direto e resolutivo.

        Tarefa: "{last_user_message}"
        """

        response = model.invoke(prompt)

        return {
            "messages": [AIMessage(content=response.content)],
            "steps": state.get("steps", 0) + 1,
        }

    graph = StateGraph(AppState)

    graph.add_node("task", task_node)
    graph.set_entry_point("task")
    graph.add_edge("task", END)

    return graph.compile()
