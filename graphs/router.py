from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from state import AppState
from graphs.faq_graph import create_faq_graph


def create_router_graph():
    model = ChatOpenAI(model="gpt-5-nano")

    faq_graph = create_faq_graph()

    def router_node(state: AppState):
        last_user_message = state["messages"][-1].content

        prompt = f"""
            Classifique a intenção do usuário em UMA palavra:
            - faq → perguntas simples ou conceituais
            - research → explicações profundas ou técnicas
            - task → pedidos de ação ou execução

            Usuário: "{last_user_message}"

            Responda apenas com: faq, research ou task.
            """

        response = model.invoke(prompt)
        route = response.content.strip().lower()

        return {
            "route": route,
            "steps": state.get("steps", 0) + 1,
        }

    graph = StateGraph(AppState)

    graph.add_node("router", router_node)

    # adiciona subgrafo como nó
    graph.add_node("faq_graph", faq_graph)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "faq": "faq_graph",
        },
    )

    graph.add_edge("faq_graph", END)

    return graph.compile()
