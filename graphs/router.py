from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

from state import AppState


def create_router_graph():
    model = ChatOpenAI(model="gpt-5-nano")

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
    graph.set_entry_point("router")

    # Por enquanto, só finalizamos
    graph.add_edge("router", END)

    return graph.compile()
