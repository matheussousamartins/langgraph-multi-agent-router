from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from state import AppState
from graphs.faq_graph import create_faq_graph
from graphs.research_graph import create_research_graph
from graphs.task_graph import create_task_graph


def create_router_graph():
    model = ChatOpenAI(model="gpt-5-nano")

    faq_graph = create_faq_graph()
    research_graph = create_research_graph()
    task_graph = create_task_graph()

    def router_node(state: AppState):
        last_user_message = state["messages"][-1].content

        prompt = f"""
                Classifique a intenção do usuário em UMA palavra:

                faq → perguntas simples ou conceituais
                research → explicações profundas ou técnicas
                task → pedidos de ação ou execução

                Responda APENAS com:
                faq
                research
                task

                Usuário: "{last_user_message}"
                """

        response = model.invoke([HumanMessage(content=prompt)])
        route = response.content.strip().lower()

        if route not in ["faq", "research", "task"]:
            route = "faq"

        return {
            "route": route,
            "steps": state.get("steps", 0) + 1,
        }

    graph = StateGraph(AppState)

    graph.add_node("router", router_node)
    graph.add_node("faq_graph", faq_graph)
    graph.add_node("research_graph", research_graph)
    graph.add_node("task_graph", task_graph)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "faq": "faq_graph",
            "research": "research_graph",
            "task": "task_graph",
        },
    )

    graph.add_edge("faq_graph", END)
    graph.add_edge("research_graph", END)
    graph.add_edge("task_graph", END)

    return graph.compile()


app = create_router_graph()

