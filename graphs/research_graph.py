from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

from state import AppState


def create_research_graph():
    model = ChatOpenAI(model="gpt-5-nano")

    def research_node(state: AppState):
        last_user_message = state["messages"][-1].content

        prompt = f"""
            Responda de forma detalhada, técnica e aprofundada.
            Inclua contexto, exemplos e implicações práticas.

            Pergunta: "{last_user_message}"
            """

        response = model.invoke(prompt)

        return {
            "messages": [AIMessage(content=response.content)],
            "steps": state.get("steps", 0) + 1,
        }

    graph = StateGraph(AppState)

    graph.add_node("research", research_node)
    graph.set_entry_point("research")
    graph.add_edge("research", END)

    return graph.compile()
